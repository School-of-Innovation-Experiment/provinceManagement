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
from adminStaff.forms import TeacherDispatchForm ,ExpertDispatchForm
from teacher.models import TeacherMonthComment
from student.models import  StudentWeeklySummary, Student_Group, Funds_Group
from const.models import *
from const import *
from django.db.models import Q

from school.utility import *
from backend.logging import logger, loginfo
from backend.decorators import *
from backend.fund import CFundManage
from adminStaff.views import AdminStaffService
from adminStaff.forms import FundsChangeForm,StudentNameForm
from student.models import Funds_Group

from settings import IS_MINZU_SCHOOL, IS_DLUT_SCHOOL


from school.forms import InfoForm, ApplicationReportForm, FinalReportForm,EnterpriseApplicationReportForm,TechCompetitionForm,Teacher_EnterpriseForm
from student.forms import StudentGroupForm, StudentGroupInfoForm,ProcessRecordForm
from student.views import application_report_view_work, final_report_view_work, mid_report_view_work, open_report_view_work
from adminStaff.views import member_change_work
from adminStaff.utility import file_download_gen
@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def member_change(request, pid):
    data = member_change_work(request, pid)
    return render(request, "school/member_change.html",data)


@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def open_report_view(request, pid=None):
    data = open_report_view_work(request, pid)
    return render(request, 'school/open.html', data)



@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def final_report_view(request, pid=None):
    data = final_report_view_work(request, pid)
    return render(request, 'school/final.html', data)

@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def mid_report_view(request, pid = None):
    data = mid_report_view_work(request, pid)
    return render(request, 'school/mid.html', data)

@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def application_report_view(request, pid=None):        
    data = application_report_view_work(request, pid)
    return render(request, 'school/application.html', data)

@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def home_view(request):
    context = projectListInfor(request)
    context["IS_MINZU_SCHOOL"] = IS_MINZU_SCHOOL
    context["IS_DLUT_SCHOOL"] = IS_DLUT_SCHOOL
    context["pro_list"] = is_showoverstatus(context["pro_list"])#添加是否显示结题的属性以及文件下载链接
    return render(request, "school/school_home.html",context)

@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def dispatch(request):
    teacher_form = TeacherDispatchForm()
    expert_form = ExpertDispatchForm()
    school = SchoolProfile.objects.get(userid=request.user)
    if not school:
        raise Http404
    email_list  = AdminStaffService.GetRegisterListBySchool(school)
    email_list.extend(AdminStaffService.GetRegisterExpertListBySchool(school))

    def unique(lst):
        keys = {}
        for item in lst:
            keys[item["email"]] = item
        return keys.values()
    email_list = unique(email_list)

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
    for p in teacher_list:
        if TeacherProjectPerLimits.objects.filter(teacher=p).count() == 0:
            newTeacherProjPerLimits = TeacherProjectPerLimits(
                teacher = p,
                number = 0)
            newTeacherProjPerLimits.save()
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
    subject_list = get_current_project_query_set().filter(school = school)
    #subject_list =  AdminStaffService.GetSubject_list(school)
    limit, remaining = get_recommend_limit(school)
    for subject in subject_list:
        student_group = Student_Group.objects.filter(project = subject) 
       # subject.members = ','.join([student.studentName for student in student_group])
        try:
            subject.members = student_group[0]
        except:
            pass
    undef_subject_list = filter(lambda x: (not x.recommend) and (x.project_grade.grade == GRADE_UN), subject_list)
    #未分级项目为未推荐and未分级的项目
    def_subject_list = filter(lambda x: (x.recommend) or (x.project_grade.grade != GRADE_UN), subject_list)
    # def_subject_list = filter(lambda x: x.project_grade.grade == GRADE_SCHOOL or x.project_grade.grade == GRADE_INSITUTE, subject_list)
    #已分级项目为所有划分为校级or学院级的项目
    #！！民族学院只含有学院级项目
    context = {'subject_list': subject_list,
               'undef_subject_list': undef_subject_list,
               'def_subject_list': def_subject_list,
               'subject_grade_form' : subject_grade_form,
               'readonly': readonly,
               'limit': limit,
               'remaining': remaining,
               'is_minzu_school': IS_MINZU_SCHOOL,
                }
    return render(request, "school/subject_rating.html",context)


