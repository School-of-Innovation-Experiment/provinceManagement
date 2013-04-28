# coding: UTF8
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from django.template.loader import render_to_string
from const.models import SchoolDict
from const import *
from adminStaff.utils import DateFormatTransfer
from adminStaff.views import AdminStaffService
from users.models import SchoolProfile, TeacherProfile
from news.models import News
import datetime
from school.forms import TeacherDispatchForm, TeacherNumLimitForm, ExpertDispatchForm
from school.models import Project_Is_Assigned, InsituteCategory, TeacherProjectPerLimits
from school.views import get_project_num_and_remaining, teacherLimitNumList

def refresh_mail_table(request):
    school = SchoolProfile.objects.get(userid=request.user)
    if not school:
        raise Http404
    email_list  = AdminStaffService.GetRegisterListBySchool(school)
    email_list.extend(AdminStaffService.GetRegisterExpertListBySchool(school))

    return render_to_string("school/widgets/mail_table.html",
                            {"email_list": email_list})

def refresh_numlimit_table(request):
    teacher_limit_num_list = teacherLimitNumList(request)
    return render_to_string("school/widgets/numlimit_table.html",
                            {'teacher_limit_num_list': teacher_limit_num_list})

@dajaxice_register
def  ExpertDispatch(request, form):
    expert_form =  ExpertDispatchForm(deserialize_form(form))
    if expert_form.is_valid():
        password = expert_form.cleaned_data["expert_password"]
        email = expert_form.cleaned_data["expert_email"]
        name = email
        if password == "":
            password = email.split('@')[0]
        flag = AdminStaffService.sendemail(request, name, password, email,EXPERT_USER, expert_user="assigned_by_school")
        if flag:
            message = u"发送邮件成功"
            table = refresh_mail_table(request)
            return simplejson.dumps({'field':expert_form.data.keys(), 'status':'1', 'message':message, 'table': table})
        else:
            message = u"相同邮件已经发送，中断发送"
            return simplejson.dumps({'field':expert_form.data.keys(), 'status':'1', 'message':message})
    else:
        return simplejson.dumps({'field':expert_form.data.keys(),'error_id':expert_form.errors.keys(),'message':u"输入有误,请检查邮箱的合法性"})

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
            ret["table"] = refresh_numlimit_table(request)
            return simplejson.dumps(ret)
        except TeacherProfile.DoesNotExist:
            return simplejson.dumps({'id':'teacer_name', 'message':u'更新失败，选定的指导老师没有进行注册'})
    else:
        return simplejson.dumps({'id':form.errors.keys(),'message':u'输入错误'})


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
            table = refresh_mail_table(request)
            return simplejson.dumps({'field':teacher_form.data.keys(), 'status':'1', 'message':message, 'table': table})
        else:
            message = u"相同邮件已经发送，中断发送"
            return simplejson.dumps({'field':teacher_form.data.keys(), 'status':'1', 'message':message})
    else:
        return simplejson.dumps({'field':teacher_form.data.keys(),'error_id':teacher_form.errors.keys(),'message':u"输入有误,请检查邮箱的合法性"})

@dajaxice_register
def judge_is_assigned(request):
    try:
        schoolObj = SchoolProfile.objects.get(userid = request.user)
    except SchoolProfile.DoesNotExist:
        return simplejson.dumps({'flag':None,'message':u"SchoolProfile 数据不完全，请联系管理员更新数据库"}) 
    try:
        obj = Project_Is_Assigned.objects.get(school = schoolObj)
    except Project_Is_Assigned.DoesNotExist:
        return simplejson.dumps({'flag':None,'message':u"Project_Is_Assigned 数据不完全，请联系管理员更新数据库"}) 
    return simplejson.dumps({'flag': obj.is_assigned_in_presubmit})


