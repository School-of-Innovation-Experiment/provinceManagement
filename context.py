"""
    Author:tianwei
    Email: liutianweidlut@gmail.com
    Desc: settings context processor for templates,
          then we can use
"""

from django.conf import settings
from backend.decorators import check_auth
from const import *
from users.models import *


all_required = ('WEB_TITLE',)


def application_settings(request):
    """The context processor function"""
    mysettings = {}
    for keyword in all_required:
        mysettings[keyword] = getattr(settings, keyword)

    context = {
        'settings': mysettings,
    }

    return context


def userauth_settings(request):
    """
    The context processor will add user authorities variables
    into all template
    """
    userauth = {"is_schooler": False,
                "is_adminstaff": False,
                "is_experter": False
                }

    if check_auth(user=request.user, authority=SCHOOL_USER):
        userauth["is_schooler"] = True
        userauth["school"] = SchoolProfile.objects.get(userid=request.user)
    if check_auth(user=request.user, authority=ADMINSTAFF_USER):
        userauth["is_adminstaff"] = True
        userauth["adminstaff"] = AdminStaffProfile.objects.get(userid=request.user)
    if check_auth(user=request.user, authority=EXPERT_USER):
        userauth["is_experter"] = True
        userauth["expert"] = ExpertProfile.objects.get(userid=request.user)

    context = {"userauth": userauth}

    return context
