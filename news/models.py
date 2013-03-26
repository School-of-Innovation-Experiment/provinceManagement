# coding: UTF-8
'''
Created on Sat Mar 23 17:12:42 2013

@author: Liao Pengyu

Desc: news model
'''


from django.db import models
import datetime

class News(models.Model):
    news_title = models.CharField(verbose_name = u"标题",
                                  blank=True, max_length=100)
    news_content = models.TextField(verbose_name = u"新闻内容",
                                    blank=True)
    news_date = models.DateField(verbose_name = u"发表时间",
                                 default=datetime.datetime.today,
                                 blank=True)
