# coding: UTF8
from django.shortcuts import get_object_or_404
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from django.template.loader import render_to_string
from const.models import SchoolDict
from const import *
from const.models import *
from adminStaff.utils import DateFormatTransfer
from adminStaff.views import AdminStaffService
from users.models import SchoolProfile, TeacherProfile, ExpertProfile
from news.models import News
from django.contrib.auth.models import User
import datetime
from adminStaff.forms import TeacherDispatchForm, ExpertDispatchForm
from school.forms import TeacherNumLimitForm
from school.models import Project_Is_Assigned, InsituteCategory, TeacherProjectPerLimits,ProjectFinishControl,ProjectSingle, Re_Project_Expert
from school.views import get_project_num_and_remaining, teacherLimitNumList
from backend.logging import logger, loginfo
from django.db.models import Q

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
        person_name = expert_form.cleaned_data["person_firstname"]
        if password == "":
            password = email.split('@')[0]
        flag = AdminStaffService.sendemail(request, name, password, email,EXPERT_USER, expert_user="assigned_by_school",person_name=person_name)
        if flag:
            message = u"发送邮件成功"
            table = refresh_mail_table(request)
            return simplejson.dumps({'field':expert_form.data.keys(), 'status':'1', 'message':message, 'table': table})
        else:
            message = u"相同邮件已经发送，中断发送"
            return simplejson.dumps({'field':expert_form.data.keys(), 'status':'1', 'message':message})
    else:
        return simplejson.dumps({'field':expert_form.data.keys(),'error_id':expert_form.errors.keys(),'message':u"输入有误"})

@dajaxice_register
def teacherProjNumLimit(request, form):
    # dajax = Dajax()
    form = TeacherNumLimitForm(deserialize_form(form), request = request)
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
        loginfo(form.fields["teacher_name"].choices)
        loginfo(p=form.errors.keys(),label="keys")
        loginfo(form.errors)
        return simplejson.dumps({'id':form.errors.keys(),'message':u'输入错误'})
@dajaxice_register
def Alloc_Project_to_Expert(request, expert_list, project_list, user_grade):
    flag = (user_grade == 'adminStaff')
    message = ''
    if len(expert_list) == 0:
        message = 'no expert input'
    if len(project_list) == 0:
        message = 'no project input'
    for project_id in project_list:
        project = get_object_or_404(ProjectSingle, project_id = project_id)
        for expert_id in expert_list:
            expert = ExpertProfile.objects.get(userid__email = expert_id)
            try:
                re_project_expert = Re_Project_Expert.objects.get(project = project, expert = expert, is_assign_by_adminStaff = flag)
                re_project_expert.delete()
            except:
                pass
            finally:
                Re_Project_Expert(project = project, expert = expert, is_assign_by_adminStaff = flag).save()
    return simplejson.dumps({'message': message})

@dajaxice_register
def Query_Alloced_Expert(request, project_id, user_grade):
    flag = (user_grade == 'adminStaff')
    message = ''
    project = get_object_or_404(ProjectSingle, project_id = project_id)
    expert_list = [item.expert for item in Re_Project_Expert.objects.filter(Q(project = project) & Q(is_assign_by_adminStaff = flag))]

    expert_list_html = ''
    for expert in expert_list:
        expert_list_html += '<p>' + expert.name + '(' + str(expert) + ')' + '</p>'

    return simplejson.dumps({'message': message, 'expert_list_html': expert_list_html})

@dajaxice_register
def Cancel_Alloced_Experts(request, project_list, user_grade):
    flag = (user_grade == 'adminStaff')
    message = ''
    if len(project_list) == 0:
        message = 'no project input'
    for project_id in project_list:
        project = get_object_or_404(ProjectSingle, project_id = project_id)
        for re_project_expert in Re_Project_Expert.objects.filter(Q(project = project) & Q(is_assign_by_adminStaff = flag)):
            re_project_expert.delete()
            
    return simplejson.dumps({'message': message})

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
        person_name = teacher_form.cleaned_data["person_firstname"]
        if password == "":
            password = email.split('@')[0]
        flag = AdminStaffService.sendemail(request, name, password, email,TEACHER_USER, teacher_school=school,person_name = person_name)
        if flag:
            message = u"发送邮件成功"
            table = refresh_mail_table(request)
            return simplejson.dumps({'field':teacher_form.data.keys(), 'status':'1', 'message':message, 'table': table})
        else:
            message = u"相同邮件已经发送，中断发送"
            return simplejson.dumps({'field':teacher_form.data.keys(), 'status':'1', 'message':message})
    else:
        return simplejson.dumps({'field':teacher_form.data.keys(),'error_id':teacher_form.errors.keys(),'message':u"输入有误"})

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

@dajaxice_register
def applicaton_control(request):
    try:
        schoolObj = SchoolProfile.objects.get(userid = request.user)
    except SchoolProfile.DoesNotExist:
        return simplejson.dumps({'flag':None,'message':u"SchoolProfile 数据不完全，请联系管理员更新数据库"}) 
    if schoolObj.is_applying:
        schoolObj.is_applying = False
        schoolObj.save()
    else:
        schoolObj.is_applying =True
        schoolObj.save()
    flag=schoolObj.is_applying
    return simplejson.dumps({'flag': flag})

@dajaxice_register
def finish_control(request,year_list):
    try:
        schoolObj = SchoolProfile.objects.get(userid = request.user)
    except SchoolProfile.DoesNotExist:
        return simplejson.dumps({'flag':None,'message':u"SchoolProfile 数据不完全，请联系管理员更新数据库"}) 
    user = User.objects.get(id=schoolObj.userid_id)
    if schoolObj.is_finishing ==False:
        if year_list != []:            
            for temp in year_list:
                projectcontrol=ProjectFinishControl()
                projectcontrol.userid=user
                projectcontrol.project_year=temp
                projectcontrol.save()
            schoolObj.is_finishing=True
            schoolObj.save()
            flag = True
        else:
            return simplejson.dumps({'flag':None,'message':u"项目年份未选择或是没有未结题项目"}) 
    else:
        projectcontrol_list=ProjectFinishControl.objects.filter(userid=user)
        projectcontrol_list.delete()
        schoolObj.is_finishing=False
        schoolObj.save()
    flag = schoolObj.is_finishing 
    return simplejson.dumps({'flag': flag})

@dajaxice_register
def change_project_overstatus(request, project_id, changed_overstatus):
    '''
    change project overstatus
    '''
    choices = dict(OVER_STATUS_CHOICES)
    if changed_overstatus in choices:
        project_obj = ProjectSingle.objects.get(project_id = project_id)
        try:
            project_obj.over_status = OverStatus.objects.get(status = changed_overstatus)
            project_obj.save()
        except:
            pass
        res = choices[changed_overstatus]
    else:
        res = "操作失败，请重试"
    return simplejson.dumps({'status':'1', 'res':res})

@dajaxice_register
def isover_control(request,pid):
    project=ProjectSingle.objects.get(project_id=pid)
    if project.is_over:
        project.is_over =False
    else:
        project.is_over = True
    project.save()
    return simplejson.dumps({"flag":project.is_over,"pid":pid})
