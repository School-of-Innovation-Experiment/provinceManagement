from django.conf.urls import patterns, url
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from teacher import views as teacher_views


urlpatterns = patterns('',
    url(
        r'^$',
        teacher_views.home_view,
    ),
    # url(
    #     r'^review/(?P<pid>.{36})$',
    #     teacher_views.review_report_view,
    # ),
)
