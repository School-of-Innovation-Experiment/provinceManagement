# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'AuthorityRelation'
        db.create_table('users_authorityrelation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('userid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('authority', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['const.UserIdentity'])),
        ))
        db.send_create_signal('users', ['AuthorityRelation'])

        # Adding unique constraint on 'AuthorityRelation', fields ['userid', 'authority']
        db.create_unique('users_authorityrelation', ['userid_id', 'authority_id'])

        # Adding model 'SchoolProfile'
        db.create_table('users_schoolprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['const.SchoolDict'], unique=True)),
            ('userid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.AuthorityRelation'], unique=True)),
        ))
        db.send_create_signal('users', ['SchoolProfile'])

        # Adding model 'ExpertProfile'
        db.create_table('users_expertprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('userid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.AuthorityRelation'], unique=True)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['const.InsituteCategory'])),
            ('jobs', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('users', ['ExpertProfile'])

        # Adding model 'AdminStaffProfile'
        db.create_table('users_adminstaffprofile', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('userid', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.AuthorityRelation'], unique=True)),
            ('jobs', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('users', ['AdminStaffProfile'])


    def backwards(self, orm):
        # Removing unique constraint on 'AuthorityRelation', fields ['userid', 'authority']
        db.delete_unique('users_authorityrelation', ['userid_id', 'authority_id'])

        # Deleting model 'AuthorityRelation'
        db.delete_table('users_authorityrelation')

        # Deleting model 'SchoolProfile'
        db.delete_table('users_schoolprofile')

        # Deleting model 'ExpertProfile'
        db.delete_table('users_expertprofile')

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
            'identity': ('django.db.models.fields.CharField', [], {'default': "'visitor'", 'unique': 'True', 'max_length': '50'})
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
            'jobs': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'userid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.AuthorityRelation']", 'unique': 'True'})
        },
        'users.authorityrelation': {
            'Meta': {'unique_together': "(('userid', 'authority'),)", 'object_name': 'AuthorityRelation'},
            'authority': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['const.UserIdentity']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'userid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'users.expertprofile': {
            'Meta': {'object_name': 'ExpertProfile'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'jobs': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['const.InsituteCategory']"}),
            'userid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.AuthorityRelation']", 'unique': 'True'})
        },
        'users.schoolprofile': {
            'Meta': {'object_name': 'SchoolProfile'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['const.SchoolDict']", 'unique': 'True'}),
            'userid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.AuthorityRelation']", 'unique': 'True'})
        }
    }

    complete_apps = ['users']