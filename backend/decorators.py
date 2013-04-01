# coding: UTF-8
'''
Created on 2013-04-01

@author: tianwei

Desc: decorators for some controlers, such as time, authorities
'''

import os
import sys
import datetime

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

from const import *
from adminStaff.models import *
from backend.logging import loginfo
from school.utility import get_current_year
from school.models import *


class only_user_required(object):
    """
    This decorator will deal with project varify, when the logined user 
    can control this project, he can continue.
    """
    def __init__(self, method):
        self.method = method

    def check_auth(self, pid, request):
        if pid is None:
            return False

        user = ProjectSingle.objects.get(project_id=pid).adminuser
        if user is request.user or request.user.is_superuser:
            return True
        else:
            return False

    def __call__(self, request, *args, **kwargs):
        pid = kwargs.get("pid", None)
        is_passed = self.check_auth(pid, request)
        if is_passed:
            response = self.method(request, *args, **kwargs)
            return response
        else:
            return HttpResponseRedirect(reverse('school.views.non_authority_view'))


class time_controller(object):
    """
    This decorator will deal with time control, time the following:
        pre_start --> pre_end --> pre_start_review --> pre_end_review
        final_start --> final_end --> final_start_review --> final_end_review
    """
    def __init__(self, phase):
        self.phase = phase

    def check_day(self, pid):
        """
        return True or False
        """
        if pid is None:
            return True

        year = ProjectSingle.objects.get(project_id=pid).year
        if year != get_current_year():
            return True

        control = ProjectControl.objects.all()
        loginfo(control)
        if len(control) == 0:
            return True

        control = control[0]
        today = datetime.date.today()

        if self.phase == STATUS_PRESUBMIT:
            is_passed = True if today >= control.pre_start_day and today <= control.pre_end_day else False
        elif self.phase == STATUS_PREREVIEW:
            is_passed = True if today >= control.pre_start_review_day and today <= control.pre_end_review_day else False
        elif self.phase == STATUS_ONGOING:
            is_passed = True if today >= control.pre_end_review_day and today <= control.final_start_day else False
        elif self.phase == STATUS_FINSUBMIT:
            is_passed = True if today >= control.final_start_day and today <= control.final_end_day else False
        elif self.phase == STATUS_FINREVIEW:
            is_passed = True if today >= control.final_start_review_day and today <= control.final_end_review_day else False
        elif self.phase == STATUS_FIRST:
            is_passed = True
        else:
            is_passed = False

        return is_passed

    def __call__(self, method):
        def wrappered_method(request, *args, **kwargs):
            #check time control
            loginfo(kwargs)
            pid = kwargs.get("pid", None)
            is_passed = self.check_day(pid)
            loginfo(p=is_passed, label="time decorator")
            if is_passed:
                response = method(request, *args, **kwargs)
                return response
            else:
                return HttpResponseRedirect(reverse('school.views.non_authority_view'))
        return wrappered_method