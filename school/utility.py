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

from chartit import PivotDataPool, PivotChart

from school.models import *
from const.models import SchoolDict, ProjectCategory, InsituteCategory
from const.models import UserIdentity, ProjectGrade, ProjectStatus
from adminStaff.models import ProjectPerLimits
from users.models import SchoolProfile

from const import *
from const.models import *

from backend.utility import search_tuple

from backend.logging import logger, loginfo


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

        logger.info("save succes")
        return True
    except Exception, err:
        logger.info("save process"+"**"*10)
        logger.info(err)
        logger.info("--"*10)
        return False

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
        logger.info("save succes")
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
                chart_options={'title': {'text': u'历史数据统计'},
                                'xAxis':{
                                            'title':{'text': u'年份'},
                                        },
                                'yAxis':{'title':{'text': u'类别数量'},'allowDecimals':False},
                                }
                )
    return cht


def get_grade_lines(user):
    """
    Get category datapool data fot datachartit
    Arguments:
        In: user
        Out: grade_pies object
    """
    data = ProjectSingle.objects.filter(adminuser=user)

    ds = PivotDataPool(series=[{'options': {'source': data,
                                            'categories': ['year'],
                                            'legend_by':['project_grade__grade',]
                                            },
                                            'terms': {'number':Count('project_grade'),
                                                }},
                            ],
                       )
    cht = PivotChart(datasource=ds,
                series_options=[{'options': {'type': 'column', 'stacking':False},
                                'terms': ['number']},
                               ],
                chart_options={'title': {'text': u'历史数据统计'},
                                'xAxis':{
                                            'title':{'text': u'年份'},
                                        },
                                'yAxis':{'title':{'text': u'获奖评级'},'allowDecimals':False},
                                }
                )
    return cht


def get_statistics_from_user(user):
    """
    Get statistics infomation by user, the user it request.user

    Args:
        In: user, it is request user
        Out: data, it is a dict for statistics
    """
    if user is None:
        raise Http404

    trend_lines = get_trend_lines(user)
    grade_lines = get_grade_lines(user)
    current_numbers = len(ProjectSingle.objects.filter(adminuser=user, year=get_current_year))
    currentnation_numbers = get_gradecount(user, GRADE_NATION, True)
    currentprovince_numbers = get_gradecount(user, GRADE_PROVINCE, True)

    history_numbers = len(ProjectSingle.objects.filter(adminuser=user).exclude(year=get_current_year))
    historynation_numbers = get_gradecount(user, GRADE_NATION, False)
    historyprovince_numbers = get_gradecount(user, GRADE_PROVINCE, False)

    innovation_numbers = get_categorycount(user, CATE_INNOVATION, True)
    enterprise_numbers = get_categorycount(user, CATE_ENTERPRISE, True)
    enterprise_ee_numbers = get_categorycount(user, CATE_ENTERPRISE_EE, True)

    school_name = SchoolProfile.objects.get(userid=user).school.schoolName

    data = {"innovation_numbers": innovation_numbers,
            "enterprise_numbers": enterprise_numbers,
            "enterprie_ee_numbers": enterprise_ee_numbers,
            "current_numbers": current_numbers,
            "currentprovince_numbers": currentprovince_numbers,
            "currentnation_numbers": currentnation_numbers,
            "history_numbers": history_numbers,
            "historynation_numbers": historynation_numbers,
            "historyprovince_numbers": historyprovince_numbers,
            "school_name": school_name,
            "charts": [trend_lines, grade_lines]
            }

    return data


def map_school_name(school_id):

    name = SchoolDict.objects.get(id=school_id[0]).schoolName

    return (name,)


def get_province_trend_lines():
    """
    Get category datapool data fot datachartit
    Arguments:
        In: user
        Out: school numbers object
    """
    data = ProjectSingle.objects.all()

    ds = PivotDataPool(series=[{'options': {'source': data,
                                            'categories': ['school__id'],
                                            'legend_by':['project_grade__grade',]
                                            },
                                            'terms': {'number': Count('project_grade'),
                                                }},
                            ],
                        sortf_mapf_mts=(None, map_school_name, True)
                       )
    cht = PivotChart(datasource=ds,
            series_options=[{'options': {'type': 'column', 'stacking':True},
                                'terms': ['number']},
                               ],
                chart_options={'title': {'text': '学校-评级数据统计'},
                                'xAxis':{
                                            'title':{'text': '参赛学校'},
                                        },
                                'yAxis':{'title':{'text': '评级数量'},'allowDecimals':False},
                                }
                )
    return cht



def create_newproject(request, new_user, financial_cate=FINANCIAL_CATE_UN):
    """
    create a new project for this usr, it is student profile
    """
    #TODO: add some necessary decorators

    student = get_object_or_404(StudentProfile, user=new_user)

    try:
        pid = uuid.uuid4()
        project = ProjectSingle()
        project.project_id = pid
        project.adminuser = request.user
        project.student = student
        project.school = student.school.school
        project.year = get_current_year()
        project.project_grade = ProjectGrade.objects.get(grade=GRADE_UN)
        project.project_status = ProjectStatus.objects.get(status=STATUS_FIRST)
        project.project_category = ProjectCategory.objects.all()[0]
        project.insitute = InsituteCategory.objects.all()[0]
        project.financial_category= FinancialCategory.objects.get(category=financial_cate)
        project.save()

        # create presubmit and final report
        pre = PreSubmit()
        pre.content_id = uuid.uuid4()
        pre.project_id = project
        pre.save()

        # create presubmit and final report
        enterpriseTeacher = Teacher_Enterprise()
        enterpriseTeacher.save()
        pre = PreSubmitEnterprise()
        pre.enterpriseTeacher = enterpriseTeacher
        pre.content_id = uuid.uuid4()
        pre.project_id = project
        pre.save()

        #create final report
        final = FinalSubmit()
        final.content_id = uuid.uuid4()
        final.project_id = project
        final.save()
    except Exception, err:
        loginfo(p=err, label="creat a project for the user")
        return False

    return True
