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
from django.core.files.storage import default_storage

from school.models import ProjectSingle, PreSubmit, FinalSubmit,TechCompetition, OpenSubmit
from school.models import UploadedFiles
from adminStaff.models import ProjectPerLimits
from users.models import StudentProfile
from school.forms import *
from backend.fund import CFundManage

from const.models import *
from const import *

from school.utility import *
from backend.logging import logger, loginfo
from backend.decorators import *
from student.models import Student_Group,StudentWeeklySummary,Funds_Group
from student.forms import StudentGroupForm, StudentGroupInfoForm,ProcessRecordForm

from settings import IS_DLUT_SCHOOL, IS_MINZU_SCHOOL
#from student.utility import checkidentity

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
def home_view(request):
    """
    display project at the current year
    """
    delete_bad_files(request)
    item_list = get_running_project_query_set().filter(student__userid=request.user)
    #item_list = ProjectSingle.objects.filter(student__userid=request.user)
    return render(request, "student/student_home.html", {"item_list": item_list})


def delete_bad_files(request):
    """
    临时检查文件是否在服务器端已损毁
    若已损毁，则删除数据库对应记录
    """
    try:
        project = get_current_project_query_set().get(student__userid = request.user)   
        file_set = UploadedFiles.objects.filter(project_id = project)
        for f in file_set:
            if not default_storage.exists(f.file_obj.path):
                f.delete()
    except:
        pass

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
def member_change(request):
    """
    project group member change
    """
    student_account = StudentProfile.objects.get(userid = request.user)
    print student_account
    project = ProjectSingle.objects.get(student=student_account)
    student_group = Student_Group.objects.filter(project = project)
    lock = project.recommend or (project.project_grade.grade != GRADE_UN)
    files = set()
    for s in student_group:
        if s.scoreFile:
            files.add(s.scoreFile)
        s.sex_val = s.sex
        s.sex = s.get_sex_display()

    student_group_form = StudentGroupForm()
    student_group_info_form = StudentGroupInfoForm()
    return render(request, "student/member_change.html",
                  {"lock": lock,
                    "pid":project.project_id,
                    "files":files,
                   "student_group": student_group,
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
@time_controller(phase=STATUS_FINSUBMIT)
def open_report_view(request, pid = None, is_expired = False):
    data = open_report_view_work(request, pid, is_expired)
    if data['isRedirect'] :
        return HttpResponseRedirect( '/student/file_upload_view/' + str(pid) )
    else:
        return render(request, 'student/open.html', data)

def open_report_view_work(request, pid = None, is_expired = False):
    project = get_object_or_404(ProjectSingle, project_id=pid)
    readonly = get_opencheck_readonly(request,project)
    try:
        open_data = OpenSubmit.objects.get(project_id=pid)
    except:
        open_data = OpenSubmit()
        open_data.content_id = uuid.uuid4()
        open_data.project_id = project
        open_data.save()
    isRedirect = False
    if request.method == "POST" and readonly is not True:
        open_form = OpenReportForm(request.POST, instance=open_data)
        if open_form.is_valid():
            open_form.save()
            # project.project_status = ProjectStatus.objects.get(status=STATUS_FINSUBMIT)
            project.save()

            isRedirect = True
            # return HttpResponseRedirect(reverse('student.views.home_view'))
        else:
            logger.info(open_form.errors)
    else:
        open_form = OpenReportForm(instance=open_data)
    is_show =  check_auth(user=request.user,authority=STUDENT_USER)
    data = {'pid': pid,
            'open': open_form,
            'is_show': is_show,
            'readonly':readonly,
            'isRedirect': isRedirect,
            }
    return data

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
@only_user_required
def mid_report_view(request, pid = None, is_expired = False):
    data = mid_report_view_work(request, pid, is_expired)
    print data
    if data["isRedirect"]:
        return HttpResponseRedirect( '/student/file_upload_view/' + pid ) 
    else:
        return render(request, "student/mid.html", data)

def mid_report_view_work(request, pid = None, is_expired = False):
    """
    student mid report
    """
    project = get_object_or_404(ProjectSingle, project_id = pid)
    #readonly = get_opencheck_readonly(request,project)
    try:
        mid = get_object_or_404(MidSubmit, project_id = pid)
    except:
        mid = MidSubmit()
        mid.content_id = uuid.uuid4()
        mid.project_id = project
        mid.save()
    is_show =  check_auth(user=request.user,authority=STUDENT_USER)
    isRedirect = False
    if request.method == "POST" and readonly is not True:
        mid_form = MidReportForm(request.POST, instance = mid)
        if mid_form.is_valid():
            mid_form.save()
            project.save()
            isRedirect = True
        else:
            logger.info("Mid Form Valid Failed"+"**"*10)
            logger.info(mid_form.errors)
    else:
        mid_form = MidReportForm(instance = mid)

    data = {'pid': pid,
            'mid': mid_form,
            'readonly':False,
            'isRedirect': isRedirect,
            'is_show': is_show,
            }
    return data
@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
@only_user_required
@time_controller(phase=STATUS_FINSUBMIT)
def final_report_view(request, pid=None,is_expired=False):    
    data = final_report_view_work(request, pid, is_expired)
    if data['isRedirect'] :
        return HttpResponseRedirect( '/student/file_upload_view/' + str(pid) ) 
    else :         
        return render(request, 'student/final.html', data)


def final_report_view_work(request, pid=None,is_expired=False):

    """
    student final report
    Arguments:
        In: id, it is project id
    """

    loginfo(p=pid+str(is_expired), label="in application")
    final = get_object_or_404(FinalSubmit, project_id=pid)
    project = get_object_or_404(ProjectSingle, project_id=pid)
    is_finishing = check_finishingyear(project)
    over_status = project.over_status.status
   
    if check_auth(user=request.user,authority=STUDENT_USER):
        readonly = (over_status != OVER_STATUS_NOTOVER) or not is_finishing
    elif check_auth(user=request.user,authority=TEACHER_USER):
        readonly = (over_status != OVER_STATUS_NOTOVER) or not is_finishing
    elif check_auth(user=request.user,authority=ADMINSTAFF_USER):
        readonly = False
    elif check_auth(user=request.user,authority=SCHOOL_USER):
        readonly = not get_schooluser_project_modify_status(project)
    else :
        readonly = False

    isRedirect = False
    is_show =  check_auth(user=request.user,authority=STUDENT_USER)
    if request.method == "POST" and readonly is not True:
        final_form = FinalReportForm(request.POST, instance=final)
        if final_form.is_valid():
            final_form.save()
            project.project_status = ProjectStatus.objects.get(status=STATUS_FINSUBMIT)
            project.save()

            isRedirect = True
            # return HttpResponseRedirect(reverse('student.views.home_view'))
        else:
            pass
            logger.info("Final Form Valid Failed"+"**"*10)
            logger.info(final_form.errors)

    final_form = FinalReportForm(instance=final)
    # techcompetition_form = TechCompetitionForm(instance=techcompetition)

    data = {'pid': pid,
            'final': final_form,
            # 'techcompetition':techcompetition,
            'readonly':readonly,
            'isRedirect': isRedirect,
            'is_show': is_show,
            }
    return data


@csrf.csrf_protect
@login_required
#@authority_required(STUDENT_USER)
@only_user_required
@time_controller(phase=STATUS_PRESUBMIT)
def application_report_view(request,pid=None,is_expired=False):    
    data = application_report_view_work(request, pid, is_expired)
    if request.method == 'POST' and data['isRedirect'] :
        return HttpResponseRedirect( '/student/file_upload_view/' + str(pid) ) 
    else :         
        return render(request, 'student/application.html', data)




def application_report_view_work(request, pid=None, is_expired=False):
    """
        readonly determined by time
        is_show determined by identity 
        is_innovation determined by project_category
    """
    loginfo(p=pid+str(is_expired), label="in application")
    project = get_object_or_404(ProjectSingle, project_id=pid)
    is_currentyear = check_year(project)
    teammember=get_studentmessage(project)
    is_applying = check_applycontrol(project)
    pro_type = PreSubmit if project.project_category.category == CATE_INNOVATION else PreSubmitEnterprise
    try:
        innovation = pro_type.objects.get(project_id=project.project_id)
    except Exception, err:
        loginfo(p=err, label="get innovation")
        loginfo(p=project.project_category.category, label="project category")

    if check_auth(user=request.user,authority=STUDENT_USER):
        readonly = not is_applying or project.is_past    
    elif check_auth(user=request.user,authority=TEACHER_USER):
        readonly = not is_applying or project.is_past    
    elif check_auth(user = request.user, authority = ADMINSTAFF_USER):
        readonly = False
    elif check_auth(user = request.user, authority = SCHOOL_USER):
        readonly = not get_schooluser_project_modify_status(project)
    else:
        readonly = False

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

    isRedirect = False
    # print "^^^pre ^^^^^ " + str(pre.key_notes)
    



    teacher_enterpriseform=Teacher_EnterpriseForm(instance=teacher_enterprise)
    if request.method == "POST" and readonly is not True:
        info_form = InfoForm(request.POST,pid=pid,instance=project)
        application_form = iform(request.POST, instance=pre)
        if is_innovation == True:
            if info_form.is_valid() and application_form.is_valid():
                if save_application(project, pre, info_form, application_form, request.user):
                    project.project_status = ProjectStatus.objects.get(status=STATUS_PRESUBMIT)
                    project.save()
                    isRedirect = True
                    # print "lzlzlzlzl " + str(pre.key_notes)
                    # isRedirect = True
                    
            else:
                logger.info("Form Valid Failed"+"**"*10)
                logger.info(info_form.errors)
                logger.info(application_form.errors)
        else :
            teacher_enterpriseform=Teacher_EnterpriseForm(request.POST,instance=teacher_enterprise)
            if info_form.is_valid() and application_form.is_valid() and teacher_enterpriseform.is_valid():
                if save_enterpriseapplication(project, pre, info_form, application_form, teacher_enterpriseform,request.user):
                    project.project_status = ProjectStatus.objects.get(status=STATUS_PRESUBMIT)
                    project.save()
                    isRedirect = True
                    # isRedirect = True
                    # return (0, HttpResponseRedirect(reverse('student.views.home_view')))
            else:
                logger.info("info  application teacher Form Valid Failed"+"**"*10)
                logger.info(info_form.errors)
                logger.info(application_form.errors)
                logger.info(teacher_enterpriseform.errors)

    else:
        info_form = InfoForm(instance=project,pid=pid)
        application_form = iform(instance=pre)
        isRedirect = True
        # teacher_enterpriseform=Teacher_EnterpriseForm(instance=teacher_enterprise)



    data = {'pid': pid,
            'info': info_form,
            'application': application_form,
            'teacher_enterpriseform':teacher_enterpriseform,
            'readonly': readonly,
            'is_innovation':is_innovation,
            'is_show':is_show,
            'project':project,
            'teammember':teammember,
            'innovation':innovation,
            #lz add
            'isRedirect':isRedirect, 
            }
    return data


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
# @authority_required(STUDENT_USER)
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

# @csrf.csrf_protect
# @login_required
# @authority_required(STUDENT_USER)
# def files_important_view(request,pid=None,is_expired=False):
#     """
#     project group member change
#     """
#     data = files_important_view_work(request,pid)
#     return render(request, 'student/fileimportant.html', data)


# def files_important_view_work(request,pid):
#     error_flagset = fileupload_flag_init()

#     project = get_object_or_404(ProjectSingle, project_id=pid)
#     file_history = UploadedFiles.objects.filter(project_id=project.project_id)
#     file_history=enabledelete_file(file_history)
#     data = {'pid': pid,
#             'files': file_history,
#             'readonly': False,
#             'error_flagset':error_flagset,
#             'IS_DLUT_SCHOOL':IS_DLUT_SCHOOL,
#             'IS_MINZU_SCHOOL':IS_MINZU_SCHOOL,
#                         }
#     return data

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
@only_user_required
def file_upload_view(request,errortype=None,pid=None,is_expired=False):
    """
        file_upload_view
    """
    data = files_upload_view_work(request,pid,errortype)
    if data[0]:
        return data[1]
    else:
        data = data[1]

    return render(request, 'student/fileimportant.html', data)


def files_upload_view_work(request,pid=None,errortype=None):
    project = get_object_or_404(ProjectSingle, project_id=pid) 
    error_flagset = fileupload_flag_init()

    if request.method == "POST" :
        if request.FILES != {}:
            des_name=check_filename(errortype,error_flagset)
            if check_uploadfile_name(request,des_name):
                if errortype != 'show_other':
                   check_uploadfile_exist(des_name,pid)
                upload_response(request, pid)
                project_fileupload_flag(project,errortype)
                return (1,HttpResponseRedirect('/student/file_upload_view/' + str(pid)))
            else:
                set_error(error_flagset,errortype,True)

    file_history = UploadedFiles.objects.filter(project_id=pid)
    file_history=enabledelete_file(file_history)
    data = {'pid': pid,
            'files': file_history,
            'readonly': False,
            'error_flagset':error_flagset,
            'IS_DLUT_SCHOOL':IS_DLUT_SCHOOL,
            'IS_MINZU_SCHOOL':IS_MINZU_SCHOOL,
            }
    return (0,data)

@csrf.csrf_protect
@login_required
@authority_required(STUDENT_USER)
@only_user_required
def score_upload_view(request,pid=None):
    """
    score file upload
    """
    print "student_id=" + str(request.GET['student_id'])
    student_id = request.GET['student_id']
    project = get_object_or_404(ProjectSingle, project_id=pid)
    student_set = Student_Group.objects.filter(project = project)

    for student_temp in student_set:
        if str(student_temp.id) == student_id:
            student = student_temp
            break
    else:
        raise Http404

    loginfo(p=student,label="student")
    des_name = student.studentName + u'学分申请表'
    if request.method == "POST" :
        check_uploadfile_exist(des_name,pid)
        obj=upload_score_save_process(request,pid,des_name)
        student.scoreFile = obj
        student.save()
        project_fileupload_flag(project,'show_scoreapplication')
        return HttpResponseRedirect('/student/memberchange')




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
    ret = CFundManage.get_form_tabledata(project)
    return render(request, 'student/funds_change.html',ret)

def get_opencheck_readonly(request,project):
    if check_auth(user=request.user,authority=STUDENT_USER):
        readonly = project.is_past
    elif check_auth(user=request.user,authority=TEACHER_USER):
        readonly = project.is_past
    elif check_auth(user = request.user, authority = ADMINSTAFF_USER):
        readonly = False
    elif check_auth(user = request.user, authority = SCHOOL_USER):
        readonly = not get_schooluser_project_modify_status(project)
    elif check_auth(user = request.user, authority = EXPERT_USER):
        readonly = False
    else:
        readonly = False
    return readonly

