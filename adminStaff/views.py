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
from school.models import ProjectSingle
from const.models import UserIdentity 
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
    def GetSubject_list(category=None):
        subject_list = []
        if category == None:
            subject_list = ProjectSingle.objects.all()
        else:
            subject_list = ProjectSingle.objects.filter(project_category=category)
        return subject_list
    @staticmethod
    def SubjectFeedback(request):
        if request.method == "GET":
            subject_insitute_form = forms.SubjectInsituteForm()
            subject_list =  AdminStaffService.GetSubject_list()
        else:
            subject_insitute_form = forms.SubjectInsituteForm(request.POST)
            if subject_insitute_form.is_valid():
                category =  subject_insitute_form.cleaned_data["insitute_choice"]
                subject_list =  AdminStaffService.GetSubject_list(category=category)    
        return render_to_response("adminStaff/subject_feedback.html",{'subject_list':subject_list,'subject_insitute_form':subject_insitute_form},context_instance=RequestContext(request))
      
                                                                          
                                            
        