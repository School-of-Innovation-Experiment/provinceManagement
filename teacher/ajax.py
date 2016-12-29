#!/usr/local/bin/python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-12-29 16:57
# Last modified: 2016-12-29 16:57
# Filename: ajax.py
# Description:
# coding: UTF-8

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.http import Http404

from adminStaff.forms import StudentDispatchForm
from teacher.forms import  MonthCommentForm
from teacher.views import  TeacherLimitNumber, Send_email_to_student
from teacher.models import TeacherMonthComment
from school.models import *
from users.models import StudentProfile,TeacherProfile,SchoolProfile
from const.models import SchoolDict
from adminStaff.views import AdminStaffService
from const import *
import datetime
from backend.logging import logger, loginfo
from backend.decorators import check_auth

def refresh_project_table(request):
    teacher_profile = TeacherProfile.objects.get(userid = request.user)
    email_list  = AdminStaffService.GetRegisterListByTeacher(teacher_profile)
    return render_to_string("teacher/widgets/project_table.html",
                            {"email_list": email_list})

def delete_project_ralated(project):
    category = project.project_category.category
    if category == CATE_INNOVATION:
        pre = PreSubmit.objects.get(project_id = project)
        pre.delete()
    else:
        pre_interprise = PreSubmitEnterprise.objects.get(project_id = project)
        teacher_enterprise = pre_interprise.enterpriseTeacher
        teacher_enterprise.delete()
        pre_interprise.delete()

    final = FinalSubmit.objects.get(project_id = project)
    for achievement in AchievementObjects.objects.filter(project_id = final):
        achievement.delete()
    final.delete()

def ext_delete_project_ralated(project):
    for re_project_expert in Re_Project_Single.objects.filter(project = project):
        re_project_expert.delete()

    for paper in Papers.objects.filter(project_id = project):
        paper.delete()

    for tech_competition in TechCompetition.objects.filter(project_id = project):
        tech_competition.delete()

    for patent in Patents.objects.filter(project_id = project):
        patent.delete()

    for uploaderfile in UploadedFiles.objects.filter(project_id = project):
        uploaderfile.delete()


@dajaxice_register
def brute_delete(request, email):
    """
    删除已激活User，删除User, Student及相关Project，Presubmit，finalsubmit
    追加删除Re_Project_Single, Papers, TechCompetition, patents, UploadedFiles
    """
    message = ""
    user = User.objects.get(email = email)
    if not has_delete_access(request,user):
        message = u"超出权限，删除失败"
        return simplejson.dumps({"message":message})
    student = StudentProfile.objects.get(userid = user)
    student.delete()
    try:
        project = ProjectSingle.objects.get(student__userid = user)
        delete_project_ralated(project)
        ext_delete_project_ralated(project)
        project.delete()
    except:
        pass
    user.delete()
    return simplejson.dumps({"message": message})

@dajaxice_register
def StudentDispatch(request, form):
    student_form =  StudentDispatchForm(deserialize_form(form))
    if student_form.is_valid():
        password = student_form.cleaned_data["student_password"]
        email = student_form.cleaned_data["student_email"]
        category = student_form.cleaned_data["category"]
        name = email
        person_name = student_form.cleaned_data["student_personname"]
        if password == "":
            password = email.split('@')[0]
        #判断是否达到发送邮件的最大数量
        email_list  = AdminStaffService.GetRegisterListByTeacher(teacher = TeacherProfile.objects.get(userid = request.user))
        email_num = email_list and len(email_list) or 0
        limited_num = TeacherLimitNumber(request)
        remaining_activation_times = limited_num - email_num
        if remaining_activation_times<=0:
            message = u"已经达到最大限度，无权发送"
            return simplejson.dumps({'field':student_form.data.keys(), 'status':'1', 'remaining_activation_times':remaining_activation_times, 'message':message})
        else:
            flag = Send_email_to_student(request, name, password, email, category,person_name, STUDENT_USER)
            if flag:
                message = u"发送邮件成功"
                remaining_activation_times -= 1
                table = refresh_project_table(request)
                return simplejson.dumps({'field':student_form.data.keys(), 'status':'1', 'message':message,'remaining_activation_times':remaining_activation_times, 'table':table})
            else:
                message = u"相同邮件已经发送，中断发送或发生内部错误"
                return simplejson.dumps({'field':student_form.data.keys(), 'status':'1', 'message':message,'remaining_activation_times':remaining_activation_times})
    else:
        email_list  = AdminStaffService.GetRegisterListByTeacher(teacher = TeacherProfile.objects.get(userid = request.user))
        email_num = email_list and len(email_list) or 0
        limited_num = TeacherLimitNumber(request)
        remaining_activation_times = limited_num - email_num
        return simplejson.dumps({'field':student_form.data.keys(),'error_id':student_form.errors.keys(),'message':u"输入有误",'remaining_activation_times':remaining_activation_times})

