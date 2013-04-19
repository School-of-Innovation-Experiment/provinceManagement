# -*- coding: UTF-8 -*-
'''
Created on 2013-3-11

@author: yaoyuan
'''

from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from teacher import views as teacher_views

urlpatterns = patterns('',
    
    url(
        r'^dispatch',
        teacher_views.StudentDispatch,
    ),
    url(
        r'^$',
        teacher_views.home_view,
    ),
    url(
        r'^history$',
        direct_to_template, {'template': 'teacher/history.html'}
    ),
    url(
        r'^initial$',
        direct_to_template, {'template': 'teacher/initial.html'}
    ),
    url(
        r'^midterm$',
        direct_to_template, {'template': 'teacher/initial.html'}
    ),
    url(
        r'^final$',
        direct_to_template, {'template': 'teacher/initial.html'}
    ),
    url(
        r'^progress$',
        direct_to_template, {'template': 'teacher/progress.html'}
    ),
    url(
        r'^finance$',
        direct_to_template, {'template': 'teacher/finance.html'}
    ),
    url(
        r'^studentcharge$',
        direct_to_template, {'template': 'teacher/studentcharge.html'}
    ),
        url(
        r'^modifyproject$',
        direct_to_template, {'template': 'teacher/modifyproject.html'}
    ),
            url(
        r'^projectapp$',
        direct_to_template, {'template': 'teacher/projectapp.html'}
    ),
)
