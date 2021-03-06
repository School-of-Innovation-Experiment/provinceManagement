# coding: UTF-8
'''
Created on Sat Mar 23 17:12:42 2013

@author: Liao Pengyu

Desc: news model
'''


from django.db import models
import datetime, os
from settings import MEDIA_ROOT
from settings import NEWS_DOCUMENTS_PATH
from const.models import NewsCategory

class News(models.Model):
    news_title = models.CharField(verbose_name = u"标题",
                                  blank=True, max_length=200)
    news_content = models.TextField(verbose_name = u"新闻内容",
                                    blank=True)
    news_date = models.DateField(verbose_name = u"发表时间",
                                 default=datetime.datetime.today,
                                 blank=True)
    news_category = models.ForeignKey(NewsCategory, verbose_name = u"新闻类型", blank=True, null=True)
    news_document = models.FileField(upload_to=NEWS_DOCUMENTS_PATH, null=True, blank=True)

    def document_name(self):
        return os.path.basename(self.news_document.name)

    def __unicode__(self):
        return self.news_title

    class Meta:
        verbose_name = "新闻"
        verbose_name_plural = "新闻"

