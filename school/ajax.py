#!/usr/bin/python
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-09-13 13:19
# Last modified: 2016-09-13 16:17
# Filename: ajax.py
# Description:
# coding: UTF-8
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
from school.forms import TeacherNumLimitForm, UsersForm, SubjectGradeForm
from school.models import Project_Is_Assigned, InsituteCategory, TeacherProjectPerLimits,ProjectFinishControl,ProjectSingle, Re_Project_Expert, AchievementObjects, ProjectSingle
from school.views import get_project_num_and_remaining, teacherLimitNumList
from backend.logging import logger, loginfo
from django.db.models import Q
from school.utility import *
from backend.decorators import *
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
        person_name = expert_form.cleaned_data["expert_personname"]
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

        if form.cleaned_data['teacher_name'] == '-1': #特殊处理所有指导教师的批量处理问题
            limited_num = form.cleaned_data['limited_num']
            num_and_remaining = get_project_num_and_remaining(request)
            test_sum = 0
            
            for teacher in TeacherProfile.objects.filter(school__userid = request.user):
                if TeacherProjectPerLimits.objects.filter(teacher = teacher).count() == 0:
                    test_sum += limited_num
                else:
                    minnum = ProjectSingle.objects.filter(Q(adminuser = teacher) & Q(is_past = False)).count()
                    test_sum += max(minnum, limited_num)
            if test_sum > num_and_remaining['projects_remaining']:
                return simplejson.dumps({'id': 'limited_num', 'message': u"分配数量剩余不足"})
            for teacher in TeacherProfile.objects.filter(school__userid = request.user):
                if TeacherProjectPerLimits.objects.filter(teacher = teacher).count() == 0:
                    projLimit_obj = TeacherProjectPerLimits(teacher = teacher, number = limited_num)
                    projLimit_obj.save()
                else:
                    projLimit_obj = TeacherProjectPerLimits.objects.get(teacher = teacher)
                    minnum = ProjectSingle.objects.filter(Q(adminuser = teacher) & Q(is_past = False)).count()
                    projLimit_obj.number = max(minnum, limited_num)
                    projLimit_obj.save()
            table = refresh_numlimit_table(request)
            projects_remaining = get_project_num_and_remaining(request)['projects_remaining']
            return simplejson.dumps({'message': "批量更新成功", 'status': "1", "table": table, 'projects_remaining': projects_remaining})
            
        teacher_obj = TeacherProfile.objects.get(id=form.cleaned_data["teacher_name"])
        limited_num = form.cleaned_data["limited_num"]
        num_and_remaining = get_project_num_and_remaining(request)
        # if num_and_remaining['projects_remaining'] < limited_num:
        #     return simplejson.dumps({'id':"limited_num" ,'message':u'分配数量不能大于剩余数量'})
        try:
            if  TeacherProjectPerLimits.objects.filter(teacher=teacher_obj).count() == 0:
                if num_and_remaining['projects_remaining'] < limited_num:
                    return simplejson.dumps({'id':"limited_num" ,'message':u'分配数量剩余不足'})

                projLimit_obj = TeacherProjectPerLimits(teacher=teacher_obj,
                                                       number=limited_num)
                projLimit_obj.save()
            else:
                projLimit_obj = TeacherProjectPerLimits.objects.get(teacher=teacher_obj)
                if num_and_remaining['projects_remaining']+projLimit_obj.number < limited_num:
                    return simplejson.dumps({'id':"limited_num" ,'message':u'分配数量剩余不足'})
                minnum = ProjectSingle.objects.filter(Q(adminuser=teacher_obj)&Q(is_past=False)).count()
                if limited_num < minnum:
                    return simplejson.dumps({'message':u'更新失败,数量不得少于该老师已开始项目数量',})
                projLimit_obj.number = limited_num
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
def Alloc_Project_to_Expert(request, expert_list, project_list):
    flag = check_auth(user = request.user, authority = ADMINSTAFF_USER)
    message = ''

    if len(expert_list) == 0:
        message = 'no expert input'
    if len(project_list) == 0:
        message = 'no project input'
    for project_id in project_list:
        project = get_object_or_404(ProjectSingle, project_id = project_id)
        for expert_id in expert_list:
            expert = ExpertProfile.objects.get(userid__id = expert_id)
            try:
                re_project_expert = Re_Project_Expert.objects.get(project = project, expert = expert, is_assign_by_adminStaff = flag)
                re_project_expert.delete()
            except Exception, e:
                loginfo(e)
                pass
            finally:
                re = Re_Project_Expert.objects.create(project = project, expert = expert, is_assign_by_adminStaff = flag)
                re.save()
                if flag:
                    project.project_status = ProjectStatus.objects.get(status=STATUS_FINREVIEW)
                    project.save()
                else:
                    project.project_status = ProjectStatus.objects.get(status=STATUS_PREREVIEW)
                    project.save()
                    
    if flag:
        expert_list = ExpertProfile.objects.filter(assigned_by_adminstaff__userid = request.user)
    else:
        expert_list = ExpertProfile.objects.filter(assigned_by_school__userid = request.user)
    expert_list = get_alloced_num(expert_list, flag)
    expert_list_html = render_to_string('adminStaff/widgets/expert_list.html', {'expert_list':expert_list})
    return simplejson.dumps({'message': message, 'expert_list_html': expert_list_html})

