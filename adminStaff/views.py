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
from adminStaff import forms
from adminStaff.models import ProjectPerLimits, ProjectControl, NoticeMessage
from django.shortcuts import render_to_response, render, get_object_or_404, redirect
from django.template import  RequestContext
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from const import *
from school.models import ProjectSingle, Project_Is_Assigned, Re_Project_Expert
from const.models import UserIdentity, InsituteCategory, ProjectGrade
from users.models import ExpertProfile
from school.utility import get_running_project_query_set, get_current_project_query_set
from registration.models import *
from registration.models import RegistrationProfile

from django.db import transaction

from const import MESSAGE_EXPERT_HEAD, MESSAGE_SCHOOL_HEAD
from backend.decorators import *
from backend.logging import logger, loginfo
from news.models import News
from news.forms import NewsForm
from backend.utility import getContext
from adminStaff.utility import *

import SocketServer
from wsgiref import handlers

class AdminStaffService(object):
    @staticmethod
    def sendemail(request,username,person_firstname,password,email,identity,send_email=True, **kwargs):
        #判断用户名是否存在存在直接返回
        if not AdminStaffService.AuthUserExist(email, identity):
            if kwargs.has_key('school_name'):
                RegistrationManager().create_inactive_user(request,username,person_firstname,password,email,identity,send_email, school_name=kwargs['school_name'])
            else:
                RegistrationManager().create_inactive_user(request,username,person_firstname,password,email,identity,send_email, expert_insitute=kwargs['expert_insitute'])
            return True
        else:
            return False
    @staticmethod
    def GetRegisterSchoolList():
        res_list = []
        auth_name = []
        for register in SchoolProfile.objects.all():
            dict = {}
            auth_list = UserIdentity.objects.filter(auth_groups = register.userid).all()
            dict["auth"] = ''
            dict["email"] = register.userid.email
            dict["is_active"] = register.userid.is_active
            dict["first_name"] = register.userid.first_name
            for auth in auth_list:
                dict["auth"] += auth.__unicode__() + ' '
            res_list.append(dict)
        return res_list


    @staticmethod
    def GetRegisterExpertList():
        res_list = []
        auth_name = []
        for register in ExpertProfile.objects.all():
            dict = {}
            auth_list = UserIdentity.objects.filter(auth_groups = register.userid).all()
            dict["auth"] = ''
            dict["email"] = register.userid.email
            dict["is_active"] = register.userid.is_active
            dict["first_name"] = register.userid.first_name
            for auth in auth_list:
                dict["auth"] += auth.__unicode__() + ' '
            res_list.append(dict)
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
            dict["first_name"] = register.userid.first_name
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
            dict["first_name"] = register.userid.first_name
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
            school_form = forms.SchoolDispatchForm()
            resetSchoolPasswd_form = forms.ResetSchoolPasswordForm()
            email_list  = AdminStaffService.GetRegisterSchoolList()
            page = request.GET.get('page')
            loginfo(p=page, label="current page num")
            context = getContext(email_list, page, 'item', 0)
            context['school_form'] = school_form
            context['resetSchoolPasswd_form'] = resetSchoolPasswd_form

            #loginfo(p=email_list, label="news email_list ")
            return render(request, "adminStaff/dispatch.html", context)
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
                AdminStaffService.sendemail(request, name, password, email, EXPERT_USER)
                expert_form = forms.ExpertDispatchForm()
            return render_to_response("adminStaff/dispatch.html",{'expert_form':expert_form,'school_form':school_form},context_instance=RequestContext(request))

    @staticmethod
    def ImportExpert(request):
        """
        """
        if request.method == "GET":
            expert_form = forms.ExpertDispatchForm()
            email_list = AdminStaffService.GetRegisterExpertList()

            page = request.GET.get('page')
            context = getContext(email_list, page, 'item', 0)
            context.update({'expert_form': expert_form})
            return render(request, "adminStaff/ImportExpert.html", context)


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
        print "LLLLLLLLLLLLLLLZZZZZZZZZZZZZZZZZ"
        if request.method == "GET":
            #timeform = forms.TimeSettingForm()
            num_limit_form = forms.NumLimitForm()
            school_limit_num_list = AdminStaffService.SchoolLimitNumList()
            page = request.GET.get('page')
            context = getContext(school_limit_num_list, page, 'item', 0)
            context.update({'num_limit_form':num_limit_form})
            return render(request, "adminStaff/projectlimitnumSettings.html", context)

    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def ProjectLimitNumReset(request):
        '''
        学校上传数量重置
        '''
        num_limit_form = forms.NumLimitForm()
        school_limit_num_list = AdminStaffService.SchoolLimitNumList()
        ProjectPerLimits.objects.all().delete()
        for p in ProjectSingle.objects.filter(is_past=False):
            p.is_past = True
            p.save()
        for p in ProjectSingle.objects.filter(is_over=False):
            p.is_over = True
            p.save()
        return HttpResponseRedirect('ProjectLimitNumSettings')
        # return render_to_response("adminStaff/projectlimitnumSettings.html", {'num_limit_form': num_limit_form, 'school_limit_list':school_limit_num_list}, context_instance=RequestContext(request))

    @staticmethod
    def SchoolLimitNumList():
        '''
        返回存在的每个学校限制数目列表
        '''
        limit_list = ProjectPerLimits.objects.all()
        for obj in limit_list:
            obj.b_cate_number = obj.number - obj.a_cate_number
        return limit_list
    @staticmethod
    def GetSubject_list(category=None,school=None):
        subject_list = []
        if category:
            subject_list = ProjectSingle.objects.filter(insitute_id=category)
        elif school:
            subject_list = ProjectSingle.objects.filter(school=school)
        else:
            subject_list = ProjectSingle.objects.all()
        return subject_list
    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    @time_controller(phase=STATUS_FINSUBMIT)
    def SubjectFeedback(request,is_expired=False):
        exist_message = ''
        readonly=is_expired
        context = {}
        if request.method == "GET":
            page = request.GET.get('page')
            subject_insitute_form = forms.SubjectInsituteForm()
            #subject_list =  AdminStaffService.GetSubject_list()
            subject_list = get_current_project_query_set()
            context = getContext(subject_list, page, 'subject', 0) 

        else:
            subject_insitute_form = forms.SubjectInsituteForm(request.POST)
            if subject_insitute_form.is_valid():
                category = subject_insitute_form.cleaned_data["insitute_choice"]
                #subject_list =  AdminStaffService.GetSubject_list(category=category)
                subject_list = get_current_project_query_set().filter(insitute_id=category)
                page = request.GET.get('page')
                context = getContext(subject_list, page, 'subject', 0)
                expert_category = InsituteCategory.objects.get(id=category)
                try:
                    obj = Project_Is_Assigned.objects.get(insitute = expert_category)
                    #如果已经指派专家了则对新项目进行追加
                    if obj.is_assigned == 1:
                        expert_list = ExpertProfile.objects.filter(subject = expert_category)
                        extra_subject_list = [subject for subject in subject_list if len(subject.expert.all()) == 0]
                        # print subject_list[1].expert.all()
                        if len(extra_subject_list) == 0 or len(expert_list) == 0:
                            if not extra_subject_list:
                                exist_message = "没有需要分配的新项目存在，无法进行指派"
                            else:
                                exist_message = "所属专业的专家不存在,无法进行指派"
                        else:
                            done_num = len(subject_list) - len(extra_subject_list)

                            re_dict = AdminStaffService.Assign_Expert_For_Subject(extra_subject_list, expert_list, done_num)
                            for subject in re_dict.keys():
                                for expert in re_dict[subject]:
                                    Re_Project_Expert(project=subject, expert=expert).save()

                    #没有指派专家，则进行专家指派
                    else:
                        #筛选专家列表
                        expert_list = ExpertProfile.objects.filter(subject=expert_category)
                        #如果所属学科专家不存在，则进行提示
                        if len(expert_list) == 0 or len(subject_list) == 0:
                            if not expert_list :
                                exist_message = '所属专业的专家不存在,无法进行指派'
                            else:
                                exist_message = '没有专业指定的题目，无法进行指派'

                        else:
                            re_dict = AdminStaffService.Assign_Expert_For_Subject(subject_list, expert_list)
                            #将返回数据进入Re_Project_Expert表中

                            for subject in re_dict.keys():
                                for expert in re_dict[subject]:
                                    #subject.expert.add(expert)
                                    Re_Project_Expert(project=subject, expert_id=expert.id).save()
                            #保存已分配标志，值为1
                            obj.is_assigned = 1
                            obj.save()
                except Project_Is_Assigned.DoesNotExist:
                    obj = None
        context.update({'subject_insitute_form':subject_insitute_form,'exist_message':exist_message,'readonly':readonly})
        return render(request, "adminStaff/subject_feedback.html", context)

    @staticmethod
    def Assign_Expert_For_Subject(subject_list, expert_list, done_num = 0):

        ret = {}
        for i in xrange(len(subject_list)):
            subject = subject_list[i]
            #num = min(len(expert_list), random.randint(3,5))
            num = min(len(expert_list), 3)
            ret[subject] = []
            for j in xrange(num):
                ret[subject].append(expert_list[(done_num + i + j) % len(expert_list)])
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
            page = request.GET.get('page')
            school_name = request.GET.get('school_name')
            if school_name == "None": school_name = None
            #subject_list = AdminStaffService.GetSubject_list(school = school_name)
            subject_list = get_running_project_query_set().filter(school = school_name)
            context = getContext(subject_list, page, 'item', 0) 

        else:
            school_category_form = forms.SchoolCategoryForm(request.POST)
            if school_category_form.is_valid():
                school_name = school_category_form.cleaned_data["school_choice"]
                #subject_list =  AdminStaffService.GetSubject_list(school=school_name)
                subject_list = get_running_project_query_set().filter(school = school_name)
                context = getContext(subject_list, 1, 'item', 0)
        context.update({'school_category_form':school_category_form, 
                        'subject_grade_form':subject_grade_form,
                        'school_name':school_name,
                        'readonly':readonly})
        return render(request, "adminStaff/subject_rating.html", context)
    @staticmethod
    def GetSubjectReviewList(project_id):
        review_obj_list = Re_Project_Expert.objects.filter(project=project_id).all()
        review_list = []
        for obj in review_obj_list:
            obj_list = [obj.comments, obj.score_significant,
                        obj.score_value, obj.score_innovation,
                        obj.score_practice, obj.score_achievement,
                        obj.score_capacity, obj.pass_p]
            review_list.append(obj_list)
        return review_list

    @staticmethod
    def GetSubjectReviewPassPList(project_id):
        review_obj_list = Re_Project_Expert.objects.filter(project=project_id).all()
        review_list = []
        for obj in review_obj_list:
            obj_list = u"通过" if obj.pass_p else u"未通过"
            review_list.append(obj_list)
        return review_list

    @staticmethod
    def GetSubjectReviewPassPStatistic(project_id):
        review_obj_list = Re_Project_Expert.objects.filter(project=project_id).all()
        review_list = [0, 0]
        for obj in review_obj_list:
            if obj.pass_p:
                review_list[0] += 1
            else:
                review_list[1] += 1
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
    def RecommendRatingSetting(request):
        recommend_rate_obj = SchoolRecommendRate.load()
        context = {"recommend_rate": recommend_rate_obj,}
        return render(request, "adminStaff/rating_setting.html", context)
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
            else:
                rolemessage = MESSAGE_SCHOOL_HEAD
            _message = rolemessage + request.POST["message_content"] + "  " + datemessage
            message = NoticeMessage(noticemessage = _message)
            message.save()
        return render(request, "adminStaff/noticeMessageSettings.html")

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
                loginfo(newsform.cleaned_data["news_content"])
            else:
                loginfo(p=newsform.errors.keys(), label="news form error")
            return redirect('/newslist/%d' % new_news.id)
        else:
            context = getContext(news_list, page, 'news', 0)
            context.update({"newsform": NewsForm})
            return render(request, "adminStaff/news_release.html", context)
    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def get_xls_path(request):

        # SocketServer.BaseServer.handle_error = lambda *args, **kwargs: None
        # handlers.BaseHandler.log_exception = lambda *args, **kwargs: None
        file_path = info_xls(request)
        return MEDIA_URL + "tmp" + file_path[len(TMP_FILES_PATH):]
