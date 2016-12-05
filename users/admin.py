# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-12-05 11:17
# Last modified: 2016-12-05 11:21
# Filename: admin.py
# Description:
'''
Created on 2012-11-5

@author: tianwei
'''

from django.contrib import admin
from users.models import *


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['name']


RegisterClass = (SchoolProfile,
                 ExpertProfile,
                 AdminStaffProfile,
                 StudentProfile,
                 )

for item in RegisterClass:
    admin.site.register(item)

admin.site.register(TeacherProfile, ProfileAdmin)
