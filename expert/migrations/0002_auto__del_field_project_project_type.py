# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Project.project_type'
        db.delete_column('expert_project', 'project_type')


    def backwards(self, orm):
        # Adding field 'Project.project_type'
        db.add_column('expert_project', 'project_type',
                      self.gf('django.db.models.fields.CharField')(default=0, max_length=1),
                      keep_default=False)


    models = {
        'expert.project': {
            'Meta': {'object_name': 'Project'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'project_name': ('django.db.models.fields.TextField', [], {})
        }
    }

    complete_apps = ['expert']