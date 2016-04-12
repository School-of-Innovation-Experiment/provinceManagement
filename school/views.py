#!/usr/bin/python
# coding:UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-04-12 10:05
# Last modified: 2016-04-12 10:05
# Filename: views.py
# Description:
# coding: UTF-8
'''
Created on 2013-03-28

@author: tianwei

Desc: School's view, includes home(manage), final report,
      application report, statistics information.
'''
import datetime
import os
import sys
import uuid

from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.conf import settings
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseForbidden, Http404, HttpResponseBadRequest
from django.template import RequestContext
from django.utils import simplejson
from django.views.decorators import csrf
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import *
from django.contrib.auth.models import User

from school.models import ProjectSingle, PreSubmit, FinalSubmit
from school.models import UploadedFiles
from school.forms import *

from adminStaff.models import ProjectPerLimits
from adminStaff.forms import ProjectManageForm
from users.models import SchoolProfile, StudentProfile

from registration.models import RegistrationProfile
from registration.models import *

from django.db import transaction

from const.models import *
from const import *

from student.models import Student_Group
from student.forms import StudentGroupForm, StudentGroupInfoForm

from school.utility import *
from backend.logging import logger, loginfo
from backend.decorators import *

"""
About the decorators sequence, it will impact the the function squeneces,
the top will be called first!
"""


@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
def student_view(request):

    try:
        student = get_object_or_404(StudentProfile, user=request.user)
        project = student.projectsingle
    except Exception, err:
        loginfo(p=err, label="student home view")
        raise Http404
    loginfo(p=project.project_id)
    try:
        insitute = project.insitute.category
    except:
        insitute = u"未选择"
    data = {"project": project,
            "project_cate": project.project_category.category,
            "proj_insitute_choice": INSITUTE_CATEGORY_CHOICES,
            "project_insitute": insitute,
            "proj_cate_choice": PROJECT_CATE_CHOICES}

    return render(request, "school/student.html", data)


@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
def member_change(request):
    """
    project group member change
    """
    student_account = StudentProfile.objects.get(user_id = request.user)
    project = ProjectSingle.objects.get(student=student_account)
    student_group = Student_Group.objects.filter(project = project)

    student_group_form = StudentGroupForm()

    student_group_info_form = StudentGroupInfoForm()

    # student_group_info_form.email = student_group[0].email


    return render(request, "school/member_change.html",
                  {"student_group": student_group,
                   "student_group_form": student_group_form,
                   "student_group_info_form": student_group_info_form})

@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
@time_controller(phase=STATUS_PRESUBMIT)
def home_view(request, is_expired=False):
    """
    school home management page
    """
#    current_list = get_running_project_query_set().filter(adminuser = request.user)
    school_obj = SchoolProfile.objects.get(userid = request.user)
    current_list = ProjectSingle.objects.filter(school_id = school_obj.school_id).order_by('-year','financial_category__category','project_code')
    url_para=''
    try:
        if request.method == 'POST':
            project_form = ProjectManageForm(request.POST)
        else:
            project_form = ProjectManageForm(request.GET)
        if project_form.is_valid():
            current_list = current_list.filter(project_form.get_qset())
            url_para     = project_form.get_url_para()
    except:
        pass
    readonly=is_expired
    readonly=False

    try:
        limits = ProjectPerLimits.objects.get(school__userid=request.user)
    except Exception, err:
        logger.info(err)
        limits = None
    if limits is not None:
        pro_list =ProjectSingle.objects.filter(Q(adminuser = request.user) & Q(year=get_current_year()))
        remainings = int(limits.number) - pro_list.count()
        total = limits.number
        a_remainings = int(limits.a_cate_number) - pro_list.filter(financial_category__category = FINANCIAL_CATE_A).count()
    else:
        total = 0
        remainings = 0
        a_remainings = 0
    #add_current_list = current_list_add(list=current_list)
    page = request.GET.get('page') or 1
    context = getContext(current_list, page, "item", 0)
    
    context["item_list"] = current_list_add(list = context["item_list"])
    #context = getContext(add_current_list, page, "item", 0)
    # loginfo(p=add_current_list[0].final_isaudited, label="in add_current_list") 
    data = {"financial_cate_choice": FINANCIAL_CATE_CHOICES,
            "readonly":readonly,
            "project_form":project_form,
            "url_para":url_para,
            "info": {"applications_limits": total,
                     "applications_remaining": remainings,
                     "applications_a_remaining": a_remainings,
                     }
            }
    context.update(data)
    return render(request, 'school/home.html', context)


