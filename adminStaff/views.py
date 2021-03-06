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
from django.utils import timezone
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
from const.models import UserIdentity, InsituteCategory, ProjectGrade, ProjectCategory, ApplyControl
from users.models import ExpertProfile, AdminStaffProfile
from registration.models import RegistrationProfile
from django.db import transaction
from django.db.models import Q
from backend.decorators import *
from backend.logging import loginfo
from backend.fund import CFundManage
from news.models import News
from news.forms import NewsForm
from school.utility import (
    check_project_is_assign, split_name, get_manager,
    get_yearlist_forform, get_yearlist)
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
from adminStaff.forms import Sync_form

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

from student.views import application_report_view_work, final_report_view_work,files_upload_view_work
from student.views import open_report_view_work, mid_report_view_work

class AdminStaffService(object):
    @staticmethod
    def sendemail(request, username, password, email, identity, **kwargs):
        #判断用户名是否存在存在直接返回

        #expert多重身份特殊处理
        if (identity == "expert"
                and ExpertProfile.objects.filter(userid__email=email).count()):
            expert_obj = ExpertProfile.objects.get(userid__email = email)
            if kwargs["expert_user"] == "assigned_by_school":
                if expert_obj.assigned_by_school:
                    return False
                expert_obj.assigned_by_school = SchoolProfile.objects.get(
                    userid=request.user)
                expert_obj.save()
                return True
            else:
                if expert_obj.assigned_by_adminstaff:
                    return False
                expert_obj.assigned_by_adminstaff = AdminStaffProfile.objects.get(userid=request.user)
                expert_obj.save()
                return True

        if not AdminStaffService.AuthUserExist(username, identity, **kwargs):
            RegistrationManager().create_inactive_user(
                request, username, password, email, identity, **kwargs)
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
            dict['titles'] = u'专家,无职称'
            if isinstance(register, TeacherProfile):
                dict["titles"] = register.titles
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
        获得对应`教师`的指导学生用户列表
        '''
        src=StudentProfile.objects.filter(teacher = teacher.id,projectsingle__is_past = False)
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
            # expert_form = forms.ExpertDispatchForm()
            school_form = forms.SchoolDictDispatchForm()
            email_list = AdminStaffService.GetRegisterList(request)
            def unique(lst):
                keys = {}
                for item in lst:
                    keys[item["email"]] = item
                return keys.values()
            email_list = unique(email_list)
            return render_to_response(
                "adminStaff/dispatch.html",{
                    # 'expert_form': expert_form,
                    'school_form': school_form,
                    'email_list': email_list},
                context_instance=RequestContext(request))
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
    def AuthUserExist(username, identity, **kwargs):
        user = User.objects.filter(username=username)
        if user:
            user = user[0]
            ui_obj = UserIdentity.objects.get(identity=identity)
            if ui_obj.auth_groups.filter(id=user.id).count():
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
        subject_list = get_current_project_query_set().order_by("project_unique_code")
        if request.method == "GET":
            school_category_form = forms.SchoolCategoryForm()
            tab=request.GET.get("tab", "None")
            if tab == "None": tab = "nrec"
            page1 = request.GET.get('page1')
            if page1 == "None": page1 = None
            page2 = request.GET.get('page2')
            if page2 == "None": page2 = None
            school_name = request.GET.get('school_name')
            if school_name == "None": school_name = None

            if school_name and int(school_name) != -1:
                subject_list = subject_list.filter(Q(school=SchoolProfile.objects.get(id = school_name)))
        else:
            page1 = 1
            page2 = 1
            tab="nrec"
            school_name = None
            school_category_form = forms.SchoolCategoryForm(request.POST)
            if school_category_form.is_valid():
                school_name = school_category_form.cleaned_data["school_choice"]
                if int(school_name) != -1:
                    subject_list = subject_list.filter(Q(school = SchoolProfile.objects.get(id = school_name)))
            name = request.POST.get('search_info_input',None)
            if name:
                subject_list = subject_list.filter(Q(adminuser__name = name))

        for subject in subject_list:
            student_group = Student_Group.objects.filter(project = subject)
            try:
                subject.members = get_manager(subject)
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
			'tab': tab,
            }
        return render(request, "adminStaff/subject_rating.html", context)

    @staticmethod
    def GetSubjectReviewList(project_id, identity):
        class ReviewItem(list):
            def __init__(self, review_list, name, comments):
                super(ReviewItem, self).__init__()
                self.name = name
                self.comments = comments
                self.extend(review_list)

        flag = (identity == ADMINSTAFF_USER)
        review_obj_list = Re_Project_Expert.objects.filter(Q(project=project_id)&Q(is_assign_by_adminStaff=flag))
        review_list = []
        for obj in review_obj_list:
            obj_list = [obj.score_significant,
                        obj.score_value, obj.score_innovation,
                        obj.score_practice, obj.score_achievement,
                        obj.score_capacity,]
            obj_list.append(sum(map(float, obj_list)))
            review_obj = ReviewItem(obj_list, obj.expert.name, obj.comments)
            review_list.append(review_obj)
        return review_list

    @staticmethod
    def SubjectGradeChange(project_id, changed_grade):
        subject_obj = ProjectSingle.objects.get(project_id = project_id)
        try:
            subject_obj.project_grade = ProjectGrade.objects.get(grade=changed_grade)
            subject_obj.recommend = True
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
        try:
            if ProjectSingle.objects.filter(project_unique_code = project_unique_code).count():
                raise
            project_obj.project_unique_code = project_unique_code
            project_obj.save()
            if len(project_unique_code.strip()) == 0:
               project_unique_code = "无"
        except Exception, e:
            loginfo(e)
            project_unique_code = "error"
        return project_unique_code
    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def NoticeMessageSetting(request):
        message_role_choice =list(MESSAGE_ROLE_CHOICES)
        if request.POST.get("message_content", False):
            datemessage = ""
            if request.POST.get('message_checkbox', False):
                datemessage = "1"
            else:
                datemessage = "0"
            # TODO: 前台控制角色选择验证
            for item in message_role_choice:
                if request.POST["message_role"] == item[0]:
                    rolemessage = item[2]
                    break
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
                       "templatenotice_group_form": templatenotice_group_form,
                       "message_role_choice":message_role_choice })
    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def project_control(request):
        adminStaff = AdminStaffProfile.objects.get(userid = request.user)
        is_finishing = adminStaff.is_finishing
        # pro_list=ProjectSingle.objects.filter(Q(project_grade=1)|Q(project_grade=2))
        pro_list = ProjectSingle.objects.filter(Q(over_status__status=OVER_STATUS_NOTOVER)
                                                |Q(over_status__status=OVER_STATUS_DELAY))

        year_list = get_yearlist(pro_list,'year')
        if year_list:
            havedata_p = True
        else:
            havedata_p = False
        #查看正在结题的年份
        year_finishing_list = []
        adminObj = AdminStaffProfile.objects.get(userid = request.user)
        user = User.objects.get(id=adminObj.userid_id)
        projectfinish = ProjectFinishControl.objects.filter(userid =user.id)
        for finishtemp in projectfinish :
            if finishtemp.project_year not in year_finishing_list:
                year_finishing_list.append(finishtemp.project_year)

        year_finishing_list = get_yearlist(projectfinish,'project_year')

        loginfo(p=year_finishing_list,label="year_finishing_list")


        recommend_rate_obj = SchoolRecommendRate.load()
        ac, _ = ApplyControl.objects.get_or_create(origin=None)
        is_applying = ac.is_applying

        cates = ProjectCategory.objects.all()

        return render(request, "adminStaff/project_control.html",
                    {
                        "recommend_rate": recommend_rate_obj,
                        "is_finishing":is_finishing,
                        "year_list":year_list,
                        "havedata_p":havedata_p,
                        "year_finishing_list":year_finishing_list,
                        "is_applying": is_applying,
                        'cates': cates,
                    })

    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def project_informationexport(request):

        project_manage_form = forms.ProjectManageForm()
        return render(request, "adminStaff/project_informationexport.html",
                    {
                        "project_manage_form":project_manage_form,
                    })
    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def file_download(request,fileid = None,filename = None):
        response = file_download_gen(request,fileid)
        return response

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
        # fix_bad_flag(context["pro_list"])
        for pro_obj in context["pro_list"]:
            add_fileurl(pro_obj)
            add_telephone(pro_obj)
            pro_obj.has_other_files = False
            for files in pro_obj.uploadedfiles_set.all():
                if files.name not in [u'申报书', u'中期检查表', u'结题报告', u'项目汇编', u'开题报告']:
                    pro_obj.has_other_files = True
                    break
            if len(pro_obj.project_unique_code.strip()) == 0:
                pro_obj.project_unique_code = "无"
        return render(request, "adminStaff/adminstaff_home.html",context)

    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def changepassword(request):
        user_list = []
        context = {'users': user_list, 'havedata_u': 0}
        if request.method == 'POST':
            search_username = request.POST.get('search_username', None)
            user_list = User.objects.filter(Q(username__icontains = search_username)|Q(email__icontains = search_username))
            if user_list:
                context = {'user_list': user_list, 'havedata_u':1}
                return render(request, "adminStaff/changepassword.html", context)
        return render(request, "adminStaff/changepassword.html", context)

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
                pro_list = get_current_project_query_set().filter(Q(project_grade=grade_nation) & \
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
        pro_list = pro_list.order_by('project_unique_code')
        #loginfo(p=pro_list,label="pro_list")
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
            project_category = project_manage_form.cleaned_data['project_category']
            project_teacher_student_name = project_manage_form.cleaned_data["teacher_student_name"]
            loginfo(project_teacher_student_name)
            # qset = AdminStaffService.get_filter(project_grade,project_year,project_isover,project_scoreapplication)
            qset = AdminStaffService.get_filter(
                    project_grade,project_year,project_overstatus,
                    project_teacher_student_name,project_scoreapplication,
                    project_school, project_category)
            if qset :
                qset = reduce(lambda x, y: x & y, qset)
                # if project_grade == "-1" and project_scoreapplication == "-1":
                #     pro_list = ProjectSingle.objects.filter(qset).exclude(Q(project_grade__grade=GRADE_INSITUTE) or Q(project_grade__grade=GRADE_SCHOOL) or Q(project_grade__grade=GRADE_UN))
                # else:
                pro_list = ProjectSingle.objects.filter(qset).distinct()
            else:
                pro_list = ProjectSingle.objects.all()
        loginfo(p=qset,label="qset")
        return pro_list

    ##
    # TODO: fixed the `isover` to over status
    @staticmethod
    def get_filter(project_grade,project_year,project_overstatus,
                   project_teacher_student_name,
                   project_scoreapplication = "-1",project_school= "-1",
                   project_category="-1"):
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
        if project_category == "-1":
            project_category = ''

        q1 = (project_year and Q(year=project_year)) or None
        # q2 = (project_isover and Q(is_over=project_isover)) or None
        q2 = (project_overstatus and Q(over_status__status=project_overstatus)) or None
        q3 = (project_grade and Q(project_grade__grade=project_grade)) or None
        q4 = (project_scoreapplication and Q(score_application=project_scoreapplication)) or None
        q5 = (project_school and Q(school_id = project_school)) or None
        q6 = (project_teacher_student_name and (Q(adminuser__name__contains = project_teacher_student_name) | Q(student_group__studentName__contains = project_teacher_student_name))) or None
        q7 = (project_category and Q(project_category__category=project_category)) or None
        qset = filter(lambda x: x != None, [q1, q2, q3, q4, q5, q6, q7])
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
        TeacherProjectPerLimits.objects.all().delete()  # Delete teacher limits
        ProjectPerLimits.objects.all().delete()  # Delete school limits
        ProjectSingle.objects.filter(is_past=False).update(is_past=True)
        # Allow to complete new application
        ac, _ = ApplyControl.objects.get_or_create(origin=None)
        ac.is_applying = True
        ac.save()
        # Reset time settings
        pc = ProjectControl.objects.get()
        pc.pre_start_day = timezone.now()
        pc.save()
        return render_to_response("adminStaff/projectlimitnumSettings.html",{'num_limit_form':num_limit_form,'school_limit_list':school_limit_num_list},context_instance=RequestContext(request))

    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def ProjectLimitNumRecycle(request):
        num_limit_form = forms.NumLimitForm()
        school_limit_num_list = AdminStaffService.SchoolLimitNumList()
        TeacherProjectPerLimits.objects.all().delete()
        ProjectPerLimits.objects.all().delete()
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

    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def open_report_view(request, pid=None):
        data = open_report_view_work(request, pid)
        return render(request, 'adminStaff/open.html', data)

    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def mid_report_view(request, pid=None):
        data = mid_report_view_work(request, pid)
        return render(request, 'adminStaff/mid.html', data)


    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def application_report_view(request, pid=None):
        data = application_report_view_work(request, pid)
        # if data['isRedirect'] :
        #     return HttpResponseRedirect( '/adminStaff/memberchange/' + str(pid))
        # else:
        return render(request, 'adminStaff/application.html', data)

    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def final_report_view(request, pid=None,is_expired=False):

        data = final_report_view_work(request, pid, is_expired = False)




        # if data['isRedirect'] :
        #     return HttpResponseRedirect( '/adminStaff/memberchange/' + str(pid))
        # else:

        return render(request, 'adminStaff/final.html', data)


    @staticmethod
    @csrf.csrf_protect
    #@login_required
    #@authority_required(ADMINSTAFF_USER)
    def member_change(request, pid):

        data = member_change_work(request, pid)

        return render(request, "adminStaff/member_change.html", data)


    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def files_upload_view(request,errortype=None,pid=None,is_expired=False):
        data = files_upload_view_work(request,pid,errortype)

        if data[0]:
            return HttpResponseRedirect('/adminStaff/')
        else:
            data = data[1]
        return render(request,'adminStaff/fileimportant.html',data)

    @staticmethod
    @csrf.csrf_protect
    @login_required
    # @authority_required(ADMINSTAFF_USER)
    def get_xls_path(request,exceltype,project_manage_form):

        # SocketServer.BaseServer.handle_error = lambda *args, **kwargs: None
        # handlers.BaseHandler.log_exception = lambda *args, **kwargs: None

        try:
            pro_set = get_projectlist(request,project_manage_form)
            if exceltype == EXCEL_TYPE_BASEINFORMATION:
                file_path = info_xls_baseinformation(request,pro_set)
            elif exceltype == EXCEL_TYPE_APPLICATIONSCORE:
                file_path = info_xls_expertscore(request,pro_set)
            elif exceltype == EXCEL_TYPE_SUMMARYSHEET_INNOVATE:
                file_path = info_xls_summaryinnovate(request,pro_set)
            elif exceltype == EXCEL_TYPE_SUMMARYSHEET_RESEARCH:
                file_path = info_xls_summaryresearch(request,pro_set)
            elif exceltype == EXCEL_TYPE_SUMMARYSHEET_ENTREPRENEUSHIP:
                file_path  = info_xls_summaryentrepreneuship(request,pro_set)
            elif exceltype == EXCEL_TYPE_PROJECTSUMMARY:
                file_path = info_xls_projectsummary(request,pro_set)
            elif exceltype == EXCEL_TYPE_SCOREAPPLICATION:
                file_path = info_xls_scoreapplication(request,pro_set)
            elif exceltype == EXCEL_TYPE_CERTIFICATES:
                file_path = info_xls_certificates(request, pro_set)
            elif exceltype == EXCEL_TYPE_ACHIEVEMENTS:
                file_path = info_xls_achievements(request, pro_set)
        except Exception,err:
            loginfo(err)
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


    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def project_assistant_view(request):
        data = {}
        return render(request, 'adminStaff/project_assistant.html', data)

    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def project_sync(request):

        current_project_list=ProjectSingle.objects.filter((Q(project_grade__grade=GRADE_NATION)|Q(project_grade__grade=GRADE_PROVINCE)) & \
                                                          Q(is_past = False))
#        if request.method == "POST":
#            sync_form = Sync_form(request.POST)
#            loginfo(p=request,label="request")
#            if sync_form.is_valid():
#                username = sync_form.cleaned_data['Sync_username']
#                password = sync_form.cleaned_data['Sync_passeword']
#                loginfo(p=username,label="username")
#                loginfo(p=password,label="password")
#                check_box_list = request.POST.getlist("check_box")
#                loginfo(p=check_box_list,label="checkbox_temp")
#                for checkbox_temp in check_box_list:
#                    loginfo(p=checkbox_temp,label="checkbox_temp")
#                    if checkbox_temp.checked:
#                        loginfo(p=checkbox_temp.value,label="checkbox_temp.value")
#                return HttpResponse('success')
#        else:
        sync_form = Sync_form()

        logger.info(sync_form.errors)
        import jsonrpclib
        from settings import RPC_SITE
        try:
            server = jsonrpclib.Server(RPC_SITE)
            for proj in current_project_list:
                proj.is_synced = server.CheckSyncProjects(proj.project_id)
        except: pass
        data = {
           'current_project_list':current_project_list,
            'sync_form':sync_form,
        }
        return render(request, 'adminStaff/project_sync.html', data)


def member_change_work(request, pid):
    """
    project group member change
    """
    #student_account = StudentProfile.objects.get(userid = request.user)
    #project = ProjectSingle.objects.get(student=student_account)

    project = ProjectSingle.objects.get(project_id = pid)
    # isIN =  get_schooluser_project_modify_status(project)
    student_group = Student_Group.objects.filter(project = project)
    files = set()

    for s in student_group:
        if s.scoreFile:
            files.add(s.scoreFile)
        s.sex = s.get_sex_display()

    student_group_form = StudentGroupForm()
    student_group_info_form = StudentGroupInfoForm()

    if check_auth(user=request.user,authority=SCHOOL_USER):
        readonly = not get_schooluser_project_modify_status(project)

    else:
        readonly = False


    data = {"pid": pid,
            "files":files,
            "student_group": student_group,
            "student_group_form": student_group_form,
            "student_group_info_form": student_group_info_form,
            'readonly': readonly,
            }
    return  data
