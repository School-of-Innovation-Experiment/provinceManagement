# coding: UTF-8
'''
Created on 2013-04-02

@author: tianwei

Desc: Experts' view, includes home(manage), review report view
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

from school.models import *
from adminStaff.models import *
from users.models import *
from const.models import *
from const import *
from school.forms import InfoForm, ApplicationReportForm, FinalReportForm, EnterpriseApplicationReportForm
from expert.forms import *
from const import *
from school.utility import *
from backend.logging import logger, loginfo
from backend.decorators import *
from student.views import open_report_view_work
"""
About the decorators sequence, it will impact the the function squeneces,
the top will be called first!
"""


@csrf.csrf_protect
@login_required
@authority_required(EXPERT_USER)
def home_view(request):
    """
    expert home management page
    """
    expert = get_object_or_404(ExpertProfile, userid=request.user)
    re_project = Re_Project_Expert.objects.filter(expert=expert)
    
    school_project_list = Re_Project_Expert.objects.filter(Q(expert = expert) & Q(is_assign_by_adminStaff = False)&Q(project__is_past=False))
    adminStaff_project_list = Re_Project_Expert.objects.filter(Q(expert = expert) & Q(is_assign_by_adminStaff = True)&Q(project__is_past=False))
    
    for project in school_project_list:
        project.is_assigned_by_adminStaff = False

    for project in adminStaff_project_list:
        project.is_assigned_by_adminStaff = True
    #为project对象临时添加属性，方便之后Re_Project_Expert的获取

    data = {'school_list': school_project_list,
            'adminStaff_list': adminStaff_project_list,}

    return render(request, 'expert/home.html', data)


@csrf.csrf_protect
@login_required
@authority_required(EXPERT_USER)
def review_report_view(request):
    """
    expert home management page
    """
    # get or check authorities
    pid = request.GET.get('pid')
    flag = request.GET.get('flag') == 'True'
    expert = get_object_or_404(ExpertProfile, userid=request.user)
    project = get_object_or_404(ProjectSingle, project_id=pid)
    re_project = get_object_or_404(Re_Project_Expert, expert=expert, project=project, is_assign_by_adminStaff = flag)
    doc_list = UploadedFiles.objects.filter(project_id=pid)

    info_form = InfoForm(instance=re_project.project, pid=pid)
    if project.project_category.category == CATE_INNOVATION:
        is_innovation = True
        application = get_object_or_404(PreSubmit, project_id = pid)
        application_form = ApplicationReportForm(instance=application)
    else:
        is_innovation = False
        application = get_object_or_404(PreSubmitEnterprise, project_id = pid)
        application_form = EnterpriseApplicationReportForm(instance=application)

    if request.method == "POST":
        review_form = ReviewForm(request.POST, instance=re_project)
        if review_form.is_valid():
            review_form.save()
            #re_project.save()
            return HttpResponseRedirect(reverse('expert.views.home_view'))
        else:
            loginfo(p = review_form.errors)
            return HttpResponseRedirect(reverse('expert.views.home_view'))
    else:
        review_form = ReviewForm(instance=re_project)
    for i, doc in enumerate(doc_list):
        doc.index = i + 1


    open_data = open_report_view_work(request, pid)
    data = {
            "is_innovation": is_innovation,
            "pid": pid,
            "flag": flag,
            "info": info_form,
            "application": application_form,
            "review": review_form,
            "doc_list": doc_list,
            "open":open_data['open'],
            "readonly": open_data['readonly'],
            }

    return render(request, 'expert/review.html', data)

BUF_SIZE = 262144
def download_view(request, file_id=None):
    """
    download the file
    """
    def read_file(fn, buf_size = BUF_SIZE):
        f = open(fn, 'rb')
        while True:
            _c = f.read(buf_size)
            if _c:
                yield _c
            else:
                break
        f.close()
    doc = UploadedFiles.objects.get(file_id = file_id)
    doc_path = doc.file_obj.path
    response = HttpResponse(read_file(doc_path), content_type='application/vnd.ms-excel')  
    response['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(doc_path).encode("UTF-8")
    return response
