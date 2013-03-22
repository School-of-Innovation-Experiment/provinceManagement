# -*- coding: UTF-8 -*-
'''
Created on 2012-11-5

@author: tianwei
'''
from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from news.views import testmce

urlpatterns = patterns('',
        url(r'^$', testmce),
)
