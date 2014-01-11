# coding: UTF-8
'''
Created on 2013-03-28

@author: sytmac
'''
# Create your views here.
import random
import re,sha
import uuid
from datetime import date
from django.http import HttpResponse, Http404
from registration.models import *
from adminStaff import forms
from adminStaff.models import ProjectPerLimits, ProjectControl, NoticeMessage, TemplateNoticeMessage
from django.shortcuts import render_to_response, render, get_object_or_404
from django.template import  RequestContext
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from const import *
from teacher.models import TeacherMonthComment
from student.models import  StudentWeeklySummary, Student_Group, Funds_Group
from school.models import ProjectSingle, Project_Is_Assigned, Re_Project_Expert,UploadedFiles
from const.models import UserIdentity, InsituteCategory, ProjectGrade
from users.models import ExpertProfile, AdminStaffProfile
from registration.models import RegistrationProfile
from django.db import transaction
from django.db.models import Q
from backend.decorators import *
from backend.logging import loginfo
from backend.fund import CFundManage
from news.models import News
from news.forms import NewsForm
from school.utility import check_project_is_assign, split_name
#liuzhuo add
import datetime
import os
import sys
import uuid

from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.shortcuts import render_to_response
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseForbidden, Http404, HttpResponseBadRequest
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators import csrf
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

from school.models import ProjectSingle, PreSubmit, FinalSubmit,TechCompetition
from school.models import UploadedFiles
from adminStaff.models import ProjectPerLimits
from users.models import StudentProfile
from school.forms import InfoForm, ApplicationReportForm, FinalReportForm,EnterpriseApplicationReportForm,TechCompetitionForm,Teacher_EnterpriseForm

from const.models import *
from const import *
from school.utility import *
from adminStaff.utility import *
from backend.logging import logger, loginfo
from backend.decorators import *
from student.models import Student_Group,StudentWeeklySummary,Funds_Group
from student.forms import StudentGroupForm, StudentGroupInfoForm,ProcessRecordForm

from django.core.files.uploadedfile import UploadedFile
from settings import IS_MINZU_SCHOOL, IS_DLUT_SCHOOL




