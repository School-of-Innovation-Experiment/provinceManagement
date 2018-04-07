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
from registration.views import login_redirect

from django_cas.views import login as login_view, logout as logout_view

urlpatterns = patterns('',
         # Activation keys get matched by \w+ instead of the more specific
         # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
         # that way it can return a sensible "invalid key" message instead of a confusing 404.
          url(r'^active/(?P<activation_key>\w+)/$',active,name='registration_avtive'),
          # url(r'^login/$', login_view, name='auth_login'),
          # url(r'^logout/$', logout_view, name='auth_logout'),
          url(r'^login/$',auth_views.login,{'template_name':'registration/login.html'},name='auth_login'),
          url(r'^logout/$',auth_views.logout,{'next_page':'/'},name='auth_logout'),
          url(r'^password/change/$',auth_views.password_change,name='auth_password_change'),
          url(r'^password/change/done/$',auth_views.password_change_done, name='auth_password_change_done'),

          url(r'^password/reset/$',auth_views.password_reset, name='auth_password_reset'),
          url(r'^password/reset/confirm/(?P<uidb36>[0-9a-zA-Z]+)-(?P<token>.+)/$',auth_views.password_reset_confirm,name='auth_password_reset_confirm'),
          url(r'^password/reset/complete/$',auth_views.password_reset_complete,name='auth_password_reset_complete'),
          url(r'^password/reset/done/$',auth_views.password_reset_done,name='auth_password_reset_done'),

          #url(r'register/$',register,name='registration_register'),
          #url(r'register/complete/$',direct_to_template, {'template': 'registration/registration_complete.html'},name = 'registration_complete'),
          url(r'^redirect/$', login_redirect, name="auth_login_redirect"),
        )
