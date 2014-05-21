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
from django.db.models import Q
from backend.logging import loginfo
from adminStaff.models import NoticeMessage, ProjectControl
from const import MESSAGE_EXPERT_HEAD, MESSAGE_SCHOOL_HEAD ,MESSAGE_STUDENT_HEAD,IS_DLUT_SCHOOL,IS_MINZU_SCHOOL

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
    context = {}
    userauth = {"is_schooler": False,
                "is_adminstaff": False,
                "is_experter": False,
                "is_teacher": False,
                "is_student": False,
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
        except AdminStaffProfile.DoesNotExist, err:
            loginfo(p=err, label="context AdminStaffProfile")

    if check_auth(user=request.user, authority=EXPERT_USER):
        userauth["is_experter"] = True
        try:
            userauth["expert"] = ExpertProfile.objects.get(userid=request.user)
        except ExpertProfile.DoesNotExist, err:
            loginfo(p=err, label="context ExpertProfile")

    if check_auth(user=request.user, authority=TEACHER_USER):
        userauth["is_teacher"] = True
        try:
            userauth["teacher"] = TeacherProfile.objects.get(userid=request.user)
        except TeacherProfile.DoesNotExist, err:
            loginfo(p=err, label="context TeacherProfile")

    if check_auth(user=request.user, authority=STUDENT_USER):
        userauth["is_student"] = True
        try:
            userauth["student"] = StudentProfile.objects.get(userid=request.user)
        except StudentProfile.DoesNotExist, err:
            loginfo(p=err, label="context StudentProfile")
    school_message, expert_message, student_message, teacher_message = "", "" ,"",""
    try:
        expert_message = NoticeMessage.objects.filter(Q(noticemessage__startswith = MESSAGE_EXPERT_HEAD) | Q(noticemessage__startswith = MESSAGE_ALL_HEAD)).order_by('-noticedatetime')[0].noticemessage[len(MESSAGE_EXPERT_HEAD): -1]
    except:
        pass
    try:
        school_message = NoticeMessage.objects.filter(Q(noticemessage__startswith = MESSAGE_SCHOOL_HEAD) | Q(noticemessage__startswith = MESSAGE_ALL_HEAD)).order_by('-noticedatetime')[0].noticemessage[len(MESSAGE_SCHOOL_HEAD):]
        school_message, school_check = school_message[:-1], school_message[-1]
    except:
        pass
    try:
        student_message = NoticeMessage.objects.filter(Q(noticemessage__startswith = MESSAGE_STUDENT_HEAD) | Q(noticemessage__startswith = MESSAGE_ALL_HEAD)).order_by('-noticedatetime')[0].noticemessage[len(MESSAGE_STUDENT_HEAD):]
        student_message, student_check = student_message[:-1], student_message[-1]
    except:
        pass
    try:
        teacher_message = NoticeMessage.objects.filter(Q(noticemessage__startswith = MESSAGE_TEACHER_HEAD) | Q(noticemessage__startswith = MESSAGE_ALL_HEAD)).order_by('-noticedatetime')[0].noticemessage[len(MESSAGE_TEACHER_HEAD):]
        teacher_message, teacher_check = teacher_message[:-1], teacher_message[-1]
    except:
        pass
    # if ProjectControl.objects.all().count():
    #     projectctl_obj = ProjectControl.objects.all()[0]
    #     if school_message and school_check == '1':
    #         nowstatus = projectctl_obj.now_status()
    #         if nowstatus[0]:
    #             school_message = school_message[:-1] + \
    #                 u' 提示:当前状态 "%s"，距离截止还有 %d 天' %(nowstatus[0], nowstatus[1])
    if userauth["is_experter"]:
        userauth["notice_message"] = expert_message
    if userauth["is_schooler"]:
        userauth["notice_message"] = school_message
    if userauth["is_student"]:
        userauth["notice_message"] = student_message
    if userauth["is_teacher"]:
        loginfo("teacher_message"+teacher_message);
        userauth["notice_message"] = teacher_message
    if userauth["is_adminstaff"]:
        userauth["notice_message"] = ""
   
	context = {"userauth": userauth}

    context["IS_DLUT_SCHOOL"] = IS_DLUT_SCHOOL
    context["IS_MINZU_SCHOOL"] = IS_MINZU_SCHOOL
    context["IS_SCHOOL_BASIC"] = IS_SCHOOL_BASIC
    return context

def notice_message_settings(request):
    #TODO: 计算动态时间
    context = {}
    return context


def adminStaffinfo_settings(request):
    context = {}
    currenturl = os.path.dirname(os.path.abspath('__file__'))
    mediaurl = os.path.join(currenturl,"media")
    infotxt_path = os.path.join(mediaurl,"adminStaffinfo.txt")
    if os.path.exists(infotxt_path):
        print "file exist"
        data = pickle.load(open(infotxt_path,"r"))
        SCHOOL_CHINAME = data["chinese_name"]
        SCHOOL_ENGNAME = data["english_name"]
        SCHOOL_CODE = data["index"]
    else:
        print "file not exist"
        SCHOOL_CHINAME = ""
        SCHOOL_ENGNAME = ""
        SCHOOL_CODE = ""
    context["SCHOOL_CHINAME"] = SCHOOL_CHINAME
    context["SCHOOL_ENGNAME"] = SCHOOL_ENGNAME
    context["SCHOOL_CODE"] = SCHOOL_CODE
    loginfo(p=context["SCHOOL_CHINAME"],label="SCHOOL_CHINAME")
    return context
