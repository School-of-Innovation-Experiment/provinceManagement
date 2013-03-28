# coding: UTF-8
'''
Created on 2013-3-28

@author: tianwei

Desc: School URL defination
'''

from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from school import views as school_views


urlpatterns = patterns('',
    url(
        r'^$',
        school_views.home_view,
        name="school_views.home_view"
    ),
    url(
        r'^final/(?P<pid>.{36})$',
        school_views.final_report_view,
        name="school_views.final_report_view"
    ),
    url(
        r'^application/(?P<pid>.{36})$',
        school_views.application_report_view,
    ),
    url(
        r'^statistics/$',
        school_views.statistics_view,
        name="school_views.statistics_view"
    ),
    url(
        r'^new/$',
        school_views.new_report_view,
        name="school_views.new_report_view"
    ),
    url(
        r'^history/$',
        school_views.history_view,
        name="school_views.history_view"
    ),


)
