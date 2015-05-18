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
import xlwt
import types

from django.shortcuts import get_object_or_404
from django.utils import simplejson
from django.http import HttpResponse
from django.conf import settings
from django.core.files.uploadedfile import UploadedFile
from django.db.models import Count

from chartit import PivotDataPool, PivotChart

from school.models import *
from users.models import *
from const.models import SchoolDict, ProjectCategory, InsituteCategory
from const.models import UserIdentity, ProjectGrade, ProjectStatus
from adminStaff.models import ProjectPerLimits
from users.models import SchoolProfile,StudentProfile

from const import *
from const.models import *

from backend.utility import search_tuple

from backend.logging import logger, loginfo
from settings import TMP_FILES_PATH

from django.contrib.auth.models import User
from student.models import Student_Group

from django.db.models import Q

def get_current_project_query_set():
    """
    得到当前数据库中当前届的项目集合
    返回：QuerySet对象
    """
    return ProjectSingle.objects.filter(is_past = False)
def get_running_project_query_set():
    """
    得到当前数据库中正在进行的项目集合
    返回：QuerySet对象
    """
    return ProjectSingle.objects.filter(is_over = False)

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

    currents = ProjectSingle.objects.filter(adminuser=user, year=get_current_year()).count()
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
    return project.is_past

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
        statistics_number=ProjectSingle.objects.filter(adminuser=user,project_category__category=des_type,year=get_current_year()).count()
    else:
        statistics_number=statistics_number=ProjectSingle.objects.filter(adminuser=user,project_category__category=des_type).exclude(year=get_current_year()).count()
    return statistics_number

def get_gradecount(user,des_type,current):
    """
        if current is True
            return current gradecount
        else
            return history gradecount
    """
    if current==True:
        statistics_number=ProjectSingle.objects.filter(adminuser=user,project_grade__grade=des_type,year=get_current_year()).count()
        return statistics_number
    else:
        grade = ProjectGrade.objects.get(grade=des_type)
        statistics_proj=ProjectSingle.objects.filter(adminuser=user, project_grade__grade=des_type).exclude(year=get_current_year())
        statistics_number = statistics_proj.count()
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
                chart_options={'title': {'text': u'历史项目类型数据统计'},
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
                chart_options={'title': {'text': u'历史项目级别数据统计'},
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
    current_numbers = len(ProjectSingle.objects.filter(adminuser=user, year=get_current_year()))
    currentnation_numbers = get_gradecount(user, GRADE_NATION, True)
    currentprovince_numbers = get_gradecount(user, GRADE_PROVINCE, True)

    history_numbers = len(ProjectSingle.objects.filter(adminuser=user).exclude(year=get_current_year()))
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
                                    'labels':{
                                        'step': 1,
                                        'rotation': 45,
                                        'align': 'bottom'
                                    },
                                        },
                                'yAxis':{
                                    'title':{'text': '评级数量'},
                                    'allowDecimals':False},
                                }
                )
    return cht



def create_newproject(request, new_user, managername,financial_cate=FINANCIAL_CATE_UN, pid=None):
    """
    create a new project for this usr, it is student profile
    """
    #TODO: add some necessary decorators

    student = get_object_or_404(StudentProfile, user=new_user)

    try:
        if pid == None:
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

        #create team manager
        new_student = Student_Group(studentName = managername,
                                    project=project)
        new_student.save()        

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
        
        # create midsubmit
        mid = MidSubmit()
        mid.content_id = uuid.uuid4()
        mid.project_id = project
        mid.save()

        #create final report
        final = FinalSubmit()
        final.content_id = uuid.uuid4()
        final.project_id = project
        final.save()
    except Exception, err:
        loginfo(p=err, label="creat a project for the user")
        return False

    return True

