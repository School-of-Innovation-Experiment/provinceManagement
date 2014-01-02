import datetime, os, sys, uuid

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.http import HttpResponseForbidden, Http404, HttpResponseBadRequest
from django.template import RequestContext

from backend.decorators import *
from const import *
from const.models import *
from users.models import TeacherProfile, StudentProfile
from teacher.models import TeacherMonthComment
from student.models import  StudentWeeklySummary,Funds_Group
from school.models import TeacherProjectPerLimits, ProjectSingle, PreSubmit, FinalSubmit,UploadedFiles
from student.forms import  ProcessRecordForm
from school.forms import *
from teacher.forms import   MonthCommentForm
from adminStaff.forms import StudentDispatchForm 
from registration.models import *
from teacher.utility import *
from school.utility import *
from adminStaff.views import AdminStaffService
from backend.fund import CFundManage

@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def home_view(request, is_expired = False):
    limited_num ,remaining_activation_times = get_limited_num_and_remaining_times(request)
    project_list = get_running_project_query_set().filter(adminuser__userid = request.user)
    #project_list = ProjectSingle.objects.filter(Q(adminuser__userid = request.user) & \
    #                                            Q(over_status__status = OVER_STATUS_NOTOVER))
    data = {
        "project_list": project_list,
        "limited_num": limited_num,
        "remaining_activation_times": remaining_activation_times,
        }
    return render(request, "teacher/home.html", data)

@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
@only_user_required
@time_controller(phase=STATUS_PRESUBMIT)
def application_report_view(request,pid=None,is_expired=False):
    loginfo(p=pid+str(is_expired), label="in application")
    project = get_object_or_404(ProjectSingle, project_id=pid)  
    is_currentyear = check_year(project)
    is_applying = check_applycontrol(project)  
    # readonly= is_expired or not is_currentyear or not is_applying
    readonly=  not is_applying
    if check_auth(user=request.user,authority=TEACHER_USER):
        is_show = False
    else:
        is_show = True


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
                    return HttpResponseRedirect(reverse('teacher.views.home_view'))
            else:
                logger.info("Form Valid Failed"+"**"*10)
                logger.info(info_form.errors)
                logger.info(application_form.errors)
                logger.info("--"*10)
        else :
            teacher_enterpriseform=Teacher_EnterpriseForm(request.POST,instance=teacher_enterprise)
            if info_form.is_valid() and application_form.is_valid() and teacher_enterpriseform.is_valid():
                if save_enterpriseapplication(project, pre, info_form, application_form, teacher_enterpriseform,request.user):
                    project.project_status = ProjectStatus.objects.get(status=STATUS_PRESUBMIT)
                    project.save()
                    return HttpResponseRedirect(reverse('teacher.views.home_view'))
            else:
                logger.info("Form Valid Failed"+"**"*10)
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
    return render(request, 'teacher/application.html', data)

@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
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
    is_finishing = check_finishingyear(project)
    over_status = project.over_status
    readonly = (over_status.status != OVER_STATUS_NOTOVER) or not is_finishing

    if request.method == "POST" and readonly is not True:
        final_form = FinalReportForm(request.POST, instance=final)
        if final_form.is_valid():
            final_form.save()
            project.project_status = ProjectStatus.objects.get(status=STATUS_FINSUBMIT)
            project.save()
            return HttpResponseRedirect(reverse('teacher.views.home_view'))
        else:
            logger.info("Final Form Valid Failed"+"**"*10)
            logger.info(final_form.errors)
            logger.info("--"*10)

    final_form = FinalReportForm(instance=final)

    data = {'pid': pid,
            'final': final_form,
            'readonly':readonly,
            }
    return render(request, 'teacher/final.html', data)

@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
@only_user_required
@time_controller(phase=STATUS_FINSUBMIT)
def file_view(request, pid=None,is_expired = False):
    """
    file management view
    """
    readonly = is_expired
    if request.method == "POST" :
        if request.FILES is not None:
            return upload_response(request, pid)

    file_history = UploadedFiles.objects.filter(project_id=pid)
    logger.info("**"*10)
    logger.info(file_history)

    data = {'pid': pid,
            'files': file_history,
            'readonly': readonly,
            }
    return render(request, 'teacher/fileupload.html', data)

@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
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

def Send_email_to_student(request, username, password, email, category,person_name, identity):
    """
    check the existence of user
    """
    if User.objects.filter(email = email).count() == 0:
        user = RegistrationManager().create_inactive_user(request, username, password, email, identity,student_user=True,person_name=person_name )
        result = create_newproject(request=request, new_user=user, category=category)
        return True and result
    else:
        return False


@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def StudentDispatch(request):
    if request.method == "GET":
        student_form = StudentDispatchForm()
        teacher_profile = TeacherProfile.objects.get(userid = request.user)
        email_list  = AdminStaffService.GetRegisterListByTeacher(teacher_profile)
        limited_num ,remaining_activation_times = get_limited_num_and_remaining_times(request)
        data = {
            'student_form': student_form,
            'email_list': email_list,
            'remaining_activation_times': remaining_activation_times
            }
        return render(request, 'teacher/dispatch.html', data)


@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
@only_user_required
@time_controller(phase=STATUS_FINSUBMIT)
def processrecord_view(request, pid=None,is_expired = False):
    """
    file management view
    """
    comment_group       = TeacherMonthComment.objects.filter(project=pid).order_by("monthId")
    record_group        = StudentWeeklySummary.objects.filter(project=pid).order_by("weekId")
    monthcomment_form   = MonthCommentForm()
    data = {"record_group"  : record_group,
            "comment_group" : comment_group,
            "monthcomment_form":monthcomment_form,
            }
    return render(request, 'teacher/processrecord.html',data)


@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def funds_manage(request):
    ret = AdminStaffService.projectListInfor(request,TEACHER_USER)
    return render(request, "teacher/funds_manage.html", ret)
@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def funds_view(request,pid):
    project = ProjectSingle.objects.get(project_id = pid)
    ret = CFundManage.get_form_tabledata(project)
    return render(request, 'teacher/funds_change.html',ret)

