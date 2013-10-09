'''
Created on 2013-3-18

@author: sytmac
'''
from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from adminStaff.views import AdminStaffService
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()
urlpatterns = patterns('',
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^$',AdminStaffService.home_view),
    url(r'^processrecord$',AdminStaffService.processrecord),
    url(r'^processrecord_view/(?P<pid>.{36})$', AdminStaffService.record_view),
    url(r'^settings$',AdminStaffService.AdminSetting),
    url(r'^DeadlineSettings$',AdminStaffService.DeadlineSetting),
    url(r'^ProjectLimitNumSettings$',AdminStaffService.ProjectLimitNumSetting),
    url(r'^subject_alloc/$', AdminStaffService.SubjectAlloc),
    url(r'^subject_feedback/$',AdminStaffService.SubjectFeedback),
    url(r'^subject_rating/$',AdminStaffService.SubjectRating),
    #(r'^subject_grade_change /$',AdminStaffService.SubjectGradeChange),

    url(r'^dispatch/$',AdminStaffService.Dispatch),
    url(r'^expert_dispatch/$',AdminStaffService.expertDispatch),
    url(r'^school_dispatch/$',AdminStaffService.schoolDispatch),
    url(r'^create_inactive_user$',AdminStaffService.expertDispatch),
    
    url(r'^fundsmanage/$',AdminStaffService.funds_manage),
    url(r'^fundschange/(?P<pid>.{36})$',AdminStaffService.funds_change),

    url(r'^NoticeMessageSettings$',AdminStaffService.NoticeMessageSetting),
    url(r'^project_control$',AdminStaffService.project_control),

    (r'^news_release$', AdminStaffService.NewsRelease),

)
urlpatterns += staticfiles_urlpatterns()
