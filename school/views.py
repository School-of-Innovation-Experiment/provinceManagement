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
from django.http import HttpResponseForbidden, Http404
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators import csrf
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from school.models import ProjectSingle, PreSubmit, FinalSubmit
from school.models import TechCompetition, Patents, Papers, AchievementObjects
from school.models import UploadedFiles
from adminStaff.models import ProjectPerLimits
from users.models import SchoolProfile
from school.forms import InfoForm, ApplicationReportForm, FinalReportForm

from const.models import SchoolDict, ProjectCategory, InsituteCategory
from const.models import UserIdentity, ProjectGrade, ProjectStatus
from const import AUTH_CHOICES, VISITOR_USER
from const import PROJECT_CATE_CHOICES, CATE_UN
from const import PROJECT_GRADE_CHOICES, GRADE_UN
from const import PROJECT_STATUS_CHOICES, STATUS_FIRST

from school.utility import check_limits, get_year
from school.utility import save_application
from backend.logging import logger

#TODO: for decorators, later I will add time control, authority control


@csrf.csrf_protect
@login_required
def home_view(request):
    """
    school home management page
    """
    current_list = ProjectSingle.objects.filter(adminuser=request.user)
    try:
        limits = ProjectPerLimits.objects.get(school__userid__userid=request.user)
    except:
        limits = None

    if limits is not None:
        remainings = int(limits.number) - len(current_list)
        total = limits.number
    else:
        total = 0
        remainings = 0

    data = {"current_list": current_list,
            "info": {"applications_limits": total,
                     "applications_remaining": remainings}
            }
    return render(request, 'school/home.html', data)


@csrf.csrf_protect
@login_required
def application_report_view(request, pid):
    """
    school application report
    Arguments:
        In: id, it is project id
    """
    project = get_object_or_404(ProjectSingle, project_id=pid)
    pre = get_object_or_404(PreSubmit, project_id=pid)

    if request.method == "POST":
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

    info_form = InfoForm(instance=project)
    application_form = ApplicationReportForm(instance=pre)

    data = {'pid': pid,
            'info': info_form,
            'application': application_form}

    return render(request, 'school/application.html', data)


@csrf.csrf_protect
@login_required
def final_report_view(request, pid):
    """
    school final report
    Arguments:
        In: id, it is project id
    """
    final = get_object_or_404(FinalSubmit, project_id=pid)

    if request.method == "POST":
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
            'final': final_form}

    return render(request, 'school/final.html', data)


@csrf.csrf_protect
@login_required
def statistics_view(request):
    """
    school statistics view
    """

    data = {}

    return render(request, 'school/statistics.html', data)


@csrf.csrf_protect
@login_required
def new_report_view(request):
    """
    school start a new application report, then it will
    jump the real project URL.
    """
    if check_limits(request.user):
        # create a new project
        pid = uuid.uuid4()
        project = ProjectSingle()
        project.project_id = pid
        project.adminuser = request.user
        project.school = SchoolProfile.objects.get(userid__userid=request.user).school
        project.year = get_year()
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
def history_view(request):
    """
    school history report list
    """

    data = {}

    return render(request, 'school/history.html', data)


@csrf.csrf_protect
@login_required
def file_view(request, pid=None):
    """
    file management view
    """

    data = {'pid':pid}

    return render(request, 'school/fileupload.html', data)
