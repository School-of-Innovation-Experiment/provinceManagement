# coding: UTF-8
'''
Created on 2013-04-02

@author: tianwei

Desc: Experts' view, includes home(manage), review report view
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

from school.models import *
from adminStaff.models import *
from users.models import *
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
@authority_required(EXPERT_USER)
def home_view(request):
    """
    expert home management page
    """
    expert = get_object_or_404(ExpertProfile, userid=request.user)
    re_project = Re_Project_Expert.objects.filter(expert=expert)

    loginfo(p=re_project, label="EXPERT HOME")

    data = {'current_list': re_project}
    return render(request, 'expert/home.html', data)


@csrf.csrf_protect
@login_required
@authority_required(EXPERT_USER)
def review_report_view(request, pid=None):
    """
    expert home management page
    """
    data = {}
    return render(request, 'expert/review.html', data)
