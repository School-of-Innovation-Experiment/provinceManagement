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

from school.models import ProjectSingle, PreSubmit, FinalSubmit
from school.models import TechCompetition, Patents, Papers, AchievementObjects
from school.models import UploadedFiles
from adminStaff.models import ProjectPerLimits
from users.models import SchoolProfile


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
