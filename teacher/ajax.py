# coding: UTF-8

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from django.template.loader import render_to_string

from django.http import Http404

from adminStaff.forms import StudentDispatchForm
from teacher.forms import  MonthCommentForm
from teacher.views import GetStudentRegisterList, TeacherLimitNumber, Send_email_to_student
from teacher.models import TeacherMonthComment
from school.models import ProjectSingle
from const.models import SchoolDict
from const import *
import datetime

def refresh_project_table(request):
    email_list  = GetStudentRegisterList(request)
    return render_to_string("teacher/widgets/project_table.html",
                            {"email_list": email_list})

@dajaxice_register
def StudentDispatch(request, form):
    student_form =  StudentDispatchForm(deserialize_form(form))
    if student_form.is_valid():
        password = student_form.cleaned_data["student_password"]
        email = student_form.cleaned_data["student_email"]
        category = student_form.cleaned_data["category"]
        name = email
        person_name = student_form.cleaned_data["person_firstname"]
        if password == "":
            password = email.split('@')[0]
        #判断是否达到发送邮件的最大数量
        email_list  = GetStudentRegisterList(request)
        email_num = email_list and len(email_list) or 0
        limited_num = TeacherLimitNumber(request)
        remaining_activation_times = limited_num - email_num
        if remaining_activation_times==0:
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
        return simplejson.dumps({'field':student_form.data.keys(),'error_id':student_form.errors.keys(),'message':u"输入有误,"})

@dajaxice_register
def commentChange(request, form, pid):
    comment_form = MonthCommentForm(deserialize_form(form))
    if not comment_form.is_valid():
        ret = {'status': '2',
               'error_id': comment_form.errors.keys(),
               'message': u"输入有误，请重新输入"}
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




