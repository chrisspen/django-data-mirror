# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DataSourceControl'
        db.create_table(u'django_data_mirror_datasourcecontrol', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.CharField')(unique=True, max_length=1000)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'django_data_mirror', ['DataSourceControl'])


    def backwards(self, orm):
        # Deleting model 'DataSourceControl'
        db.delete_table(u'django_data_mirror_datasourcecontrol')


    models = {
        u'django_data_mirror.datasourcecontrol': {
            'Meta': {'object_name': 'DataSourceControl'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '1000'})
        }
    }

    complete_apps = ['django_data_mirror']