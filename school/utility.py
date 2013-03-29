# coding: UTF-8
'''
Created on 2013-03-29

@author: tianwei

Desc: Utility functions for school page
'''

import uuid
import os
import sys
import time

from django.shortcuts import get_object_or_404

from school.models import ProjectSingle, PreSubmit, FinalSubmit
from school.models import TechCompetition, Patents, Papers, AchievementObjects
from school.models import UploadedFiles
from const.models import SchoolDict, ProjectCategory, InsituteCategory
from const.models import UserIdentity, ProjectGrade, ProjectStatus
from adminStaff.models import ProjectPerLimits
from users.models import SchoolProfile

from const import AUTH_CHOICES, VISITOR_USER
from const import PROJECT_CATE_CHOICES, CATE_UN
from const import PROJECT_GRADE_CHOICES, GRADE_UN
from const import PROJECT_STATUS_CHOICES, STATUS_FIRST

from backend.utility import search_tuple


from backend.logging import logger


def check_limits(user):
    """
    Check school limits of quota
    Arguments:
        In: user, it is request.user, user id
        Out: True or False
    """
    try:
        limits = ProjectPerLimits.objects.get(school__userid__userid=user)
    except:
        limits = None

    currents = ProjectSingle.objects.filter(adminuser=user).count()
    total = limits.number if limits is not None else 0

    return True if total > currents else False


def get_year():
    """
    Get current year
    Arguments:
        Out: current year
    """
    return str(time.localtime()[0])


def save_application(pid=None, info_form=None, application_form=None, user=None):
    """
    Application Report Save
    Arguments:
        In:
            *pid, project id
            *info_form, ProjectSingle form
            *application_form, PreSubmit form
        Out:
            *True or False
    """
    if pid is None or info_form is None or application_form is None:
        return False

    project = get_object_or_404(ProjectSingle, project_id=pid)

    try:
        info = info_form.save(commit=False)
        info.project_grade = ProjectGrade.objects.get(grade=GRADE_UN)
        info.project_status = ProjectStatus.objects.get(status=STATUS_FIRST)
        info.school = SchoolProfile.objects.get(userid__userid=user).school
        info.adminuser = user
        info.year = get_year()
        info.save()

        application = application_form.save(commit=False)
        application.content_id = uuid.uuid4()
        application.project_id = project
        application.save()

        return True
    except Exception, err:
        logger.info("save process"+"**"*10)
        logger.info(err)
        logger.info("--"*10)
        return False
