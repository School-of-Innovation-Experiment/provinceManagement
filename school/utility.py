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
from django.utils import simplejson
from django.http import HttpResponse
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile

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


def save_application(project=None, info_form=None, application_form=None, user=None):
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
    if project is None or info_form is None or application_form is None:
        return False

    try:
        info = info_form.save(commit=False)
        info.save()

        application = application_form.save(commit=False)
        application.save()

        return True
    except Exception, err:
        logger.info("save process"+"**"*10)
        logger.info(err)
        logger.info("--"*10)
        return False


def response_minetype(request):
    """
    File upload mine type escape
    """
    if "application/json" in request.META["HTTP_ACCEPT"]:
        return "application/json"
    else:
        return "text/plain"


class JSONResponse(HttpResponse):
    """Json response class"""
    def __init__(self, obj='', json_opts={}, mimetype="application/json",
                 *args, **kwargs):
        content = simplejson.dumps(obj, **json_opts)
        super(JSONResponse, self).__init__(content, mimetype, *args, **kwargs)


def upload_save_process(request, pid):
    """
        save file into local storage
    """
    f = request.FILES["file"]
    wrapper_f = UploadedFile(f)

    name, filetype = split_name(wrapper_f.name)

    obj = UploadedFiles()
    obj.name = name
    obj.project_id = ProjectSingle.objects.get(project_id=pid)
    obj.file_id = uuid.uuid4()
    obj.file_obj = f

    #TODO: we will check file type
    obj.file_type = filetype if filetype != " " else "unknown"
    obj.save()

    return wrapper_f


def upload_response(request, pid):
    """
        use AJAX to process file upload
    """
    wrapper_f = upload_save_process(request, pid)
    path = settings.MEDIA_URL + settings.PROCESS_FILE_PATH
    data = [{'name': wrapper_f.name,
             'url': path + wrapper_f.name.replace(" ", "_"),
             }]

    response = JSONResponse(data, {}, response_minetype(request))
    response["Content-Dispostion"] = "inline; filename=files.json"

    return response


def split_name(name, sep="."):
    """
        split type and name in a filename
    """
    name = str(name)
    if sep in name:
        f = name.split(sep)[0]
        t = name.split(sep)[1]
    else:
        f = name
        t = " "

    return (f, t)
