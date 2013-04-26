# Create your views here.
import datetime
import os
import sys
import uuid

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseForbidden, Http404, HttpResponseBadRequest
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators import csrf
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from school.models import ProjectSingle, PreSubmit, FinalSubmit
from school.models import UploadedFiles
from adminStaff.models import ProjectPerLimits
from users.models import StudentProfile
from school.forms import InfoForm, ApplicationReportForm, FinalReportForm,EnterpriseApplicationReportForm,TechCompetitionForm

from const.models import *
from const import *

from school.utility import *
from backend.logging import logger, loginfo
from backend.decorators import *
from student.models import Student_Group
from student.forms import StudentGroupForm

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
def home_view(request):
    """
    display project at the current year
    """
    item = ProjectSingle.objects.get(student__userid=request.user,year=get_current_year)
    return render(request, "student/student_home.html", {"item": item})

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
def member_change(request):
    """
    project group member change
    """
    student_account = StudentProfile.objects.get(userid = request.user)
    project = ProjectSingle.objects.get(student=student_account)
    student_group = Student_Group.objects.filter(project = project)

    student_group_form = StudentGroupForm()
    return render(request, "student/member_change.html",
                  {"student_group": student_group,
                   "student_group_form": student_group_form})

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
@only_user_required
@time_controller(phase=STATUS_PRESUBMIT)
def application_report_view(request,pid=None,is_expired=False):
    loginfo(p=pid+str(is_expired), label="in application")
    project = get_object_or_404(ProjectSingle, project_id=pid)
    pre = get_object_or_404(PreSubmit, project_id=pid)

    projectcategory=project.project_category.category
    is_innovation = True

    readonly= is_expired
    if request.method == "POST" and readonly is not True:
        info_form = InfoForm(request.POST,pid=pid,instance=project)
        application_form = ApplicationReportForm(request.POST, instance=pre) 
        if projectcategory != CATE_INNOVATION:
            application_form = EnterpriseApplicationReportForm(instance=pre)
            is_innovation = False        
        if info_form.is_valid() and application_form.is_valid():
            if save_application(project, info_form, application_form, request.user):
                project.project_status = ProjectStatus.objects.get(status=STATUS_PRESUBMIT)
                project.save()

            return HttpResponseRedirect(reverse('student.views.home_view'))
        else:
            logger.info("Form Valid Failed"+"**"*10)
            logger.info(info_form.errors)
            logger.info(application_form.errors)
            logger.info("--"*10)
    else:
        info_form = InfoForm(instance=project,pid=pid)
        application_form = ApplicationReportForm(instance=pre)
        if projectcategory != CATE_INNOVATION:
            application_form = EnterpriseApplicationReportForm(instance=pre)
            is_innovation = False
            loginfo(p=is_innovation, label="in application")

    data = {'pid': pid,
            'info': info_form,
            'application': application_form,
            'readonly': readonly,
            'is_innovation':is_innovation
            }
    return render(request, 'student/application.html', data)

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
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
        # techcompetition_form = 
        if final_form.is_valid():
            final_form.save()
            project.project_status = ProjectStatus.objects.get(status=STATUS_FINSUBMIT)
            project.save()
            return HttpResponseRedirect(reverse('student.views.home_view'))
        else:
            logger.info("Final Form Valid Failed"+"**"*10)
            logger.info(final_form.errors)
            logger.info("--"*10)

    final_form = FinalReportForm(instance=final)

    data = {'pid': pid,
            'final': final_form,
            'readonly':readonly,
            }
    return render(request, 'student/final.html', data)

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
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
    return render(request, 'student/fileupload.html', data)

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
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
