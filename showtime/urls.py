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
                           # direct_to_template, {'template': 'showtime/showtime.html'}
                           ),
                       )
