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
from adminStaff.models import ProjectPerLimits, ProjectControl, NoticeMessage
from django.shortcuts import render_to_response, render, get_object_or_404
from django.template import  RequestContext
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from const import *
from school.models import ProjectSingle, Project_Is_Assigned, Re_Project_Expert
from const.models import UserIdentity, InsituteCategory, ProjectGrade
from users.models import ExpertProfile
from registration.models import RegistrationProfile
from django.db import transaction
from const import MESSAGE_EXPERT_HEAD, MESSAGE_SCHOOL_HEAD ,MESSAGE_STUDENT_HEAD
from backend.decorators import *
from backend.logging import loginfo
from student.models import Student_Group

class AdminStaffService(object):
    @staticmethod
    def sendemail(request,username,password,email,identity, **kwargs):
        #判断用户名是否存在存在直接返回
        if not AdminStaffService.AuthUserExist(email, identity):
            if kwargs.has_key('school_name'):
                RegistrationManager().create_inactive_user(request,username,password,email,identity, school_name=kwargs['school_name'])
            elif kwargs.has_key('expert_user'):
                RegistrationManager().create_inactive_user(request,username,password,email,identity, expert_user=kwargs['expert_user'])
            elif kwargs.has_key('teacher_school'):
                RegistrationManager().create_inactive_user(request,username,password,email,identity, **kwargs)
            elif kwargs.has_key('student_user'):
                RegistrationManager().create_inactive_user(request,username,password,email,identity,**kwargs)
            return True
        else:
            return False

    @staticmethod
    def getUserInfoList(src):
        res_list = []
        for register in src:
            dict = {}
            #查询权限列表
            ##########################################################################
            auth_list = UserIdentity.objects.filter(auth_groups=register.userid).all()
            dict["auth"] = ''
            dict["email"] = register.userid.email or u"非邮箱注册"
            dict["is_active"] = register.userid.is_active
            for auth in auth_list:
                dict["auth"] += auth.__unicode__()+' '
            ##########################################################################
            res_list.append(dict)
        return res_list

    @staticmethod
    def GetRegisterListBySchool(school):
        '''
        获得对应`学院`的指导教师用户列表
        '''
        src=TeacherProfile.objects.filter(school = school.id)
        res_list = AdminStaffService.getUserInfoList(src)
        return res_list

    @staticmethod
    def GetRegisterExpertListBySchool(school):
        src = ExpertProfile.objects.filter(assigned_by_school = school)
        res_list = AdminStaffService.getUserInfoList(src)
        return res_list

    @staticmethod
    def GetRegisterList():
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
            dict["auth"] = ''
            dict["email"] = register.userid.email
            dict["is_active"] = register.userid.is_active
            for auth in auth_list:
                dict["auth"] += auth.__unicode__()+' '
            ##########################################################################
            res_list.append(dict)
        # 添加所有的评委用户
        for register in ExpertProfile.objects.all():
            dict = {}
            auth_list = UserIdentity.objects.filter(auth_groups=register.userid).all()
            dict["auth"] = ''
            dict["email"] = register.userid.email
            dict["is_active"] = register.userid.is_active
            for auth in auth_list:
                dict["auth"] += auth.__unicode__()+' '
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
            email_list  = AdminStaffService.GetRegisterList()
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
    def AuthUserExist(email, identity):
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
    def SubjectFeedback(request, is_expired=False):
        exist_message = ''
        readonly=is_expired
        subject_list =  AdminStaffService.GetSubject_list()
        if request.method == "GET":
            #subject_insitute_form = forms.SubjectInsituteForm()
            subject_insitute_form = forms.SchoolCategoryForm()
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
        if request.method == "GET":
            school_category_form = forms.SchoolCategoryForm()
            subject_list =  AdminStaffService.GetSubject_list()

        else:
            school_category_form = forms.SchoolCategoryForm(request.POST)
            if school_category_form.is_valid():
                school_name = school_category_form.cleaned_data["school_choice"]
                subject_list =  AdminStaffService.GetSubject_list(school=school_name)
        
        for subject in subject_list:
            student_group = Student_Group.objects.filter(project = subject)
            subject.members = ','.join([student.studentName for student in student_group])  

        return render_to_response("adminStaff/subject_rating.html",{'subject_list':subject_list,'school_category_form':school_category_form, 'subject_grade_form':subject_grade_form,'readonly':readonly},context_instance=RequestContext(request))
    @staticmethod
    def GetSubjectReviewList(project_id):
        review_obj_list = Re_Project_Expert.objects.filter(project=project_id).all()
        review_list = []
        for obj in review_obj_list:
            obj_list = [obj.comments, obj.score_significant, 
                        obj.score_value, obj.score_innovation, 
                        obj.score_practice, obj.score_achievement,
                        obj.score_capacity,]
            review_list.append(obj_list)
        return review_list

    @staticmethod
    def SubjectGradeChange(project_id, changed_grade):
        subject_obj = ProjectSingle.objects.get(project_id = project_id)
        subject_obj.project_grade = ProjectGrade.objects.get(grade=changed_grade)
        subject_obj.save()


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
            if rolemessage:
                _message = rolemessage + request.POST["message_content"] + "  " + datemessage
                message = NoticeMessage(noticemessage = _message)
                message.save()
        return render(request, "adminStaff/noticeMessageSettings.html")
