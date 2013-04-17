# coding: UTF-8
'''
Created on 2013-03-28

@author: tianwei

Desc: School's view, includes home(manage), final report,
      application report, statistics information.
'''
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
from users.models import SchoolProfile
from school.forms import InfoForm, ApplicationReportForm, FinalReportForm

from const.models import *
from const import *

from school.utility import *
from backend.logging import logger, loginfo
from backend.decorators import *

"""
About the decorators sequence, it will impact the the function squeneces,
the top will be called first!
"""


@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
@time_controller(phase=STATUS_PRESUBMIT)
def home_view(request, is_expired=False):
    """
    school home management page
    """
    current_list = ProjectSingle.objects.filter(adminuser=request.user,
                                                year=get_current_year)
    readonly=is_expired
    try:
        limits = ProjectPerLimits.objects.get(school__userid=request.user)
    except Exception, err:
        logger.info(err)
        limits = None

    if limits is not None:
        remainings = int(limits.number) - len(current_list)
        total = limits.number
    else:
        total = 0
        remainings = 0

    data = {"current_list": current_list,
            "readonly":readonly,
            "info": {"applications_limits": total,
                     "applications_remaining": remainings}
            }
    return render(request, 'school/home.html', data)


@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
@only_user_required
@time_controller(phase=STATUS_PRESUBMIT)
def application_report_view(request, pid=None, is_expired=False):
    """
    school application report
    Arguments:
        In: id, it is project id
    """
    loginfo(p=pid+str(is_expired), label="in application")
    project = get_object_or_404(ProjectSingle, project_id=pid)
    pre = get_object_or_404(PreSubmit, project_id=pid)

    readonly = check_history_readonly(pid) or is_expired

    if request.method == "POST" and readonly is not True:
        info_form = InfoForm(request.POST, instance=project)
        application_form = ApplicationReportForm(request.POST, instance=pre)
        if info_form.is_valid() and application_form.is_valid():
            if save_application(project, info_form, application_form, request.user):
                return HttpResponseRedirect(reverse('school.views.home_view'))
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

    return render(request, 'school/application.html', data)


@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
@only_user_required
@time_controller(phase=STATUS_FINSUBMIT)
def final_report_view(request, pid=None, is_expired=False):
    """
    school final report
    Arguments:
        In: id, it is project id
    """
    loginfo(p=pid+str(is_expired), label="in application")
    final = get_object_or_404(FinalSubmit, project_id=pid)

    readonly = check_history_readonly(pid) or is_expired

    if request.method == "POST" and readonly is not True:
        final_form = FinalReportForm(request.POST, instance=final)
        if final_form.is_valid():
            final_form.save()
            return HttpResponseRedirect(reverse('school.views.home_view'))
        else:
            logger.info("Final Form Valid Failed"+"**"*10)
            logger.info(final_form.errors)
            logger.info("--"*10)

    final_form = FinalReportForm(instance=final)

    data = {'pid': pid,
            'final': final_form,
            'readonly': readonly,
            }

    return render(request, 'school/final.html', data)


@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def statistics_view(request):
    """
    school statistics view
    """
    data = get_statistics_from_user(request.user)

    return render(request, 'school/statistics.html', data)


@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
@time_controller(phase=STATUS_PRESUBMIT)
def new_report_view(request, is_expired=False):
    """
    school start a new application report, then it will
    jump the real project URL.
    """
    if check_limits(request.user) and is_expired is False:
        # create a new project
        pid = uuid.uuid4()
        project = ProjectSingle()
        project.project_id = pid
        project.adminuser = request.user
        project.school = SchoolProfile.objects.get(userid=request.user).school
        project.year = get_current_year()
        project.project_grade = ProjectGrade.objects.get(grade=GRADE_UN)
        project.project_status = ProjectStatus.objects.get(status=STATUS_FIRST)
        project.save()

        # create presubmit and final report
        pre = PreSubmit()
        pre.content_id = uuid.uuid4()
        pre.project_id = project
        pre.save()

        #create final report
        final = FinalSubmit()
        final.content_id = uuid.uuid4()
        final.project_id = project
        final.save()

        return HttpResponseRedirect(reverse('school.views.application_report_view', args=(pid,)))
    else:
        return HttpResponseRedirect(reverse('school.views.home_view'))


@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def history_view(request):
    """
    school history report list
    """

    history_list = ProjectSingle.objects.filter(adminuser=request.user).exclude(year=get_current_year)

    data = {"history_list": history_list}

    return render(request, 'school/history.html', data)


@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
@only_user_required
@time_controller(phase=STATUS_FINSUBMIT)
def file_view(request, pid=None, is_expired=False):
    """
    file management view
    """
    readonly = check_history_readonly(pid) or is_expired

    if request.method == "POST" and readonly is not True:
        if request.FILES is not None:
            return upload_response(request, pid)

    file_history = UploadedFiles.objects.filter(project_id=pid)
    logger.info("**"*10)
    logger.info(file_history)

    data = {'pid': pid,
            'files': file_history,
            'readonly': readonly,
            }

    return render(request, 'school/fileupload.html', data)


@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
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


@login_required
def non_authority_view(request):
    """
    cannot visit
    """
    #TODO: I will add more usefull information, such as control time
    return render(request, 'school/non_authority.html')
