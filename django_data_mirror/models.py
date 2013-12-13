import re
from pprint import pprint
from collections import namedtuple

MAX_CHAR_LENGTH = 100

class ForeignKey(object):
    
    def __init__(self, model_name):
        self.model_name = model_name

class SchemaColumn(object):
    
    def __init__(self, model_name, column_name):
        self.model_name = model_name
        self.column_name = column_name
        self.types = set()
        self.min_length = 1e999999999
        self.max_length = 0
        self.isdigit = True
        self.primary = False
        self.unique = False
        self.related_model_to = None
        
    def to_python(self, indent=0, app_label=''):
        app_label = app_label or ''
        if app_label:
            app_label = app_label+'.'
        assert len(self.types) == 1, \
            'Column %s.%s uses multiple types: %s' \
                % (self.model_name, self.column_name, ', '.join(map(str, self.types)))
        type = list(self.types)[0]
        if self.isdigit:
            type = int
        if self.primary:
            blank = False
            null = False
        else:
            blank = True
            null = True
        if type in (str, unicode):
            ml = int(5 * round(float(self.max_length*2)/5))
            if ml >= MAX_CHAR_LENGTH:
                s = '%s = models.TextField(blank=%s, null=%s)' % (self.column_name, blank, null)
            else:
                s = '%s = models.CharField(max_length=%i, blank=%s, null=%s, primary_key=%s, unique=%s)' % (self.column_name, ml, blank, null, self.primary, self.unique)
        elif type in (int,):
            s = '%s = models.IntegerField(blank=%s, null=%s, primary_key=%s, unique=%s)' % (self.column_name, blank, null, self.primary, self.unique)
        elif type in (float,):
            s = '%s = models.FloatField(blank=%s, null=%s, primary_key=%s, unique=%s)' % (self.column_name, blank, null, self.primary, self.unique)
        elif type in (bool,):
            s = '%s = models.BooleanField()' % (self.column_name,)
        elif type in (list,):
            s = '%s = models.ManyToManyField(%s)' % (self.column_name, repr(app_label+self.related_model_to))
        elif type in (dict, ForeignKey):
            s = '%s = models.ForeignKey(%s)' % (self.column_name, repr(app_label+self.related_model_to))
        else:
            raise NotImplementedError, self.types
        return (' '*indent) + s

def mixed_to_underscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

class DataSource(object):
    """
    A general definition for the source where we'll be retrieving data from.
    """
    
    app_label = None
    
    model_name_prefix = None
    
    @classmethod
    def get_feeds(cls):
        """
        Returns a generator yielding each unique feed of data to be retrieved.
        Each feed is assumed to be a list, corresponding to a single database
        table, where each items corresponds to a row in that table.
        
        e.g.
        [
            ('model_name', [{1: {'col1':'abc'}, 2:{'col1':'def'}, ...}, ...}]),
        ]
        """
        raise NotImplementedError
    
    @classmethod
    def refresh(cls, **kwargs):
        """
        Reads the associated API and saves data to tables.
        """
        todo
    
    @classmethod
    def analyze(cls, max_lines=1000, **kwargs):
        """
        Looks at its data and attempts to auto-generate an appropriate
        Django model.
        
        Can handle forms like:
        
            {
                pk1:{ col1:val1, col2:val2, ... },
                pk2:{ col1:val1, col2:val2, ... },
                ...
            }
        
        """
        
        schema = {} # {name:SchemaColumn}
        
        def build_schema(model_name, col_name, col_data, primary=False):
            key = (model_name, col_name)
            schema.setdefault(key, SchemaColumn(model_name=model_name, column_name=col_name))
            schema[key].types.add(type(col_data))
            if primary:
                schema[key].primary = True
                schema[key].unique = True
                
            if isinstance(col_data, basestring):
                schema[key].max_length = max(schema[key].max_length, len(col_data))
                schema[key].min_length = min(schema[key].min_length, len(col_data))
                schema[key].isdigit = schema[key].isdigit and col_data.isdigit()
            elif isinstance(col_data, ForeignKey):
                #schema[key].types = set([ForeignKey])
                schema[key].related_model_to = col_data.model_name
                schema[key].isdigit = False
            elif isinstance(col_data, list):
                model_name = col_name[0].upper()+col_name[1:]
                if model_name.endswith('s'):
                    model_name = model_name[:-1]
                schema[key].related_model_to = model_name
                schema[key].isdigit = False
                for items in col_data:
                    for k, v in items.iteritems():
                        build_schema(model_name, k, v, primary=(k == 'id'))
            elif isinstance(col_data, dict):
                schema[key].isdigit = False
                model_name = col_name[0].upper()+col_name[1:]
                schema[key].related_model_to = model_name
                if model_name.endswith('s'):
                    model_name = model_name[:-1]
                for k, v in col_data.iteritems():
                    build_schema(model_name, k, v, primary=(k == 'id'))
        
        formats = [1]
        
        using_format = None
        for model_name, feed in cls.get_feeds():
            i = 0
            for line in feed:
                i += 1
                if i ==1:
                    pprint(line, indent=4)
                if using_format == 1 or (isinstance(line, tuple) and len(line) == 2 and isinstance(line[0], (int, float, bool, basestring)) and isinstance(line[1], dict)):
                    # Handle format {pk: {data}, ...}
                    pk_value, data = line
                    build_schema(model_name, 'id', pk_value, primary=True)
                    for col_name, col_data in data.iteritems():
                        build_schema(model_name, col_name, col_data)
                else:
                    raise NotImplementedError, 'Unknown format: %s' % (line,)
                if i >= max_lines:
                    break
                
        # Output Django ORM Python.
        print '-'*80
        schemas = {}
        for (model_name, col_name), col_schema in schema.iteritems():
            schemas.setdefault(model_name, [])
            schemas[model_name].append(col_schema)
        for model_name, columns in schemas.iteritems():
            verbose_name = mixed_to_underscore(model_name).replace('_', ' ')
            print
            print 'class %s%s(models.Model):' % (cls.model_name_prefix or '', model_name,)
            print 
            for column in columns:
                print column.to_python(indent=4, app_label=cls.app_label)
            print
            print '    class Meta:'
            if cls.app_label:
                print '        app_label = "%s"' % (cls.app_label,)
            print '        verbose_name = "%s"' % (verbose_name,)
            