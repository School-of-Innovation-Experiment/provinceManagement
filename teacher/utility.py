#!/usr/local/bin/python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-12-29 16:57
# Last modified: 2016-12-29 16:57
# Filename: utility.py
# Description:
# coding: UTF-8

import os, sys, datetime, uuid

from django.shortcuts import get_object_or_404

from school.models import TeacherProjectPerLimits
from users.models import StudentProfile, TeacherProfile
from school.models import *
from const import *
from const.models import *
from school.utility import get_current_year,get_current_project_query_set
from backend.logging import logger, loginfo
from django.db.models import Q
from adminStaff.models import ProjectControl


def get_project_count():
    return "%04d" % get_current_project_query_set().count()

def create_newproject(request, new_user, category):
    student = get_object_or_404(StudentProfile, userid = new_user)
    teacher = get_object_or_404(TeacherProfile, userid = request.user)
    project_control = ProjectControl.objects.all()[0]
    year = project_control.pre_start_day.year
    loginfo(p=year,label="year")
    try:
        pid = uuid.uuid4()
        project = ProjectSingle()
        project.project_id = pid
        project.title = u"未命名"
        project.adminuser = teacher
        project.student = student
        project.school = teacher.school
        project.project_category = ProjectCategory.objects.get(category = category)
        project.year = year+1
        project.project_grade = ProjectGrade.objects.get(grade = GRADE_UN)
        project.project_status = ProjectStatus.objects.get(status = STATUS_FIRST)
        project.project_code = str(year + 1 ) + DUT_code + str(get_project_count())
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
        
        open = OpenSubmit()
        open.content_id = uuid.uuid4()
        open.project_id = project
        open.save()

        mid = MidSubmit()
        mid.content_id = uuid.uuid4()
        mid.project_id = project
        mid.save()

        final = FinalSubmit()
        final.content_id = uuid.uuid4()
        final.project_id = project
        final.save()
    except Exception, err:
        loginfo(p=err, label="creat a project for the user")
        return False
    return True

def Teacher_Profile(request):
    return TeacherProfile.objects.get(userid = request.user)

def TeacherLimitNumber(request):
    teacher_profile = Teacher_Profile(request)
    if TeacherProjectPerLimits.objects.filter(teacher__userid=request.user).count() == 0:
        newT = TeacherProjectPerLimits(teacher = teacher_profile,
                                       number = 0)
        newT.save()
    limit = TeacherProjectPerLimits.objects.get(teacher__userid = request.user)
    return limit.number

def get_limited_num_and_remaining_times(request):
    teacher_profile = TeacherProfile.objects.get(userid = request.user)
    proj_list = get_current_project_query_set().filter(Q(adminuser = teacher_profile))
    proj_num = len(proj_list)
    limited_num = TeacherLimitNumber(request)
    remaining_activation_times = max(0, limited_num - proj_num)
    return limited_num, remaining_activation_times
