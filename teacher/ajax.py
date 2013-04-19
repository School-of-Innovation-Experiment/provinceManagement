# coding: UTF-8

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from teacher.forms import StudentDispatchForm
from teacher.views import GetStudentRegisterList, TeacherLimitNumber, Send_email_to_student
from const.models import SchoolDict
from const import *
import datetime


@dajaxice_register
def StudentDispatch(request, form):
    student_form =  StudentDispatchForm(deserialize_form(form))
    if student_form.is_valid():
        password = student_form.cleaned_data["student_password"]
        email = student_form.cleaned_data["student_email"]
        name = email
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
            flag = Send_email_to_student(request, name, password, email, STUDENT_USER)
            if flag:
                message = u"发送邮件成功"
                remaining_activation_times -= 1
                return simplejson.dumps({'field':student_form.data.keys(), 'status':'1', 'message':message,'remaining_activation_times':remaining_activation_times})
            else:
                message = u"相同邮件已经发送，中断发送或发生内部错误"
                return simplejson.dumps({'field':student_form.data.keys(), 'status':'1', 'message':message,'remaining_activation_times':remaining_activation_times})
    else:
        return simplejson.dumps({'field':student_form.data.keys(),'error_id':student_form.errors.keys(),'message':u"输入有误,请检查邮箱的合法性"})

    
