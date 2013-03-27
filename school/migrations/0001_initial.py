# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProjectSingle'
        db.create_table('school_projectsingle', (
            ('project_id', self.gf('django.db.models.fields.CharField')(default=UUID('c8b44ba3-3ac3-402c-a5b7-a8d5d4bdd581'), unique=True, max_length=50, primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['const.SchoolDict'])),
            ('project_category', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['const.ProjectCategory'])),
            ('insitute', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['const.InsituteCategory'])),
            ('project_grade', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['const.ProjectGrade'])),
            ('project_status', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['const.ProjectStatus'])),
            ('email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('telephone', self.gf('django.db.models.fields.CharField')(max_length=20, blank=True)),
            ('inspector', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('members', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('im', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('school', ['ProjectSingle'])

        # Adding model 'PreSubmit'
        db.create_table('school_presubmit', (
            ('content_id', self.gf('django.db.models.fields.CharField')(default=UUID('cc72ffcd-a6be-467a-ae98-22c0e7d16938'), unique=True, max_length=50, primary_key=True)),
            ('project_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['school.ProjectSingle'], unique=True)),
            ('original', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('background', self.gf('django.db.models.fields.TextField')()),
            ('key_notes', self.gf('django.db.models.fields.TextField')()),
            ('innovation', self.gf('django.db.models.fields.TextField')()),
            ('progress_plan', self.gf('django.db.models.fields.TextField')()),
            ('pre_results', self.gf('django.db.models.fields.TextField')()),
            ('inspector_comments', self.gf('django.db.models.fields.TextField')()),
            ('school_comments', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('school', ['PreSubmit'])

        # Adding model 'FinalSubmit'
        db.create_table('school_finalsubmit', (
            ('content_id', self.gf('django.db.models.fields.CharField')(default=UUID('c206209c-9129-4175-8bce-4357789688f8'), unique=True, max_length=50, primary_key=True)),
            ('project_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['school.ProjectSingle'], unique=True)),
            ('achievement_fashion', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('achievement_summary', self.gf('django.db.models.fields.TextField')()),
            ('inspector_comments', self.gf('django.db.models.fields.TextField')()),
            ('school_comments', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('school', ['FinalSubmit'])

        # Adding model 'TechCompetition'
        db.create_table('school_techcompetition', (
            ('content_id', self.gf('django.db.models.fields.CharField')(default=UUID('ac8c027b-f564-4239-840b-1712177c7a67'), unique=True, max_length=50, primary_key=True)),
            ('project_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.FinalSubmit'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('members', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('competition_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('competition_grade', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('school', ['TechCompetition'])

        # Adding model 'Patents'
        db.create_table('school_patents', (
            ('content_id', self.gf('django.db.models.fields.CharField')(default=UUID('2335c919-3fd1-4e64-a90a-c0c7e1af0806'), unique=True, max_length=50, primary_key=True)),
            ('project_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.FinalSubmit'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('members', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('finish_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('school', ['Patents'])

        # Adding model 'Papers'
        db.create_table('school_papers', (
            ('content_id', self.gf('django.db.models.fields.CharField')(default=UUID('a12782fb-b3a9-4b84-9aaf-0cf43a2c721f'), unique=True, max_length=50, primary_key=True)),
            ('project_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.FinalSubmit'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('members', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('publication', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('finish_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('school', ['Papers'])

        # Adding model 'AchievementObjects'
        db.create_table('school_achievementobjects', (
            ('content_id', self.gf('django.db.models.fields.CharField')(default=UUID('1e3abc0a-bdaa-47a6-8bff-2c554d3c5d6c'), unique=True, max_length=50, primary_key=True)),
            ('project_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.FinalSubmit'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('members', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('finish_date', self.gf('django.db.models.fields.DateField')()),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('school', ['AchievementObjects'])

        # Adding model 'UploadedFiles'
        db.create_table('school_uploadedfiles', (
            ('file_id', self.gf('django.db.models.fields.CharField')(default=UUID('ea5b0c16-e1be-4a3e-8982-e6eb4a6e533c'), unique=True, max_length=50, primary_key=True)),
            ('project_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.ProjectSingle'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('file_obj', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('school', ['UploadedFiles'])


    def backwards(self, orm):
        # Deleting model 'ProjectSingle'
        db.delete_table('school_projectsingle')

        # Deleting model 'PreSubmit'
        db.delete_table('school_presubmit')

        # Deleting model 'FinalSubmit'
        db.delete_table('school_finalsubmit')

        # Deleting model 'TechCompetition'
        db.delete_table('school_techcompetition')

        # Deleting model 'Patents'
        db.delete_table('school_patents')

        # Deleting model 'Papers'
        db.delete_table('school_papers')

        # Deleting model 'AchievementObjects'
        db.delete_table('school_achievementobjects')

        # Deleting model 'UploadedFiles'
        db.delete_table('school_uploadedfiles')


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
        'school.achievementobjects': {
            'Meta': {'object_name': 'AchievementObjects'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_id': ('django.db.models.fields.CharField', [], {'default': "UUID('1e3abc0a-bdaa-47a6-8bff-2c554d3c5d6c')", 'unique': 'True', 'max_length': '50', 'primary_key': 'True'}),
            'finish_date': ('django.db.models.fields.DateField', [], {}),
            'members': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.FinalSubmit']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'school.finalsubmit': {
            'Meta': {'object_name': 'FinalSubmit'},
            'achievement_fashion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'achievement_summary': ('django.db.models.fields.TextField', [], {}),
            'content_id': ('django.db.models.fields.CharField', [], {'default': "UUID('c206209c-9129-4175-8bce-4357789688f8')", 'unique': 'True', 'max_length': '50', 'primary_key': 'True'}),
            'inspector_comments': ('django.db.models.fields.TextField', [], {}),
            'project_id': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['school.ProjectSingle']", 'unique': 'True'}),
            'school_comments': ('django.db.models.fields.TextField', [], {})
        },
        'school.papers': {
            'Meta': {'object_name': 'Papers'},
            'content_id': ('django.db.models.fields.CharField', [], {'default': "UUID('a12782fb-b3a9-4b84-9aaf-0cf43a2c721f')", 'unique': 'True', 'max_length': '50', 'primary_key': 'True'}),
            'finish_date': ('django.db.models.fields.DateField', [], {}),
            'members': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.FinalSubmit']"}),
            'publication': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'school.patents': {
            'Meta': {'object_name': 'Patents'},
            'content_id': ('django.db.models.fields.CharField', [], {'default': "UUID('2335c919-3fd1-4e64-a90a-c0c7e1af0806')", 'unique': 'True', 'max_length': '50', 'primary_key': 'True'}),
            'finish_date': ('django.db.models.fields.DateField', [], {}),
            'members': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.FinalSubmit']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'school.presubmit': {
            'Meta': {'object_name': 'PreSubmit'},
            'background': ('django.db.models.fields.TextField', [], {}),
            'content_id': ('django.db.models.fields.CharField', [], {'default': "UUID('cc72ffcd-a6be-467a-ae98-22c0e7d16938')", 'unique': 'True', 'max_length': '50', 'primary_key': 'True'}),
            'innovation': ('django.db.models.fields.TextField', [], {}),
            'inspector_comments': ('django.db.models.fields.TextField', [], {}),
            'key_notes': ('django.db.models.fields.TextField', [], {}),
            'original': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'pre_results': ('django.db.models.fields.TextField', [], {}),
            'progress_plan': ('django.db.models.fields.TextField', [], {}),
            'project_id': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['school.ProjectSingle']", 'unique': 'True'}),
            'school_comments': ('django.db.models.fields.TextField', [], {})
        },
        'school.projectsingle': {
            'Meta': {'object_name': 'ProjectSingle'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'im': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'insitute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['const.InsituteCategory']"}),
            'inspector': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'members': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'project_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['const.ProjectCategory']"}),
            'project_grade': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['const.ProjectGrade']"}),
            'project_id': ('django.db.models.fields.CharField', [], {'default': "UUID('c8b44ba3-3ac3-402c-a5b7-a8d5d4bdd581')", 'unique': 'True', 'max_length': '50', 'primary_key': 'True'}),
            'project_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['const.ProjectStatus']"}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['const.SchoolDict']"}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        },
        'school.techcompetition': {
            'Meta': {'object_name': 'TechCompetition'},
            'competition_grade': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'competition_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_id': ('django.db.models.fields.CharField', [], {'default': "UUID('ac8c027b-f564-4239-840b-1712177c7a67')", 'unique': 'True', 'max_length': '50', 'primary_key': 'True'}),
            'members': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.FinalSubmit']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'school.uploadedfiles': {
            'Meta': {'object_name': 'UploadedFiles'},
            'file_id': ('django.db.models.fields.CharField', [], {'default': "UUID('ea5b0c16-e1be-4a3e-8982-e6eb4a6e533c')", 'unique': 'True', 'max_length': '50', 'primary_key': 'True'}),
            'file_obj': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.ProjectSingle']"})
        }
    }

    complete_apps = ['school']