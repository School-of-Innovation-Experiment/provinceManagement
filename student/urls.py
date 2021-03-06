from django.conf.urls import patterns, url,include
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from student import views as student_views


# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:

    url(
        r'^$',
        student_views.home_view,
        name="student_home"
    ),
    url(
        r'^memberchange$',
        student_views.member_change,
    ),
    url(
        r'^techcompetition$',
        student_views.techcompetition,
    ),

    url(
        r'^open/(?P<pid>.{36})$',
        student_views.open_report_view,
    ),

    url(
        r'^application/(?P<pid>.{36})$',
        student_views.application_report_view,name = "student_application_report_view"
    ),
    url(
        r'^final/(?P<pid>.{36})$',
        student_views.final_report_view,name = "student_final_report_view"
    ),
    url(
        r'^mid/(?P<pid>.{36})$',
        student_views.mid_report_view,
    ),
    url(
        r'^files/(?P<pid>.{36})$',
        student_views.file_view,
    ),
    url(
        r'delete/(?P<pid>.{36})/(?P<fid>.{36})$',
        student_views.file_delete_view,
    ),
    url(
        r'^newtechcompetition/$',
        student_views.new_techcompetition,
    ),
    url(
        r'^file_upload_view/(?P<pid>.{36})&(?P<errortype>\w+)$',
        student_views.file_upload_view,name="student_file_upload_errortype_view",
    ),
    url(
        r'^file_upload_view/(?P<pid>.{36})$',
        student_views.file_upload_view, name="student_file_upload_view",
    ),
    url(
        r'^score_upload_view/(?P<pid>.{36})$',
        student_views.score_upload_view, name="score_upload_view",
    ),
    url(
        r'^score_upload_view/(?P<pid>.{36})$',
        student_views.score_upload_view, name="student_score_upload_view"
    ),
    url(
        r'^processrecord$',
        student_views.processrecord_view,
    ),
    url(
        r'^funds_view$',
        student_views.funds_view,
    ),
)
