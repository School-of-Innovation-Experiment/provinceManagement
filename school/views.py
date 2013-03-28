# coding: UTF-8
'''
Created on 2013-03-28

@author: tianwei

Desc: School's view, includes home(manage), final report,
      application report, statistics information.
'''
import datetime
import logging
import os
import sys

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

#TODO: for decorators, later I will add time control, authority control


@csrf.csrf_protect
@login_required
def home_view(request):
    """
    school home management page
    """
    current_list = ProjectSingle.objects.filter(adminuser=request.user)

    limits = ProjectPerLimits.objects.get(school__userid__userid=request.user)
    remainings = int(limits.number) - len(current_list)

    data = {
            "current_list": current_list,
            "info": {"applications_limits": limits,
                     "applications_remaining": remainings,}
            
           }
    return render(request, 'school/home.html', data)


@csrf.csrf_protect
@login_required
def application_report_view(request, pid=None):
    """
    school application report
    Arguments:
        In: id, it is project id
    """

    data = {}

    return render(request, 'school/application.html', data)


@csrf.csrf_protect
@login_required
def final_report_view(request, pid=None):
    """
    school final report
    Arguments:
        In: id, it is project id
    """

    data = {}

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

    data = {}

    return render(request, 'school/application.html', data)


@csrf.csrf_protect
@login_required
def history_view(request):
    """
    school history report list
    """

    data = {}

    return render(request, 'school/history.html', data)
