# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Reminder'
        db.create_table(u'reminders_reminder', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('message', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('when', self.gf('django.db.models.fields.DateTimeField')()),
            ('sent', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'reminders', ['Reminder'])


    def backwards(self, orm):
        # Deleting model 'Reminder'
        db.delete_table(u'reminders_reminder')


    models = {
        u'reminders.reminder': {
            'Meta': {'object_name': 'Reminder'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'when': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['reminders']