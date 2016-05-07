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
from school.forms import *
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
import math
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
    re_project = Re_Project_Expert.objects.filter(expert=expert, project__is_past=False).order_by("pass_p")
    total_num = re_project.count()
    scored_num = re_project.filter(pass_p=True).count()
    unscored_num = re_project.filter(pass_p=False).count()
    page = request.GET.get('page')
    context = getContext(re_project, page, 'item', 0)
    data = {'page': page,
            'total_num': total_num,
            'scored_num': scored_num,
            'unscored_num': unscored_num}
    context.update(data)
    return render(request, 'expert/home.html', context)


@csrf.csrf_protect
@login_required
@authority_required(EXPERT_USER)
def review_report_view(request, pid=None):
    """
    expert home management page
    """
    # get or check authorities
    expert = get_object_or_404(ExpertProfile, userid=request.user)
    project = get_object_or_404(ProjectSingle, project_id=pid)
    re_project = get_object_or_404(Re_Project_Expert, expert=expert, project=project)
    doc_list = UploadedFiles.objects.filter(project_id=pid)

    info_form = InfoForm(instance=re_project.project,pid=pid)
    logger.info(project.project_category.category)
    teacher_enterpriseform = None
    page = request.GET.get('page')
    if project.project_category.category == CATE_INNOVATION:
        is_innovation = True
        application = get_object_or_404(PreSubmit, project_id = pid)
        application_form = ApplicationReportForm(instance=application)
    else:
        is_innovation = False
        pre = get_object_or_404(PreSubmitEnterprise, project_id=pid)
        application_form = EnterpriseApplicationReportForm(instance=pre)
        teacher_enterprise = get_object_or_404(Teacher_Enterprise,id=pre.enterpriseTeacher_id)
        teacher_enterpriseform=Teacher_EnterpriseForm(instance=teacher_enterprise)
    for i, doc in enumerate(doc_list):
        doc.index = i + 1
    data = {
            "is_innovation": is_innovation,
            "pid": pid,
            "info": info_form,
            "application": application_form,
            "doc_list": doc_list,
            'teacher_enterpriseform':teacher_enterpriseform,
            'page':page,
            }

    return render(request, 'expert/review.html', data)

@csrf.csrf_protect
@login_required
@authority_required(EXPERT_USER)
def review_report_pass_p(request, pid, pass_p):
    proj = Re_Project_Expert.objects.filter(project=pid).get(expert__userid=request.user)
    proj.comments = u"已审核"
    try:
        pass_p = int(pass_p)
    except:
        pass_p = 0
    expert = get_object_or_404(ExpertProfile, userid=request.user)
    re_project = Re_Project_Expert.objects.filter(expert=expert)
    page = request.GET.get('page')
    proj_single = ProjectSingle.objects.get(project_id = pid)
    rate = SchoolRecommendRate.load().rate
    if expert.subject.category == "12":
        limitnum = int(math.ceil(re_project.count()*rate/100))
        really = re_project.filter(pass_p=True).count()
    else:
        if proj_single.financial_category.category == FINANCIAL_CATE_A:
            project_listA = re_project.filter(project__financial_category__category=FINANCIAL_CATE_A)
            limitnum = int(math.ceil(project_listA.count()*rate/100))
            really = project_listA.filter(pass_p=True).count()
        else:
            project_listA = re_project.filter(project__financial_category__category=FINANCIAL_CATE_B)
            limitnum = int(math.ceil(project_listA.count()*rate/100))
            really = project_listA.filter(pass_p=True).count()
    if pass_p and (limitnum > really):
        proj.pass_p = True
    else:
        proj.pass_p = False
    proj.save()
    url_str= '/expert/?page=%s'% page
    return HttpResponseRedirect(url_str)
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
