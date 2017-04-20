#!/usr/local/bin/python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-04-19 22:01
# Last modified: 2017-04-20 09:20
# Filename: urls.py
# Description:
# coding: UTF-8
'''
Created on 2012-11-10

@author: tianwei
'''
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.contrib.auth import views as auth_views

from registration.views import active
from registration.views import register
from registration.views import provincelogin_redirect, schoollogin_redirect
from registration.views import expertlogin_redirect, studentlogin_redirect
from registration.views import identity_redirect

urlpatterns = patterns(
    # Activation keys get matched by \w+ instead of the more specific
    # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
    # that way it can return a sensible "invalid key" message instead of a confusing 404.
    url(r'^active/(?P<activation_key>\w+)/$',active,name='registration_avtive'),
    url(r'^provincelogin/$',auth_views.login,{'template_name':'registration/provincelogin.html'},name='auth_provincelogin'),
    url(r'^schoollogin/$',auth_views.login,{'template_name':'registration/schoollogin.html'},name='auth_schoollogin'),
    url(r'^expertlogin/$',auth_views.login,{'template_name':'registration/expertlogin.html'},name='auth_expertlogin'), 
    url(r'^studentlogin/$',auth_views.login,{'template_name':'registration/studentlogin.html'},name='auth_studentlogin'), 
    url(r'^logout/$',auth_views.logout,{'next_page':'/'},name='auth_logout'),
    url(r'^password/change/$',auth_views.password_change,name='auth_password_change'),
    url(r'^password/change/done/$',auth_views.password_change_done, name='auth_password_change_done'),

    url(r'^password/reset/$',auth_views.password_reset, name='auth_password_reset'),
    url(r'^password/reset/confirm/(?P<uidb36>[0-9a-zA-Z]+)-(?P<token>.+)/$',auth_views.password_reset_confirm,name='auth_password_reset_confirm'),
    url(r'^password/reset/complete/$',auth_views.password_reset_complete,name='auth_password_reset_complete'),
    url(r'^password/reset/done/$',auth_views.password_reset_done,name='auth_password_reset_done'),

    #url(r'register/$',register,name='registration_register'),
    #url(r'register/complete/$',direct_to_template, {'template': 'registration/registration_complete.html'},name = 'registration_complete'),
    url(r'^provinceredirect/$', provincelogin_redirect, name="auth_provincelogin_redirect"),
    url(r'^schoolredirect/$', schoollogin_redirect, name="auth_schoollogin_redirect"),
    url(r'^expertredirect/$', expertlogin_redirect, name="auth_expertlogin_redirect"),
    url(r'^studentredirect/$', studentlogin_redirect, name="auth_studentlogin_redirect"),
    url(r'^identity_redirect/$', identity_redirect, name="identity_redirect"),
)