class AdminStaffService(object):
    @staticmethod
    def sendemail(request,username,password,email,identity, **kwargs):
        #判断用户名是否存在存在直接返回
        #expert多重身份特殊处理
        if identity == "expert" and ExpertProfile.objects.filter(userid__email = email).count():
            expert_obj = ExpertProfile.objects.get(userid__email = email)
            if kwargs["expert_user"] == "assigned_by_school":
                if expert_obj.assigned_by_school: return False
                expert_obj.assigned_by_school = SchoolProfile.objects.get(userid = request.user)
                expert_obj.save()
                return True
            else:
                if expert_obj.assigned_by_adminstaff: return False
                expert_obj.assigned_by_adminstaff = AdminStaffProfile.objects.get(userid = request.user)
                expert_obj.save()
                return True

        if not AdminStaffService.AuthUserExist(email, identity, **kwargs):
            # if kwargs.has_key('school_name'):
            #     RegistrationManager().create_inactive_user(request,username,password,email,identity, **kwargs)
            # elif kwargs.has_key('expert_user'):
            #     RegistrationManager().create_inactive_user(request,username,password,email,identity,**kwargs)
            # elif kwargs.has_key('teacher_school'):
            RegistrationManager().create_inactive_user(request,username,password,email,identity,**kwargs)
            return True
        else:
            return False

    @staticmethod
    def filter_display(email, auth_list, host_email):
        """
        过滤所有dispatch页面中显示帐号与该管理员无关的身份权限
        """
        ret_list = []
        for auth in auth_list:
            if auth.identity == SCHOOL_USER:
                school = SchoolProfile.objects.filter(userid__email = email)
                if school.count(): school = school[0]
                else: continue
                if AdminStaffProfile.objects.filter(userid__email = host_email).count():
                    ret_list.append(auth)
            elif auth.identity == EXPERT_USER:
                expert = ExpertProfile.objects.filter(userid__email = email)
                if expert.count(): expert = expert[0]
                else: continue
                if (expert.assigned_by_school and expert.assigned_by_school.userid.email == host_email) \
                    or (expert.assigned_by_adminstaff and expert.assigned_by_adminstaff.userid.email == host_email):
                    ret_list.append(auth)
            elif auth.identity == TEACHER_USER:
                teacher = TeacherProfile.objects.filter(userid__email = email)
                if teacher.count(): teacher = teacher[0]
                else: continue
                if teacher.school.userid.email == host_email:
                    ret_list.append(auth)
            elif auth.identity == STUDENT_USER:
                student = StudentProfile.objects.filter(userid__email = email)
                if student.count(): student = student[0]
                else: continue
                if student.teacher.userid.email == host_email:
                    ret_list.append(auth)
        return ret_list

    @staticmethod
    def getUserInfoList(src, host_email):
        res_list = []
        for register in src:
            dict = {}
            #查询权限列表
            ##########################################################################
            auth_list = UserIdentity.objects.filter(auth_groups=register.userid).all()
            auth_list = AdminStaffService.filter_display(register.userid.email, auth_list, host_email)
            dict["name"] = register.get_name
            dict["email"] = register.userid.email or u"非邮箱注册"
            dict["is_active"] = register.userid.is_active
            dict["auth"] = []
            for auth in auth_list:
                dict["auth"].append(auth.__unicode__())

            dict["auth"] = u'、'.join(dict["auth"])
            ##########################################################################
            res_list.append(dict)
        return res_list

    @staticmethod
    def GetRegisterListBySchool(school):
        '''
        获得对应`学院`的指导教师用户列表
        '''
        src=TeacherProfile.objects.filter(school = school.id)
        res_list = AdminStaffService.getUserInfoList(src, school.userid.email)
        return res_list
    @staticmethod
    def GetRegisterListByTeacher(teacher):
        '''
        获得对应`学院`的指导教师用户列表
        '''
        src=StudentProfile.objects.filter(teacher = teacher.id)
        res_list = AdminStaffService.getUserInfoList(src, teacher.userid.email)
        return res_list

    @staticmethod
    def GetRegisterExpertListBySchool(school):
        src = ExpertProfile.objects.filter(assigned_by_school = school)
        res_list = AdminStaffService.getUserInfoList(src, school.userid.email)
        return res_list

    @staticmethod
    def GetRegisterList(request):
        '''
        获得学校及评委用户列表
        '''
        res_list = []
        auth_name = []
        # 添加所有的学校用户
        for register in SchoolProfile.objects.all():
            dict = {}
            #查询权限列表
            ##########################################################################
            auth_list = UserIdentity.objects.filter(auth_groups=register.userid).all()
            auth_list = AdminStaffService.filter_display(register.userid.email, auth_list, request.user.email)
            dict["email"] = register.userid.email
            dict["name"] = register.get_name
            dict["is_active"] = register.userid.is_active
            dict["auth"] = []
            for auth in auth_list:
                dict["auth"].append(auth.__unicode__())
            dict["auth"] = u'、'.join(dict["auth"])

            ##########################################################################
            res_list.append(dict)
        # 添加所有的校级评委用户
        for register in ExpertProfile.objects.filter(assigned_by_adminstaff__userid = request.user):
            dict = {}
            auth_list = UserIdentity.objects.filter(auth_groups=register.userid).all()
            auth_list = AdminStaffService.filter_display(register.userid.email, auth_list, request.user.email)
            dict["name"] = register.get_name
            dict["email"] = register.userid.email
            dict["is_active"] = register.userid.is_active
            dict["auth"] = []
            for auth in auth_list:
                dict["auth"].append(auth.__unicode__())
            dict["auth"] = u'、'.join(dict["auth"])
            res_list.append(dict)
        return res_list

    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def Dispatch(request):
        if request.method == "GET":
            expert_form = forms.ExpertDispatchForm()
            school_form = forms.SchoolDictDispatchForm()
            email_list  = AdminStaffService.GetRegisterList(request)
            def unique(lst):
                keys = {}
                for item in lst:
                    keys[item["email"]] = item
                return keys.values()
            email_list = unique(email_list)
            return render_to_response("adminStaff/dispatch.html",{'expert_form':expert_form,'school_form':school_form,'email_list':email_list},context_instance=RequestContext(request))
    @staticmethod
    def expertDispatch(request):
        if request.method == "POST":
            school_form = forms.SchoolDispatchForm()
            expert_form = forms.ExpertDispatchForm(request.POST)
            if expert_form.is_valid():
                #name = form.cleaned_data["expert_name"]
                password = expert_form.cleaned_data["expert_password"]
                email = expert_form.cleaned_data["expert_email"]
                name = email
                if password == "":
                    password = email.split('@')[0]
                AdminStaffService.sendemail(request, name, password, email, EXPERT_USER, expert_user=True)
                expert_form = forms.ExpertDispatchForm()
            return render_to_response("adminStaff/dispatch.html",{'expert_form':expert_form, 'school_form':school_form},context_instance=RequestContext(request))
    @staticmethod
    def schoolDispatch(request):
        if request.method == "POST":
            expert_form = forms.ExpertDispatchForm()
            school_form = forms.SchoolDispatchForm(request.POST)
            if school_form.is_valid():
                #name = form.cleaned_data["expert_name"]
                password = school_form.cleaned_data["school_password"]
                email = school_form.cleaned_data["school_email"]
                name = email
                if password == "":
                    password = email.split('@')[0]
                AdminStaffService.sendemail(request, name, password, email, SCHOOL_USER)
                school_form = forms.SchoolDispatchForm()
            return render_to_response("adminStaff/dispatch.html",{'expert_form':expert_form,'school_form':school_form},context_instance=RequestContext(request))
    @staticmethod
    def AuthUserExist(email, identity, **kwargs):
        if User.objects.filter(email=email).count():
            user_obj = User.objects.get(email=email)
            ui_obj = UserIdentity.objects.get(identity=identity)
            if ui_obj.auth_groups.filter(id=user_obj.id).count():
                return True
            else:
                return False
        else:
            return False
    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def AdminSetting(request):
        if request.method == "GET":
            timeform = forms.TimeSettingForm()
            num_limit_form = forms.NumLimitForm()
            return render_to_response("adminStaff/settings.html",{'time_form':timeform,'num_limit_form':num_limit_form},context_instance=RequestContext(request))

    @staticmethod
    @transaction.commit_on_success
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def DeadlineSetting(request):
        '''
        提交时间节点限制
        '''

        if request.method == "GET":
            if ProjectControl.objects.count() == 0:
                pc_obj =  ProjectControl(pre_start_day = date.today(),
                       pre_end_day   = date.today(),
                       pre_start_day_review = date.today(),
                       pre_end_day_review = date.today(),
                       final_start_day = date.today(),
                       final_end_day = date.today(),
                       final_start_day_review = date.today(),
                       final_end_day_review = date.today(),
                       )
                pc_obj.save()
            else:
                pc_obj = ProjectControl.objects.get()
            data = {
                    'pre_start_date' : pc_obj.pre_start_day,
                    'pre_end_date' : pc_obj.pre_end_day,
                    'pre_start_date_review' : pc_obj.pre_start_day_review,
                    'pre_end_date_review' : pc_obj.pre_end_day_review,
                    'final_start_date' : pc_obj.final_start_day,
                    'final_end_date' : pc_obj.final_end_day,
                    'final_start_date_review' : pc_obj.final_start_day_review,
                    'final_end_date_review' : pc_obj.final_end_day_review,
                    }
            timeform = forms.TimeSettingForm(initial=data)
            #num_limit_form = forms.NumLimitForm()
            return render_to_response("adminStaff/deadlineSettings.html",{'time_form':timeform},context_instance=RequestContext(request))
    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def ProjectLimitNumSetting(request):
        '''
        学校上传数量限制
        '''
        if request.method == "GET":
            #timeform = forms.TimeSettingForm()
            num_limit_form = forms.NumLimitForm()
            school_limit_num_list = AdminStaffService.SchoolLimitNumList()
            return render_to_response("adminStaff/projectlimitnumSettings.html",{'num_limit_form':num_limit_form,'school_limit_list':school_limit_num_list},context_instance=RequestContext(request))
    @staticmethod
    def SchoolLimitNumList():
        '''
        返回存在的每个学校限制数目列表
        '''
        limit_list = ProjectPerLimits.objects.all()
        return limit_list
    @staticmethod
    def GetSubject_list(school=None):
        subject_list = []
        if school == None:
            subject_list = ProjectSingle.objects.all()
        elif not school == None:
            subject_list = ProjectSingle.objects.filter(school=school)
        return subject_list
    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    @transaction.commit_on_success
    @time_controller(phase=STATUS_FINSUBMIT)
    def SubjectAlloc(request, is_expired=False):
        """
        手动指派项目
        """
        exist_message = ''
        readonly=is_expired
        subject_list = get_current_project_query_set().filter(recommend = True)
        #subject_list =  ProjectSingle.objects.filter(recommend = True)
        expert_list = ExpertProfile.objects.filter(assigned_by_adminstaff__userid = request.user)
        expert_list = get_alloced_num(expert_list, 1)

        if len(expert_list) == 0 or len(subject_list) == 0:
            if not expert_list :
                exist_message = '专家用户不存在或未激活，请确认已发送激活邮件并提醒专家激活'
            else:
                exist_message = '没有可分配的项目，无法进行指派'


        if request.method == "GET":
            subject_insitute_form = forms.SchoolCategoryForm()
            subject_insitute_form.fields['school_choice'].choices = subject_insitute_form.fields['school_choice'].choices[1:] #特殊处理：去除form中的“显示所有学部学院”选项
        else:
            subject_insitute_form = forms.SchoolCategoryForm(request.POST)
            subject_insitute_form.fields['school_choice'].choices = subject_insitute_form.fields['school_choice'].choices[1:] #特殊处理：去除form中的“显示所有学部学院”选项

            if subject_insitute_form.is_valid():
                school = subject_insitute_form.cleaned_data["school_choice"]
                subject_list =  ProjectSingle.objects.filter(Q(recommend = True) & Q(school__id = school))

        alloced_subject_list = [subject for subject in subject_list if check_project_is_assign(subject, True)]
        unalloced_subject_list = [subject for subject in subject_list if not check_project_is_assign(subject, True)] 
        context = {'subject_list': subject_list,
                   'alloced_subject_list': alloced_subject_list,
                   'unalloced_subject_list': unalloced_subject_list,
                   'expert_list': expert_list,
                   'subject_insitute_form': subject_insitute_form,
                   'exist_message': exist_message,
                   'readonly': readonly,}
        return render(request, "adminStaff/subject_alloc.html", context)


    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    @transaction.commit_on_success
    @time_controller(phase=STATUS_FINSUBMIT)
    def SubjectFeedback(request, is_expired=False):
        exist_message = ''
        readonly=is_expired
        subject_list =  AdminStaffService.GetSubject_list()
        if request.method == "GET":
            #subject_insitute_form = forms.SubjectInsituteForm()
            subject_insitute_form = forms.SchoolCategoryForm()
            subject_insitute_form.fields['school_choice'].choices = subject_insitute_form.fields['school_choice'].choices[1:] #特殊处理：去除form中的“显示所有学部学院”选项
        else:
            #subject_insitute_form = forms.SubjectInsituteForm(request.POST)
            subject_insitute_form = forms.SchoolCategoryForm(request.POST)
            if subject_insitute_form.is_valid():
                school = subject_insitute_form.cleaned_data["school_choice"]
                subject_list =  AdminStaffService.GetSubject_list(school=school)
                expert_school = SchoolProfile.objects.get(id=school)
                try:
                    obj = Project_Is_Assigned.objects.get(school = expert_school)
                    #如果已经指派专家了直接返回列表即可
                    if obj.is_assigned == 1:
                        pass
                    #没有指派专家，则进行专家指派
                    else:
                        #筛选专家列表
                        expert_list = ExpertProfile.objects.filter(assigned_by_adminstaff__userid = request.user)
                        #如果所属学科专家不存在，则进行提示
                        if len(expert_list) == 0 or len(subject_list) == 0:
                            if not expert_list :
                                exist_message = '专家用户不存在或未激活，请确认已发送激活邮件并提醒专家激活'
                            else:
                                exist_message = '没有可分配的项目，无法进行指派'

                        else:
                            re_dict = AdminStaffService.Assign_Expert_For_Subject(subject_list, expert_list)
                            #将返回数据进入Re_Project_Expert表中

                            for subject in re_dict.keys():
                                for expert in re_dict[subject]:
                                    loginfo(p = subject.project_id, label="subject.project_id: ")
                                    #subject.expert.add(expert)
                                    try:
                                        re_project_expert = Re_Project_Expert.objects.get(project_id=subject.project_id,
                                            expert_id=expert.id)
                                        re_project_expert.delete()
                                    except:
                                        pass
                                    finally:
                                        Re_Project_Expert(project_id=subject.project_id, expert_id=expert.id).save()
                            #保存已分配标志，值为1
                            obj.is_assigned = True
                            obj.save()
                except Project_Is_Assigned.DoesNotExist:
                    obj = None
        return render_to_response("adminStaff/subject_feedback.html",{'subject_list':subject_list,'subject_insitute_form':subject_insitute_form,'exist_message':exist_message,'readonly':readonly},context_instance=RequestContext(request))

    @staticmethod
    def Assign_Expert_For_Subject(subject_list, expert_list):
        ret = {}
        for i in xrange(len(subject_list)):
            subject = subject_list[i]
            num = min(len(expert_list), random.randint(3,5))
            ret[subject] = []
            for j in xrange(num):
                ret[subject].append(expert_list[(i + j) % len(expert_list)])
        return ret

    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    @time_controller(phase=STATUS_FINSUBMIT)
    def SubjectRating(request,is_expired=False):
        readonly=is_expired
        subject_grade_form = forms.SubjectGradeForm()
        subject_list = get_current_project_query_set()
        if request.method == "GET":
            school_category_form = forms.SchoolCategoryForm()
            page1 = request.GET.get('page1')
            if page1 == "None": page1 = None
            page2 = request.GET.get('page2')
            if page2 == "None": page2 = None
            school_name = request.GET.get('school_name')
            if school_name == "None": school_name = None

            if (not school_name) or int(school_name) == -1:
                subject_list =  subject_list.filter(recommend = True)
            else:
                subject_list = subject_list.filter(Q(recommend = True) & Q(school = SchoolProfile.objects.get(id = school_name)))
        else:
            school_category_form = forms.SchoolCategoryForm(request.POST)
            if school_category_form.is_valid():
                page1 = 1
                page2 = 1
                school_name = school_category_form.cleaned_data["school_choice"]
                if int(school_name) == -1:
                    subject_list = subject_list.filter(recommend = True)
                else:
                    subject_list = subject_list.filter(Q(recommend = True) & Q(school = SchoolProfile.objects.get(id = school_name)))

        for subject in subject_list:
            student_group = Student_Group.objects.filter(project = subject)
            try:
                subject.members = student_group[0]
            except:
                pass
        rec_subject_list = [subject for subject in subject_list if subject.project_grade.grade != GRADE_UN]
        rec = getContext(rec_subject_list, page1, 'subject', 0)
        nrec_subject_list = [subject for subject in subject_list if subject.project_grade.grade == GRADE_UN]
        nrec = getContext(nrec_subject_list, page2, 'subject', 0)
        context = {
            'page1': page1,
            'page2': page2,
            'rec': rec,
            'nrec': nrec,
            'school_category_form': school_category_form,
            'subject_grade_form': subject_grade_form,
            'school_name': school_name,
            'readonly': readonly,
            }
        return render(request, "adminStaff/subject_rating.html", context)

    @staticmethod
    def GetSubjectReviewList(project_id, identity):
        flag = (identity == 'adminStaff')
        review_obj_list = Re_Project_Expert.objects.filter(Q(project=project_id)&Q(is_assign_by_adminStaff=flag))
        review_list = []
        for obj in review_obj_list:
            obj_list = [obj.comments, obj.score_significant,
                        obj.score_value, obj.score_innovation,
                        obj.score_practice, obj.score_achievement,
                        obj.score_capacity,]
            obj_list.append(sum(map(float, obj_list[1:])))

            review_list.append(obj_list)
        return review_list

    @staticmethod
    def SubjectGradeChange(project_id, changed_grade):
        subject_obj = ProjectSingle.objects.get(project_id = project_id)
        try:
            subject_obj.project_grade = ProjectGrade.objects.get(grade=changed_grade)
            subject_obj.save()
        except:
            pass

    @staticmethod
    def ProjectOverStatusChange(project_id, changed_overstatus):
        project_obj = ProjectSingle.objects.get(project_id = project_id)
        try:
            project_obj.over_status = OverStatus.objects.get(status = changed_overstatus)
            project_obj.save()
        except:
            pass
        # subject_obj.project_grade = ProjectGrade.objects.get(grade=changed_grade)
        # subject_obj.save()
    @staticmethod
    def ProjectUniqueCodeChange(project_id, project_unique_code):
        project_obj = ProjectSingle.objects.get(project_id = project_id)
        loginfo(project_obj)
        try:
            project_obj.project_unique_code = project_unique_code
            project_obj.save()
            if len(project_unique_code.strip()) == 0:
               project_unique_code = "无"
        except:
            project_unique_code = "操作失败，请重试"
        return project_unique_code
    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def NoticeMessageSetting(request):
        if request.POST.get("message_content", False):
            datemessage = ""
            if request.POST.get('message_checkbox', False):
                datemessage = "1"
            else:
                datemessage = "0"
            # TODO: 前台控制角色选择验证
            if request.POST["message_role"] == '1':
                rolemessage = MESSAGE_EXPERT_HEAD
            elif request.POST["message_role"] == '2':
                rolemessage = MESSAGE_SCHOOL_HEAD
            elif request.POST["message_role"] == '3':
                rolemessage = MESSAGE_STUDENT_HEAD
            elif request.POST["message_role"] == '4':
                rolemessage = MESSAGE_TEACHER_HEAD
            elif request.POST["message_role"] == '5':
                rolemessage = MESSAGE_ALL_HEAD
            if rolemessage:
                _message = rolemessage + request.POST["message_content"] + "  " + datemessage
                message = NoticeMessage(noticemessage = _message)
                message.save()
        templatenotice_group_form = forms.TemplateNoticeForm()
        templatenotice_group = TemplateNoticeMessage.objects.all()
        _range = 1
        for i in templatenotice_group:
            i.iid = _range
            _range += 1
        return render(request, "adminStaff/noticeMessageSettings.html",
                      {"templatenotice_group": templatenotice_group,
                     "templatenotice_group_form": templatenotice_group_form})
    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def project_control(request):
        adminStaff = AdminStaffProfile.objects.get(userid = request.user)
        is_finishing = adminStaff.is_finishing
        # pro_list=ProjectSingle.objects.filter(Q(project_grade=1)|Q(project_grade=2))
        pro_list = ProjectSingle.objects.filter(over_status__status=OVER_STATUS_NOTOVER)
        year_list=[]
        for pro_obj in pro_list :
            if pro_obj.year not in year_list :
                year_list.append(pro_obj.year)
        if year_list:
            havedata_p = True
        else:
            havedata_p = False

        recommend_rate_obj = SchoolRecommendRate.load()

        return render(request, "adminStaff/project_control.html",
                    {
                        "recommend_rate": recommend_rate_obj,
                        "is_finishing":is_finishing,
                        "year_list":year_list,
                        "havedata_p":havedata_p,
                    })

    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def project_informationexport(request):
        return render(request, "adminStaff/project_informationexport.html",
                    {

                    })

    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def funds_manage(request,is_expired=False):
        context = AdminStaffService.projectListInfor(request)
        return render_to_response("adminStaff/funds_manage.html",context,context_instance=RequestContext(request))

    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def funds_change(request,pid):
        project = ProjectSingle.objects.get(project_id = pid)
        ret = CFundManage.get_form_tabledata(project)
        return render(request,"adminStaff/funds_change.html",ret)

    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def home_view(request):
        context = AdminStaffService.projectListInfor(request)
        for pro_obj in context["pro_list"]:
            if len(pro_obj.project_unique_code.strip()) == 0:
                pro_obj.project_unique_code = "无"
                add_fileurl(pro_obj)

        context["IS_MINZU_SCHOOL"] = IS_MINZU_SCHOOL
        context["IS_DLUT_SCHOOL"] = IS_DLUT_SCHOOL
        return render(request, "adminStaff/adminstaff_home.html",context)
    @staticmethod
    @csrf.csrf_protect
    def projectListInfor(request,auth_identity = ADMINSTAFF_USER):
        """
        默认只显示省级和国家级项目
        """
        if request.method =="POST":
            project_manage_form = forms.ProjectManageForm(request.POST)
            pro_list = AdminStaffService.projectFilterList(request,project_manage_form)
        else:
            project_manage_form = forms.ProjectManageForm()
            over_notover_status = OverStatus.objects.get(status=OVER_STATUS_NOTOVER)
            grade_nation = ProjectGrade.objects.get(grade=GRADE_NATION)
            grade_province = ProjectGrade.objects.get(grade=GRADE_PROVINCE)
            if auth_identity == ADMINSTAFF_USER:
                pro_list=ProjectSingle.objects.filter((Q(project_grade=grade_nation)|Q(project_grade=grade_province)) & \
                                                      Q(over_status__status = OVER_STATUS_NOTOVER))
            elif auth_identity == SCHOOL_USER:
                pro_list = ProjectSingle.objects.filter(Q(school__userid=request.user)& \
                                                        Q(over_status__status = OVER_STATUS_NOTOVER))
            elif auth_identity == TEACHER_USER:
                pro_list = ProjectSingle.objects.filter(Q(adminuser__userid=request.user) & \
                                                        Q(over_status__status = OVER_STATUS_NOTOVER))
            elif auth_identity == EXPERT_USER:
                pro_list = ProjectSingle.objects.filter(Q(expert__userid=request.user) &\
                                                        Q(over_status__status = OVER_STATUS_NOTOVER))
        pro_list = pro_list.order_by('adminuser')
        loginfo(p=pro_list,label="pro_list")
        if pro_list.count() != 0 or request.method == "POST":
            havedata_p = True
        else: havedata_p = False
        context = {
                    'havedata_p': havedata_p,
                    'pro_list': pro_list,
                    'project_manage_form':project_manage_form
                  }
        return context
    @staticmethod
    @csrf.csrf_protect
    def projectFilterList(request,project_manage_form):
        if project_manage_form.is_valid():
            project_grade = project_manage_form.cleaned_data["project_grade"]
            project_year =  project_manage_form.cleaned_data["project_year"]
            project_overstatus = project_manage_form.cleaned_data["project_overstatus"]
            project_scoreapplication = project_manage_form.cleaned_data["project_scoreapplication"]
            project_school = project_manage_form.cleaned_data["project_school"]
            # qset = AdminStaffService.get_filter(project_grade,project_year,project_isover,project_scoreapplication)
            qset = AdminStaffService.get_filter(project_grade,project_year,project_overstatus,project_scoreapplication,project_school)
            if qset :
                qset = reduce(lambda x, y: x & y, qset)
                # if project_grade == "-1" and project_scoreapplication == "-1":
                #     pro_list = ProjectSingle.objects.filter(qset).exclude(Q(project_grade__grade=GRADE_INSITUTE) or Q(project_grade__grade=GRADE_SCHOOL) or Q(project_grade__grade=GRADE_UN))
                # else:
                pro_list = ProjectSingle.objects.filter(qset)
            else:
                pro_list = ProjectSingle.objects.all()
        loginfo(p=qset,label="qset")
        return pro_list

    ##
    # TODO: fixed the `isover` to over status
    @staticmethod
    def get_filter(project_grade,project_year,project_overstatus, project_scoreapplication,project_school):
        if project_grade == "-1":
            project_grade=''
        if project_year == '-1':
            project_year=''
        # if project_isover == '-1':
        #     project_isover=''
        if project_overstatus == '-1':
            project_overstatus=''
        if project_scoreapplication == '-1':
            project_scoreapplication=''
        if project_school  == '-1':
            project_school = '';
        q1 = (project_year and Q(year=project_year)) or None
        # q2 = (project_isover and Q(is_over=project_isover)) or None
        q2 = (project_overstatus and Q(over_status__status=project_overstatus)) or None
        q3 = (project_grade and Q(project_grade__grade=project_grade)) or None
        q4 = (project_scoreapplication and Q(score_application=project_scoreapplication)) or None
        q5 = (project_school and Q(school_id = project_school)) or None
        qset = filter(lambda x: x != None, [q1, q2, q3,q4,q5])
        return qset

    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def processrecord(request):
        """
        process record view
        """
        """
        默认只显示省级和国家级项目
        """
        context = AdminStaffService.projectListInfor(request)
        return render(request, "adminStaff/project_processrecord.html",context)
    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def record_view(request, pid):
        loginfo("record_view")
        comment_group       = TeacherMonthComment.objects.filter(project_id=pid).order_by("monthId")
        record_group        = StudentWeeklySummary.objects.filter(project=pid).order_by("weekId")
        data = {"record_group"  : record_group,
                "comment_group" : comment_group,
                }
        return render(request, 'adminStaff/processrecord.html',data)

    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def ProjectLimitNumReset(request):
        num_limit_form = forms.NumLimitForm()
        school_limit_num_list = AdminStaffService.SchoolLimitNumList()
        TeacherProjectPerLimits.objects.all().delete()
        ProjectPerLimits.objects.all().delete()
        for p in ProjectSingle.objects.filter(is_past=False):
            p.is_past = True
            p.save()
        return render_to_response("adminStaff/projectlimitnumSettings.html",{'num_limit_form':num_limit_form,'school_limit_list':school_limit_num_list},context_instance=RequestContext(request))

    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def NewsRelease(request):
        news_list = News.objects.all().order_by("-news_date")
        page = request.GET.get('page')
        if request.method == 'POST':
            newsform = NewsForm(request.POST, request.FILES)
            if newsform.is_valid():
                new_news = News(news_title = newsform.cleaned_data["news_title"],
                                news_content = newsform.cleaned_data["news_content"],
                                news_date = newsform.cleaned_data["news_date"],
                                news_category = NewsCategory.objects.get(id=newsform.cleaned_data["news_category"]),
                                news_document = request.FILES.get("news_document", None),)
                new_news.save()
                return redirect('/newslist/%s' % new_news.id)
            else:
                loginfo(p=newsform.errors.keys(), label="news form error")
                context = getContext(news_list, page, 'news', 0)
                context.update({"newsform": NewsForm()})
                return render(request, "adminStaff/news_release.html", context)
        else:
            context = getContext(news_list, page, 'news', 0)
            context.update({"newsform": NewsForm()})
            return render(request, "adminStaff/news_release.html", context)

    #liuzhuo write
    # @csrf.csrf_protect
    # @login_required
    # @authority_required(ADMINSTAFF_USER)
    # def showProject(request, pid):

        # return render(request,"adminStaff/project_view.html", None)


    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def application_report_view(request, pid=None):
        
        """
            readonly determined by time
            is_show determined by identity
            is_innovation determined by project_category
        """        

        is_expired=False
        loginfo(p=pid+str(is_expired), label="in application")
        project = get_object_or_404(ProjectSingle, project_id=pid) 
        is_currentyear = check_year(project)
        is_applying = check_applycontrol(project)
        #readonly= is_expired or (not is_currentyear) or (not is_applying)
        
        readonly = False
        is_show =  check_auth(user=request.user,authority=STUDENT_USER)

        if project.project_category.category == CATE_INNOVATION:
            iform = ApplicationReportForm
            pre = get_object_or_404(PreSubmit, project_id=pid)
            teacher_enterprise=None
            is_innovation = True
        else:
            iform = EnterpriseApplicationReportForm
            pre = get_object_or_404(PreSubmitEnterprise, project_id=pid)
            teacher_enterprise = get_object_or_404(Teacher_Enterprise,id=pre.enterpriseTeacher_id)
            is_innovation = False

        teacher_enterpriseform=Teacher_EnterpriseForm(instance=teacher_enterprise)
        if request.method == "POST" and readonly is not True:
            info_form = InfoForm(request.POST,pid=pid,instance=project)
            application_form = iform(request.POST, instance=pre)
            if is_innovation == True:
                if info_form.is_valid() and application_form.is_valid():
                    if save_application(project, pre, info_form, application_form, request.user):
                        project.project_status = ProjectStatus.objects.get(status=STATUS_PRESUBMIT)
                        project.save()
                else:
                    pass
                    # logger.info(" info  application Form Valid Failed"+"**"*10)
                    # logger.info(info_form.errors)
                    # logger.info(application_form.errors)
                    # logger.info("--"*10)
            else :
                teacher_enterpriseform=Teacher_EnterpriseForm(request.POST,instance=teacher_enterprise)
                if info_form.is_valid() and application_form.is_valid() and teacher_enterpriseform.is_valid():
                    if save_enterpriseapplication(project, pre, info_form, application_form, teacher_enterpriseform,request.user):
                        project.project_status = ProjectStatus.objects.get(status=STATUS_PRESUBMIT)
                        project.save()
                else:
                    pass                    
                    # logger.info("info  application teacher Form Valid Failed"+"**"*10)
                    # logger.info(info_form.errors)
                    # logger.info(application_form.errors)
                    # logger.info(teacher_enterpriseform.errors)
                    # logger.info("--"*10)
        else:
            info_form = InfoForm(instance=project,pid=pid)
            application_form = iform(instance=pre)
            # teacher_enterpriseform=Teacher_EnterpriseForm(instance=teacher_enterprise)
        data = {'pid': pid,
                'info': info_form,
                'application': application_form,
                'teacher_enterpriseform':teacher_enterpriseform,
                'readonly': readonly,
                'is_innovation':is_innovation,
                'is_show':is_show,
                }
        return render(request, 'adminStaff/application.html', data)

    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def final_report_view(request, pid=None,is_expired=False):
        """
        student final report
        Arguments:
            In: id, it is project id
        """
        loginfo(p=pid+str(is_expired), label="in application")
        final = get_object_or_404(FinalSubmit, project_id=pid)
        project = get_object_or_404(ProjectSingle, project_id=pid)
        #techcompetition=get_object_or_404(TechCompetition,project_id=final.content_id)
        is_finishing = check_finishingyear(project)
        over_status = project.over_status

        # readonly = (over_status != OVER_STATUS_NOTOVER) or not is_finishing

        
        readonly = False

        if request.method == "POST" and readonly is not True:
            final_form = FinalReportForm(request.POST, instance=final)
            # techcompetition_form =
            if final_form.is_valid():
                final_form.save()
                project.project_status = ProjectStatus.objects.get(status=STATUS_FINSUBMIT)
                project.save()
                #return HttpResponseRedirect(reverse('student.views.home_view'))
            else:
                pass            
                # logger.info("Final Form Valid Failed"+"**"*10)
                # logger.info(final_form.errors)
                # logger.info("--"*10)
        final_form = FinalReportForm(instance=final)
        #techcompetition_form = TechCompetitionForm(instance=techcompetition)

        data = {'pid': pid,
                'final': final_form,
              #   'techcompetition':techcompetition,
                'readonly':readonly,
                }
        return render(request, 'adminStaff/final.html', data)


    @staticmethod
    @csrf.csrf_protect
    #@login_required
    #@authority_required(ADMINSTAFF_USER)    
    def member_change(request, pid):
        """
        project group member change
		"""
        # student_account = StudentProfile.objects.get(userid = request.user)
        project = ProjectSingle.objects.get(project_id = pid)

        

        # isIN =  get_schooluser_project_modify_status(project)
        student_group = Student_Group.objects.filter(project = project)
        

        for s in student_group:
            s.sex = s.get_sex_display()
            student_group_form = StudentGroupForm()
            student_group_info_form = StudentGroupInfoForm()

        student_group_form = StudentGroupForm()
        student_group_info_form = StudentGroupInfoForm()




        readonly = False
        return render(request, "adminStaff/member_change.html",
                      {"pid": pid,
                       "student_group": student_group,
                       "student_group_form": student_group_form,
                       "student_group_info_form": student_group_info_form,
                       'readonly': readonly,
                       })
    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def get_xls_path(request,exceltype):
        if exceltype == EXCEL_TYPE_BASEINFORMATION:
            file_path = info_xls_baseinformation(request)
        elif exceltype == EXCEL_TYPE_APPLICATIONSCORE:
            file_path = info_xls_expertscore(request)
        elif exceltype == EXCEL_TYPE_SUMMARYSHEET_INNOVATE:
            file_path = info_xls_summaryinnovate(request)
        elif exceltype == EXCEL_TYPE_SUMMARYSHEET_ENTREPRENEUSHIP:
            file_path = info_xls_summaryentrepreneuship(request)
        return MEDIA_URL + "tmp" + file_path[len(TMP_FILES_PATH):]

    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def homepage_import_view(request):
        """
        project group member change
        """
        if request.method == "POST":
            try:
                f = request.FILES["file"]
                wrapper_f = UploadedFile(f)
                size = wrapper_f.file.size
                name, filetype = split_name(wrapper_f.name)

                new_pic = HomePagePic()
                name, filetype = split_name(wrapper_f.name)
                new_pic.pic_obj = f
                new_pic.name = name
                new_pic.file_type = filetype
                new_pic.file_type = filetype if filetype != " " else "unknown"
                new_pic.uploadtime = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
                new_pic.file_size = size
                new_pic.save()
            except:
                pass

        file_history = HomePagePic.objects.all()
        data = {'files': file_history,
        }
        return render(request, 'adminStaff/homepage_pic_import.html', data)
