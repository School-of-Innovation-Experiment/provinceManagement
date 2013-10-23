# coding: UTF-8
'''
Created on 2013-03-29

@author: tianwei

Desc: Utility functions for school page
'''

import uuid
import os
import sys
import time
import datetime

from django.shortcuts import get_object_or_404         
from django.utils import simplejson
from django.http import HttpResponse
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.db.models import Count
from django.contrib.auth.models import User

from chartit import PivotDataPool, PivotChart

from school.models import *
from const.models import SchoolDict, ProjectCategory, InsituteCategory
from const.models import UserIdentity, ProjectGrade, ProjectStatus
from adminStaff.models import ProjectPerLimits
from users.models import SchoolProfile,AdminStaffProfile

from const import AUTH_CHOICES, VISITOR_USER
from const import PROJECT_CATE_CHOICES, CATE_UN
from const import PROJECT_GRADE_CHOICES, GRADE_UN,GRADE_PROVINCE,GRADE_NATION
from const import PROJECT_STATUS_CHOICES, STATUS_FIRST

from backend.utility import search_tuple
from backend.logging import logger,loginfo
from django.db.models import Q

def check_limits(user):
    """
    Check school limits of quota
    Arguments:
        In: user, it is request.user, user id
        Out: True or False
    """
    try:
        limits = ProjectPerLimits.objects.get(school__userid=user)
    except:
        limits = None

    currents = ProjectSingle.objects.filter(adminuser=user, year=get_current_year).count()
    total = limits.number if limits is not None else 0

    return True if total > currents else False

def check_project_is_assign(project, is_assign_by_adminStaff = False):
    """
    check a project is assign by someone
    """
    return Re_Project_Expert.objects.filter(Q(project = project) & 
                                   Q(is_assign_by_adminStaff = is_assign_by_adminStaff)).count()

def get_current_year():
    """
    Get current year
    Arguments:
        Out: current year
    """
    return datetime.datetime.today().year


def save_application(project=None, info_form=None, application_form=None, user=None):
    """
    Application Report Save
    Arguments:
        In:
            *pid, project id
            *info_form, ProjectSingle form
            *application_form, PreSubmit form
        Out:
            *True or False
    """
    if project is None or info_form is None or application_form is None:
        return False

    try:
        info = info_form.save(commit=False)
        info.save()

        application = application_form.save(commit=False)
        application.save()

        return True
    except Exception, err:
        logger.info("save process"+"**"*10)
        logger.info(err)
        logger.info("--"*10)
        return False

def get_recommend_limit(school = None, scale = 0.3):
    """
    get the limit of recommending the projects
    """
    import math
    project_list = ProjectSingle.objects.filter(school = school)
    limit = int(math.ceil(project_list.count() * scale)) # 向上取整
    print limit, '*' * 10
    used = project_list.filter(recommend = True).count()
    return limit, limit - used

def save_enterpriseapplication(project=None, info_form=None, application_form=None,teacher_enterpriseform=None, user=None):
    """
    Application Report Save
    Arguments:
        In:
            *pid, project id
            *info_form, ProjectSingle form
            *application_form, PreSubmit form
        Out:
            *True or False
    """
    if project is None or info_form is None or application_form is None or teacher_enterpriseform is None :
        return False

    try:
        info = info_form.save(commit=False)
        info.save()

        application = application_form.save(commit=False)
        application.save()

        teacher_enterprise=teacher_enterpriseform.save(commit=False)
        teacher_enterprise.save()

        return True
    except Exception, err:
        logger.info("save process"+"**"*10)
        logger.info(err)
        logger.info("--"*10)
        return False


def response_minetype(request):
    """
    File upload mine type escape
    """
    if "application/json" in request.META["HTTP_ACCEPT"]:
        return "application/json"
    else:
        return "text/plain"


class JSONResponse(HttpResponse):
    """Json response class"""
    def __init__(self, obj='', json_opts={}, mimetype="application/json",
                 *args, **kwargs):
        content = simplejson.dumps(obj, **json_opts)
        super(JSONResponse, self).__init__(content, mimetype, *args, **kwargs)


def upload_save_process(request, pid):
    """
        save file into local storage
    """
    f = request.FILES["file"]
    wrapper_f = UploadedFile(f)
    size = wrapper_f.file.size
    name, filetype = split_name(wrapper_f.name)

    obj = UploadedFiles()
    obj.name = name
    obj.project_id = ProjectSingle.objects.get(project_id=pid)
    obj.file_id = uuid.uuid4()
    obj.file_obj = f
    obj.uploadtime = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
    obj.file_type = filetype
    obj.file_size = size

    #TODO: we will check file type
    obj.file_type = filetype if filetype != " " else "unknown"
    obj.save()

    return obj


def upload_response(request, pid):
    """
        use AJAX to process file upload
    """
    obj = upload_save_process(request, pid)

    data = [{'name': obj.name,
             'size': obj.file_size,
             'delete_url': settings.FILE_DELETE_URL + \
                           str(pid) + "/" + str(obj.file_id),
             'delete_type': "POST",
             }]

    response = JSONResponse(data, {}, response_minetype(request))
    response["Content-Dispostion"] = "inline; filename=files.json"
    loginfo(p=response,label="response")
    return response


