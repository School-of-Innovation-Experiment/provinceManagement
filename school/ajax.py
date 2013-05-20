# coding: UTF-8
'''
Created on 2013-4-17

@author: sytmac
'''

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from django.http import Http404
from school.models import ProjectSingle
from school.forms import StudentDispatchForm
from school.views import Send_email_to_student, Count_email_already_exist, school_limit_num
from const.models import SchoolDict, ProjectCategory, FinancialCategory, InsituteCategory
from const import *
import datetime
from backend.logging import logger, loginfo
from school.utility import *

@dajaxice_register
def  StudentDispatch(request, form):
    #dajax = Dajax()
    student_form =  StudentDispatchForm(deserialize_form(form))
    if student_form.is_valid():
        password = student_form.cleaned_data["student_password"]
        email = student_form.cleaned_data["student_email"]
        financial_cate = student_form.cleaned_data["proj_cate"]
        name = email
        if password == "":
            password = email.split('@')[0]
        #判断是否达到发送邮件的最大数量
        email_num = Count_email_already_exist(request)
        limited_num = school_limit_num(request)
        remaining_activation_times = limited_num-email_num
        if remaining_activation_times==0:
            message = u"已经达到最大限度，无权发送"
            return simplejson.dumps({'field':student_form.data.keys(), 'status':'1', 'remaining_activation_times':remaining_activation_times, 'message':message})
        else:
            if financial_cate == FINANCIAL_CATE_A:
                current_list = ProjectSingle.objects.filter(adminuser=request.user, year = get_current_year)
                limits = ProjectPerLimits.objects.get(school__userid=request.user)
                a_remainings = int(limits.a_cate_number) - len([project for project in current_list if project.financial_category.category == FINANCIAL_CATE_A])
                if a_remainings <= 0:
                    message = u"甲类项目达到最大限度，无权发送"
                    return simplejson.dumps({'field':student_form.data.keys(), 'status':'1', 'remaining_activation_times':remaining_activation_times, 'message':message})

            flag = Send_email_to_student(request, name, password, email,STUDENT_USER, financial_cate=financial_cate)
            if flag:
                message = u"发送邮件成功"
                remaining_activation_times -= 1
                return simplejson.dumps({'field':student_form.data.keys(), 'status':'1', 'message':message,'remaining_activation_times':remaining_activation_times})
            else:
                message = u"相同邮件已经发送，中断发送或发生内部错误"
                return simplejson.dumps({'field':student_form.data.keys(), 'status':'1', 'message':message,'remaining_activation_times':remaining_activation_times})
    else:
        return simplejson.dumps({'field':student_form.data.keys(),'error_id':student_form.errors.keys(),'message':u"输入有误,请检查邮箱的合法性"})

@dajaxice_register
def ProjCateChange(request, cate):
    #dajax = Dajax()
    try:
        project = ProjectSingle.objects.get(student__user=request.user)
        new_cate = ProjectCategory.objects.get(category=cate)
    except Exception, err:
        loginfo(p=err, label="change project cate")
        raise Http404
    project.project_category = new_cate
    project.save()
    return simplejson.dumps({"message": u"更新成功: %s" % new_cate})

@dajaxice_register
def ProjInsituteChange(request, cate):
    try:
        project = ProjectSingle.objects.get(student__user=request.user)
        new_cate = InsituteCategory.objects.get(category=cate)
    except Exception, err:
        loginfo(p=err, label="change project insitute")
        raise Http404
    project.insitute = new_cate
    project.save()
    return simplejson.dumps({"message": u"更新成功: %s" % new_cate})

@dajaxice_register
def FinancialCateChange(request, cate, pid):
    #dajax = Dajax()
    if cate == FINANCIAL_CATE_A:
        current_list = ProjectSingle.objects.filter(adminuser=request.user, year = get_current_year)
        limits = ProjectPerLimits.objects.get(school__userid=request.user)
        a_remainings = int(limits.a_cate_number) - len([project for project in current_list if project.financial_category.category == FINANCIAL_CATE_A])
        if a_remainings <= 0:
            return simplejson.dumps({"message":u"甲类项目数量超额"})
    try:
        project = ProjectSingle.objects.get(project_id=pid)
        new_cate = FinancialCategory.objects.get(category=cate)
    except Exception, err:
        loginfo(p=err, label="change financial cate")
        raise Http404
    project.financial_category = new_cate
    project.save()
    return simplejson.dumps({"message": u"更新成功: %s" % new_cate})


@dajaxice_register
def FileDeleteConsistence(request, pid, fid):
    """
    Delete files in history file list
    """
    logger.info("sep delete files"+"**"*10)
    # check mapping relation
    f = get_object_or_404(UploadedFiles, file_id=fid)
    p = get_object_or_404(ProjectSingle, project_id=pid)

    logger.info(f.project_id.project_id)
    logger.info(p.project_id)

    if f.project_id.project_id != p.project_id:
        return simplejson.dumps({"is_deleted": False,
                                 "message": "Authority Failed!!!"})

    if request.method == "POST":
        f.delete()
        return simplejson.dumps({"is_deleted": True,
                                 "message": "delete it successfully!",
                                 "fid": str(fid)})
    else:
        return simplejson.dumps({"is_deleted": False,
                                 "message": "Warning! Only POST accepted!"})