@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER, STUDENT_USER)
@only_user_required
@time_controller(phase=STATUS_PRESUBMIT)
def application_report_view(request, pid=None, is_expired=False):
    """
    school application report
    Arguments:
        In: id, it is project id
    """
    loginfo(p=pid+str(is_expired), label="in application")
    project = get_object_or_404(ProjectSingle, project_id=pid)
    teammember=get_studentmessage(project)
    pro_type = PreSubmit if project.project_category.category == CATE_INNOVATION else PreSubmitEnterprise
    fin_type = ("15000", "5000", "10000") if project.financial_category.category == FINANCIAL_CATE_A else ("10000", "0", "10000")
    try:
        innovation = pro_type.objects.get(project_id=project.project_id)
    except Exception, err:
        loginfo(p=err, label="get innovation")
        loginfo(p=project.project_category.category, label="project category")

    loginfo(p=teammember, label="in teammember")
    readonly = check_history_readonly(pid) or is_expired
    if check_auth(user = request.user,authority = SCHOOL_USER):
        readonly = False
    is_show =  check_auth(user=request.user,authority=STUDENT_USER)

    # ... sb requirement
    readonly = False

    if project.project_category.category == CATE_INNOVATION:
        iform = ApplicationReportForm
        imodel = PreSubmit
        pre = get_object_or_404(PreSubmit, project_id=pid)
        teacher_enterprise=None
        is_innovation = True
    else:
        iform = EnterpriseApplicationReportForm
        imodel = PreSubmitEnterprise
        pre = get_object_or_404(PreSubmitEnterprise, project_id=pid)
        teacher_enterprise = get_object_or_404(Teacher_Enterprise,id=pre.enterpriseTeacher_id)
        is_innovation = False

    teacher_enterpriseform=Teacher_EnterpriseForm(instance=teacher_enterprise)

    isRedirect = False

    if request.method == "POST" and readonly is not True:
        role=check_is_audited(user=request.user,presubmit=pre,checkuser=SCHOOL_USER)
        info_form = InfoForm(request.POST, pid=pid,instance=project)
        application_form = iform(request.POST, instance=pre)
        loginfo(p=application_form,label='test')
        if is_innovation:
            if info_form.is_valid() and application_form.is_valid():
                if save_application(project, info_form, application_form, request.user):
                    project.project_status = ProjectStatus.objects.get(status=STATUS_PRESUBMIT)
                    project.save()
                    isRedirect = True
                    return HttpResponseRedirect(reverse('school.views.%s_view' % role))
            else:
                logger.info("Form Valid Failed"+"**"*10)
                logger.info(info_form.errors)
                logger.info(application_form.errors)
                logger.info("--"*10)
        else:
            teacher_enterpriseform=Teacher_EnterpriseForm(request.POST,instance=teacher_enterprise)
            if info_form.is_valid() and application_form.is_valid() and teacher_enterpriseform.is_valid():
                set_unique_telphone(request, info_form, teacher_enterpriseform)
                if save_enterpriseapplication(project, info_form, application_form, teacher_enterpriseform,request.user):
                    project.project_status = ProjectStatus.objects.get(status=STATUS_PRESUBMIT)
                    project.save()
                    isRedirect = True
                    return HttpResponseRedirect(reverse('school.views.%s_view' % role))
            else:
                logger.info("Form Valid Failed"+"**"*10)
                logger.info(info_form.errors)
                logger.info(application_form.errors)
                logger.info(teacher_enterpriseform.errors)
                logger.info("--"*10)
    else:
        info_form = InfoForm(instance=project,pid=pid)
        application_form = iform(instance=pre)
        isRedirect = True

    data = {'pid': pid,
            'info': info_form,
            'application': application_form,
            'teacher_enterpriseform':teacher_enterpriseform,
            'readonly': readonly,
            'is_innovation':is_innovation,
            'is_show':is_show,
            'project':project,
            'teammember':teammember,
            'pro_type':pro_type,
            'fin_type':fin_type,
            'innovation':innovation,
            'isRedirect':isRedirect,
            }

    return render(request, 'school/application.html', data)

