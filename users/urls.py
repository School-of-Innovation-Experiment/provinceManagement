# coding: UTF-8
'''
Created on 2013-4-03

@author: tianwei

Desc: User settings URL defination
'''

from django.conf.urls import patterns, include, url
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from users import views as users_views


urlpatterns = patterns('',
    url(
        r'^$',
        users_views.profile_view
    ),
    url(
        r'^profile/$',
        users_views.profile_view
    ),
    url(
        r'^admin/$',
        users_views.admin_account_view
    ),
    url(
        r'^search/$',
        users_views.search_user_view
    ),
    url(
        r'^relogin/(?P<name>.+)$',
        users_views.reset_login_view,
        name="relogin"
    ),
    url(
        r'^binding/$',
        users_views.binding_view,
        name="binding"
    ),
)
