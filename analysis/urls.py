# coding: UTF-8
'''
Created on 2013-4-17

@author: tianwei

Desc: Analysis URL defination
'''

from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from analysis import views as anaylsis_views


urlpatterns = patterns('',
    url(
        r'^$',
        anaylsis_views.school_statistics_view,
    ),
    url(
        r'^school/$',
        anaylsis_views.school_statistics_view,
    ),
    url(
        r'^province/$',
        anaylsis_views.province_statistics_view,
    ),
)
