# coding: UTF-8
'''
Created on 2013-3-27

@author: tianwei
'''

from django.contrib import admin
from school.models import *


RegisterClass = (# ProjectSingle,
                 # Re_Project_Expert,
                 # PreSubmit,
                 Project_Is_Assigned,
                 FinalSubmit,
                 Teacher_Enterprise,
                 # PreSubmitEnterprise,
                 UploadedFiles)
class Re_Project_ExpertAdmin(admin.ModelAdmin):
    search_fields = ['project__inspector','project__title',]
class ProjectSingleAdmin(admin.ModelAdmin):
    search_fields = ['project_id', 'title', 'project_code', ]
class PreSubmitAdmin(admin.ModelAdmin):
    search_fields = ['project_id__title',]
class PreSubmitEnterpriseAdmin(admin.ModelAdmin):
    search_fields = ['project_id__title',]
admin.site.register(ProjectSingle, ProjectSingleAdmin)
admin.site.register(PreSubmit, PreSubmitAdmin)
admin.site.register(PreSubmitEnterprise, PreSubmitEnterpriseAdmin)
admin.site.register(Re_Project_Expert, Re_Project_ExpertAdmin)
for item in RegisterClass:
    admin.site.register(item)
