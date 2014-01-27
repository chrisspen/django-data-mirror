# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DataSourceFile'
        db.create_table(u'django_data_mirror_datasourcefile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_data_mirror.DataSourceControl'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('complete', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('total_lines', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('total_lines_complete', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('completed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'django_data_mirror', ['DataSourceFile'])

        # Adding index on 'DataSourceControl', fields ['enabled']
        db.create_index(u'django_data_mirror_datasourcecontrol', ['enabled'])

        # Adding index on 'DataSourceControl', fields ['slug']
        db.create_index(u'django_data_mirror_datasourcecontrol', ['slug'])


    def backwards(self, orm):
        # Removing index on 'DataSourceControl', fields ['slug']
        db.delete_index(u'django_data_mirror_datasourcecontrol', ['slug'])

        # Removing index on 'DataSourceControl', fields ['enabled']
        db.delete_index(u'django_data_mirror_datasourcecontrol', ['enabled'])

        # Deleting model 'DataSourceFile'
        db.delete_table(u'django_data_mirror_datasourcefile')


    models = {
        'django_data_mirror.datasourcecontrol': {
            'Meta': {'object_name': 'DataSourceControl'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1000', 'db_index': 'True'})
        },
        u'django_data_mirror.datasourcefile': {
            'Meta': {'object_name': 'DataSourceFile'},
            'complete': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'completed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'db_index': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['django_data_mirror.DataSourceControl']"}),
            'total_lines': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'total_lines_complete': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['django_data_mirror']