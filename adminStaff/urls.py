'''
Created on 2013-3-18

@author: sytmac
'''
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
urlpatterns = patterns('',
    url(
        r'^expert_dispatch/$',
        direct_to_template, {'template': 'adminStaff/expert_dispatch.html'}
    ),
    url(
        r'^basic_info/$',
        direct_to_template, {'template': 'adminStaff/basic_info.html'}
    ),
    url(
        r'^teacher_dispatch/$',
        direct_to_template, {'template': 'adminStaff/teacher_dispatch.html'}
    ),
    url(
        r'^password_admin/$',
        direct_to_template, {'template': 'adminStaff/password_admin.html'}
    ),
    url(
        r'^subject_feedback/$',
        direct_to_template, {'template': 'adminStaff/subject_feedback.html'}
    ),
    url(
        r'^$',
        direct_to_template, {'template': 'adminStaff/administrator.html'}
    ),
    url(
        r'^settings$',
        direct_to_template, {'template': 'adminStaff/settings.html'}
    ),
)
