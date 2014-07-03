# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Server'
        db.create_table(u'dbsnapshot_server', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('host', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('port', self.gf('django.db.models.fields.PositiveIntegerField')(default=61216)),
            ('days', self.gf('django.db.models.fields.PositiveIntegerField')(default=7)),
            ('per_day', self.gf('django.db.models.fields.PositiveIntegerField')(default=6)),
        ))
        db.send_create_signal(u'dbsnapshot', ['Server'])


    def backwards(self, orm):
        # Deleting model 'Server'
        db.delete_table(u'dbsnapshot_server')


    models = {
        u'dbsnapshot.server': {
            'Meta': {'object_name': 'Server'},
            'days': ('django.db.models.fields.PositiveIntegerField', [], {'default': '7'}),
            'host': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'per_day': ('django.db.models.fields.PositiveIntegerField', [], {'default': '6'}),
            'port': ('django.db.models.fields.PositiveIntegerField', [], {'default': '61216'})
        }
    }

    complete_apps = ['dbsnapshot']