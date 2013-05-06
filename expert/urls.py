# coding: UTF-8
'''
Created on Tue Mar 12 21:39:38 2013

@author: Liao Pengyu

Desc: urls for expert
'''
from django.conf.urls import patterns, url
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from expert import views as expert_views


urlpatterns = patterns('',
    url(
        r'^$',
        expert_views.home_view,
    ),
    url(
        r'^review/(?P<pid>.{36})$',
        expert_views.review_report_view,
    ),
    url(
        r'^review/(?P<file_id>.{36})/download$',
        expert_views.download_view,
    ),
)
