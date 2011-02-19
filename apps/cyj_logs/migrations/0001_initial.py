# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'SearchLog'
        db.create_table('cyj_logs_searchlog', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(default=40, blank=True)),
            ('tuvo_exito', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('type_search', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('cyj_logs', ['SearchLog'])


    def backwards(self, orm):
        
        # Deleting model 'SearchLog'
        db.delete_table('cyj_logs_searchlog')


    models = {
        'cyj_logs.searchlog': {
            'Meta': {'object_name': 'SearchLog'},
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'default': '40', 'blank': 'True'}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'tuvo_exito': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'type_search': ('django.db.models.fields.TextField', [], {}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['cyj_logs']
