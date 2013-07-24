# coding: UTF-8 

import os, sys, datetime, uuid

from django.shortcuts import get_object_or_404

from users.models import StudentProfile, TeacherProfile
from school.models import ProjectSingle, PreSubmit, FinalSubmit, PreSubmitEnterprise, Teacher_Enterprise
from const import *
from const.models import *
from school.utility import get_current_year
from backend.logging import logger, loginfo

DUT_code = "10141"

def get_project_count():
    return "%04d" % ProjectSingle.objects.all().count()

def create_newproject(request, new_user, category):
    student = get_object_or_404(StudentProfile, userid = new_user)
    teacher = get_object_or_404(TeacherProfile, userid = request.user)
    try:
        pid = uuid.uuid4()
        project = ProjectSingle()
        project.project_id = pid
        project.title = u"未命名"
        project.adminuser = teacher
        project.student = student 
        project.school = teacher.school
        project.project_category = ProjectCategory.objects.get(category = category)
        project.year = get_current_year() 
        project.project_grade = ProjectGrade.objects.get(grade = GRADE_UN) 
        project.project_status = ProjectStatus.objects.get(status = STATUS_FIRST) 
        project.project_code = str(get_current_year()) + DUT_code + str(get_project_count())
        project.save()
        
        
        if category == CATE_INNOVATION:
            pre = PreSubmit()
            pre.content_id = uuid.uuid4() 
            pre.project_id = project 
            pre.save()
        else:
            pre_interprise = PreSubmitEnterprise()
            pre_interprise.content_id = uuid.uuid4()
            pre_interprise.project_id = project

            teacher_enterprise = Teacher_Enterprise()
            teacher_enterprise.save()

            pre_interprise.enterpriseTeacher = teacher_enterprise
            pre_interprise.save()

        final = FinalSubmit()
        final.content_id = uuid.uuid4() 
        final.project_id = project
        final.save()
    except Exception, err:
        loginfo(p=err, label="creat a project for the user")  
        return False
    return True