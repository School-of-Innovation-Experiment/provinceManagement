# Create your views here.
from django.shortcuts import render

from django.contrib.auth.decorators import login_required
from backend.decorators import *
from const import *

@csrf.csrf_protect
@login_required
# @authority_required(STUDENT_USER)
def home_view(request):
    return render(request, "student/student_home.html", {})
@csrf.csrf_protect
@login_required
# @authority_required(STUDENT_USER)
def application_report_view(request,pid=None):
    pid=1;
    data = {
        'pid': pid,
    }
    return render(request, "student/application.html", data)

@csrf.csrf_protect
@login_required
# @authority_required(SCHOOL_USER)
# @only_user_required
# @time_controller(phase=STATUS_FINSUBMIT)
def final_report_view(request, pid=None, is_expired=False):
    """
    student final report
    Arguments:
        In: id, it is project id
    """

    data = {
            'pid': pid,
        }

    return render(request, 'student/final.html', data)

@csrf.csrf_protect
@login_required
# @authority_required(SCHOOL_USER)
# @only_user_required
# @time_controller(phase=STATUS_FINSUBMIT)
def file_view(request, pid=None, is_expired=False):
    """
    file management view
    """

    data = {
            'pid': pid,
        }

    return render(request, 'student/fileupload.html', data)

