# Create your views here.
# coding: UTF-8
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


from const.models import *
from const import *

from school.utility import *
from backend.logging import logger, loginfo
from backend.decorators import *
from student.models import Student_Group,StudentWeeklySummary,Funds_Group
from student.forms import StudentGroupForm, StudentGroupInfoForm,ProcessRecordForm
#from student.utility import checkidentity

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
def home_view(request):
    """
    display project at the current year
    """
    item_list = ProjectSingle.objects.filter(student__userid=request.user)

    return render(request, "student/student_home.html", {"item_list": item_list})

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
def member_change(request):
    """
    project group member change
    """
    student_account = StudentProfile.objects.get(userid = request.user)
    project = ProjectSingle.objects.get(student=student_account)
    student_group = Student_Group.objects.filter(project = project)

    for s in student_group:
        s.sex = s.get_sex_display()

    student_group_form = StudentGroupForm()
    student_group_info_form = StudentGroupInfoForm()
    return render(request, "student/member_change.html",
                  {"student_group": student_group,
                   "student_group_form": student_group_form,
                   "student_group_info_form": student_group_info_form})


@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
def techcompetition(request):
    """
    display project at the current year
    """
    project = ProjectSingle.objects.get(student__userid=request.user,year=get_current_year)
    final = get_object_or_404(FinalSubmit, project_id=project.project_id)
    techcompetition_group=TechCompetition.objects.filter(project_id=final.content_id)
    techcompetitionnumber=len(techcompetition_group)
    return render(request, "student/techcompetition.html", {"techcompetition_group": techcompetition_group,"techcompetitionnumber":techcompetitionnumber})

@csrf.csrf_protect
@login_required
@authority_required(SCHOOL_USER)
# @time_controller(phase=STATUS_PRESUBMIT)
def new_techcompetition(request):
    # create a new project
    content_id = uuid.uuid4()
    project = ProjectSingle.objects.get(student__userid=request.user,year=get_current_year)
    final = get_object_or_404(FinalSubmit, project_id=project.project_id)
    project = TechCompetition()
    project.content_id = contentid
    project.project_id = final.content_id
    project.save()
    return HttpResponseRedirect(reverse('student.views.techcompetition_detail', args=(pid,)))

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
def techcompetition_detail(request,pid=None):
    """
    project group techcompetition
    """
    techcompetition=get_object_or_404(TechCompetition,project_id=pid)


    techcompetition_form = TechCompetitionForm(instance=techcompetition)
    return render(request, "student/techcompetition_detail.html",
                  {"techcompetition": techcompetition,
                   "techcompetition_form": techcompetition_form})

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
@only_user_required
@time_controller(phase=STATUS_PRESUBMIT)
def application_report_view(request,pid=None,is_expired=False):
    """
        readonly determined by time
        is_show determined by identity 
        is_innovation determined by project_category
    """
    loginfo(p=pid+str(is_expired), label="in application")
    project = get_object_or_404(ProjectSingle, project_id=pid) 
    is_currentyear = check_year(project)
    is_applying = check_applycontrol(project)
    readonly= is_expired or (not is_currentyear) or (not is_applying)
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
                logger.info("form")
                if save_application(project, info_form, application_form, request.user):
                    project.project_status = ProjectStatus.objects.get(status=STATUS_PRESUBMIT)
                    project.save()
                    return HttpResponseRedirect(reverse('student.views.home_view'))
            else:
                logger.info(" info  application Form Valid Failed"+"**"*10)
                logger.info(info_form.errors)
                logger.info(application_form.errors)
                logger.info("--"*10)
        else :
            teacher_enterpriseform=Teacher_EnterpriseForm(request.POST,instance=teacher_enterprise)
            if info_form.is_valid() and application_form.is_valid() and teacher_enterpriseform.is_valid():
                if save_enterpriseapplication(project, info_form, application_form, teacher_enterpriseform,request.user):
                    project.project_status = ProjectStatus.objects.get(status=STATUS_PRESUBMIT)
                    project.save()
                    return HttpResponseRedirect(reverse('student.views.home_view'))
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
            'is_show':is_show
            }
    return render(request, 'student/application.html', data)


