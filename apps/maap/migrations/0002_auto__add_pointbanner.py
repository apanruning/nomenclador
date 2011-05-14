# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PointBanner'
        db.create_table('maap_pointbanner', (
            ('templatebanner_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['banners.TemplateBanner'], unique=True, primary_key=True)),
            ('point', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maap.MaapPoint'], null=True)),
        ))
        db.send_create_signal('maap', ['PointBanner'])


    def backwards(self, orm):
        
        # Deleting model 'PointBanner'
        db.delete_table('maap_pointbanner')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'banners.banner': {
            'Meta': {'object_name': 'Banner'},
            'clicks': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slot': ('tagging.fields.TagField', [], {}),
            'views': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'})
        },
        'banners.templatebanner': {
            'Meta': {'object_name': 'TemplateBanner', '_ormbases': ['banners.Banner']},
            'banner_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['banners.Banner']", 'unique': 'True', 'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True'}),
            'template': ('django.db.models.fields.CharField', [], {'default': "'banner.html'", 'max_length': '70'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'maap.icon': {
            'Meta': {'object_name': 'Icon'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'maap.maaparea': {
            'Meta': {'ordering': "('created', 'name')", 'object_name': 'MaapArea', '_ormbases': ['maap.MaapModel']},
            'geom': ('django.contrib.gis.db.models.fields.PolygonField', [], {'srid': '900913'}),
            'maapmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['maap.MaapModel']", 'unique': 'True', 'primary_key': 'True'})
        },
        'maap.maapcategory': {
            'Meta': {'object_name': 'MaapCategory'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': "orm['maap.MaapCategory']"}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'show_all': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'maap.maapmetadata': {
            'Meta': {'object_name': 'MaapMetadata'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'maap.maapmodel': {
            'Meta': {'ordering': "('created', 'name')", 'object_name': 'MaapModel'},
            'banner_slots': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'category': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'maapmodel_set'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['maap.MaapCategory']"}),
            'changed': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'created'", 'to': "orm['auth.User']"}),
            'default_layers': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'edited'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maap.MaapMetadata']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'tags': ('tagging.fields.TagField', [], {})
        },
        'maap.maapmultiline': {
            'Meta': {'ordering': "('created', 'name')", 'object_name': 'MaapMultiLine', '_ormbases': ['maap.MaapModel']},
            'geom': ('django.contrib.gis.db.models.fields.MultiLineStringField', [], {'srid': '900913'}),
            'maapmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['maap.MaapModel']", 'unique': 'True', 'primary_key': 'True'})
        },
        'maap.maappoint': {
            'Meta': {'ordering': "('created', 'name')", 'object_name': 'MaapPoint', '_ormbases': ['maap.MaapModel']},
            'closest': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'geom': ('django.contrib.gis.db.models.fields.PointField', [], {'srid': '900913'}),
            'icon': ('django.db.models.fields.related.ForeignKey', [], {'default': '185', 'to': "orm['maap.Icon']", 'blank': 'True'}),
            'maapmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['maap.MaapModel']", 'unique': 'True', 'primary_key': 'True'}),
            'popup_text': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        'maap.maapzone': {
            'Meta': {'ordering': "('created', 'name')", 'object_name': 'MaapZone', '_ormbases': ['maap.MaapArea']},
            'maaparea_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['maap.MaapArea']", 'unique': 'True', 'primary_key': 'True'})
        },
        'maap.pointbanner': {
            'Meta': {'object_name': 'PointBanner', '_ormbases': ['banners.TemplateBanner']},
            'point': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maap.MaapPoint']", 'null': 'True'}),
            'templatebanner_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['banners.TemplateBanner']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['maap']