def info_xls_school_gen(school):
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')

    # generate header
    worksheet.write_merge(0, 0, 0, 1, '高校名称: %s' % school.school)
    worksheet.write_merge(0, 0, 3, 4, '联系人:')
    worksheet.write_merge(0, 0, 6, 7, '联系电话:')
    worksheet.write_merge(0, 0, 9, 10, '电子邮箱:')

    # generate body
    worksheet.write_merge(1, 4, 0, 0, '项目编号')
    worksheet.col(0).width = len('项目编号') * 400  
    worksheet.write_merge(1, 4, 1, 1, '项目名称')
    worksheet.col(1).width = len('项目名称') * 800
    worksheet.write_merge(1, 4, 2, 2, '项目类别（甲类、乙类）')
    worksheet.col(2).width = len('项目类别（甲类、乙类）') * 256
    worksheet.write_merge(1, 4, 3, 3, '项目类型')
    worksheet.write_merge(1, 2, 4, 5, '项目负责人')
    worksheet.write_merge(3, 4, 4, 4, '姓名')
    worksheet.write_merge(3, 4, 5, 5, '学号')
    worksheet.write_merge(1, 4, 6, 6, '参与学生人数')
    worksheet.col(6).width = len('参与学生人数') * 256
    worksheet.write_merge(1, 4, 7, 7, '项目其他成员信息')
    worksheet.col(7).width = len('项目其他成员信息') * 256
    worksheet.write_merge(1, 2, 8, 9, '指导教师姓名')
    worksheet.write_merge(3, 4, 8, 8, '姓名')
    worksheet.write_merge(3, 4, 9, 9, '职称')
    worksheet.write_merge(1, 2, 10, 12, '项目经费（元）')
    worksheet.write_merge(3, 4, 10, 10, '总经费')
    worksheet.write_merge(3, 4, 11, 11, '财政拨款')
    worksheet.write_merge(3, 4, 12, 12, '校拨')
    worksheet.write_merge(1, 4, 13, 13, '项目所属一级学科')
    worksheet.col(13).width = len('项目所属一级学科') * 256
    worksheet.write_merge(1, 4, 14, 17, '项目简介（100字以内）')

    return worksheet, workbook

def info_xls(request):
    """
    """
    def _format_index(i):
        i = str(i)
        i = '0' * (4-len(i)) + i
        return i

    name_code = '2013' + request.user.username
    # loginfo(p=teammanager.first_name, label="get first_name")
    school_prof = SchoolProfile.objects.get(userid=request.user)
    proj_set = get_current_project_query_set().filter(school=school_prof.school).order_by('financial_category')
    xls_obj, workbook = info_xls_school_gen(school_prof)

    _index = 1
    for proj_obj in proj_set:
        teammember = get_studentmessage(proj_obj)

        pro_type = PreSubmit if proj_obj.project_category.category == CATE_INNOVATION else PreSubmitEnterprise
        fin_type = ("15000", "5000", "10000") if proj_obj.financial_category.category == FINANCIAL_CATE_A else ("10000", "0", "10000")
        try:
            innovation = pro_type.objects.get(project_id=proj_obj.project_id)
        except Exception, err:
            loginfo(p=err, label="get innovation")
            loginfo(p=proj_obj.project_category.category, label="project category")

        row = 4 + _index
        # pro_code = name_code+_format_index(_index)

        #保存项目编号
        # project_temp = ProjectSingle.objects.get(project_id = proj_obj.project_id)
        # project_temp.project_code = pro_code
        # project_temp.save()

        xls_obj.write(row, 0, unicode(proj_obj.project_code))
        xls_obj.write(row, 1, unicode(proj_obj.title))
        xls_obj.write(row, 2, unicode(proj_obj.financial_category))
        xls_obj.write(row, 3, unicode(proj_obj.project_category))
        xls_obj.write(row, 4, unicode(teammember['manager_name']))# 负责人
        xls_obj.write(row, 5, unicode(teammember['manager_studentid'])) # 学号
        xls_obj.write(row, 6, unicode(teammember['member_number'])) # 学生人数
        xls_obj.write(row, 7, unicode(teammember['othermember'])) # 项目其他成员
        xls_obj.write(row, 8, unicode(proj_obj.inspector))
        xls_obj.write(row, 9, unicode(proj_obj.inspector_title)) # 指导老师职称
        xls_obj.write(row, 10, fin_type[0]) # 经费
        xls_obj.write(row, 11, fin_type[1]) # 经费
        xls_obj.write(row, 12, fin_type[2]) # 经费
        xls_obj.write(row, 13, unicode(proj_obj.insitute))
        xls_obj.write_merge(row, row, 14, 17, unicode(innovation.proj_introduction)) # both enterprise and innovation has innovation attr

        _index += 1

    # write xls file
    save_path = os.path.join(TMP_FILES_PATH, "info-%s-%s.xls" % (str(datetime.date.today()), request.user.username))
    workbook.save(save_path)
    return save_path


