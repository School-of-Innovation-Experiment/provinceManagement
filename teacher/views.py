# coding: UTF-8

import datetime, os, sys, uuid

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseForbidden, Http404, HttpResponseBadRequest
from django.template import RequestContext

from backend.decorators import *
from const import *
from const.models import *
from users.models import TeacherProfile, StudentProfile
from school.models import TeacherProjectPerLimits, ProjectSingle, PreSubmit, FinalSubmit
from school.models import UploadedFiles
from school.forms import InfoForm, ApplicationReportForm, FinalReportForm
from teacher.forms import StudentDispatchForm
from registration.models import *
from teacher.utility import *
from school.utility import *

@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def home_view(request, is_expired = False):
    email_list  = GetStudentRegisterList(request)
    email_num = len(email_list) 
    limited_num = TeacherLimitNumber(request) 
    remaining_activation_times = limited_num - email_num

    project_list = ProjectSingle.objects.filter(adminuser = request.user, 
                                                year = get_current_year)
    
    data = {
        "project_list": project_list,
        "limited_num": limited_num,
        "remaining_activation_times": remaining_activation_times,
        }
    return render(request, "teacher/home.html", data)

@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
@only_user_required
@time_controller(phase=STATUS_PRESUBMIT)
def application_report_view(request, pid = None, is_expired = False):
    loginfo(p=pid+str(is_expired), label="in application")
    project = get_object_or_404(ProjectSingle, project_id=pid)
    pre = get_object_or_404(PreSubmit, project_id=pid)
    readonly= is_expired
    if request.method == "POST" and readonly is not True:
        info_form = InfoForm(request.POST, instance=project)
        application_form = ApplicationReportForm(request.POST, instance=pre)
        if info_form.is_valid() and application_form.is_valid():            
            if save_application(project, info_form, application_form, request.user):
                project.project_status = ProjectStatus.objects.get(status=STATUS_PRESUBMIT)
                project.save()
                return HttpResponseRedirect(reverse('teacher.views.home_view'))
        else:
            logger.info("Form Valid Failed"+"**"*10)
            logger.info(info_form.errors)
            logger.info(application_form.errors)
            logger.info("--"*10)
    else:
        info_form = InfoForm(instance=project)
        application_form = ApplicationReportForm(instance=pre)

    data = {'pid': pid,
            'info': info_form,
            'application': application_form,
            'readonly': readonly,
            }
    return render(request, 'teacher/application.html', data)

@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
@only_user_required
@time_controller(phase=STATUS_FINSUBMIT)
def final_report_view(request, pid=None,is_expired=False):
    """
    student final report
    Arguments:
        In: id, it is project id
    """
    loginfo(p=pid+str(is_expired), label="in application")
    final = get_object_or_404(FinalSubmit, project_id=pid)
    project = get_object_or_404(ProjectSingle, project_id=pid)
    readonly = is_expired



    if request.method == "POST" and readonly is not True:
        final_form = FinalReportForm(request.POST, instance=final)
        if final_form.is_valid():
            final_form.save()
            project.project_status = ProjectStatus.objects.get(status=STATUS_FINSUBMIT)
            project.save()
            return HttpResponseRedirect(reverse('teacher.views.home_view'))
        else:
            logger.info("Final Form Valid Failed"+"**"*10)
            logger.info(final_form.errors)
            logger.info("--"*10)

    final_form = FinalReportForm(instance=final)

    data = {'pid': pid,
            'final': final_form,
            'readonly':readonly,
            }
    return render(request, 'teacher/final.html', data)

@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
@only_user_required
@time_controller(phase=STATUS_FINSUBMIT)
def file_view(request, pid=None,is_expired = False):
    """
    file management view
    """
    readonly = is_expired
    if request.method == "POST" :
        if request.FILES is not None:
            return upload_response(request, pid)

    file_history = UploadedFiles.objects.filter(project_id=pid)
    logger.info("**"*10)
    logger.info(file_history)

    data = {'pid': pid,
            'files': file_history,
            'readonly': readonly,
            }
    return render(request, 'teacher/fileupload.html', data)

@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
@only_user_required
@time_controller(phase=STATUS_FINSUBMIT)
def file_delete_view(request, pid=None, fid=None, is_expired=False):
    """
    file delete view
    """
    logger.info("delete files"+"**"*10)
    # check mapping relation
    f = get_object_or_404(UploadedFiles, file_id=fid)
    p = get_object_or_404(ProjectSingle, project_id=pid)

    logger.info(f.project_id.project_id)
    logger.info(p.project_id)

    if f.project_id.project_id != p.project_id:
        raise HttpResponseForbidden("Authority Failed!")

    # delete file
    if request.method == "POST":
        # delete record
        f.delete()
        return HttpResponse(str(fid))
    else:
        return HttpResponseBadRequest("Warning! Only POST accepted!")

def Send_email_to_student(request, username, password, email, category, identity):
    """
    check the existence of user
    """
    if User.objects.filter(email = email).count() == 0:
        user = RegistrationManager().create_inactive_user(request, username, password, email,
                identity)
        result = create_newproject(request=request, new_user=user, category=category)
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

@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
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
