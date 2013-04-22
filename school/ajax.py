# coding: UTF8
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from const.models import SchoolDict
from const import *
from adminStaff.utils import DateFormatTransfer
from adminStaff.views import AdminStaffService
from users.models import SchoolProfile, TeacherProfile
from news.models import News
import datetime
from school.forms import TeacherDispatchForm, TeacherNumLimitForm, ExpertDispatchForm
from school.models import Project_Is_Assigned, InsituteCategory, TeacherProjectPerLimits
from school.views import get_project_num_and_remaining

@dajaxice_register
def teacherProjNumLimit(request, form):
    # dajax = Dajax()
    form = TeacherNumLimitForm(deserialize_form(form))
    if form.is_valid():
        teacher_obj = TeacherProfile.objects.get(id=form.cleaned_data["teacher_name"])
        limited_num = form.cleaned_data["limited_num"]
        num_and_remaining = get_project_num_and_remaining(request)
        if num_and_remaining['projects_remaining'] < limited_num:
            return simplejson.dumps({'id':"limited_num" ,'message':u'分配数量不能大于剩余数量'})
        try:
            if  TeacherProjectPerLimits.objects.filter(teacher=teacher_obj).count() == 0:
                projLimit_obj = TeacherProjectPerLimits(teacher=teacher_obj,
                                                       number=limited_num)
                projLimit_obj.save()
            else:
                projLimit_obj = TeacherProjectPerLimits.objects.get(teacher=teacher_obj)
                projLimit_obj.number += limited_num
                projLimit_obj.save()
                # return simplejson.dumps({'id':"teacher_name" ,'message':u'已分配项目给该指导老师，不可重复分配'})
            ret = {'status':'1','message':u'更新成功'}
            ret['projects_remaining'] = get_project_num_and_remaining(request)['projects_remaining']
            return simplejson.dumps(ret)
        except TeacherProfile.DoesNotExist:
            return simplejson.dumps({'id':'teacer_name', 'message':u'更新失败，选定的指导老师没有进行注册'})
    else:
        return simplejson.dumps({'id':form.errors.keys(),'message':u'输入错误'})

@dajaxice_register
def  ExpertDispatch(request, form):
    #dajax = Dajax()
    expert_form =  ExpertDispatchForm(deserialize_form(form))
    if expert_form.is_valid():
        password = expert_form.cleaned_data["expert_password"]
        email = expert_form.cleaned_data["expert_email"]
 #       school = expert_form.cleaned_data["expert_school"]
        name = email
        if password == "":
            password = email.split('@')[0]
        flag = AdminStaffService.sendemail(request, name, password, email,EXPERT_USER)#, expert_school=school)
        if flag:
            message = u"发送邮件成功"
            return simplejson.dumps({'field':expert_form.data.keys(), 'status':'1', 'message':message})
        else:
            message = u"相同邮件已经发送，中断发送"
            return simplejson.dumps({'field':expert_form.data.keys(), 'status':'1', 'message':message})
    else:
        return simplejson.dumps({'field':expert_form.data.keys(),'error_id':expert_form.errors.keys(),'message':u"输入有误,请检查邮箱的合法性"})

@dajaxice_register
def  TeacherDispatch(request, form):
    #dajax = Dajax()
    teacher_form =  TeacherDispatchForm(deserialize_form(form))
    if teacher_form.is_valid():
        password = teacher_form.cleaned_data["teacher_password"]
        email = teacher_form.cleaned_data["teacher_email"]
        # school = teacher_form.cleaned_data["teacher_school"]
        school = SchoolProfile.objects.get(userid=request.user)
        name = email
        if password == "":
            password = email.split('@')[0]
        flag = AdminStaffService.sendemail(request, name, password, email,TEACHER_USER, teacher_school=school)
        if flag:
            message = u"发送邮件成功"
            return simplejson.dumps({'field':teacher_form.data.keys(), 'status':'1', 'message':message})
        else:
            message = u"相同邮件已经发送，中断发送"
            return simplejson.dumps({'field':teacher_form.data.keys(), 'status':'1', 'message':message})
    else:
        return simplejson.dumps({'field':teacher_form.data.keys(),'error_id':teacher_form.errors.keys(),'message':u"输入有误,请检查邮箱的合法性"})
