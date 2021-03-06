# coding: UTF-8
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
from adminStaff import views as adminStaff_views
dajaxice_autodiscover()
urlpatterns = patterns('',

    url(r'^application/(?P<pid>.{36})$', AdminStaffService.application_report_view),
    url(r'^open/(?P<pid>.{36})$', AdminStaffService.open_report_view),
    url(r'^mid/(?P<pid>.{36})$', AdminStaffService.mid_report_view),
    url(r'^final/(?P<pid>.{36})$', AdminStaffService.final_report_view),
    url(r'^memberchange/(?P<pid>.{36})$', AdminStaffService.member_change),
    url(r'^files_upload_view/(?P<pid>.{36})$',AdminStaffService.files_upload_view),
    url(
        r'^file_upload_view/(?P<pid>.{36})&(?P<errortype>\w+)$',
        AdminStaffService.files_upload_view,name="adminStaff_uploadfile_errortype",
    ),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    url(r'^$',AdminStaffService.home_view, name='adminStaff_home'),
    url(r'^processrecord$',AdminStaffService.processrecord),
    url(r'^changepassword$',AdminStaffService.changepassword),
    url(r'^processrecord_view/(?P<pid>.{36})$', AdminStaffService.record_view),
    url(r'^settings$',AdminStaffService.AdminSetting),
    # url(r'^DeadlineSettings$',AdminStaffService.DeadlineSetting),
    url(r'^ProjectLimitNumSettings$',AdminStaffService.ProjectLimitNumSetting),
    url(r'^ProjectLimitNumReset$',AdminStaffService.ProjectLimitNumReset),
    url(r'^ProjectLimitNumRecycle$',AdminStaffService.ProjectLimitNumRecycle),
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
    url(r'^project_informationexport$',AdminStaffService.project_informationexport),
    url(r'^news_release$', AdminStaffService.NewsRelease),
    url(r'^homepage_import$', AdminStaffService.homepage_import_view),

    url(r'^project_assistant$', AdminStaffService.project_assistant_view),
    url(r'^project_sync$', AdminStaffService.project_sync),
    url(r'^file_download/(?P<fileid>.{36})$',AdminStaffService.file_download,name="adminStaff_downloadfile"),
)
urlpatterns += staticfiles_urlpatterns()