@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER, STUDENT_USER)
@only_user_required
#@time_controller(phase=STATUS_MIDSUBMIT)
#TODO add time controller
def mid_report_view(request, pid = None, is_expired = False):
    """
    school mid report
    Arguments:
        In: id, it is project id
    """
    loginfo(p=pid+str(is_expired), label="in applicatioan")
    try:
        mid = get_object_or_404(MidSubmit, project_id=pid)
    except:
        mid = MidSubmit()
        mid.content_id = uuid.uuid4()
        mid.project_id = ProjectSingle.objects.get(project_id = pid)
        mid.save()

    is_show =  check_auth(user=request.user,authority=STUDENT_USER)
    readonly = check_history_readonly(pid) or is_expired
    if check_auth(user = request.user,authority = SCHOOL_USER):
        readonly = False

    # ... sb requirement
    readonly = False

    if request.method == "POST" and readonly is not True:
        role=check_is_audited(user=request.user,presubmit=mid,checkuser=SCHOOL_USER)
        mid_form = MidReportForm(request.POST, instance=mid)
        if mid_form.is_valid():
            mid_form.save()
            return HttpResponseRedirect(reverse('school.views.%s_view' % role))
        else:
            logger.info("Mid Form Valid Failed"+"**"*10)
            logger.info(mid_form.errors)
            logger.info("--"*10)
    else:
        mid_form = MidReportForm(instance=mid)

    data = {'pid': pid,
            'mid': mid_form,
            'readonly': readonly,
            'is_show':is_show,
            }

    return render(request, 'school/mid.html', data)

@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER, STUDENT_USER)
@only_user_required
@time_controller(phase=STATUS_FINSUBMIT)
def final_report_view(request, pid=None, is_expired=False):
    """
    school final report
    Arguments:
        In: id, it is project id
    """
    loginfo(p=pid+str(is_expired), label="in application")
    final = get_object_or_404(FinalSubmit, project_id=pid)
    is_show =  check_auth(user=request.user,authority=STUDENT_USER)
    readonly = check_history_readonly(pid) or is_expired
    if check_auth(user = request.user,authority = SCHOOL_USER):
        readonly = False

    # ... sb requirement
    readonly = False

    if request.method == "POST" and readonly is not True:
        role=check_is_audited(user=request.user,presubmit=final,checkuser=SCHOOL_USER)
        final_form = FinalReportForm(request.POST, instance=final)
        if final_form.is_valid():
            final_form.save()
            return HttpResponseRedirect(reverse('school.views.%s_view' % role))
        else:
            logger.info("Final Form Valid Failed"+"**"*10)
            logger.info(final_form.errors)
            logger.info("--"*10)

    final_form = FinalReportForm(instance=final)

    data = {'pid': pid,
            'final': final_form,
            'readonly': readonly,
            'is_show':is_show,
            }

    return render(request, 'school/final.html', data)


@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def statistics_view(request):
    """
    school statistics view
    """
    data = get_statistics_from_user(request.user)

    return render(request, 'school/statistics.html', data)


@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
@time_controller(phase=STATUS_PRESUBMIT)
def new_report_view(request, is_expired=False):
    """
    school start a new application report, then it will
    jump the real project URL.
    """
    if check_limits(request.user) and is_expired is False:
        # create a new project
        pid = uuid.uuid4()
        project = ProjectSingle()
        project.project_id = pid
        project.adminuser = request.user
        project.school = SchoolProfile.objects.get(userid=request.user).school
        project.year = get_current_year()
        project.project_grade = ProjectGrade.objects.get(grade=GRADE_UN)
        project.project_status = ProjectStatus.objects.get(status=STATUS_FIRST)
        project.save()

        # create presubmit and final report
        pre = PreSubmit()
        pre.content_id = uuid.uuid4()
        pre.project_id = project
        pre.save()
        
        #create mid report
        mid = MidSubmit()
        mid.content_id = uuid.uuid4()
        mid.project_id = project
        mid.save()

        #create final report
        final = FinalSubmit()
        final.content_id = uuid.uuid4()
        final.project_id = project
        final.save()

        return HttpResponseRedirect(reverse('school.views.application_report_view', args=(pid,)))
    else:
        return HttpResponseRedirect(reverse('school.views.home_view'))


@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def history_view(request):
    """
    school history report list
    """

    history_list = ProjectSingle.objects.filter(adminuser=request.user,is_over = True)

    page = request.GET.get('page')
    context = getContext(history_list, page, 'item', 0)
    return render(request, 'school/history.html', context)


@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER, STUDENT_USER)
@only_user_required
@time_controller(phase=STATUS_FINSUBMIT)
def file_view(request, pid=None, is_expired=False):
    """
    file management view
    """
    readonly = is_expired
    print readonly

    # ... sb requirement
    readonly = False

    is_show =  check_auth(user=request.user,authority=STUDENT_USER)
    if request.method == "POST" and readonly is not True:
        if request.FILES is not None:
            return upload_response(request, pid)

    file_history = UploadedFiles.objects.filter(project_id=pid)
    logger.info("**"*10)
    logger.info(file_history)

    data = {'pid': pid,
            'files': file_history,
            'readonly': readonly,
            'is_show':is_show,
            }

    return render(request, 'school/fileupload.html', data)


