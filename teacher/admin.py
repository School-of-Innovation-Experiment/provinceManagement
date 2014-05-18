# coding: UTF-8
'''
Created on 2013-3-27

@author: tianwei
'''

from django.contrib import admin
from teacher.models import *


RegisterClass = (TeacherMonthComment,
                )

for item in RegisterClass:
    admin.site.register(item)
