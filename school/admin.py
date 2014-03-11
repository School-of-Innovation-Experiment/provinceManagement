# coding: UTF-8
'''
Created on 2013-3-27

@author: tianwei
'''

from django.contrib import admin
from school.models import *


RegisterClass = (
                 Project_Is_Assigned,
                 Re_Project_Expert,
                 PreSubmit,             
                 FinalSubmit,
                 UploadedFiles,
                 PreSubmitEnterprise,
                 Teacher_Enterprise,
                 OpenSubmit,
                 TeacherProjectPerLimits,
                 ProjectFinishControl)

for item in RegisterClass:
    admin.site.register(item)

class ProjectSingleAdmin(admin.ModelAdmin):
    search_fields = ['project_code','title']

admin.site.register(ProjectSingle,ProjectSingleAdmin)
