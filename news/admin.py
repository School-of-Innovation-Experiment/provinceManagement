# coding: UTF-8
'''
Created on Sat Mar 23 17:12:56 2013

@author: Liao Pengyu

Desc: admin of news
'''

from django.contrib import admin
from news.models import *

from settings import STATIC_URL

RegisterClass =tuple()

for item in RegisterClass:
    admin.site.register(item)

class NewsAdmin(admin.ModelAdmin):
    list_display = ('news_title', 'news_date', )#'news_content',
    # fields = list_display
    class Media:
        js = [
            # STATIC_URL + '/tiny_mce/tiny_mce_src.js',
            STATIC_URL + '/tiny_mce/tiny_mce.js',
            STATIC_URL + '/tiny_mce/tiny_textarea.js',
            ]

admin.site.register(News, NewsAdmin)
