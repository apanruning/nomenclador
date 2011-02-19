# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MaapMetadata'
        db.create_table('maap_maapmetadata', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('maap', ['MaapMetadata'])

        # Adding model 'MaapModel'
        db.create_table('maap_maapmodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=50, null=True, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('changed', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='creators', to=orm['auth.User'])),
            ('editor', self.gf('django.db.models.fields.related.ForeignKey')(related_name='editors', to=orm['auth.User'])),
            ('tags', self.gf('tagging.fields.TagField')(default='')),
            ('banner_slots', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('default_layers', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('metadata', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['maap.MaapMetadata'], null=True, blank=True)),
        ))
        db.send_create_signal('maap', ['MaapModel'])

        # Adding M2M table for field category on 'MaapModel'
        db.create_table('maap_maapmodel_category', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('maapmodel', models.ForeignKey(orm['maap.maapmodel'], null=False)),
            ('maapcategory', models.ForeignKey(orm['maap.maapcategory'], null=False))
        ))
        db.create_unique('maap_maapmodel_category', ['maapmodel_id', 'maapcategory_id'])

        # Adding model 'MaapCategory'
        db.create_table('maap_maapcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=50, db_index=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['maap.MaapCategory'])),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('show_all', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('maap', ['MaapCategory'])

        # Adding model 'MaapPoint'
        db.create_table('maap_maappoint', (
            ('maapmodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['maap.MaapModel'], unique=True, primary_key=True)),
            ('geom', self.gf('django.contrib.gis.db.models.fields.PointField')(srid=900913)),
            ('icon', self.gf('django.db.models.fields.related.ForeignKey')(default=185, to=orm['maap.Icon'], blank=True)),
            ('closest', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('popup_text', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('maap', ['MaapPoint'])

        # Adding model 'MaapArea'
        db.create_table('maap_maaparea', (
            ('maapmodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['maap.MaapModel'], unique=True, primary_key=True)),
            ('geom', self.gf('django.contrib.gis.db.models.fields.PolygonField')(srid=900913)),
        ))
        db.send_create_signal('maap', ['MaapArea'])

        # Adding model 'MaapZone'
        db.create_table('maap_maapzone', (
            ('maaparea_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['maap.MaapArea'], unique=True, primary_key=True)),
        ))
        db.send_create_signal('maap', ['MaapZone'])

        # Adding model 'MaapMultiLine'
        db.create_table('maap_maapmultiline', (
            ('maapmodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['maap.MaapModel'], unique=True, primary_key=True)),
            ('geom', self.gf('django.contrib.gis.db.models.fields.MultiLineStringField')(srid=900913)),
        ))
        db.send_create_signal('maap', ['MaapMultiLine'])

        # Adding model 'Icon'
        db.create_table('maap_icon', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
        ))
        db.send_create_signal('maap', ['Icon'])


    def backwards(self, orm):
        
        # Deleting model 'MaapMetadata'
        db.delete_table('maap_maapmetadata')

        # Deleting model 'MaapModel'
        db.delete_table('maap_maapmodel')

        # Removing M2M table for field category on 'MaapModel'
        db.delete_table('maap_maapmodel_category')

        # Deleting model 'MaapCategory'
        db.delete_table('maap_maapcategory')

        # Deleting model 'MaapPoint'
        db.delete_table('maap_maappoint')

        # Deleting model 'MaapArea'
        db.delete_table('maap_maaparea')

        # Deleting model 'MaapZone'
        db.delete_table('maap_maapzone')

        # Deleting model 'MaapMultiLine'
        db.delete_table('maap_maapmultiline')

        # Deleting model 'Icon'
        db.delete_table('maap_icon')


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
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creators'", 'to': "orm['auth.User']"}),
            'default_layers': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'editor': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'editors'", 'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'metadata': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['maap.MaapMetadata']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"})
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
        }
    }

    complete_apps = ['maap']
