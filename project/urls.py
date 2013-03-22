# coding: UTF-8
'''
Created on 2012-11-5

@author: tianwei
'''

from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',

    url(
        r'^$',
        direct_to_template, {'template': 'project/home.html'}
    ),
    url(
        r'^initial/$',
        direct_to_template, {'template': 'project/initial.html'}
    ),
    url(
        r'^initial/1$',
        direct_to_template, {'template': 'project/initial_1.html'}
    ),
    url(
        r'^initial/2$',
        direct_to_template, {'template': 'project/initial_2.html'}
    ),
    url(
        r'^midterm/$',
        direct_to_template, {'template': 'project/midterm.html'}
    ),
    url(
        r'^final/$',
        direct_to_template, {'template': 'project/final.html'}
    ),
    url(
        r'^progress/$',
        direct_to_template, {'template': 'project/progress.html'}
    ),
)
