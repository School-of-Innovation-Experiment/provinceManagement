# coding: UTF-8

from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from teacher import views as teacher_views

urlpatterns = patterns('',
    url(
        r'^dispatch',
        teacher_views.StudentDispatch,
    ),
    url(
        r'^$',
        teacher_views.home_view,
    ),
    url(
        r'^application/(?P<pid>.{36})$',
        teacher_views.application_report_view,
    ),
    url(
        r'^final/(?P<pid>.{36})$',
        teacher_views.final_report_view,
    ),
    url(
        r'^files/(?P<pid>.{36})$',
        teacher_views.file_view,
    ),
    url(
        r'delete/(?P<pid>.{36})/(?P<fid>.{36})$',
        teacher_views.file_delete_view,
    ),
    url(
        r'processrecord_view/(?P<pid>.{36})$',
        teacher_views.processrecord_view,
    ),
    url(
        r'funds_manage$',
        teacher_views.funds_manage,
    ),
    url(
        r'^fundsview/(?P<pid>.{36}$)',
        teacher_views.funds_view,
        ),
)
