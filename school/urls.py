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
        direct_to_template, {'template': 'school/home.html'}
    ),
    url(
        r'^initial$',
        direct_to_template, {'template': 'school/initial.html'}
    ),
        url(
        r'^initial1$',
        direct_to_template, {'template': 'school/initial1.html'}
    ),
    url(
        r'^midterm$',
        direct_to_template, {'template': 'school/midterm.html'}
    ),
    url(
        r'^final$',
        direct_to_template, {'template': 'school/final.html'}
    ),
    url(
        r'^progress$',
        direct_to_template, {'template': 'school/progress.html'}
    ),
    url(
        r'^finance$',
        direct_to_template, {'template': 'school/finance.html'}
    ),
    url(
        r'^studentcharge$',
        direct_to_template, {'template': 'school/studentcharge.html'}
    ),
        url(
        r'^modifyproject$',
        direct_to_template, {'template': 'school/modifyproject.html'}
    ),
            url(
        r'^projectapp$',
        direct_to_template, {'template': 'school/projectapp.html'}
    ),
            url(
        r'^application$',
        direct_to_template, {'template': 'school/application.html'}
    ),
)
