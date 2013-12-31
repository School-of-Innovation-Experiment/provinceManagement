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
        r'^application/(?P<pid>.{36})$',
        school_views.application_report_view,
        ),
    url(r'^final/(?P<pid>.{36})$',
        school_views.final_report_view,
        ),

    url(r'^memberchange/(?P<pid>.{36})$', 
        school_views.member_change),
    url(
        r'^$',
        school_views.home_view,
  	    ),
    url(
        r'^dispatch$',
        school_views.dispatch,
        ),
    url(
        r'^project_limitnumSettings$',
        school_views.project_limitnumSettings,
        ),
	url(
		r'^subject_rating$',
		school_views.SubjectRating,
		),
    url(
        r'^subject_funds$',
        school_views.funds_manage,
        ),
    url(
        r'^fundschange/(?P<pid>.{36}$)',
        school_views.funds_change,
        ),
    url(
        r'^subject_alloc$',
        school_views.SubjectAlloc,
        ),
    url(
        r'^subject_alloc_new$',
        school_views.NewSubjectAlloc,
        ),
    url(
        r'^project_control$',
        school_views.project_control,
        ),
    url(
        r'^processrecord_view/(?P<pid>.{36})$', 
        school_views.record_view
        ),    
)
