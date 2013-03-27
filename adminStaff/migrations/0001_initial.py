# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ProjectControl'
        db.create_table('adminStaff_projectcontrol', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('pre_start_day', self.gf('django.db.models.fields.DateField')()),
            ('pre_end_day', self.gf('django.db.models.fields.DateField')()),
            ('pre_start_day_review', self.gf('django.db.models.fields.DateField')()),
            ('pre_end_day_review', self.gf('django.db.models.fields.DateField')()),
            ('final_start_day', self.gf('django.db.models.fields.DateField')()),
            ('final_end_day', self.gf('django.db.models.fields.DateField')()),
            ('final_start_day_review', self.gf('django.db.models.fields.DateField')()),
            ('final_end_day_review', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal('adminStaff', ['ProjectControl'])

        # Adding model 'ProjectPerLimits'
        db.create_table('adminStaff_projectperlimits', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('school', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['users.SchoolProfile'], unique=True)),
            ('number', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('adminStaff', ['ProjectPerLimits'])

        # Adding model 'ReviewTask'
        db.create_table('adminStaff_reviewtask', (
            ('review_id', self.gf('django.db.models.fields.CharField')(default=UUID('da3e2986-a4f8-49b3-a655-2a5f3e66843c'), unique=True, max_length=50, primary_key=True)),
            ('project_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['school.ProjectSingle'])),
            ('experter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['users.ExpertProfile'])),
            ('comments', self.gf('django.db.models.fields.TextField')()),
            ('scores', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('adminStaff', ['ReviewTask'])


    def backwards(self, orm):
        # Deleting model 'ProjectControl'
        db.delete_table('adminStaff_projectcontrol')

        # Deleting model 'ProjectPerLimits'
        db.delete_table('adminStaff_projectperlimits')

        # Deleting model 'ReviewTask'
        db.delete_table('adminStaff_reviewtask')


    models = {
        'adminStaff.projectcontrol': {
            'Meta': {'object_name': 'ProjectControl'},
            'final_end_day': ('django.db.models.fields.DateField', [], {}),
            'final_end_day_review': ('django.db.models.fields.DateField', [], {}),
            'final_start_day': ('django.db.models.fields.DateField', [], {}),
            'final_start_day_review': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pre_end_day': ('django.db.models.fields.DateField', [], {}),
            'pre_end_day_review': ('django.db.models.fields.DateField', [], {}),
            'pre_start_day': ('django.db.models.fields.DateField', [], {}),
            'pre_start_day_review': ('django.db.models.fields.DateField', [], {})
        },
        'adminStaff.projectperlimits': {
            'Meta': {'object_name': 'ProjectPerLimits'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'number': ('django.db.models.fields.IntegerField', [], {}),
            'school': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['users.SchoolProfile']", 'unique': 'True'})
        },
        'adminStaff.reviewtask': {
            'Meta': {'object_name': 'ReviewTask'},
            'comments': ('django.db.models.fields.TextField', [], {}),
            'experter': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['users.ExpertProfile']"}),
            'project_id': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['school.ProjectSingle']"}),
            'review_id': ('django.db.models.fields.CharField', [], {'default': "UUID('da3e2986-a4f8-49b3-a655-2a5f3e66843c')", 'unique': 'True', 'max_length': '50', 'primary_key': 'True'}),
            'scores': ('django.db.models.fields.IntegerField', [], {})
        },
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
        'school.projectsingle': {
            'Meta': {'object_name': 'ProjectSingle'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'im': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'insitute': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['const.InsituteCategory']"}),
            'inspector': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'members': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'project_category': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['const.ProjectCategory']"}),
            'project_grade': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['const.ProjectGrade']"}),
            'project_id': ('django.db.models.fields.CharField', [], {'default': "UUID('559d6b5d-5d4a-40e7-a210-2901a303995f')", 'unique': 'True', 'max_length': '50', 'primary_key': 'True'}),
            'project_status': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['const.ProjectStatus']"}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['const.SchoolDict']"}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '400'})
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

    complete_apps = ['adminStaff']