@dajaxice_register
def commentChange(request, form, pid):
    comment_form = MonthCommentForm(deserialize_form(form))
    if not comment_form.is_valid():
        message = u"";
        if "commenttext" in  comment_form.errors.keys():
            message += u"过程记录字数超过限制!"
        if "monthId" in comment_form.errors.keys():
            message += u"请填写月次！"
        ret = {'status': '2',
               'error_id': comment_form.errors.keys(),
               'message': message}
    else:
        ret = new_or_update_comment(request,comment_form,pid)
    return simplejson.dumps(ret)

def new_or_update_comment(request,comment_form,pid):
    comment_monthId   = comment_form.cleaned_data["monthId"]
    comment_text     = comment_form.cleaned_data["commenttext"]
    try:
        project = ProjectSingle.objects.get(project_id=pid)
    except:
        raise Http404
    group = project.teachermonthcomment_set
    for comment in group.all():
        if comment.monthId == comment_monthId:
            comment.comment  = comment_text
            comment.save()
            table = refresh_comment_table(request,pid)
            ret = {'status': '0', 'message': u"评论记录更新成功", 'table':table}
            break
    else: 
        if group.count() == PROGRESS_RECORD_MAX:
            ret = {'status': '1', 'message': u"评论记录已满，不可添加"}
        else:
            new_comment = TeacherMonthComment( monthId = comment_monthId,
                                  comment   = comment_text,
                                  project=project)
            new_comment.save()
            table = refresh_comment_table(request,pid)
            ret = {'status': '0', 'message': u"评论记录添加成功", 'table':table}
    return ret

def refresh_comment_table(request,pid):
    project = ProjectSingle.objects.get(project_id=pid)
    comment_group  = TeacherMonthComment.objects.filter(project=pid).order_by("monthId")
    return render_to_string("teacher/widgets/comment_group_table.html",
                            {"comment_group": comment_group})
@dajaxice_register
def CommentDelete(request,deleteMonthId,pid):
    try:
        project = ProjectSingle.objects.get(project_id=pid)
    except:
        raise Http404
    group = project.teachermonthcomment_set
    deleteMonthId = int(deleteMonthId)
    for monthComment in group.all():
        if monthComment.monthId == deleteMonthId:
            monthComment.delete()
            table = refresh_comment_table(request,pid)
            ret = {'status': '0', 'message': u"评语记录删除成功", 'table':table}
            break
    else:
        ret = {'status': '1', 'message': u"所要删除评语记录不存在，请刷新页面"}
    return simplejson.dumps(ret)

@dajaxice_register
def simple_delete(request, email):
    """
    删除未激活User，删除User, Student及相关Project，presubmit，finalsubmit
    """
    message = ""
    try:
        user = User.objects.get(email = email)
        if not has_delete_access(request,user):
            message = u"超出权限，删除失败"
            return simplejson.dumps({"message": message,})
        user.delete()
    except Exception, e:
        loginfo(e)
    #email_list  = AdminStaffService.GetRegisterListByTeacher(teacher = TeacherProfile.objects.get(userid = request.user))
    #email_num = email_list and len(email_list) or 0
    #limited_num = TeacherLimitNumber(request)
    #remaining_activation_times = limited_num - email_num
    message = u"删除成功"
    return simplejson.dumps({"message": message})

def has_delete_access(request,user):
    access_flag = False
    if check_auth(request.user, TEACHER_USER):
        teacher = TeacherProfile.objects.get(userid = request.user)
        student_list = StudentProfile.objects.filter(teacher = teacher)
        for stu in student_list:
            if stu.userid == user:
                access_flag = True
    if check_auth(request.user,SCHOOL_USER):
        schooler = SchoolProfile.objects.get(userid = request.user)
        teacher_list = TeacherProfile.objects.filter(school = schooler.id)
        for teacher in teacher_list:
            if teacher.userid == user:
                access_flag = True
    return access_flag
