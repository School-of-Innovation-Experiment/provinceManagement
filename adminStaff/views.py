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
from const import *
from teacher.models import TeacherMonthComment
from student.models import  StudentWeeklySummary, Student_Group, Funds_Group
from school.models import ProjectSingle, Project_Is_Assigned, Re_Project_Expert,UploadedFiles
from const.models import UserIdentity, InsituteCategory, ProjectGrade
from users.models import ExpertProfile, AdminStaffProfile
from registration.models import RegistrationProfile
from django.db import transaction
from django.db.models import Q
from const import MESSAGE_EXPERT_HEAD, MESSAGE_SCHOOL_HEAD ,MESSAGE_STUDENT_HEAD
from backend.decorators import *
from backend.logging import loginfo
from news.models import News
from news.forms import NewsForm

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
                dict["auth"] += auth.__unicode__() + '(' + register.school.__unicode__() + ')'
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
        if request.method == "GET":
            school_category_form = forms.SchoolCategoryForm()
            page1 = request.GET.get('page1')
            if page1 == "None": page1 = None
            page2 = request.GET.get('page2')
            if page2 == "None": page2 = None
            school_name = request.GET.get('school_name')
            if school_name == "None": school_name = None

            if (not school_name) or int(school_name) == -1:
                subject_list =  ProjectSingle.objects.filter(recommend = True)
            else:
                subject_list = ProjectSingle.objects.filter(Q(recommend = True) & Q(school = SchoolProfile.objects.get(id = school_name)))
        else:
            school_category_form = forms.SchoolCategoryForm(request.POST)
            if school_category_form.is_valid():
                page1 = 1
                page2 = 1
                school_name = school_category_form.cleaned_data["school_choice"]
                if int(school_name) == -1:
                    subject_list = ProjectSingle.objects.filter(recommend = True)
                else:
                    subject_list = ProjectSingle.objects.filter(Q(recommend = True) & Q(school = SchoolProfile.objects.get(id = school_name)))

        for subject in subject_list:
            student_group = Student_Group.objects.filter(project = subject)
            try:
                subject.members = student_group[0]
            except:
                pass
        rec_subject_list = [subject for subject in subject_list if subject.project_grade.id == 1 or subject.project_grade.id == 2]
        rec = getContext(rec_subject_list, page1, 'subject', 0)
        nrec_subject_list = [subject for subject in subject_list if not (subject.project_grade.id == 1 or subject.project_grade.id == 2)]
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
            elif request.POST["message_role"] == '4':
                rolemessage = MESSAGE_TEACHER_HEAD
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
        pro_list=ProjectSingle.objects.filter(Q(project_grade=1)|Q(project_grade=2))
        year_list=[]
        for pro_obj in pro_list :
            if pro_obj.year not in year_list :
                year_list.append(pro_obj.year)
        if year_list:
            havedata_p = True
        else:
            havedata_p = False
        return render(request, "adminStaff/project_control.html",
                    {
                        "is_finishing":is_finishing,
                        "year_list":year_list,
                        "havedata_p":havedata_p,
                    })

    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def funds_manage(request,is_expired=False):
        subject_grade_form = forms.SubjectGradeForm()
        if request.method == "GET":
            school_category_form = forms.SchoolCategoryForm()
            subject_list =  pro_list=ProjectSingle.objects.filter(Q(project_grade=1)|Q(project_grade=2))

        else:
            school_category_form = forms.SchoolCategoryForm(request.POST)
            if school_category_form.is_valid():
                school_name = school_category_form.cleaned_data["school_choice"]
                subject_list =  pro_list=ProjectSingle.objects.filter((Q(project_grade=1)|Q(project_grade=2) )and Q(school = school_name))

        for subject in subject_list:
            student_group = Student_Group.objects.filter(project = subject)
            try:
                subject.members = student_group[0]
            except:
                pass

        return render_to_response("adminStaff/funds_manage.html",{'subject_list':subject_list,'school_category_form':school_category_form, 'subject_grade_form':subject_grade_form},context_instance=RequestContext(request))



    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def funds_change(request,pid):
        project = ProjectSingle.objects.get(project_id = pid)
        project_funds_list = Funds_Group.objects.filter(project_id = pid)

        fundsChange_group_form = forms.FundsChangeForm();

        for subject in project_funds_list:
            student_group = Student_Group.objects.filter(project = subject)
            try:
                subject.members = student_group[0]
            except:
                pass

        student_name_form = forms.StudentNameForm(pid = pid);

        return_data = {
                        "project_funds_list":project_funds_list,
                        "fundsChange_group_form":fundsChange_group_form,
                        "student_name_form":student_name_form,
                        "project":project,
                        }

        return render(request,"adminStaff/funds_change.html",return_data)

    @staticmethod
    @csrf.csrf_protect
    @login_required
    @authority_required(ADMINSTAFF_USER)
    def home_view(request):
        """
        默认只显示省级和国家级项目
        """
        pro_list=ProjectSingle.objects.filter(Q(project_grade=1)|Q(project_grade=2))
        if request.method =="POST":
            project_manage_form = forms.ProjectManageForm(request.POST)
            pro_list = AdminStaffService.projectFilterList(request,project_manage_form)
        else:
            project_manage_form = forms.ProjectManageForm()

        for pro_obj in pro_list:
            file_history = UploadedFiles.objects.filter(project_id=pro_obj.project_id)
            for file_temp in file_history:
                if file_temp.name == u"学分申请表":
                    url = file_temp.file_obj.url
                    pro_obj.url = url
        loginfo(p=pro_list,label="pro_list")
        if pro_list.count() != 0 or request.method == "POST":
            havedata_p = True
        else: havedata_p = False
        context = {
                    'havedata_p': havedata_p,
                    'pro_list': pro_list,
                    'project_manage_form':project_manage_form
                    }
        return render(request, "adminStaff/adminstaff_home.html",context)
    
    @staticmethod
    @csrf.csrf_protect
    def projectFilterList(request,project_manage_form):       
        if project_manage_form.is_valid():
            project_grade = project_manage_form.cleaned_data["project_grade"]
            project_year =  project_manage_form.cleaned_data["project_year"]
            # project_isover = project_manage_form.cleaned_data["project_isover"]
            project_overstatus = project_manage_form.cleaned_data["project_overstatus"]
            project_scoreapplication = project_manage_form.cleaned_data["project_scoreapplication"]
            # qset = AdminStaffService.get_filter(project_grade,project_year,project_isover,project_scoreapplication)
            qset = AdminStaffService.get_filter(project_grade,project_year,project_overstatus,project_scoreapplication)
            if qset :
                qset = reduce(lambda x, y: x & y, qset)
                if project_grade == "-1" and project_scoreapplication == "-1":
                    pro_list = ProjectSingle.objects.filter(qset).exclude(Q(project_grade__grade=GRADE_INSITUTE) or Q(project_grade__grade=GRADE_SCHOOL) or Q(project_grade__grade=GRADE_UN))
                else:
                    pro_list = ProjectSingle.objects.filter(qset)
        loginfo(p=qset,label="qset")
        return pro_list

    ##
    # TODO: fixed the `isover` to over status
    @staticmethod
    def get_filter(project_grade,project_year,project_overstatus, project_scoreapplication):
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
        q1 = (project_year and Q(year=project_year)) or None
        # q2 = (project_isover and Q(is_over=project_isover)) or None
        q2 = (project_overstatus and Q(over_status=project_overstatus)) or None
        q3 = (project_grade and Q(project_grade__grade=project_grade)) or None
        q4 = (project_scoreapplication and Q(score_application=project_scoreapplication)) or None
        qset = filter(lambda x: x != None, [q1, q2, q3,q4])
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
        pro_list=ProjectSingle.objects.filter(Q(project_grade=1)|Q(project_grade=2))
        if request.method =="POST":
            project_manage_form = forms.ProjectManageForm(request.POST)
            pro_list = AdminStaffService.projectFilterList(request,project_manage_form)
        else:
            project_manage_form = forms.ProjectManageForm()

        if pro_list.count() != 0 or request.method == "POST":
            havedata_p = True
        else: havedata_p = False       
        context = {
                    'havedata_p': havedata_p,
                    'pro_list': pro_list,
                    'project_manage_form':project_manage_form
                    }
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
    def NewsRelease(request):
        news_list = News.objects.all().order_by("-news_date")
        page = request.GET.get('page')
        if request.method == 'POST':
            newsform = NewsForm(request.POST, request.FILES)
            if newsform.is_valid():
                new_news = News(news_title = newsform.cleaned_data["news_title"],
                                news_content = newsform.cleaned_data["news_content"],
                                news_date = newsform.cleaned_data["news_date"],
                                news_category = NewsCategory.objects.get(id=newsform.cleaned_data["news_category"]),)
                                # news_document = request.FILES["news_document"],)
                new_news.save()
            else:
                loginfo(p=newsform.errors.keys(), label="news form error")
            return redirect('/newslist/%d' % new_news.id)
        else:
            context = getContext(news_list, page, 'news', 0)
            context.update({"newsform": NewsForm})
            return render(request, "adminStaff/news_release.html", context)
