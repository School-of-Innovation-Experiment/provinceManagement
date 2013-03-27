# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'News.news_document'
        db.add_column('news_news', 'news_document',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'News.news_document'
        db.delete_column('news_news', 'news_document')


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