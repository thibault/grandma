# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Plan'
        db.create_table(u'billing_plan', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('slug', self.gf('django.db.models.fields.SlugField')(default='', max_length=64)),
            ('price', self.gf('billing.fields.CurrencyField')(max_digits=7, decimal_places=2)),
        ))
        db.send_create_signal(u'billing', ['Plan'])


    def backwards(self, orm):
        # Deleting model 'Plan'
        db.delete_table(u'billing_plan')


    models = {
        u'billing.plan': {
            'Meta': {'object_name': 'Plan'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'price': ('billing.fields.CurrencyField', [], {'max_digits': '7', 'decimal_places': '2'}),
            'slug': ('django.db.models.fields.SlugField', [], {'default': "''", 'max_length': '64'})
        }
    }

    complete_apps = ['billing']