# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'News'
        db.create_table('news_news', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('news_title', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('news_content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('news_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 3, 27, 0, 0), blank=True)),
            ('news_document', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('news', ['News'])


    def backwards(self, orm):
        # Deleting model 'News'
        db.delete_table('news_news')


    models = {
        'news.news': {
            'Meta': {'object_name': 'News'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'news_content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'news_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 3, 27, 0, 0)', 'blank': 'True'}),
            'news_document': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'news_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'})
        }
    }

    complete_apps = ['news']