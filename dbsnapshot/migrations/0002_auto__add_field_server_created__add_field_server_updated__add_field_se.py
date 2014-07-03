# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Server.created'
        db.add_column(u'dbsnapshot_server', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 7, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Server.updated'
        db.add_column(u'dbsnapshot_server', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, default=datetime.datetime(2014, 7, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Server.status'
        db.add_column(u'dbsnapshot_server', 'status',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Server.created'
        db.delete_column(u'dbsnapshot_server', 'created')

        # Deleting field 'Server.updated'
        db.delete_column(u'dbsnapshot_server', 'updated')

        # Deleting field 'Server.status'
        db.delete_column(u'dbsnapshot_server', 'status')


    models = {
        u'dbsnapshot.server': {
            'Meta': {'object_name': 'Server'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'days': ('django.db.models.fields.PositiveIntegerField', [], {'default': '7'}),
            'host': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'per_day': ('django.db.models.fields.PositiveIntegerField', [], {'default': '6'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '61216'}),
            'status': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['dbsnapshot']