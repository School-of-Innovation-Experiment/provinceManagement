# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SchoolDict'
        db.create_table('const_schooldict', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('schoolName', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal('const', ['SchoolDict'])

        # Adding model 'ProjectCategory'
        db.create_table('const_projectcategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
        ))
        db.send_create_signal('const', ['ProjectCategory'])

        # Adding model 'InsituteCategory'
        db.create_table('const_insitutecategory', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
        ))
        db.send_create_signal('const', ['InsituteCategory'])

        # Adding model 'UserIdentity'
        db.create_table('const_useridentity', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('identity', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('const', ['UserIdentity'])

        # Adding model 'ProjectGrade'
        db.create_table('const_projectgrade', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('grade', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
        ))
        db.send_create_signal('const', ['ProjectGrade'])

        # Adding model 'ProjectStatus'
        db.create_table('const_projectstatus', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('status', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
        ))
        db.send_create_signal('const', ['ProjectStatus'])


    def backwards(self, orm):
        # Deleting model 'SchoolDict'
        db.delete_table('const_schooldict')

        # Deleting model 'ProjectCategory'
        db.delete_table('const_projectcategory')

        # Deleting model 'InsituteCategory'
        db.delete_table('const_insitutecategory')

        # Deleting model 'UserIdentity'
        db.delete_table('const_useridentity')

        # Deleting model 'ProjectGrade'
        db.delete_table('const_projectgrade')

        # Deleting model 'ProjectStatus'
        db.delete_table('const_projectstatus')


    models = {
        'const.insitutecategory': {
            'Meta': {'object_name': 'InsituteCategory'},
            'category': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'const.projectcategory': {
            'Meta': {'object_name': 'ProjectCategory'},
            'category': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'const.projectgrade': {
            'Meta': {'object_name': 'ProjectGrade'},
            'grade': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'const.projectstatus': {
            'Meta': {'object_name': 'ProjectStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'})
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
        }
    }

    complete_apps = ['const']