@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER, STUDENT_USER)
@only_user_required
@time_controller(phase=STATUS_FINSUBMIT)
def file_delete_view(request, pid=None, fid=None, is_expired=False):
    """
    file delete view
    """
    logger.info("delete files"+"**"*10)
    # check mapping relation
    f = get_object_or_404(UploadedFiles, file_id=fid)
    p = get_object_or_404(ProjectSingle, project_id=pid)

    logger.info(f.project_id.project_id)
    logger.info(p.project_id)

    if f.project_id.project_id != p.project_id:
        raise HttpResponseForbidden("Authority Failed!")

    # delete file
    if request.method == "POST":
        # delete record
        f.delete()
        return HttpResponse(str(fid))
    else:
        return HttpResponseBadRequest("Warning! Only POST accepted!")


@login_required
def non_authority_view(request):
    """
    cannot visit
    """
    #TODO: I will add more usefull information, such as control time
    return render(request, 'school/non_authority.html')


def AuthStudentExist(request, email):
    '''直接判断学生的邮箱存不存在即可
    '''
    if User.objects.filter(email=email).count():
        return True
    else:
        return False


@login_required
def Send_email_to_student(request, username, person_firstname,password, email, identity, financial_cate=FINANCIAL_CATE_UN):
    #判断用户名是否存在，存在的话直接返回
    loginfo(p=person_firstname, label="person_firstname")
    if not AuthStudentExist(request, email):
        user,send_mail_flag = RegistrationManager().create_inactive_user(request,username,person_firstname,password,email,identity)
        result = create_newproject(request=request, new_user=user, financial_cate=financial_cate,managername=person_firstname)
        return True and result and send_mail_flag
    else:
        return False


def Count_email_already_exist(request):
    school_staff = request.user
    school_profile = SchoolProfile.objects.get(userid = school_staff)
    num = StudentProfile.objects.filter(school = school_profile).filter(projectsingle__is_past = False).count()
    return num


def school_limit_num(request):
    try:
        limits = ProjectPerLimits.objects.get(school__userid=request.user)
    except:
        school = SchoolProfile.objects.get(userid=request.user)
        limits = ProjectPerLimits(school=school, number=0, a_cate_number=0)
    limit_num = limits.number
    return limit_num


def GetStudentRegisterList(request):
    school_staff = request.user
    school_profile = SchoolProfile.objects.get(userid = school_staff)
    students_list = [each.user for each in StudentProfile.objects.filter(school = school_profile)]
    return students_list


@login_required
def StudentDispatch(request):
    if request.method == "GET":
        student_form = StudentDispatchForm()
        email_list  = GetStudentRegisterList(request)
        email_num = Count_email_already_exist(request)
        limited_num = school_limit_num(request)
        remaining_activation_times = limited_num-email_num

        page = request.GET.get('page')
        context = getContext(email_list, page, 'item', 0)

        context.update({'student_form':student_form,'remaining_activation_times':remaining_activation_times})
        return render(request, "school/dispatch.html", context)

def check_is_audited(user,presubmit,checkuser):
    if check_auth(user=user, authority=checkuser):
        role = "home"
        presubmit.is_audited=True
    else:
        role = "student"
        presubmit.is_audited=False
    presubmit.save()
    return role

def current_list_add(list=None):
    for item in list:
        item.reg_email = item.student.user.username
        pid = item.project_id
        if item.project_category.category == CATE_INNOVATION:
            pre = get_object_or_404(PreSubmit, project_id=pid)
        else :
            pre = get_object_or_404(PreSubmitEnterprise, project_id=pid)
        final = get_object_or_404(FinalSubmit, project_id=pid)
        item.pre_isaudited = pre.is_audited
        item.final_isaudited = final.is_audited
    return list

@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def get_xls(request):
    file_path = info_xls(request)
    return redirect(MEDIA_URL + "tmp" + file_path[len(TMP_FILES_PATH):])


@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def auto_index(request):
    
    project_set = get_current_project_query_set().filter(adminuser = request.user)
    project_set = sorted(list(project_set), key = lambda x: (x.financial_category.category, x.project_code))
    

    for i in xrange(len(project_set)):
        project_set[i].project_code = "%d%s000%03d" % (get_current_year(), request.user, i)
        project_set[i].save()

    return HttpResponseRedirect(reverse('school.views.home_view'))
