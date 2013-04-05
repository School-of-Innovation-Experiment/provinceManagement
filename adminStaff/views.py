# coding: UTF-8
'''
Created on 2013-03-28

@author: sytmac
'''
# Create your views here.
import random
import re,sha
import uuid

from django.http import HttpResponse
from registration.models import * 
from adminStaff import forms
from django.shortcuts import render_to_response
from django.template import  RequestContext
from django.views.decorators.csrf import csrf_protect
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from const import *
from school.models import ProjectSingle, Project_Is_Assigned, Re_Project_Expert
from const.models import UserIdentity, InsituteCategory, ProjectGrade
from users.models import ExpertProfile
class AdminStaffService(object):
    @staticmethod
    def sendemail(request,username,password,email,identity, **kwargs):
        #判断用户名是否存在存在直接返回
        if not AdminStaffService.UserExist(email):
            if kwargs.has_key('school_name'):
                RegistrationManager().create_inactive_user(request,username,password,email,identity, school_name=kwargs['school_name'])
            else:
                RegistrationManager().create_inactive_user(request,username,password,email,identity)
            return True
        else:
            return False
    @staticmethod
    def Dispatch(request):
        if request.method == "GET":
            expert_form = forms.ExpertDispatchForm()
            school_form = forms.SchoolDispatchForm()
            return render_to_response("adminStaff/dispatch.html",{'expert_form':expert_form,'school_form':school_form},context_instance=RequestContext(request))
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
    def UserExist(email):
        if User.objects.filter(email=email).count():
            return True
        else:
            return False
    @staticmethod
    def AdminSetting(request):
        if request.method == "GET":
            timeform = forms.TimeSettingForm()
            num_limit_form = forms.NumLimitForm()
            return render_to_response("adminStaff/settings.html",{'time_form':timeform,'num_limit_form':num_limit_form},context_instance=RequestContext(request))
    @staticmethod
    def GetSubject_list(category=None,school=None):
        subject_list = []
        if category == None and school == None:
            subject_list = ProjectSingle.objects.all()
        elif not category == None:
            subject_list = ProjectSingle.objects.filter(project_category=category)
        elif not school == None:
            subject_list = ProjectSingle.objects.filter(school=school)           
        return subject_list
    @staticmethod
    def SubjectFeedback(request):
        if request.method == "GET":
            subject_insitute_form = forms.SubjectInsituteForm()
            subject_list =  AdminStaffService.GetSubject_list()
            
        else:
            subject_insitute_form = forms.SubjectInsituteForm(request.POST)
            if subject_insitute_form.is_valid():
                category = subject_insitute_form.cleaned_data["insitute_choice"]
                subject_list =  AdminStaffService.GetSubject_list(category=category)
                
                expert_category = InsituteCategory.objects.get(id=category)
                obj = Project_Is_Assigned.objects.get(insitute = expert_category)
                #如果已经指派专家了直接返回列表即可
                if obj.is_assigned == 1:
                    pass
                #没有指派专家，则进行专家指派
                else:
                    #筛选专家列表
                    expert_list = ExpertProfile.objects.filter(subject=expert_category)
                    re_dict = AdminStaffService.Assign_Expert_For_Subject(subject_list, expert_list)
                    #将返回数据进入Re_Project_Expert表中

                    for subject in re_dict.keys():
                        for expert in re_dict[subject]:
                            #subject.expert.add(expert)
                            Re_Project_Expert(project_id=subject.project_id, expert_id=expert.id).save()
                    #保存已分配标志，值为1  
                    obj.is_assigned = 1
                    obj.save()
        return render_to_response("adminStaff/subject_feedback.html",{'subject_list':subject_list,'subject_insitute_form':subject_insitute_form},context_instance=RequestContext(request))
    
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
    def SubjectRating(request):
        subject_grade_form = forms.SubjectGradeForm()                                   
        if request.method == "GET":
            school_category_form = forms.SchoolCategoryForm()
            subject_list =  AdminStaffService.GetSubject_list()
            
        else:
            school_category_form = forms.SchoolCategoryForm(request.POST)
            if school_category_form.is_valid():
                school_name = school_category_form.cleaned_data["school_choice"]
                subject_list =  AdminStaffService.GetSubject_list(school=school_name)
                
        return render_to_response("adminStaff/subject_rating.html",{'subject_list':subject_list,'school_category_form':school_category_form, 'subject_grade_form':subject_grade_form},context_instance=RequestContext(request))
    @staticmethod
    def GetSubjectReviewList(project_id):
        review_obj_list = Re_Project_Expert.objects.filter(project=project_id).all()
        review_list = []
        for obj in review_obj_list:
            obj_list = [obj.scores, obj.comments]
            review_list.append(obj_list)
        return review_list 
    @staticmethod
    def SubjectGradeChange(project_id, changed_grade):
        subject_obj = ProjectSingle.objects.get(project_id = project_id)
        subject_obj.project_grade = ProjectGrade.objects.get(grade=changed_grade)
        subject_obj.save()                                 
        