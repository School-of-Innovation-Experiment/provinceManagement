# coding: UTF-8

from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from backend.decorators import *
from const import *
from users.models import TeacherProfile, StudentProfile

@csrf.csrf_protect
@login_required
# @authority_required(TEACHER_USER)
def home_view(request):
    return render(request, "teacher/teacher_home.html", {})

def GetStudentRegisterList(request):
    teacher_profile = TeacherProfile.objects.get(userid = request.user)
    student_list = [each.user for each in StudentProfile.objects.filter(teacher = teacher_profile)]

@login_required
def StudentDispatch(request):
    if request.method == "GET":
        student_form = StudentDispatchForm()
        email_list  = GetStudentRegisterList(request)
        email_num = len(email_list)
#        limited_num = school_limit_num(request)
#         remaining_activation_times = limited_num - email_num
        data = {
            'student_form': student_form,
            'email_list': email_list,
            'remaining_activation_times': remaining_activation_times
            }
        return render(request, 'teacher/dispatch.html', data)

