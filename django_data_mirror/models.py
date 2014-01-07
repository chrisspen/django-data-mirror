import os
import re
from pprint import pprint
from collections import namedtuple
from datetime import date
import dateutil.parser

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

def get_remote_resource(url, method='wget', fn=None):
    """
    Downloads potentially large file.
    """
    if method not in ('wget',):
        raise NotImplementedError
    if not fn:
        'http://scdb.wustl.edu/_brickFiles/2013_01/SCDB_2013_01_justiceCentered_Citation.csv.zip'.split('/')[-1].split('?')[0]
    fn = '/tmp/'+url.split('/')[-1].split('?')[0]
    if os.path.isfile(fn):
        #TODO:check filesize?
        print 'Skipping redundant download.'
        return fn
    cmd = 'wget {url} --output-document={fn}'.format(url=url, fn=fn)
    #print cmd
    os.system(cmd)
    return fn

class DataSource(object):
    """
    A general definition for the source where we'll be retrieving data from.
    """
    
    app_label = None
    
    model_name_prefix = None
    
    @classmethod
    def to_bool(cls, v, from_string=True):
        if from_string:
            return True if str(v).strip() in (True, '1', 'True') else False
        return bool(v)
    
    @classmethod
    def to_int(cls, v, from_string=True):
        return int(v)
    
    @classmethod
    def to_positive_int(cls, v, from_string=True):
        return max(int(v), 0)
    
    @classmethod
    def to_float(cls, v, from_string=True):
        return float(v)
    
    @classmethod
    def to_date(cls, v, from_string=True):
        if isinstance(v, basestring) and not v.strip():
            return
        dt = dateutil.parser.parse(v)
        return date(dt.year, dt.month, dt.day)
    
    @classmethod
    def to_datetime(cls, v, from_string=True):
        if isinstance(v, basestring) and not v.strip():
            return
        return dateutil.parser.parse(v)
    
    @classmethod
    def to_instance(cls, raw, model,
        natural_keys=None, additional={}, field_mapping={},
        from_string=True,
        override_local=False):
        """
        Converts the raw dictionary of data into an instance of the given
        class. Unless otherwise specified, assumes there's a one-to-one mapping
        between the keys in the raw dictionary and the fields in the target
        model.
        
        Differences in field mappings should be specified by `field_mapping`,
        which is of the form {raw_field_name:model_field_name}.
        
        The parameter `key` is a tuple containing the fields that uniquely
        identify the instance and can be used as arguments to the model's
        `get_or_create()`.
        
        The parameter `additional` specifies additional data to pass to the
        model's constructor.
        
        Basic data validation will be attempted, depending on the target field,
        type, but any custom validation should be implemented as methods to
        this class of the form `clean_fieldname`, where fieldname is replaced
        with the name of the field in the raw dictionary.
        
        If `from_string` is True, assumes all data is being converted from an
        original string form. e.g. The value "False" going into a BooleanField
        should be converted into the value `False`, not bool("False") == True.
        
        If `override_local` is True, the field values in any existing record
        will be overwritten with the incoming value.
        """
        
        def get_converter(field):
            name = type(field).__name__.replace('Field', '')
            if name == 'Boolean':
                return cls.to_bool
            elif name == 'PositiveInteger':
                return cls.to_positive_int
            elif name == 'Integer':
                return cls.to_int
            elif name == 'Float':
                return cls.to_float
            elif name == 'Date':
                return cls.to_date
            elif name == 'DateTime':
                return cls.to_datetime
            elif name in ('Char', 'Text'):
                return (lambda s, from_string=True: s)
            else:
                raise NotImplementedError, 'Unhandled field type: %s=%s' \
                    % (field.name, type(field).__name__,)
        
        natural_keys = natural_keys or getattr(model, 'natural_keys', None)
        if not natural_keys:
            raise NotImplementedError, 'No model natural_keys list specified.'
        key_data = {}
        defaults_data = {}
        override_data = {}
        for field in model._meta.fields:
            print field.name
            name = field_mapping.get(field.name, field.name)
            if name in raw:
                value = raw[name]
                print 'raw field:',name,value
                if hasattr(cls, 'clean_%s' % name):
                    value = getattr(cls, 'clean_%s' % name)(value)
                else:
                    value = get_converter(field)(value)
                if name in natural_keys:
                    key_data[name] = value
                else:
                    defaults_data[name] = value
                    if override_local:
                        override_data[name] = value
        for name, value in additional.iteritems():
            #name = field_mapping.get(field.name, field.name)
            if name in natural_keys:
                key_data[name] = additional[name]
            else:
                defaults_data[name] = value
                if override_local:
                    override_data[name] = value
        print 'key_data:',key_data
        print 'defaults_data:',defaults_data
        print 'override_data:',override_data
        key_data['defaults'] = defaults_data
        o, _ = model.objects.get_or_create(**key_data)
        for k, v in override_data.iteritems():
            setattr(o, k, v)
        if override_data:
            o.save()
        return o
    
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
    def refresh(cls, bulk=False, skip_to=None, **kwargs):
        """
        Reads the associated API and saves data to tables.
        """
        raise NotImplementedError
    
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
            