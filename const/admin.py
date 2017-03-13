#!/usr/local/bin/python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-03-13 16:29
# Last modified: 2017-03-13 16:29
# Filename: admin.py
# Description:
# coding: UTF-8
'''
Created on 2012-11-5

@author: tianwei
'''

from django.contrib import admin
from const.models import *


RegisterClass = (SchoolDict,
                 MajorDict,
                 ProjectCategory,
                 ProjectGrade,
                 ProjectStatus,
                 # InsituteCategory,
                 UserIdentity,
                 ProjectOrigin,
                 ProjectEnterpriseOrigin,
                 ProjectEnterpriseMaturity,
                 NewsCategory,
                 OverStatus,
                 ApplyControl,
                )

for item in RegisterClass:
    admin.site.register(item)
