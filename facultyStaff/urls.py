'''
Created on 2013-3-20

@author: sytmac
'''
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
urlpatterns = patterns('',
    url(
        r'^instructor_dispatch/$',
        direct_to_template, {'template': 'facultyStaff/instructor_dispatch.html'}
    ),
    url(
        r'^subject_feedback/$',
        direct_to_template, {'template': 'facultyStaff/subject_feedback.html'}
    ),
    url(
        r'^$',
        direct_to_template, {'template': 'facultyStaff/administrator.html'}
    ),
)
