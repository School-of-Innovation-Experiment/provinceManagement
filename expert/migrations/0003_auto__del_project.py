# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Project'
        db.delete_table('expert_project')


    def backwards(self, orm):
        # Adding model 'Project'
        db.create_table('expert_project', (
            ('project_name', self.gf('django.db.models.fields.TextField')()),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('expert', ['Project'])


    models = {
        
    }

    complete_apps = ['expert']