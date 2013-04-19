# coding: UTF-8

import datetime, os, sys, uuid

from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from backend.decorators import *
from const import *
from users.models import TeacherProfile, StudentProfile
from school.models import TeacherProjectPerLimits, ProjectSingle
from teacher.forms import StudentDispatchForm
from registration.models import *
from teacher.utility import create_newproject

@csrf.csrf_protect
@login_required
# @authority_required(TEACHER_USER)
def home_view(request):
    email_list  = GetStudentRegisterList(request)
    email_num = len(email_list) 
    limited_num = TeacherLimitNumber(request) 
    remaining_activation_times = limited_num - email_num

    project_list = ProjectSingle.objects.filter(adminuser = request.user)
    
    data = {
        "project_list": project_list,
        "limited_num": limited_num,
        "remaining_activation_times": remaining_activation_times,
        }
    return render(request, "teacher/home.html", data)


def Send_email_to_student(request, username, password, email, identity):
    """
    check the existence of user
    """
    if User.objects.filter(email = email).count() == 0:
        user = RegistrationManager().create_inactive_user(request, username, password, email, 
                identity)
        result = create_newproject(request=request, new_user=user)
        return True and result
    else:
        return False

def GetStudentRegisterList(request):
    teacher_profile = TeacherProfile.objects.get(userid = request.user)
    student_list = [each.userid for each in StudentProfile.objects.filter(teacher = teacher_profile)]
    return student_list

def TeacherLimitNumber(request):
    limit = TeacherProjectPerLimits.objects.get(teacher__userid = request.user)
    return limit.number

@login_required
def StudentDispatch(request):
    if request.method == "GET":
        student_form = StudentDispatchForm()
        email_list  = GetStudentRegisterList(request)
        email_num = len(email_list)
        limited_num = TeacherLimitNumber(request)
        remaining_activation_times = limited_num - email_num
        data = {
            'student_form': student_form,
            'email_list': email_list,
            'remaining_activation_times': remaining_activation_times
            }
        return render(request, 'teacher/dispatch.html', data)

