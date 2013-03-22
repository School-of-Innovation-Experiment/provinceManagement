# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table('expert_project', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('project_name', self.gf('django.db.models.fields.TextField')()),
            ('project_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('expert', ['Project'])


    def backwards(self, orm):
        # Deleting model 'Project'
        db.delete_table('expert_project')


    models = {
        'expert.project': {
            'Meta': {'object_name': 'Project'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project_name': ('django.db.models.fields.TextField', [], {}),
            'project_type': ('django.db.models.fields.CharField', [], {'max_length': '1'})
        }
    }

    complete_apps = ['expert']