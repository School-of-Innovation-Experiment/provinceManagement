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

from school.models import ProjectSingle, PreSubmit, FinalSubmit
from school.models import UploadedFiles
from adminStaff.models import ProjectPerLimits
from users.models import SchoolProfile
from school import forms
from student.models import Student_Group
from const.models import *
from const import *
from django.db.models import Q 

from school.utility import *
from backend.logging import logger, loginfo
from backend.decorators import *
from adminStaff.views import AdminStaffService
from adminStaff.forms import FundsChangeForm,StudentNameForm
from student.models import Funds_Group



@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def home_view(request):
    school = SchoolProfile.objects.get(userid=request.user)
    pro_list=ProjectSingle.objects.filter(Q(school_id=school)&(Q(project_grade=4)|Q(project_grade=6)))
    if request.method =="POST":
        project_manage_form = forms.ProjectManageForm(request.POST,school=school)
        if project_manage_form.is_valid():
            project_grade = project_manage_form.cleaned_data["project_grade"]
            project_year =  project_manage_form.cleaned_data["project_year"]
            project_isover = project_manage_form.cleaned_data["project_isover"]
            if project_grade == "-1":
                project_grade= ''
            if project_year == '-1':
                project_year=''
            if project_isover == '-1':
                project_isover=''

            loginfo(p=project_grade,label="project_grade")
            q1 = (project_year and Q(year=project_year)) or None
            q2 = (project_isover and Q(is_over=project_isover)) or None
            q3 = (project_grade and Q(project_grade__grade=project_grade)) or None
            qset = filter(lambda x: x != None, [q1, q2, q3])
            loginfo(p=qset,label="qset")
            if qset :
                qset = reduce(lambda x, y: x & y, qset)
                pro_list = ProjectSingle.objects.filter(Q(school_id=school)&(Q(project_grade=4)|Q(project_grade=6))).filter(qset)
                #.exclude(Q(project_grade__grade=GRADE_NATION) or Q(project_grade__grade=GRADE_PROVINCE) or Q(project_grade__grade=GRADE_UN))
            else:
                pro_list = ProjectSingle.objects.filter(Q(school_id=school)&(Q(project_grade=4)|Q(project_grade=6)))
    else:
        project_manage_form = forms.ProjectManageForm(school=school)

    context = {
                'pro_list': pro_list,
                'project_manage_form':project_manage_form
                }
    return render(request, "school/school_home.html",context)

@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def dispatch(request):
    teacher_form = forms.TeacherDispatchForm()
    expert_form = forms.ExpertDispatchForm()
    school = SchoolProfile.objects.get(userid=request.user)
    if not school:
        raise Http404

    email_list  = AdminStaffService.GetRegisterListBySchool(school)
    email_list.extend(AdminStaffService.GetRegisterExpertListBySchool(school))
    return render_to_response("school/dispatch.html",{'expert_form':expert_form, 'teacher_form':teacher_form, 'teacher_school' : school, 'email_list':email_list},context_instance=RequestContext(request))

@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def project_limitnumSettings(request):
    num_limit_form = forms.TeacherNumLimitForm(request=request)
    teacher_limit_num_list = teacherLimitNumList(request)
    context = {'num_limit_form': num_limit_form,
               'teacher_limit_num_list': teacher_limit_num_list}
    context.update(get_project_num_and_remaining(request))
    return render_to_response("school/projectlimitnumSettings.html",
                              context,
                              context_instance=RequestContext(request))

@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def get_project_num_and_remaining(request):
    teacher_list = TeacherProfile.objects.filter(school__userid=request.user)
    used_proj_num = sum([p.teacherprojectperlimits.number
                        for p in teacher_list \
                        if hasattr(p, 'teacherprojectperlimits')])

    try:
        limits = ProjectPerLimits.objects.get(school__userid=request.user)
    except Exception, err:
        logger.info(err)
        limits = None

    total = (limits and int(limits.number)) or 0
    remainings = (limits and (total - used_proj_num)) or 0
    context = dict((('projects_limit', total),
                    ('projects_remaining', remainings)))
    return context

def teacherLimitNumList(request):
    return TeacherProjectPerLimits.objects.filter(teacher__school__userid=request.user)

