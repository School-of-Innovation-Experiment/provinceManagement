from django.conf.urls import patterns, url,include
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from rpc import views as rpc_views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(
        r'^$',
        rpc_views.rpc_handler,
    ),
)
