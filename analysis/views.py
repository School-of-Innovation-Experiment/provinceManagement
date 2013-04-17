# coding: UTF-8
'''
Created on 2013-4-17

@author: tianwei

Desc: statistics for school and province
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
from django.contrib.auth.models import User

from school.models import ProjectSingle, PreSubmit, FinalSubmit
from school.models import UploadedFiles
from adminStaff.models import ProjectPerLimits
from users.models import SchoolProfile
from school.forms import InfoForm, ApplicationReportForm, FinalReportForm

from const.models import *
from const import *
from users.models import *

from school.utility import *
from backend.logging import logger, loginfo
from backend.decorators import *
from analysis.forms import SearchForm

"""
About the decorators sequence, it will impact the the function squeneces,
the top will be called first!
"""


@csrf.csrf_protect
def school_statistics_view(request):
    """
    school statistics view
    """
    # check users
    default_users = SchoolProfile.objects.all()
    if default_users is None:
        return HttpResponseRedirect("/")

    data = get_statistics_from_user(user=default_users[0])

    # search post
    if request.method == "POST":
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            schoolName = search_form.cleaned["schoolname"]
            user = get_object_or_404(SchoolProfile, school__schoolName=schoolName)
            data = get_statistics_from_user(user=user)

    return render(request, 'analysis/school_statistics.html', data)


@csrf.csrf_protect
def province_statistics_view(request):
    """
    province statistics view
    """
    return render(request, 'analysis/province_statistics.html')
