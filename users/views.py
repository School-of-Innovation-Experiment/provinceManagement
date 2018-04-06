# coding: UTF-8
'''
Created on 2013-4-03

@author: tianwei

Desc: This module contains views that allow users to submit the calculated
      tasks.
'''
import datetime
import logging
import os
import sys

from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseForbidden, Http404
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, load_backend, authenticate
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators import csrf
from django.contrib.auth.decorators import login_required

from backend.logging import logger, loginfo
from backend.decorators import *
from const import *
from users.models import *
from users.forms import *


def base_profile_view(request, authority=None):
    """
        check and load base view
        Arguments:
            In:
                *request, http request
                *authority, CONST lib
            Out: basic profile object or None
    """
    is_auth = check_auth(user=request.user, authority=authority)
    if not is_auth:
        return None

    if authority == SCHOOL_USER:
        user = SchoolProfile.objects.get(userid=request.user)
    elif authority == EXPERT_USER:
        user = ExpertProfile.objects.get(userid=request.user)
    elif authority == ADMINSTAFF_USER:
        user = AdminStaffProfile.objects.get(userid=request.user)
    elif authority == TEACHER_USER:
        user = TeacherProfile.objects.get(userid=request.user)
    else:
        return None

    if request.method == "POST":
        if authority == SCHOOL_USER:
            form = SchoolProfileForm(request.POST, instance=user)
        elif authority == EXPERT_USER:
            form = ExpertProfileForm(request.POST, instance=user)
        elif authority == ADMINSTAFF_USER:
            form = AdminStaffProfileForm(request.POST, instance=user)
        elif authority == TEACHER_USER:
            form = TeacherProfileForm(request.POST, instance=user)
        else:
            return None
        if form.is_valid():
            form.save()
    else:
        if authority == SCHOOL_USER:
            form = SchoolProfileForm(instance=user)
        elif authority == EXPERT_USER:
            form = ExpertProfileForm(instance=user)
        elif authority == ADMINSTAFF_USER:
            form = AdminStaffProfileForm(instance=user)
        elif authority == TEACHER_USER:
            form = TeacherProfileForm(instance=user)
        else:
            return None

    return form
def get_redirect_urls(request):
    if check_auth(user=request.user, authority=SCHOOL_USER):
        return "/school"
    elif check_auth(user=request.user, authority=EXPERT_USER):
        return "/expert"
    elif check_auth(user=request.user, authority=ADMINSTAFF_USER):
        return "/adminStaff"
    elif check_auth(user=request.user, authority=TEACHER_USER):
        return "/teacher"
    else:
        return  "/settings/profile"

@login_required
@csrf.csrf_protect
def profile_view(request):
    """
        Get or Post UserProfile, it will check the user authorities first
    """
    school_form = base_profile_view(request, authority=SCHOOL_USER)
    expert_form = base_profile_view(request, authority=EXPERT_USER)
    adminstaff_form = base_profile_view(request, authority=ADMINSTAFF_USER)
    teacher_form =  base_profile_view(request,authority=TEACHER_USER)

    if request.method == "POST":
        return redirect(get_redirect_urls(request))
    else:
        data = {"school_form": school_form,
            "expert_form": expert_form,
            "adminstaff_form": adminstaff_form,
            "teacher_form":teacher_form,}
        return render(request, "settings/profile.html", data)


@login_required
@csrf.csrf_protect
def admin_account_view(request):
    """
        Set Password
    """
    user = request.user

    if request.method == "POST":
        form = PasswordForm(user, request.POST)
        if form.is_valid():
            user.set_password(form.cleaned_data["new_password"])
            user.save()
    else:
        form = PasswordForm(user)

    data = {"form": form}
    return render(request, "settings/admin.html", data)



@login_required
@csrf.csrf_protect
def search_user_view(request):
    user = request.user
    query_set = User.objects.filter(username__endswith=user.username)
    data = {"query_set": query_set}
    return render(request, "registration/search_user.html", data)


@login_required
@csrf.csrf_protect
def reset_login_view(request, name):
    user = request.user
    username = name
    if username and user.username == username.split('_')[-1]:
        logout(request)
        new_user = User.objects.filter(username=username)[0]
        if new_user is not None and new_user.is_active:
            backend = load_backend(settings.AUTHENTICATION_BACKENDS[0])
            new_user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
            login(request, new_user)
    return HttpResponseRedirect('/')


@login_required
@csrf.csrf_protect
def binding_view(request):
    login_failed = False
    data = {"login_failed": login_failed}
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        new_username = request.user.username
        if user is not None and user.is_active:
            if check_auth(user=user, authority=STUDENT_USER):
                year = user.studentprofile_set.all()[0].projectsingle.year
                user.username = "s_{0}".format(year)+ "_" + new_username
                print("#"*10,user.username)
                user.save()
                return HttpResponseRedirect('/settings/search/')
            elif check_auth(user=user, authority=TEACHER_USER):
                user.username = "t_" + new_username
                user.save()
                return HttpResponseRedirect('/settings/search/')
        else:
            login_failed = True
            data = {"login_failed": login_failed}
            return render(request, "registration/binding.html", data)
    return render(request, "registration/binding.html", data)