@dajaxice_register
def Query_Alloced_Expert(request, project_id):
    flag = check_auth(user = request.user, authority = ADMINSTAFF_USER)
    message = ''

    project = get_object_or_404(ProjectSingle, project_id = project_id)
    expert_list = [item.expert for item in Re_Project_Expert.objects.filter(Q(project = project) & Q(is_assign_by_adminStaff = flag))]

    expert_list_html = ''
    for expert in expert_list:
        expert_list_html += r'<p>' + expert.__str__() + r'</p>'

    return simplejson.dumps({'message': message, 'expert_list_html': expert_list_html})

@dajaxice_register
def Cancel_Alloced_Experts(request, project_list):
    flag = check_auth(user = request.user, authority = ADMINSTAFF_USER)
    message = ''

    if len(project_list) == 0:
        message = 'no project input'
    for project_id in project_list:
        project = get_object_or_404(ProjectSingle, project_id = project_id)
        for re_project_expert in Re_Project_Expert.objects.filter(Q(project = project) & Q(is_assign_by_adminStaff = flag)):
            re_project_expert.delete()
    if flag:
        expert_list = ExpertProfile.objects.filter(assigned_by_adminstaff__userid = request.user)
    else:
        expert_list = ExpertProfile.objects.filter(assigned_by_school__userid = request.user)
    expert_list = get_alloced_num(expert_list, flag)
    expert_list_html = render_to_string('adminStaff/widgets/expert_list.html', {'expert_list':expert_list})
    return simplejson.dumps({'message': message, 'expert_list_html': expert_list_html})

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
        person_name = teacher_form.cleaned_data["teacher_personname"]
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
    year_finishing_list = []
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

            projectfinish = ProjectFinishControl.objects.filter(userid =user.id)
            for finishtemp in projectfinish :
                if finishtemp.project_year not in year_finishing_list:
                    year_finishing_list.append(finishtemp.project_year)
            year_finishing_list = sorted(year_finishing_list)
        else:
            return simplejson.dumps({'flag':None,'message':u"项目年份未选择或是没有未结题项目"}) 
    else:
        projectcontrol_list=ProjectFinishControl.objects.filter(userid=user)
        projectcontrol_list.delete()
        schoolObj.is_finishing=False
        schoolObj.save()
    flag = schoolObj.is_finishing 
    return simplejson.dumps({'flag': flag,'year_finishing_list':year_finishing_list})

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


@dajaxice_register
def achievement_save(request, project_id, values, category):
    context = {}
    project = get_object_or_404(ProjectSingle, project_id = project_id)
    is_finishing = check_finishingyear(project)
    readonly = project.over_status.status != OVER_STATUS_NOTOVER or not is_finishing
    if readonly:
        return HttpResponse("readonly")
    ao = AchievementObjects(project_id=project, title=values[0], member=values[1],
                            addition1=values[2], addition2=values[3],
                            category=int(category))
    ao.save()
    related_ao = AchievementObjects.objects.filter(project_id=project)
    context['objects']=related_ao.filter(category=ACHIEVEMENT_CATEGORY_OBJECT)
    context['papers']=related_ao.filter(category=ACHIEVEMENT_CATEGORY_PAPER)
    context['patents']=related_ao.filter(category=ACHIEVEMENT_CATEGORY_PATENT)
    context['competitions']=related_ao.filter(category=ACHIEVEMENT_CATEGORY_COMPETITION)
    return render_to_string("student/widgets/achievements.html", context)


@dajaxice_register
def achievement_delete(request, project_id, id):
    context = {}
    project = get_object_or_404(ProjectSingle, project_id=project_id)
    is_finishing = check_finishingyear(project)
    readonly = project.over_status.status != OVER_STATUS_NOTOVER or not is_finishing
    if readonly:
        return HttpResponse("readonly")
    ao = get_object_or_404(AchievementObjects, id=id)
    ao.delete()
    related_ao = AchievementObjects.objects.filter(project_id=project)
    context['objects']=related_ao.filter(category=ACHIEVEMENT_CATEGORY_OBJECT)
    context['papers']=related_ao.filter(category=ACHIEVEMENT_CATEGORY_PAPER)
    context['patents']=related_ao.filter(category=ACHIEVEMENT_CATEGORY_PATENT)
    context['competitions']=related_ao.filter(category=ACHIEVEMENT_CATEGORY_COMPETITION)
    return render_to_string("student/widgets/achievements.html", context)


@time_controller(phase=STATUS_FINSUBMIT)
@dajaxice_register
def search_project_in_rating(request, form_data, is_expired=False):
    readonly = is_expired
    form = UsersForm(deserialize_form(form_data))
    if not form.is_valid():
        return HttpResponse('404')
    name = form.cleaned_data['teacher_student_name']
    school = SchoolProfile.objects.get(userid=request.user)
    subject_grade_form = SubjectGradeForm()
    users_search_form = UsersForm()
    try:
        subject_list = get_current_project_query_set().filter(Q(student__name=name)|Q(adminuser__name=name))
    except:
        return HttpResponse("404")
    if not len(subject_list):
        return HttpResponse('404')

    limit, remaining = get_recommend_limit(school)
    for subject in subject_list:
        try:
            subject.members = get_manager(subject)
        except:
            pass
    undef_subject_list = filter(lambda x: (not x.recommend) and (x.project_grade.grade == GRADE_UN), subject_list)
    def_subject_list = filter(lambda x: (x.recommend) or (x.project_grade.grade != GRADE_UN), subject_list)
    

    context = {'subject_list': subject_list,
               'undef_subject_list': undef_subject_list,
               'def_subject_list': def_subject_list,
               'subject_grade_form': subject_grade_form,
               'readonly': readonly,
               'limit': limit,
               'remaining': remaining,
               'is_minzu_school': IS_MINZU_SCHOOL,
               'search_form': users_search_form,
                }
    return render_to_string('school/rating_project_table.html', context)
