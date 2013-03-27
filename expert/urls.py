# coding: UTF-8
'''
Created on Tue Mar 12 21:39:38 2013

@author: Liao Pengyu

Desc: urls for expert
'''
from django.conf.urls import patterns, url
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

urlpatterns = patterns('',
                       url(
        r'^$',
        direct_to_template,
        {'template': 'expert/home.html'}),
                       url(
        r'^profile/$',
        direct_to_template,
        {'template': 'expert/profile.html'}),
                       url(
        r'^profile_edit/$',
        direct_to_template,
        {'template': 'expert/profile_edit.html'}),
                       )
