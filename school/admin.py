# coding: UTF-8
'''
Created on 2013-3-27

@author: tianwei
'''

from django.contrib import admin
from school.models import *


RegisterClass = (ProjectSingle,
                 Project_Is_Assigned,
                 Re_Project_Expert,
                 PreSubmit,
                 FinalSubmit,
                 UploadedFiles,
                 PreSubmitEnterprise,
                 Teacher_Enterprise,
                 TeacherProjectPerLimits,
                 ProjectFinishControl)

for item in RegisterClass:
    admin.site.register(item)