@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
@only_user_required
@time_controller(phase=STATUS_FINSUBMIT)
def final_report_view(request, pid=None,is_expired=False):
    """
    student final report
    Arguments:
        In: id, it is project id
    """
    loginfo(p=pid+str(is_expired), label="in application")
    final = get_object_or_404(FinalSubmit, project_id=pid)
    project = get_object_or_404(ProjectSingle, project_id=pid)
    # techcompetition=get_object_or_404(TechCompetition,project_id=final.content_id)
    is_finishing = check_finishingyear(project)
    over_status = project.over_status

    readonly = (over_status.status != OVER_STATUS_NOTOVER) or not is_finishing
    if request.method == "POST" and readonly is not True:
        final_form = FinalReportForm(request.POST, instance=final)
        # techcompetition_form =
        if final_form.is_valid():
            final_form.save()
            project.project_status = ProjectStatus.objects.get(status=STATUS_FINSUBMIT)
            project.save()
            return HttpResponseRedirect(reverse('student.views.home_view'))
        else:
            logger.info("Final Form Valid Failed"+"**"*10)
            logger.info(final_form.errors)
            logger.info("--"*10)

    final_form = FinalReportForm(instance=final)
    # techcompetition_form = TechCompetitionForm(instance=techcompetition)

    data = {'pid': pid,
            'final': final_form,
            # 'techcompetition':techcompetition,
            'readonly':readonly,
            }
    return render(request, 'student/final.html', data)

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
@only_user_required
@time_controller(phase=STATUS_FINSUBMIT)
def file_view(request, pid=None,is_expired = False):
    """
    file management view
    """
    # readonly = is_expired
    if request.method == "POST" :
        if request.FILES is not None:
            loginfo(p=request.FILES,label="request.FILES")
            return upload_response(request, pid)

    file_history = UploadedFiles.objects.filter(project_id=pid)
    logger.info("**"*10)
    logger.info(file_history)

    data = {'pid': pid,
            'files': file_history,
            'readonly': False,
            }
    return render(request, 'student/fileupload.html', data)

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
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

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
def files_important_view(request):
    """
    project group member change
    """
    show_applicationwarn = False
    show_interimchecklist = False
    show_summary = False
    show_projectcompilation = False
    show_scoreapplication = False
    show_other = False
    student_account = StudentProfile.objects.get(userid = request.user)
    project = ProjectSingle.objects.get(student=student_account)
    file_history = UploadedFiles.objects.filter(project_id=project.project_id)
    logger.info("**"*10)
    logger.info(file_history)
    pid=project.project_id
    file_history=enabledelete_file(file_history)
    data = {'pid': pid,
            'files': file_history,
            'readonly': False,
            'show_applicationwarn':show_applicationwarn,
            'show_interimchecklist':show_interimchecklist,
            'show_summary':show_summary,
            'show_projectcompilation':show_projectcompilation,
            'show_scoreapplication':show_scoreapplication,
            'show_other':show_other
            }
    return render(request, 'student/fileimportant.html', data)

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
@only_user_required
def file_application_view(request,pid):
    project = get_object_or_404(ProjectSingle, project_id=pid) 
    show_applicationwarn = False
    show_interimchecklist = False
    show_summary = False
    show_projectcompilation = False
    show_scoreapplication = False
    show_other = False
    if request.method == "POST" :
            if request.FILES != {}:
                loginfo(p=request.FILES,label="request.FILES")
                des_name=u"申报书"
                loginfo(p=des_name,label="des_name")
                check_uploadfile_exist(des_name,pid)
                if check_uploadfile_name(request,des_name):
                    upload_response(request, pid)
                    project.file_application = True
                    project.save()
                else:
                    show_applicationwarn = True

    file_history = UploadedFiles.objects.filter(project_id=pid)
    file_history=enabledelete_file(file_history)
    logger.info("**"*10)
    logger.info(file_history)
    data = {'pid': pid,
            'files': file_history,
            'readonly': False,
            'show_applicationwarn':show_applicationwarn,
            'show_interimchecklist':show_interimchecklist,
            'show_summary':show_summary,
            'show_projectcompilation':show_projectcompilation,
            'show_scoreapplication':show_scoreapplication,
            'show_other':show_other
            }
    return render(request, 'student/fileimportant.html', data)

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
@only_user_required
def file_interimchecklist_view(request,pid):
    project = get_object_or_404(ProjectSingle, project_id=pid) 
    show_applicationwarn = False
    show_interimchecklist = False
    show_summary = False
    show_projectcompilation = False
    show_scoreapplication = False
    show_other = False
    if request.method == "POST" :
            if request.FILES != {}:
                loginfo(p=request.FILES,label="request.FILES")
                des_name=u"中期检查表"
                check_uploadfile_exist(des_name,pid)
                if check_uploadfile_name(request,des_name):
                    upload_response(request, pid)
                    project.file_interimchecklist = True
                    project.save()
                else:
                    show_interimchecklist = True

    file_history = UploadedFiles.objects.filter(project_id=pid)
    file_history=enabledelete_file(file_history)
    logger.info("**"*10)
    logger.info(file_history)
    data = {'pid': pid,
            'files': file_history,
            'readonly': False,
            'show_applicationwarn':show_applicationwarn,
            'show_interimchecklist':show_interimchecklist,
            'show_summary':show_summary,
            'show_projectcompilation':show_projectcompilation,
            'show_scoreapplication':show_scoreapplication,
            'show_other':show_other
            }
    return render(request, 'student/fileimportant.html', data)

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
@only_user_required
def file_summary_view(request,pid):
    project = get_object_or_404(ProjectSingle, project_id=pid) 
    show_applicationwarn = False
    show_interimchecklist = False
    show_summary = False
    show_projectcompilation = False
    show_scoreapplication = False
    show_other = False
    if request.method == "POST" :
            if request.FILES != {}:
                loginfo(p=request.FILES,label="request.FILES")
                des_name=u"结题验收表"
                check_uploadfile_exist(des_name,pid)
                if check_uploadfile_name(request,des_name):
                    upload_response(request, pid)
                    project.file_summary = True
                    project.save()
                else:
                    show_summary = True

    file_history = UploadedFiles.objects.filter(project_id=pid)
    file_history=enabledelete_file(file_history)
    logger.info("**"*10)
    logger.info(file_history)
    data = {'pid': pid,
            'files': file_history,
            'readonly': False,
            'show_applicationwarn':show_applicationwarn,
            'show_interimchecklist':show_interimchecklist,
            'show_summary':show_summary,
            'show_projectcompilation':show_projectcompilation,
            'show_scoreapplication':show_scoreapplication,
            'show_other':show_other
            }
    return render(request, 'student/fileimportant.html', data)

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
@only_user_required
def file_projectcompilation_view(request,pid):
    project = get_object_or_404(ProjectSingle, project_id=pid) 
    show_applicationwarn = False
    show_interimchecklist = False
    show_summary = False
    show_projectcompilation = False
    show_scoreapplication = False
    show_other = False
    if request.method == "POST" :
            if request.FILES != {}:
                loginfo(p=request.FILES,label="request.FILES")
                des_name=u"项目汇编"
                check_uploadfile_exist(des_name,pid)               
                if check_uploadfile_name(request,des_name):
                    upload_response(request, pid)
                    project.file_projectcompilation = True
                    project.save()
                else:
                    show_projectcompilation = True

    file_history = UploadedFiles.objects.filter(project_id=pid)
    file_history=enabledelete_file(file_history)
    logger.info("**"*10)
    logger.info(file_history)
    data = {'pid': pid,
            'files': file_history,
            'readonly': False,
            'show_applicationwarn':show_applicationwarn,
            'show_interimchecklist':show_interimchecklist,
            'show_summary':show_summary,
            'show_projectcompilation':show_projectcompilation,
            'show_scoreapplication':show_scoreapplication,
            'show_other':show_other
            }
    return render(request, 'student/fileimportant.html', data)

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
@only_user_required
def file_scoreapplication_view(request,pid):
    project = get_object_or_404(ProjectSingle, project_id=pid) 
    show_applicationwarn = False
    show_interimchecklist = False
    show_summary = False
    show_projectcompilation = False
    show_scoreapplication = False
    show_other = False
    if request.method == "POST" :
            if request.FILES != {}:
                loginfo(p=request.FILES,label="request.FILES")
                des_name=u"学分申请表"
                check_uploadfile_exist(des_name,pid)               
                if check_uploadfile_name(request,des_name):
                    upload_response(request, pid)
                    project.score_application = True
                    project.save()
                else:
                    show_scoreapplication = True

    file_history = UploadedFiles.objects.filter(project_id=pid)
    file_history=enabledelete_file(file_history)
    logger.info("**"*10)
    logger.info(file_history)
    data = {'pid': pid,
            'files': file_history,
            'readonly': False,
            'show_applicationwarn':show_applicationwarn,
            'show_interimchecklist':show_interimchecklist,
            'show_summary':show_summary,
            'show_projectcompilation':show_projectcompilation,
            'show_scoreapplication':show_scoreapplication,
            'show_other':show_other
            }
    return render(request, 'student/fileimportant.html', data)

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
@only_user_required
def file_other_view(request,pid):
    project = get_object_or_404(ProjectSingle, project_id=pid) 
    show_applicationwarn = False
    show_interimchecklist = False
    show_summary = False
    show_projectcompilation = False
    show_scoreapplication = False
    show_other = False
    if request.method == "POST" :
            if request.FILES != {}:
                loginfo(p=request.FILES,label="request.FILES")
                if check_othername(request):            
                    upload_response(request, pid)
                else:
                    show_other = True

    file_history = UploadedFiles.objects.filter(project_id=pid)
    file_history=enabledelete_file(file_history)
    logger.info("**"*10)
    logger.info(file_history)
    data = {'pid': pid,
            'files': file_history,
            'readonly': False,
            'show_applicationwarn':show_applicationwarn,
            'show_interimchecklist':show_interimchecklist,
            'show_summary':show_summary,
            'show_projectcompilation':show_projectcompilation,
            'show_scoreapplication':show_scoreapplication,
            'show_other':show_other
            }
    return render(request, 'student/fileimportant.html', data)

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
def processrecord_view(request):
    student_account = StudentProfile.objects.get(userid = request.user)
    project         = ProjectSingle.objects.get(student=student_account)
    record_group    = StudentWeeklySummary.objects.filter(project = project).order_by("weekId")
    processRecord_group_form = ProcessRecordForm()
    data = {"record_group": record_group,
            "processRecord_group_form":processRecord_group_form
            }
    return render(request, 'student/processrecord.html',data)

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
def funds_view(request):
    student_account = StudentProfile.objects.get(userid = request.user)
    project         = ProjectSingle.objects.get(student=student_account)
    funds_group     = Funds_Group.objects.filter(project_id = project)

    return render(request, 'student/funds_view.html',{"funds_list":funds_group})