@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
#@transaction.commit_on_success
#@time_controller(phase=STATUS_PRESUBMIT)
def NewSubjectAlloc(request, is_expired = False):
    exist_message = ''
    readonly = is_expired
    school = get_object_or_404(SchoolProfile, userid = request.user)
    subject_list = get_current_project_query_set().filter(school = school)
    #subject_list = AdminStaffService.GetSubject_list(school)
    expert_list = ExpertProfile.objects.filter(assigned_by_school = school)
    expert_list = get_alloced_num(expert_list, 0)
   
    alloced_subject_list = [subject for subject in subject_list if check_project_is_assign(subject)]
    unalloced_subject_list = [subject for subject in subject_list if not check_project_is_assign(subject)]
    context = {'subject_list': subject_list,
               'alloced_subject_list': alloced_subject_list,
               'unalloced_subject_list': unalloced_subject_list,
               'expert_list': expert_list,
               'exist_message': exist_message,
               'readonly': readonly,}
    return render(request, "school/project_alloc_new.html",context)


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
    # try
    over_notover_status = OverStatus.objects.get(status=OVER_STATUS_NOTOVER)
    grade_un = ProjectGrade.objects.get(grade=GRADE_UN)
    grade_school = ProjectGrade.objects.get(grade=GRADE_SCHOOL)
    pro_list=ProjectSingle.objects.filter(Q(school_id = school.id)&Q(over_status=over_notover_status)&(Q(project_grade=grade_un)|Q(project_grade=grade_school)))
    loginfo(p=pro_list,label="pro_list in school %s" % request.user)
    year_list=[]
    for pro_obj in pro_list :
        if pro_obj.year not in year_list :
            year_list.append(pro_obj.year)


    year_finishing_list = []
    schoolObj = SchoolProfile.objects.get(userid = request.user)    
    user = User.objects.get(id=schoolObj.userid_id)
    projectfinish = ProjectFinishControl.objects.filter(userid =user.id)
    for finishtemp in projectfinish :
        if finishtemp.project_year not in year_finishing_list:
            year_finishing_list.append(finishtemp.project_year)

    year_list = sorted(year_list)       
    year_finishing_list = sorted(year_finishing_list)

    havedata_p = True if year_list else False
    return render(request, "school/project_control.html",
                {   "is_applying":is_applying,
                    "is_finishing":is_finishing,
                    "year_list":year_list,
                    "havedata_p":havedata_p,
                    "year_finishing_list":year_finishing_list,
                })


@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def funds_manage(request):
    context = projectListInfor(request)
    context['pro_list'] = is_addFundDetail(context['pro_list'])
    return render_to_response("school/funds_manage.html",context,context_instance=RequestContext(request))

@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def funds_change(request,pid):
    project = ProjectSingle.objects.get(project_id = pid)
    ret = CFundManage.get_form_tabledata(project)
    ret['is_addFundDetail'] = get_schooluser_project_modify_status(project)
    return render(request,"school/funds_change.html",ret)
@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def record_view(request, pid):
    loginfo("record_view")
    comment_group       = TeacherMonthComment.objects.filter(project_id=pid).order_by("monthId")
    record_group        = StudentWeeklySummary.objects.filter(project=pid).order_by("weekId")
    data = {"record_group"  : record_group,
            "comment_group" : comment_group,
            }
    return render(request, 'school/processrecord.html',data)
@csrf.csrf_protect
def projectListInfor(request):
    school = SchoolProfile.objects.get(userid=request.user)
    if request.method =="POST":
        project_manage_form = forms.ProjectManageForm(request.POST,school=school)
        pro_list = projectFilterList(request,project_manage_form,school)
    else:
        project_manage_form = forms.ProjectManageForm(school=school)
        over_notover_status = OverStatus.objects.get(status=OVER_STATUS_NOTOVER)
        grade_un = ProjectGrade.objects.get(grade=GRADE_UN)
        grade_insitute = ProjectGrade.objects.get(grade=GRADE_INSITUTE)
        grade_school = ProjectGrade.objects.get(grade=GRADE_SCHOOL)
        pro_list=ProjectSingle.objects.filter(Q(school_id=school)&(Q(project_grade=grade_un)|Q(project_grade=grade_school)|Q(project_grade=grade_insitute)))
    if pro_list.count() != 0 or request.method == "POST":
        havedata_p = True
    else:
        havedata_p = False
    context = {
               'havedata_p': havedata_p,
               'pro_list': pro_list,
               'project_manage_form':project_manage_form
              }
    return context
@csrf.csrf_protect
def projectFilterList(request,project_manage_form,school):
    if project_manage_form.is_valid():
        project_grade = project_manage_form.cleaned_data["project_grade"]
        project_year =  project_manage_form.cleaned_data["project_year"]
        project_overstatus = project_manage_form.cleaned_data["project_overstatus"]
        project_teacher_student_name = project_manage_form.cleaned_data["teacher_student_name"]
        qset = AdminStaffService.get_filter(project_grade,project_year,project_overstatus,project_teacher_student_name)
        if qset :
           qset = reduce(lambda x, y: x & y, qset)
           pro_list = ProjectSingle.objects.filter(Q(school_id=school)).filter(qset)
        else:
           pro_list = ProjectSingle.objects.filter(Q(school_id=school))
    pro_list = pro_list.order_by('adminuser')
    return pro_list

@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def project_informationexport(request):
    return render(request, "school/project_informationexport.html",
                {

                })
@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def file_download(request,fileid = None,filename = None):
    response = file_download_gen(request,fileid,filename)
    return response