# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UserProfile'
        db.create_table('users_userprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('machinecode', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('agentID', self.gf('django.db.models.fields.CharField')(default=UUID('4dedd124-8a10-477f-9d72-dca1cd13e1f2'), unique=True, max_length=40)),
            ('workunit', self.gf('django.db.models.fields.CharField')(max_length=2000, blank=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=2000, blank=True)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('users', ['UserProfile'])

        # Adding model 'SchoolProfile'
        db.create_table('users_schoolprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['const.SchoolDict'])),
            ('identity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['const.UserIdentity'])),
        ))
        db.send_create_signal('users', ['SchoolProfile'])

        # Adding model 'ExperterProfile'
        db.create_table('users_experterprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['const.InsituteCategory'])),
            ('identity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['const.UserIdentity'])),
            ('workunit', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('users', ['ExperterProfile'])

        # Adding model 'AdminStaffProfile'
        db.create_table('users_adminstaffprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('identity', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['const.UserIdentity'])),
        ))
        db.send_create_signal('users', ['AdminStaffProfile'])


    def backwards(self, orm):
        # Deleting model 'UserProfile'
        db.delete_table('users_userprofile')

        # Deleting model 'SchoolProfile'
        db.delete_table('users_schoolprofile')

        # Deleting model 'ExperterProfile'
        db.delete_table('users_experterprofile')

        # Deleting model 'AdminStaffProfile'
        db.delete_table('users_adminstaffprofile')


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
        'const.insitutecategory': {
            'Meta': {'object_name': 'InsituteCategory'},
            'category': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'const.schooldict': {
            'Meta': {'object_name': 'SchoolDict'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'schoolName': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'const.useridentity': {
            'Meta': {'object_name': 'UserIdentity'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'users.adminstaffprofile': {
            'Meta': {'object_name': 'AdminStaffProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['const.UserIdentity']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'users.experterprofile': {
            'Meta': {'object_name': 'ExperterProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['const.UserIdentity']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['const.InsituteCategory']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'workunit': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        },
        'users.schoolprofile': {
            'Meta': {'object_name': 'SchoolProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identity': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['const.UserIdentity']"}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['const.SchoolDict']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'})
        },
        'users.userprofile': {
            'Meta': {'object_name': 'UserProfile'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'}),
            'agentID': ('django.db.models.fields.CharField', [], {'default': "UUID('4dedd124-8a10-477f-9d72-dca1cd13e1f2')", 'unique': 'True', 'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'machinecode': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True'}),
            'workunit': ('django.db.models.fields.CharField', [], {'max_length': '2000', 'blank': 'True'})
        }
    }

    complete_apps = ['users']