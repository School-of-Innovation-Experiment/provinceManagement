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
        r'^application/(?P<pid>.{36})$',
        student_views.application_report_view,
    ),
    url(
        r'^final/(?P<pid>.{36})$',
        student_views.final_report_view,
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
)
