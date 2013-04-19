# coding: UTF-8 

import os, sys, datetime, uuid

from django.shortcuts import get_object_or_404

from users.models import StudentProfile, TeacherProfile
from school.models import ProjectSingle, PreSubmit, FinalSubmit
from const import *
from const.models import *

from backend.logging import logger, loginfo

def get_current_year():
    return datetime.datetime.today().year

def create_newproject(request, new_user):
    student = get_object_or_404(StudentProfile, userid = new_user)
    teacher = get_object_or_404(TeacherProfile, userid = request.user)
    try:
        pid = uuid.uuid4()
        project = ProjectSingle()
        project.project_id = pid
        project.title = u"未命名"
        project.adminuser = request.user 
        project.student = student 
        project.school = teacher.school.school
        project.year = get_current_year() 
        project.project_grade = ProjectGrade.objects.get(grade = GRADE_UN) 
        project.project_status = ProjectStatus.objects.get(status = STATUS_FIRST) 
        project.save()

        pre = PreSubmit()
        pre.content_id = uuid.uuid4() 
        pre.project_id = project 
        pre.save()

        final = FinalSubmit()
        final.content_id = uuid.uuid4() 
        final.project_id = project
        final.save()
    except Exception, err:
        loginfo(p=err, label="creat a project for the user")  
        return False
    return True
