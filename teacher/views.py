import datetime, os, sys, uuid

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.shortcuts import render_to_response
from django.shortcuts import render,redirect
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
from school.views import application_report_view_work, final_report_view_work, mid_report_view_work, open_report_view_work
from adminStaff.utility import file_download_gen

@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def home_view(request, is_expired = False):
    teacher_profile = TeacherProfile.objects.get(userid = request.user)
    """
    if len(teacher_profile.name.strip()) == 0 or len(teacher_profile.telephone.strip()) == 0 or len(teacher_profile.titles.strip()) == 0:
        return redirect("/settings/profile")
    else:
    """
    limited_num ,remaining_activation_times = get_limited_num_and_remaining_times(request)
    project_list_cur = get_running_project_query_set().filter(adminuser__userid = request.user,is_past = False)
    project_list_past = get_running_project_query_set().filter(adminuser__userid = request.user,is_past = True)
    for pro_obj in project_list_cur:
        add_fileurl(pro_obj)
    for pro_obj in project_list_past:
        add_fileurl(pro_obj)
    data = {
        "project_list_cur": project_list_cur,
        "project_list_past":project_list_past,
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
    data = application_report_view_work(request, pid, is_expired)
    if request.method == 'POST' and data['isRedirect'] :
        return HttpResponseRedirect('/teacher/')
    else :
        return render(request, 'teacher/application.html', data)


@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
@only_user_required
@time_controller(phase=STATUS_FINSUBMIT)
def open_report_view(request, pid=None,is_expired=False):
    data = open_report_view_work(request, pid, is_expired)
    if request.method == 'POST' and data['isRedirect'] :
        return HttpResponseRedirect('/teacher/')
    else :
        return render(request, 'teacher/open.html', data)



@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
@only_user_required
@time_controller(phase=STATUS_FINSUBMIT)
def final_report_view(request, pid=None,is_expired=False):
    data = final_report_view_work(request, pid, is_expired)
    if request.method == 'POST' and data['isRedirect'] :
        return HttpResponseRedirect('/teacher/')
    else :
        return render(request, 'teacher/final.html', data)

@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
@only_user_required
def mid_report_view(request,pid=None, is_expired=False):
    data = mid_report_view_work(request, pid, is_expired)
    if request.method == 'POST' and data['isRedirect'] :
        return HttpResponseRedirect('/teacher/')
    else :
        return render(request, 'teacher/mid.html', data)

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
    if User.objects.filter(username=username).count() == 0:
        try:
            user = RegistrationManager().create_inactive_user(
                request, username, password, email, identity,
                student_user=True, person_name=person_name)
        except Exception, e:
            logger.error(e)
            return False
        result = create_newproject(request=request, new_user=user,
                                   category=category)
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
        email_list = AdminStaffService.GetRegisterListByTeacher(teacher_profile)
        limited_num, remaining_activation_times = get_limited_num_and_remaining_times(request)
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
@csrf.csrf_protect
@login_required
@authority_required(TEACHER_USER)
def file_download(request,fileid = None):
    response = file_download_gen(request,fileid)
    return response
