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
    url(r'^open/(?P<pid>.{36})$',
        school_views.open_report_view,
        ),

    url(r'^final/(?P<pid>.{36})$',
        school_views.final_report_view,
        ),
    url(r'^mid/(?P<pid>.{36})$',
        school_views.mid_report_view,
        ),
    url(r'^title_change/$',
        school_views.title_change,
        ),

    url(r'^memberchange/(?P<pid>.{36})$',
        school_views.member_change),
    url(
        r'^$',
        school_views.home_view,
        name='school_home'
  	    ),
    url(
        r'^dispatch$',
        school_views.dispatch,
        ),
    url(
        r'^project_limitnumSettings$',
        school_views.project_limitnumSettings,
        ),
#    url(
#       r'^subject_rating$',
#       school_views.SubjectRating,
#       ),
    url(
        r'^fundsmanage/$',
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
    url(
        r'^project_informationexport$',
        school_views.project_informationexport
        ),
    url(r'^file_download/(?P<fileid>.{36})$',
        school_views.file_download,name="school_downloadfile"),
)
