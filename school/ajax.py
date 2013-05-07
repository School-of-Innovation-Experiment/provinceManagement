# coding: UTF-8
'''
Created on 2013-4-17

@author: sytmac
'''

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from django.http import Http404
from school.models import ProjectSingle
from school.forms import StudentDispatchForm
from school.views import Send_email_to_student, Count_email_already_exist, school_limit_num
from const.models import SchoolDict, ProjectCategory, FinancialCategory, InsituteCategory
from const import *
import datetime
from backend.logging import logger, loginfo

@dajaxice_register
def  StudentDispatch(request, form):
    #dajax = Dajax()
    student_form =  StudentDispatchForm(deserialize_form(form))
    if student_form.is_valid():
        password = student_form.cleaned_data["student_password"]
        email = student_form.cleaned_data["student_email"]
        financial_cate = student_form.cleaned_data["proj_cate"]
        name = email
        if password == "":
            password = email.split('@')[0]
        #判断是否达到发送邮件的最大数量
        email_num = Count_email_already_exist(request)
        limited_num = school_limit_num(request)
        remaining_activation_times = limited_num-email_num
        if remaining_activation_times==0:
            message = u"已经达到最大限度，无权发送"
            return simplejson.dumps({'field':student_form.data.keys(), 'status':'1', 'remaining_activation_times':remaining_activation_times, 'message':message})
        else:
            flag = Send_email_to_student(request, name, password, email,STUDENT_USER, financial_cate=financial_cate)
            if flag:
                message = u"发送邮件成功"
                remaining_activation_times -= 1
                return simplejson.dumps({'field':student_form.data.keys(), 'status':'1', 'message':message,'remaining_activation_times':remaining_activation_times})
            else:
                message = u"相同邮件已经发送，中断发送或发生内部错误"
                return simplejson.dumps({'field':student_form.data.keys(), 'status':'1', 'message':message,'remaining_activation_times':remaining_activation_times})
    else:
        return simplejson.dumps({'field':student_form.data.keys(),'error_id':student_form.errors.keys(),'message':u"输入有误,请检查邮箱的合法性"})

@dajaxice_register
def ProjCateChange(request, cate):
    #dajax = Dajax()
    try:
        project = ProjectSingle.objects.get(student__user=request.user)
        new_cate = ProjectCategory.objects.get(category=cate)
    except Exception, err:
        loginfo(p=err, label="change project cate")
        raise Http404
    project.project_category = new_cate
    project.save()
    return simplejson.dumps({"message": u"更新成功: %s" % new_cate})

@dajaxice_register
def ProjInsituteChange(request, cate):
    try:
        project = ProjectSingle.objects.get(student__user=request.user)
        new_cate = InsituteCategory.objects.get(category=cate)
    except Exception, err:
        loginfo(p=err, label="change project insitute")
        raise Http404
    project.insitute = new_cate
    project.save()
    return simplejson.dumps({"message": u"更新成功: %s" % new_cate})

@dajaxice_register
def FinancialCateChange(request, cate):
    #dajax = Dajax()
    try:
        project = ProjectSingle.objects.get(adminuser=request.user)
        new_cate = FinancialCategory.objects.get(category=cate)
    except Exception, err:
        loginfo(p=err, label="change financial cate")
        raise Http404
    project.financial_category = new_cate
    project.save()
    return simplejson.dumps({"message": u"更新成功: %s" % new_cate})
