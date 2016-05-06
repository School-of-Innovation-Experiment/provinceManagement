#!/usr/bin/python
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-05-06 16:01
# Last modified: 2016-05-06 16:01
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
def expert_score(request, pid, score):
    try:
        score = float(score)
        expert = get_object_or_404(ExpertProfile, userid=request.user)
        project = get_object_or_404(ProjectSingle, project_id=pid)
        re_project = get_object_or_404(Re_Project_Expert, expert=expert, project=project)
    except ValueError:
        return HttpResponse("ValueError")
    except:
        return HttpResponse("QueryError")
    if 0 < score < 100:
        re_project.pass_p = True
        re_project.score = score
        re_project.save()
        return HttpResponse("SUCCESS")
    else:
        return HttpResponse("ScoreError")

    return HttpResponse("FIN")


