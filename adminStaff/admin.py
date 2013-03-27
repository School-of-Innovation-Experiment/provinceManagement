# coding: UTF-8
'''
Created on 2013-3-27

@author: tianwei
'''

from django.contrib import admin
from adminStaff.models import *


RegisterClass = (ProjectControl,
                 ReviewTask,
                 ProjectPerLimits)

for item in RegisterClass:
    admin.site.register(item)