def set_unique_telphone(request, info_form, teacher_enterpriseform):
    """
    Set telephones, which are the same name in one form
    """
    telephones = request.POST.getlist("telephone")

    info = info_form.save(commit=False)
    info.telephone = telephones[0]
    info_form.save()

    teacher = teacher_enterpriseform.save(commit=False)
    teacher.telephone = telephones[1]
    teacher_enterpriseform.save()

# def get_manager(project):
#     """
#         old version get teammanager's name and student_id
#     """
#     managerid=StudentProfile.objects.get(id=project.student_id)
#     teammanager = User.objects.get(id=managerid.user_id)
#     manager_name = teammanager.first_name
#     manager_studentid = ""
#     group = project.student_group_set
#     for student in group.all():
#         if student.studentName == manager_name:
#             manager_studentid = student.studentId
#             loginfo(p=manager_studentid,label="manager_studentid")
#     return manager_name , manager_studentid

def get_manager(project):
    """
        get teammanager's name and student_id
    """
    teammanager = project.student_group_set.all()[0]
    return teammanager

def get_memberlist(manager_name,project):
    """
        get other members
    """
    group = project.student_group_set
    memberlist=[]
    for student in group.all():
        if student.studentName != manager_name:
            member=student.studentName+"("+student.studentId+")"
            memberlist.append(member)
    count=len(memberlist)+1
    memberlist=','.join(memberlist)
    return memberlist,count

def get_studentmessage(project):
    """
        get  manager and student message
    """
    memberlist=[]
    # teammember = {'manager_name':'None','manager_studentid':'None','memberlist':'None','count':0,'telephone':'',}
    teammember={'manager_name':'','manager_studentid':'','member_number':'','othermember':''}
    if project.student_group_set.all().count()>0:
        group=project.student_group_set
        loginfo(p=group,label="group")
        manager = group.all()[0]
        loginfo(p=manager,label="manager")
        teammember['manager_name']=manager.studentName
        teammember['manager_studentid']=manager.studentId
        teammember['member_number'] = project.student_group_set.count()
        for student in group.all():
            group=project.student_group_set
            loginfo(p=student.studentName,label="student")
            if student.studentName != manager.studentName:
                member=student.studentName+"("+student.studentId+")"
                memberlist.append(member)
        teammember['othermember']=','.join(memberlist)
    return teammember



# def get_memberlist(members):
#     """
#         get all members in project
#     """
#     if ";" in members :
#         memberlist = members.strip(";").split(";")
#     elif u"；" in members :
#         memberlist = members.strip(u"；").split(u"；")
#     elif "," in members :
#         memberlist = members.strip(",").split(",")
#     elif u"，" in members :
#         memberlist = members.strip(u"，").split(u"，")
#     elif " " in members :
#         memberlist = members.strip(" ").split(" ")
#     elif "." in members :
#         memberlist = members.strip(".").split(".")
#     elif u"。" in members :
#         memberlist = members.strip(u"。").split(u"。")
#     elif u"、" in members :
#         memberlist = members.strip(u"、").split(u"、")
#     elif "+" in members :
#         memberlist = members.strip("+").split("+")
#     elif "-" in members :
#         memberlist = members.strip("-").split("-")
#     elif ":" in members :
#         logger.info(members+":")
#         memberlist = members.strip(":").split(":")
#     elif u"：" in members :
#         logger.info(members+u"：")
#         memberlist = members.strip(u"：").split(u"：")
#     else:
#         memberlist=members

#     return memberlist

# def get_teammember(managername,memberlist):
#     """
#         get member expect manager
#     """
#     teammember = memberlist
#     count=1
#     loginfo(p=managername, label="in managername")
#     loginfo(p=memberlist, label="in memberlist")
#     if managername == ""  :#if no manager
#         if type(memberlist) != types.UnicodeType:
#             manager = memberlist[0]
#         else :
#              manager = memberlist  # type is unicodetype用户First_name没有填写时
#     else:
#         manager = managername

#     if manager == teammember:
#         return teammember,count,manager
#     else :
#         if manager in memberlist and manager!=memberlist and type(teammember) != types.UnicodeType:
#             count=len(teammember)
#             teammember.remove(manager)
#             teammember=",".join(teammember)
#         elif type(teammember) != types.UnicodeType : #其他成员超过一个时时
#             count=len(teammember)+1
#             teammember=",".join(teammember)
#         else :  #如果只输入一个且不是负责人时
#             count+=1
#     return teammember,count,manager
