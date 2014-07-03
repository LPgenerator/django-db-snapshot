# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Log'
        db.create_table(u'dbsnapshot_log', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('server', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dbsnapshot.Server'])),
            ('date', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')()),
            ('end', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('elapsed', self.gf('django.db.models.fields.FloatField')()),
            ('success', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('method', self.gf('django.db.models.fields.PositiveIntegerField')()),
        ))
        db.send_create_signal(u'dbsnapshot', ['Log'])


    def backwards(self, orm):
        # Deleting model 'Log'
        db.delete_table(u'dbsnapshot_log')


    models = {
        u'dbsnapshot.log': {
            'Meta': {'object_name': 'Log'},
            'date': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'elapsed': ('django.db.models.fields.FloatField', [], {}),
            'end': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'method': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'server': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['dbsnapshot.Server']"}),
            'start': ('django.db.models.fields.DateTimeField', [], {}),
            'success': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
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