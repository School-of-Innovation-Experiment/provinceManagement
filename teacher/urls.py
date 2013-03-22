# -*- coding: UTF-8 -*-
'''
Created on 2013-3-11

@author: yaoyuan
'''

from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',

    url(
        r'^$',
        direct_to_template, {'template': 'teacher/home.html'}
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