@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
@time_controller(phase=STATUS_FINSUBMIT)
def SubjectRating(request,is_expired=False):
    readonly=is_expired
    subject_grade_form = forms.SubjectGradeForm()
    school = SchoolProfile.objects.get(userid = request.user)
    subject_list =  AdminStaffService.GetSubject_list(school)
    limit, remaining = get_recommend_limit(school)
    for subject in subject_list:
        student_group = Student_Group.objects.filter(project = subject) 
       # subject.members = ','.join([student.studentName for student in student_group])
        try:
            subject.members = student_group[0]
        except:
            pass

    context = {'subject_list': subject_list,
               'subject_grade_form' : subject_grade_form,
               'readonly': readonly,
               'limit': limit,
               'remaining': remaining,
                }
    return render(request, "school/subject_rating.html",context)

@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
#@transaction.commit_on_success
#@time_controller(phase=STATUS_PRESUBMIT)
def SubjectAlloc(request, is_expired = False):
    exist_message = ''
    readonly = is_expired
    school = get_object_or_404(SchoolProfile, userid = request.user)
    subject_list = AdminStaffService.GetSubject_list(school)
    if request.method == "POST":
        try:
            obj = Project_Is_Assigned.objects.get(school=school)
            if obj.is_assigned_in_presubmit:
                pass
            else:
                expert_list = ExpertProfile.objects.filter(assigned_by_school = school)
                loginfo(p = expert_list, label = "hujun")
                if len(expert_list) == 0 or len(subject_list) == 0:
                    if not expert_list:
                        exist_message = '专家用户不存在或未激活，请确认已发送激活邮件并提醒专家激活'
                    else:
                        exist_message = '没有可分配的项目，无法进行指派'
                else:
                    re_dict = AdminStaffService.Assign_Expert_For_Subject(subject_list, expert_list)

                    for subject in re_dict.keys():
                        for expert in re_dict[subject]:
                            try:
                                re_project_expert = Re_Project_Expert.objects.get(project_id=subject.project_id, 
                                    expert_id=expert.id)
                                re_project_expert.delete()
                            except:
                                pass
                            finally:
                                Re_Project_Expert(project_id=subject.project_id, expert_id=expert.id).save() 
                    obj.is_assigned_in_presubmit = True
                    obj.save()
        except Project_Is_Assigned.DoesNotExist:
            obj = None
    return render_to_response("school/project_alloc.html",{'subject_list':subject_list,'exist_message':exist_message,'readonly':readonly},context_instance=RequestContext(request))

@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def project_control(request):
    school = SchoolProfile.objects.get(userid = request.user)
    is_applying = school.is_applying
    is_finishing = school.is_finishing
    pro_list=ProjectSingle.objects.filter(Q(school_id = school.id)&Q(is_over=False)&(Q(project_grade=6)|Q(project_grade=4)))
    year_list=[]
    for pro_obj in pro_list :
        if pro_obj.year not in pro_list :
            year_list.append(pro_obj.year)
            
    return render(request, "school/project_control.html",
                {   "is_applying":is_applying,
                    "is_finishing":is_finishing,
                    "year_list":year_list,
                })


@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def funds_manage(request):
    school = SchoolProfile.objects.get(userid = request.user)


    # pro_list=ProjectSingle.objects.filter(Q(school_id = school.id)&Q(is_over=False)&(Q(project_grade=6)|Q(project_grade=4)))


    subject_list =  AdminStaffService.GetSubject_list(school)

    for subject in subject_list:
        student_group = Student_Group.objects.filter(project = subject) 
       # subject.members = ','.join([student.studentName for student in student_group])
        try:
            subject.members = student_group[0]
        except:
            pass


    return render(request, "school/funds_manage.html",{'subject_list': subject_list})

@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def funds_change(request,pid):
        project = ProjectSingle.objects.get(project_id = pid)

        project_funds_list = Funds_Group.objects.filter(project_id = pid)
        fundsChange_group_form = FundsChangeForm();
        student_name_form = StudentNameForm(pid = pid);

        return_data = {
                        "project_funds_list":project_funds_list,
                        "fundsChange_group_form":fundsChange_group_form,
                        "student_name_form":student_name_form
                        } 

        return render(request,"school/funds_change.html",return_data)


