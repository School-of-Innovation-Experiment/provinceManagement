# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProjectSingle'
        db.create_table('school_projectsingle', (
            ('project_id', self.gf('django.db.models.fields.CharField')(default=UUID('b572aea3-e078-4c23-ae96-ae66973c670b'), unique=True, max_length=50, primary_key=True)),
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
            ('content_id', self.gf('django.db.models.fields.CharField')(default=UUID('471174b6-8f14-4895-8e35-01f58d94ad2b'), unique=True, max_length=50, primary_key=True)),
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
            ('content_id', self.gf('django.db.models.fields.CharField')(default=UUID('e070cdd4-2313-47fa-a55d-3bcc5d4ac258'), unique=True, max_length=50, primary_key=True)),
            ('project_id', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['school.ProjectSingle'], unique=True)),
            ('achievement_fashion', self.gf('django.db.models.fields.CharField')(max_length=200, blank=True)),
            ('achievement_summary', self.gf('django.db.models.fields.TextField')()),
            ('inspector_comments', self.gf('django.db.models.fields.TextField')()),
            ('school_comments', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('school', ['FinalSubmit'])

        # Adding model 'TechCompetition'
        db.create_table('school_techcompetition', (
            ('content_id', self.gf('django.db.models.fields.CharField')(default=UUID('100899d9-7156-4c14-b26e-08c0e8118f26'), unique=True, max_length=50, primary_key=True)),
            ('project_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.FinalSubmit'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('members', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('competition_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('competition_grade', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('school', ['TechCompetition'])

        # Adding model 'Patents'
        db.create_table('school_patents', (
            ('content_id', self.gf('django.db.models.fields.CharField')(default=UUID('50ce4a86-8763-4e30-880e-0899ad90c6ac'), unique=True, max_length=50, primary_key=True)),
            ('project_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.FinalSubmit'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('members', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('finish_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('school', ['Patents'])

        # Adding model 'Papers'
        db.create_table('school_papers', (
            ('content_id', self.gf('django.db.models.fields.CharField')(default=UUID('cea93bf8-f2b9-4f2c-bb47-c086678e329e'), unique=True, max_length=50, primary_key=True)),
            ('project_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.FinalSubmit'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('members', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('publication', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('finish_date', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('school', ['Papers'])

        # Adding model 'AchievementObjects'
        db.create_table('school_achievementobjects', (
            ('content_id', self.gf('django.db.models.fields.CharField')(default=UUID('48126716-0560-4cdd-9e4a-f2d1685e4c9e'), unique=True, max_length=50, primary_key=True)),
            ('project_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.FinalSubmit'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('members', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('finish_date', self.gf('django.db.models.fields.DateField')()),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('school', ['AchievementObjects'])

        # Adding model 'UploadedFiles'
        db.create_table('school_uploadedfiles', (
            ('file_id', self.gf('django.db.models.fields.CharField')(default=UUID('1db2d2e3-64c0-43ba-8a63-479d3b550e76'), unique=True, max_length=50, primary_key=True)),
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
            'category': ('django.db.models.fields.CharField', [], {'default': "'undifined'", 'unique': 'True', 'max_length': '30'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'const.projectgrade': {
            'Meta': {'object_name': 'ProjectGrade'},
            'grade': ('django.db.models.fields.CharField', [], {'default': "'undifined'", 'unique': 'True', 'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'const.projectstatus': {
            'Meta': {'object_name': 'ProjectStatus'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'undifined'", 'unique': 'True', 'max_length': '50'})
        },
        'const.schooldict': {
            'Meta': {'object_name': 'SchoolDict'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'schoolName': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'})
        },
        'school.achievementobjects': {
            'Meta': {'object_name': 'AchievementObjects'},
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_id': ('django.db.models.fields.CharField', [], {'default': "UUID('48126716-0560-4cdd-9e4a-f2d1685e4c9e')", 'unique': 'True', 'max_length': '50', 'primary_key': 'True'}),
            'finish_date': ('django.db.models.fields.DateField', [], {}),
            'members': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.FinalSubmit']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'school.finalsubmit': {
            'Meta': {'object_name': 'FinalSubmit'},
            'achievement_fashion': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'achievement_summary': ('django.db.models.fields.TextField', [], {}),
            'content_id': ('django.db.models.fields.CharField', [], {'default': "UUID('e070cdd4-2313-47fa-a55d-3bcc5d4ac258')", 'unique': 'True', 'max_length': '50', 'primary_key': 'True'}),
            'inspector_comments': ('django.db.models.fields.TextField', [], {}),
            'project_id': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['school.ProjectSingle']", 'unique': 'True'}),
            'school_comments': ('django.db.models.fields.TextField', [], {})
        },
        'school.papers': {
            'Meta': {'object_name': 'Papers'},
            'content_id': ('django.db.models.fields.CharField', [], {'default': "UUID('cea93bf8-f2b9-4f2c-bb47-c086678e329e')", 'unique': 'True', 'max_length': '50', 'primary_key': 'True'}),
            'finish_date': ('django.db.models.fields.DateField', [], {}),
            'members': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.FinalSubmit']"}),
            'publication': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'school.patents': {
            'Meta': {'object_name': 'Patents'},
            'content_id': ('django.db.models.fields.CharField', [], {'default': "UUID('50ce4a86-8763-4e30-880e-0899ad90c6ac')", 'unique': 'True', 'max_length': '50', 'primary_key': 'True'}),
            'finish_date': ('django.db.models.fields.DateField', [], {}),
            'members': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.FinalSubmit']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'school.presubmit': {
            'Meta': {'object_name': 'PreSubmit'},
            'background': ('django.db.models.fields.TextField', [], {}),
            'content_id': ('django.db.models.fields.CharField', [], {'default': "UUID('471174b6-8f14-4895-8e35-01f58d94ad2b')", 'unique': 'True', 'max_length': '50', 'primary_key': 'True'}),
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
            'project_id': ('django.db.models.fields.CharField', [], {'default': "UUID('b572aea3-e078-4c23-ae96-ae66973c670b')", 'unique': 'True', 'max_length': '50', 'primary_key': 'True'}),
            'project_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['const.ProjectStatus']"}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['const.SchoolDict']"}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400'})
        },
        'school.techcompetition': {
            'Meta': {'object_name': 'TechCompetition'},
            'competition_grade': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'competition_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_id': ('django.db.models.fields.CharField', [], {'default': "UUID('100899d9-7156-4c14-b26e-08c0e8118f26')", 'unique': 'True', 'max_length': '50', 'primary_key': 'True'}),
            'members': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.FinalSubmit']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'school.uploadedfiles': {
            'Meta': {'object_name': 'UploadedFiles'},
            'file_id': ('django.db.models.fields.CharField', [], {'default': "UUID('1db2d2e3-64c0-43ba-8a63-479d3b550e76')", 'unique': 'True', 'max_length': '50', 'primary_key': 'True'}),
            'file_obj': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'project_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.ProjectSingle']"})
        }
    }

    complete_apps = ['school']