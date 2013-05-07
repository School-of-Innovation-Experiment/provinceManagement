# coding: UTF-8
'''
Created on 2013-3-27

@author: tianwei
'''

from django.contrib import admin
from school.models import *


RegisterClass = (ProjectSingle,
                 Re_Project_Expert,
                 PreSubmit,
                 FinalSubmit,
                 Teacher_Enterprise,
                 PreSubmitEnterprise,
                 UploadedFiles)

for item in RegisterClass:
    admin.site.register(item)
