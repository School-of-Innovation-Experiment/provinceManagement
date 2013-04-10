# coding: UTF-8
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
from backend.logging import loginfo
from adminStaff.models import NoticeMessage, ProjectControl
from const import MESSAGE_EXPERT_HEAD, MESSAGE_SCHOOL_HEAD

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
        try:
            userauth["school"] = SchoolProfile.objects.get(userid=request.user)
        except SchoolProfile.DoesNotExist, err:
            loginfo(p=err, label="context SchoolProfile")

    if check_auth(user=request.user, authority=ADMINSTAFF_USER):
        userauth["is_adminstaff"] = True
        try:
            userauth["adminstaff"] = AdminStaffProfile.objects.get(userid=request.user)
        except AdminStaffProfile.DoesNotExist:
            loginfo(p=err, label="context AdminStaffProfile")

    if check_auth(user=request.user, authority=EXPERT_USER):
        userauth["is_experter"] = True
        try:
            userauth["expert"] = ExpertProfile.objects.get(userid=request.user)
        except ExpertProfile.DoesNotExist, err:
            loginfo(p=err, label="context ExpertProfile")


    context = {"userauth": userauth}

    return context

def notice_message_settings(request):
    #TODO: 计算动态时间
    school_message, expert_message = "", ""
    context = {}
    try:
        expert_message = NoticeMessage.objects.order_by('-noticedatetime').filter(noticemessage__startswith = MESSAGE_EXPERT_HEAD)[0].noticemessage[len(MESSAGE_EXPERT_HEAD): -1]
    except:
        pass
    try:
        school_message = NoticeMessage.objects.order_by('-noticedatetime').filter(noticemessage__startswith = MESSAGE_SCHOOL_HEAD)[0].noticemessage[len(MESSAGE_SCHOOL_HEAD):]
    except:
        pass
    if ProjectControl.objects.all().count():
        projectctl_obj = ProjectControl.objects.all()[0]
        if school_message[-1] == '1':
            nowstatus = projectctl_obj.now_status()
            if nowstatus[0]:
                school_message = school_message[:-1] + \
                    u' 提示:当前状态 "%s"，距离截止还有 %d 天' %(nowstatus[0], nowstatus[1])
    if expert_message:
        context["expert_notice_message"] = expert_message
    if school_message:
        context["school_notice_message"] = school_message
    return context



