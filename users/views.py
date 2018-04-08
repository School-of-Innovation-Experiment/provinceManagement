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
from school.models import ProjectSingle
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
def switch_user_list_view(request):
    user = request.user
    user_set = User.objects.filter(
        username__endswith=user.username.split('_')[-1],
            is_active=True).exclude(
            username__in=(user.username,user.username.split('_')[-1]))
    query_set = []
    identity = 0
    if user_set.count() == 0:
        data = {"query_set": query_set, "identity": identity}
        return render(request, "registration/switch_user.html", data)
    else:
        identity = 1 if user_set[0].username[0] == 'S' else 2
        if identity == 1:
            query_set = ProjectSingle.objects.select_related(
                'student__userid').filter(student__userid__in=user_set)
        elif identity == 2:
            query_set = user_set
        data = {"query_set": query_set, "identity": identity}
        return render(request, "registration/switch_user.html", data)


@login_required
@csrf.csrf_protect
def relogin_view(request, username):
    user = request.user
    identity = 'news'
    if user.username.split('_')[-1] == username.split('_')[-1]:
        logout(request)
        new_user_set = User.objects.filter(username=username, is_active=True)
        if new_user_set.count() > 0:
            new_user = new_user_set[0]
        else:
            raise HttpResponseForbidden()
        backend = load_backend(settings.AUTHENTICATION_BACKENDS[0])
        new_user.backend = "%s.%s" % (
            backend.__module__, backend.__class__.__name__)
        login(request, new_user)
        if check_auth(user=new_user, authority=STUDENT_USER):
            identity = 'student_home'
        elif check_auth(user=new_user, authority=TEACHER_USER):
            identity = 'teacher_home'
        elif check_auth(user=new_user, authority=SCHOOL_USER):
            identity = 'school_home'
    return HttpResponseRedirect(reverse(identity))


@login_required
@csrf.csrf_protect
def binding_view(request):
    error_code = 0
    if request.user.username[0] in ('S', 'T', 'A'):
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            new_username_end = request.user.username
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                if check_auth(user=user, authority=STUDENT_USER):
                    year = user.studentprofile_set.all()[0].projectsingle.year
                    new_username = "S_{0}_{1}".format(year, new_username_end)
                elif check_auth(user=user, authority=TEACHER_USER):
                    new_username = "T_" + new_username_end
                elif check_auth(user=user, authority=SCHOOL_USER):
                    new_username = "A_" + new_username_end
                if User.objects.filter(username=new_username).count() > 0:
                    error_code = 1
                    return render(request, "registration/binding.html", {
                        "error_code": error_code})
                else:
                    user.username = new_username
                    user.set_unusable_password()
                    user.save()
                    return HttpResponseRedirect(reverse('switch'))
            else:
                error_code = -1
                return render(request, "registration/binding.html", {
                    "error_code": error_code})
        return render(request, "registration/binding.html", {
            "error_code": error_code})
