# coding: UTF-8
'''
Created on 2013-3-11

@author: songyang
'''

from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from showtime import views as showtime_views


__author__ = {"songyang":"songyang8464@foxmail.com"}


urlpatterns = patterns('',
                       url(r'^$',
                       showtime_views.show_index,
                       ),
                       url(r'^(?P<project_id>.{36})$', 
                       showtime_views.show_project,
                       ),
)
