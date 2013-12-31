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

from settings import IS_MINZU_SCHOOL


from school.forms import InfoForm, ApplicationReportForm, FinalReportForm,EnterpriseApplicationReportForm,TechCompetitionForm,Teacher_EnterpriseForm
from student.forms import StudentGroupForm, StudentGroupInfoForm,ProcessRecordForm
@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def member_change(request, pid):
        """
        project group member change
        """
        print "fuck ***" 
        #student_account = StudentProfile.objects.get(userid = request.user)
        #project = ProjectSingle.objects.get(student=student_account)

        project = ProjectSingle.objects.get(project_id = pid) 

        student_group = Student_Group.objects.filter(project = project)

        for s in student_group:
            s.sex = s.get_sex_display()

        student_group_form = StudentGroupForm()
        student_group_info_form = StudentGroupInfoForm()
        return render(request, "school/member_change.html",
                      {"pid": pid,
                       "student_group": student_group,
                       "student_group_form": student_group_form,
                       "student_group_info_form": student_group_info_form})


@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def final_report_view(request, pid=None):
        """
        student final report
        Arguments:
            In: id, it is project id
        """
        is_expired=False
        loginfo(p=pid+str(is_expired), label="in application")
        final = get_object_or_404(FinalSubmit, project_id=pid)
        project = get_object_or_404(ProjectSingle, project_id=pid)
        #techcompetition=get_object_or_404(TechCompetition,project_id=final.content_id)
        is_finishing = check_finishingyear(project)
        over_status = project.over_status

        readonly = (over_status != OVER_STATUS_NOTOVER) or not is_finishing

        readonly = False
        print "mid" * 10
        if request.method == "POST" and readonly is not True:
            final_form = FinalReportForm(request.POST, instance=final)
            # techcompetition_form =
            if final_form.is_valid():
                print "$$$" * 20
                final_form.save()
                project.project_status = ProjectStatus.objects.get(status=STATUS_FINSUBMIT)
                project.save()
                #return HttpResponseRedirect(reverse('student.views.home_view'))
            else:
                logger.info("Final Form Valid Failed"+"**"*10)
                logger.info(final_form.errors)
                logger.info("--"*10)

        final_form = FinalReportForm(instance=final)
        #techcompetition_form = TechCompetitionForm(instance=techcompetition)

        data = {'pid': pid,
                'final': final_form,
              #   'techcompetition':techcompetition,
                'readonly':readonly,
                }
        print "end:" * 20 
        return render(request, 'school/final.html', data)


@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
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
        logger.info(readonly)

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
                    logger.info(" info  application Form Valid Failed"+"**"*10)
                    logger.info(info_form.errors)
                    logger.info(application_form.errors)
                    logger.info("--"*10)
            else :
                teacher_enterpriseform=Teacher_EnterpriseForm(request.POST,instance=teacher_enterprise)
                if info_form.is_valid() and application_form.is_valid() and teacher_enterpriseform.is_valid():
                    if save_enterpriseapplication(project, pre, info_form, application_form, teacher_enterpriseform,request.user):
                        project.project_status = ProjectStatus.objects.get(status=STATUS_PRESUBMIT)
                        project.save()
                else:
                    logger.info("info  application teacher Form Valid Failed"+"**"*10)
                    logger.info(info_form.errors)
                    logger.info(application_form.errors)
                    logger.info(teacher_enterpriseform.errors)
                    logger.info("--"*10)
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
        return render(request, 'school/application.html', data)



@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def member_change(request, pid):
        """
        project group member change
        """
        #student_account = StudentProfile.objects.get(userid = request.user)
        #project = ProjectSingle.objects.get(student=student_account)

        project = ProjectSingle.objects.get(project_id = pid) 

        student_group = Student_Group.objects.filter(project = project)

        readonly = not get_schooluser_project_modify_status(project)
        

        for s in student_group:
            s.sex = s.get_sex_display()

        student_group_form = StudentGroupForm()
        student_group_info_form = StudentGroupInfoForm()
        return render(request, "school/member_change.html",
                      {"pid": pid,
                       "student_group": student_group,
                       "student_group_form": student_group_form,
                       "student_group_info_form": student_group_info_form,
                       "readonly": readonly})


@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def final_report_view(request, pid=None):
        """
        student final report
        Arguments:
            In: id, it is project id
        """
        is_expired=False
        # loginfo(p=pid+str(is_expired), label="in application")

        final = get_object_or_404(FinalSubmit, project_id=pid)
        project = get_object_or_404(ProjectSingle, project_id=pid)
        #techcompetition=get_object_or_404(TechCompetition,project_id=final.content_id)
        is_finishing = check_finishingyear(project)
        over_status = project.over_status

        # readonly = (over_status != OVER_STATUS_NOTOVER) or not is_finishing

        # readonly = False
        readonly = not get_schooluser_project_modify_status(project)
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
        return render(request, 'school/final.html', data)


@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def application_report_view(request, pid=None):
        """
            readonly determined by time
            is_show determined by identity
            is_innovation determined by project_category
        """

        # loginfo(p=pid+str(is_expired), label="in application")
        project = get_object_or_404(ProjectSingle, project_id=pid) 

        readonly = not get_schooluser_project_modify_status(project)
        #if ok : readonly = False
        #else readonly = True


        is_currentyear = check_year(project)
        is_applying = check_applycontrol(project)
        #readonly= is_expired or (not is_currentyear) or (not is_applying)
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
        return render(request, 'school/application.html', data)



@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
def home_view(request):
    context = projectListInfor(request)
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
    havedata_p = True if year_list else False
    return render(request, "school/project_control.html",
                {   "is_applying":is_applying,
                    "is_finishing":is_finishing,
                    "year_list":year_list,
                    "havedata_p":havedata_p,
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
        qset = get_filter(project_grade,project_year,project_overstatus)
        if qset :
           qset = reduce(lambda x, y: x & y, qset)
           pro_list = ProjectSingle.objects.filter(Q(school_id=school)).filter(qset)
        else:
           pro_list = ProjectSingle.objects.filter(Q(school_id=school))
    pro_list = pro_list.order_by('adminuser')
    return pro_list
def get_filter(project_grade,project_year,project_overstatus):
    if project_grade == "-1":
        project_grade=''
    if project_year == '-1':
        project_year=''
    if project_overstatus == '-1':
        project_overstatus=''
    q1 = (project_year and Q(year=project_year)) or None
    q2 = (project_overstatus and Q(over_status__status=project_overstatus)) or None
    q3 = (project_grade and Q(project_grade__grade=project_grade)) or None
    qset = filter(lambda x: x != None, [q1, q2, q3])
    return qset
