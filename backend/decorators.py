# coding: UTF-8
'''
Created on 2013-04-01

@author: tianwei

Desc: decorators for some controlers, such as time, authorities
'''

import os
import sys
import datetime

from django.contrib.auth.models import User
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
from const.models import *
from adminStaff.models import *
from backend.logging import loginfo
from school.utility import get_current_year
from school.models import *


def check_auth(user=None, authority=None):
    """
    if this user(a id object) has this authority, return True, else False
        Arguments:
            In: user, it is user model object
                authority, it is a const string , which can show the
                authorities
            Out:True or False
    """
    if user is None or authority is None or user.is_anonymous() is True:
        return False

    auth_list = user.identities.all()

    try:
        auth = UserIdentity.objects.get(identity=authority)
    except UserIdentity.DoesNotExist, err:
        loginfo(p=err, label="ERROR in check_auth function!!!")
        return False

    if user.is_superuser:
        return True

    for item in auth_list:
        if item.identity == auth.identity:
            return True

    return False


class authority_required(object):
    """
    This decorator will check whether the user is adminstaff
    """
    def __init__(self, *args):
        self.auth = args

    def check_auth_op(self, request):
        """
        check auth, only pass is the whole pass,
        self.auth is a tuple
        """
        for item in self.auth:
            is_passed = check_auth(user=request.user, authority=item)
            if is_passed:
                return True

        return False

    def __call__(self, method):
        def wrappered_method(request, *args, **kwargs):
            is_passed = self.check_auth_op(request)
            loginfo(p=is_passed, label="authority_required decorator")
            if is_passed:
                response = method(request, *args, **kwargs)
                return response
            else:
                # TODO: add a custom 403 page
                return HttpResponseRedirect(reverse('backend.errorviews.error403'))
        return wrappered_method


class only_user_required(object):
    """
    This decorator will deal with project varify, when the logined user
    can control this project, he can continue.
    """
    def __init__(self, method):
        self.method = method

    def check_auth_op(self, pid, request):
        if pid is None:
            return False

        #ISSUE: we should check get operation!
        try:
            project = ProjectSingle.objects.get(project_id=pid)
        except ProjectSingle.DoesNotExist, err:
            loginfo(p=err,
                    label="only_user_required -> get projectsingle")
            project = None

        if project is not None or request.user.is_superuser:
            return True
        else:
            return False

    def __call__(self, request, *args, **kwargs):
        loginfo(p=kwargs, label="only_user_required args")
        pid = kwargs.get("pid", None)
        is_passed = self.check_auth_op(pid, request)
        loginfo(p=is_passed, label="only_user_required decorator")
        if is_passed:
            response = self.method(request, *args, **kwargs)
            return response
        else:
            return HttpResponseRedirect(reverse('school.views.home_view'))


class time_controller(object):
    """
    This decorator will deal with time control, time the following:
        pre_start --> pre_end --> pre_start_review --> pre_end_review
        final_start --> final_end --> final_start_review --> final_end_review
    """
    def __init__(self, phase):
        self.phase = phase

    def get_established_time(self):
        """
        Get estabilshed time from database
        """
        control = ProjectControl.objects.all()
        loginfo(p=control, label="get_established_time")
        if len(control) == 0:
            return None
        else:
            return control[0]

    def check_year(self, pid):
        """
        Check year
        """
        #If the pid is None, it mains there is no pid imports;
        if pid is None:
            return True

        project = get_object_or_404(ProjectSingle, project_id=pid)

        #If the project year is not this year, it also means you cannot edit it
        if project.year != get_current_year():
            return False


    def check_day(self, pid=None):
        """
        return True or False
        The return value represents the project whether in the established time
        control!
            True: you can edit it!
            False: you cannot edit it!
        """
        # check database table
        control = self.get_established_time()
        #If the database doesn't set anything, it means no time limits.
        if control is None:
            loginfo(p="database check is None", label="time_controller checkday")
            return True

        # check year
        if self.check_year(pid) is False:
            return False

        # check day
        today = datetime.date.today()

        if self.phase == STATUS_PRESUBMIT:
            is_passed = True if today >= control.pre_start_day and today <= control.pre_end_day else False
        elif self.phase == STATUS_PREREVIEW:
            is_passed = True if today >= control.pre_start_day_review and today <= control.pre_end_day_review else False
        elif self.phase == STATUS_ONGOING:
            is_passed = True if today >= control.pre_end_day_review and today <= control.final_start_day else False
        elif self.phase == STATUS_FINSUBMIT:
            is_passed = True if today >= control.final_start_day and today <= control.final_end_day else False
        elif self.phase == STATUS_FINREVIEW:
            is_passed = True if today >= control.final_start_day_review and today <= control.final_end_day_review else False
        elif self.phase == STATUS_FIRST:
            is_passed = True
        else:
            is_passed = False
        return is_passed

    def __call__(self, method):
        def wrappered_method(request, *args, **kwargs):
            #check time control
            pid = kwargs.get("pid", None)
            is_expired = not self.check_day(pid)
            loginfo(p=is_expired, label="time_controller decorator, is_expired")

            #Here, we should use history view strategy to replace forbidden
            kwargs["is_expired"] = is_expired
            response = method(request, *args, **kwargs)
            return response
        return wrappered_method
