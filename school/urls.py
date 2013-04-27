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


urlpatterns = patterns(
    '',
    url(
        r'^$',
        school_views.home_view,
  	    ),
    url(
        r'^dispatch$',
        school_views.dispatch,
        ),
    url(
        r'^project_alloc$',
        school_views.project_alloc,
        ),
	url(
		r'^subject_rating$',
		school_views.SubjectRating,
		),
)
