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
    url(r'^$',AdminStaffService.Dispatch),
    (r'^settings$',AdminStaffService.AdminSetting),
    (r'^DeadlineSettings$',AdminStaffService.DeadlineSetting),
    (r'^ProjectLimitNumSettings$',AdminStaffService.ProjectLimitNumSetting),

    (r'^subject_feedback/$',AdminStaffService.SubjectFeedback),
    (r'^subject_rating/$',AdminStaffService.SubjectRating),
    #(r'^subject_grade_change /$',AdminStaffService.SubjectGradeChange),

    url(r'^ProjectLimitNumReset$', AdminStaffService.ProjectLimitNumReset),

    (r'^dispatch/$',AdminStaffService.Dispatch),
    (r'^dispatch/(?P<page>\d+)$',AdminStaffService.Dispatch),
    (r'^expert_dispatch/$',AdminStaffService.expertDispatch),
    (r'^school_dispatch/$',AdminStaffService.schoolDispatch),
    (r'^create_inactive_user$',AdminStaffService.expertDispatch),
                       (r'^NoticeMessageSettings$',
                        AdminStaffService.NoticeMessageSetting),
    (r'^news_release$',AdminStaffService.NewsRelease),
    (r'^show_release$',AdminStaffService.ShowRelease),
    (r'^show_manage$',AdminStaffService.ShowManage),
    (r'^ImportExpert$',AdminStaffService.ImportExpert),
    (r'^RecommendRatingSetting', AdminStaffService.RecommendRatingSetting),
    # url(
    #     r'get_xls/$',
    #     AdminStaffService.get_xls_path,
    # ), 
)
urlpatterns += staticfiles_urlpatterns()
