from django.conf.urls import patterns, url
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
        r'^application$',
        student_views.application_report_view,
    ),
    url(
        r'^final$',
        student_views.final_report_view,
    ),
    url(
        r'^files$',
        student_views.file_view,
    ),
)
