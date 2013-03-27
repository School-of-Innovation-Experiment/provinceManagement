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

urlpatterns = patterns('',
                       url(r'^$',
                           news_views.index,
                           name='homepage',
                           ),
                       url(r'^newslist/(?P<news_id>\d+)$',
                           news_views.read_news,
                           name='read_news'
                           ),
                       url(r'^newslist/$',
                           news_views.list_news,
                           name='newslist',
                           ),
    )
