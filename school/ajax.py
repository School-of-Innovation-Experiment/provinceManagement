# coding: UTF-8
'''
Created on 2013-4-17

@author: sytmac
'''

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from const.models import SchoolDict
from const import *
import datetime
@dajaxice_register
def  StudentDispatch(request, form):
    #dajax = Dajax()
    expert_form =  StudentDispatchForm(deserialize_form(form))
    if expert_form.is_valid():
        password = student_form.cleaned_data["student_password"]
        email = student_form.cleaned_data["student_email"]
        insitute = student_form.cleaned_data["student_insitute"]
        name = email
        if password == "":
            password = email.split('@')[0]
        flag = sendemail(request, name, password, email,EXPERT_USER, expert_insitute=insitute)
        if flag:
            message = u"发送邮件成功"
            return simplejson.dumps({'field':expert_form.data.keys(), 'status':'1', 'message':message})
        else:
            message = u"相同邮件已经发送，中断发送"
            return simplejson.dumps({'field':expert_form.data.keys(), 'status':'1', 'message':message})
    else:
        return simplejson.dumps({'field':expert_form.data.keys(),'error_id':expert_form.errors.keys(),'message':u"输入有误,请检查邮箱的合法性"})

    