def split_name(name, sep="."):
    """
        split type and name in a filename
    """
    #name = str(name)
    if sep in name:
        f = name.split(sep)[0]
        t = name.split(sep)[1]
    else:
        f = name
        t = " "

    return (f, t)


def check_history_readonly(pid):
    """
    Check whether the project is real current year
    Arguments:
        In: pid, project_id
            history, "current" or "history"
        Out:a tuple
            readonly, True or False
    """
    project = get_object_or_404(ProjectSingle, project_id=pid)
    if project.year == get_current_year():
        readonly = False
    else:
        readonly = True

    return readonly

def get_current_gradecount(user,des_type):
    """
        get the number of current_grade
    """


def get_categorycount(user,des_type,current):
    """
        if current is True
            return current categorycount
        else
            return history categorycount
    """
    if current==True:
        statistics_number=ProjectSingle.objects.filter(adminuser=user,project_category__category=des_type,year=get_current_year).count()
    else:
        statistics_number=statistics_number=ProjectSingle.objects.filter(adminuser=user,project_category__category=des_type).exclude(year=get_current_year).count()
    return statistics_number

def get_gradecount(user,des_type,current):
    """
        if current is True
            return current gradecount
        else
            return history gradecount
    """
    if current==True:
        statistics_number=ProjectSingle.objects.filter(adminuser=user,project_grade__grade=des_type,year=get_current_year).count()
        return statistics_number
    else:
        statistics_number=ProjectSingle.objects.filter(adminuser=user,project_grade__grade=des_type).exclude(year=get_current_year()).count()
        return statistics_number

def get_real_category(category):
    """
        get real category
    """
    key = category[0] if category is not None else CATE_UN
    name = search_tuple(PROJECT_CATE_CHOICES ,key)
    logger.info("*"*10+name)
    return (name,category[1])


def get_trend_lines(user):
    """
    Get category datapool data fot datachartit
    Arguments:
        In: user
        Out: category_pies object
    """
    data = ProjectSingle.objects.filter(adminuser=user)

    ds = PivotDataPool(series=[{'options': {'source': data,
                                            'categories': ['year'],
                                            'legend_by':['project_category__category',]
                                            },
                                            'terms': {'number':Count('project_category'),
                                                }},
                            ],
                       )
    cht = PivotChart(datasource=ds,
                series_options=[{'options': {'type': 'column', 'stacking':True},
                                'terms': ['number']},
                               ],
                chart_options={'title': {'text': '历史数据统计'},
                                'xAxis':{
                                            'title':{'text': '年份'},
                                        },
                                'yAxis':{'title':{'text': '类别数量'},'allowDecimals':False},
                                }
                )
    return cht

def check_year(project):
    current_year = get_current_year()
    if project.year == current_year:
        return True
    else:
        return False

def check_finishingyear(project):
    """
       检查项目年份是否在结题的年份中
    """
    if project.project_grade == GRADE_UN:
        return False
    elif project.project_grade.grade == GRADE_NATION or project.project_grade.grade ==GRADE_PROVINCE:
        adminObj = AdminStaffProfile.objects.all()
        user = User.objects.get(id=adminObj[0].userid_id)
    else:
        schoolObj=SchoolProfile.objects.get(id=project.school_id)
        user = User.objects.get(id=schoolObj.userid_id)  
    projectcontrol_list=ProjectFinishControl.objects.filter(userid=user)
    year_list=get_yearlist(projectcontrol_list)
    if  project.year in year_list:
        return True
    else:
        return False


def check_applycontrol(project):
    """
        检查申报开关是否打开，打开返回True,否则返回False
    """
    school = SchoolProfile.objects.get(id=project.school_id)

    if school.is_applying :
        return True
    else : 
        return False

def get_yearlist(object_list):
    """
    返回年份列表
    """
    year_list=[]
    for pro_obj in object_list :
        if pro_obj.project_year not in year_list :
            year_list.append(pro_obj.project_year)
    return year_list

def check_uploadfile_name(request,des_name):
    f = request.FILES["file"]    
    wrapper_f = UploadedFile(f)
    name, filetype = split_name(wrapper_f.name)
    if des_name == name:
        return True
    else:
        return False

def check_uploadfile_exist(des_name,pid):
    """
    检查上传的文件中是否已存在相同名称的文件
    """
    try:
        check_obj=UploadedFiles.objects.get(project_id_id = pid,name=des_name)
        check_obj.delete()
        return True
    except:
        return False

def enabledelete_file(file_list):
    important_filelist=[u"申报书",u"中期检查表",u"结题验收表",u"项目汇编",u"学分申请表"]
    for temp in file_list:
        if temp.name in important_filelist:
            temp.enabledelete = False
        else :
            temp.enabledelete = True
    return file_list

def check_othername(request):
    f = request.FILES["file"]    
    wrapper_f = UploadedFile(f)
    name, filetype = split_name(wrapper_f.name)
    important_filelist=[u"申报书",u"中期检查表",u"结题验收表",u"项目汇编",u"学分申请表"]
    if name in important_filelist:
        return False
    else:
        return True

def is_showoverstatus(project_list):
    """
    判断项目级别，院级管理员对于校级以上项目没有改变结题状态的权限
    """
    for temp in project_list:
        if temp.project_grade.grade in (GRADE_PROVINCE,GRADE_NATION):
            temp.is_showoverstatus = False
        else:
            temp.is_showoverstatus = True
    return project_list