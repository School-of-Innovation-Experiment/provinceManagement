#!/usr/bin/python
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-05-06 16:01
# Last modified: 2017-05-26 14:56
# Filename: ajax.py
# Description:

from dajax.core import Dajax
from django.contrib.auth.models import User
from dajaxice.decorators import dajaxice_register
from django.http import Http404, HttpResponse
from const import *
from django.shortcuts import get_object_or_404
from users.models import *
from school.models import *
from django.template.loader import render_to_string


@dajaxice_register
def expert_score(request, pid, is_pass):
    try:
        if not isinstance(is_pass, bool):
            raise ValueError()
        expert = get_object_or_404(ExpertProfile, userid=request.user)
        project = get_object_or_404(ProjectSingle, project_id=pid)
        re_project = get_object_or_404(Re_Project_Expert, expert=expert, project=project)
    except:
        return HttpResponse("Error")
    re_project.pass_p = True
    re_project.score = 1 if is_pass else 0
    re_project.save()
    return HttpResponse('SUCCESS')
