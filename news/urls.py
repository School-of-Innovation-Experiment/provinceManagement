#!/usr/local/bin/python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-04-20 08:27
# Last modified: 2017-04-20 09:05
# Filename: urls.py
# Description:
# coding: UTF-8
'''
Created on Sat Mar 23 17:13:58 2013

@author: Liao Pengyu

Desc: urls of news
'''


from django.conf.urls.defaults import patterns, include, url
# from django.views.generic.simple import direct_to_template

from news import views as news_views
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',
                       url(r'^$',
                           auth_views.login, {'template_name': 'home/new-homepage.html'},
                           # news_views.index_new,
                           #news_views.index,
                           name='auth_login',
                           ),
                       url(r'^newslist/(?P<news_id>\d+)$',
                           news_views.read_news,
                           name='read_news'
                           ),
                       url(r'^newslist/(?P<news_id>\d+)/download_news_doc$',
                           news_views.download_news_doc,
                           ),
                       url(r'^newslist/$',
                           news_views.list_news,
                           name='newslist',
                           ),
                       url(r'^newslist/news_cate=(?P<news_cate>\S+)$',
                           news_views.list_news_by_cate,
                           name='newslist_cate'
                           ),
                       )
