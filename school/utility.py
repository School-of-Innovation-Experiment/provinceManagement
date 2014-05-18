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
from const.models import SchoolDict, ProjectCategory, InsituteCategory, SchoolRecommendRate
from const.models import UserIdentity, ProjectGrade, ProjectStatus
from adminStaff.models import ProjectPerLimits
from users.models import SchoolProfile,AdminStaffProfile
from student.models import Student_Group

from const import AUTH_CHOICES, VISITOR_USER
from const import PROJECT_CATE_CHOICES, CATE_UN
from const import PROJECT_GRADE_CHOICES, GRADE_UN,GRADE_PROVINCE,GRADE_NATION
from const import PROJECT_STATUS_CHOICES, STATUS_FIRST
from school import SCHOOL_USER_PROJECT_GRADE

from backend.utility import search_tuple
from backend.logging import logger,loginfo
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
    return ProjectSingle.objects.filter(over_status__status = OVER_STATUS_NOTOVER)

def get_alloced_num(expert_list, flag):
    for expert in expert_list:
        expert.num = Re_Project_Expert.objects.filter(Q(expert = expert) & Q(is_assign_by_adminStaff = flag)).count()
    return expert_list

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


def save_application(project=None, pre=None, info_form=None, application_form=None, user=None):
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
        # info_form.save()
        # application_form.save()
        info = info_form.save(commit=False)
        info.save()
        application = application_form.save(commit=False)
        application.save()

        return True
    except Exception, err:
        logger.info("save process"+"**"*10)
        logger.info(err)
        logger.info("--"*10)
        raise err
        return False

def get_recommend_limit(school = None):
    """
    get the limit of recommending the projects
    """
    import math
    rate = SchoolRecommendRate.load().rate / 100.0
    project_list = get_current_project_query_set().filter(school = school)
    limit = int(math.ceil(project_list.count() * rate)) # 向上取整
    used = project_list.filter(recommend = True).count()
    return limit, limit - used

def save_enterpriseapplication(project=None, pre=None, info_form=None, application_form=None,teacher_enterpriseform=None, user=None):
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
        # info_form.save()
        # application_form.save()
        # teacher_enterpriseform.save()
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
    project = ProjectSingle.objects.get(project_id=pid)
    filename = project.title + name + '.' + filetype

    obj = UploadedFiles()
    obj.name = name
    obj.project_id = ProjectSingle.objects.get(project_id=pid)
    obj.file_id = uuid.uuid4()
    obj.file_obj.save(filename,f,save=False) 
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

def check_uploadfile_name(request,des_name=None):
    """
        des_name:上传入口对应的文件要求类型
        functions:将上传文件的类型与上传入口要求的类型比较
    """
    f = request.FILES["file"]    
    wrapper_f = UploadedFile(f)
    name, filetype = split_name(wrapper_f.name)
    loginfo(p=des_name,label="des_name")
    important_filelist=[u"申报书",u"中期检查表",u"结题验收表",u"项目汇编",u'开题报告',u'学分申请表']
    if des_name == name:
        return True
    elif des_name == u'其他附件' :
        for temp in important_filelist:
            if temp in  name:
                return False
        else:
            return True
 
    else :
        return False

def check_uploadfile_exist(des_name,pid):
    """
    检查上传的文件中是否已存在相同名称的文件,如果有先删除
    """
    try:
        check_obj=UploadedFiles.objects.get(project_id_id = pid,name=des_name)
        loginfo(p=des_name,label="des_name")
        loginfo(p=check_obj.name,label="check_obj.name")
        project=ProjectSingle.objects.get(project_id=pid)
        delete_file(check_obj,project)
        check_obj.delete()
        return True
    except:
        return False

def enabledelete_file(file_list):

    undelete_filelist=[u"申报书",u"中期检查表",u"结题验收表",u"项目汇编",u'开题报告']
    for temp in file_list:
        if temp.name in undelete_filelist:
            temp.enabledelete = False
        else :
            temp.enabledelete = True
    return file_list

# def check_othername(request):
#     f = request.FILES["file"]    
#     wrapper_f = UploadedFile(f)
#     name, filetype = split_name(wrapper_f.name)
#     important_filelist=[u"申报书",u"中期检查表",u"结题验收表",u"项目汇编",u"学分申请表"]
#     if name in important_filelist:
#         return False
#     else:
#         return True

def is_showoverstatus(project_list):
    """
    判断项目级别，院级管理员对于校级以上项目没有改变结题状态的权限
    """
    for temp in project_list:
        if temp.project_grade.grade in SCHOOL_USER_PROJECT_GRADE:
            temp.is_showoverstatus = True
        else:
            temp.is_showoverstatus = False
        add_fileurl(temp)
        add_telephone(temp)
    return project_list

def add_telephone(project):
    student_groups = Student_Group.objects.filter(project = project)
    for student_group in student_groups:
        project.telephone =student_group.get_telephone_display
        break
def is_addFundDetail(project_list):
    for temp in project_list:
        temp.is_addFundDetail = get_schooluser_project_modify_status(temp)
    return project_list
def get_schooluser_project_modify_status(project):
    if project.project_grade.grade in SCHOOL_USER_PROJECT_GRADE:
        return True
    else:
        return False

def add_fileurl(project):
    uploadfiles = UploadedFiles.objects.filter(project_id = project.project_id)
    for filetemp in uploadfiles:
        if filetemp.name == u"申报书":
            project.fileurl_application = filetemp.file_obj.url 
        elif filetemp.name == u"中期检查表":
            project.fileurl_interimchecklist = filetemp.file_obj.url
        elif filetemp.name == u"结题验收表":
            project.fileurl_file_summary = filetemp.file_obj.url
        elif filetemp.name == u"项目汇编":
            project.fileurl_projectcompilation = filetemp.file_obj.url
        elif filetemp.name == u"开题报告":
            project.fileurl_opencheck = filetemp.file_obj.url

class error_flag(object):
    """
        docstring for error_flag
    """
    error_type = ''
    error_flag = False
    error_message = ''
    def __init__(self, error_type,error_message):
        super(error_flag, self).__init__()
        self.error_type = error_type
        self.error_message = error_message

    def show_error(self):
        self.error_flag = True

    def unshow_error(self):
        self.error_flag = False

def set_error(error_flagset,error_type,set_false = False):
    """
    When set_false is True, show error
                   is False, do not show error
    """
    for error_temp in error_flagset:
        if error_temp.error_type == error_type:
            if set_false :
                error_temp.show_error()
            else :
                error_temp.unshow_error()


def get_errorflag_object(errortype,error_flagset):
    for error_temp in error_flagset:
        if errortype == error_temp.error_type:
            return error_temp
    else:
        return None
    
def check_filename(errortype,error_flagset):
    """
        返回上传文件对应类型的中文名称
    """
    for error_temp in error_flagset:
        if error_temp.error_type == errortype:
            return error_temp.error_message

def project_fileupload_flag(project,errortype):
    if errortype == "show_applicationwarn":
        project.file_application = True
    elif errortype == 'show_interimchecklist':
        project.file_interimchecklist = True
    elif errortype == 'show_summary':
        project.file_summary = True
    elif errortype == 'show_projectcompilation':
        project.file_projectcompilation = True
    elif errortype == 'show_scoreapplication':
        project.score_application = True
    elif errortype == 'show_opencheck':
        project.file_opencheck = True
    project.save()
    
def fileupload_flag_init():
    error_flagset = set()
    for errorkey in FileList :
        error_flagset.add(error_flag(errorkey,FileList[errorkey]))
    return error_flagset 


def upload_score_save_process(request, pid,des_name):
    """
        save score file into local storage
    """
    f = request.FILES["file"]
    wrapper_f = UploadedFile(f)
    size = wrapper_f.file.size
    name, filetype = split_name(wrapper_f.name)
    filename = des_name + '.' + filetype

    obj = UploadedFiles()
    obj.name = des_name
    obj.project_id = ProjectSingle.objects.get(project_id=pid)
    obj.file_id = uuid.uuid4()
    obj.file_obj.save(filename,f,save=False) 
    obj.uploadtime = time.strftime('%Y-%m-%d %X', time.localtime(time.time()))
    obj.file_type = filetype
    obj.file_size = size

    #TODO: we will check file type
    obj.file_type = filetype if filetype != " " else "unknown"
    obj.save()

    loginfo(p=f,label="f")
    loginfo(p=obj.file_obj,label="file_obj")
    return obj

def delete_file(uploadfile,project=None):
    """
        delete  uploadfileobject and local file 
    """
    currenturl = os.path.dirname(os.path.abspath('__file__'))
    fileurl = str(uploadfile.file_obj)
    url = currenturl+'/media/'+fileurl
    student_set = Student_Group.objects.filter(scoreFile = uploadfile)

    if student_set:
        student=student_set[0]
        loginfo(p=student,label="student")
        student.scoreFile = None
        student.save()


    uploadfile.delete()
    os.remove(url)
    check_scoreaplication(project,project.project_id)

def check_scoreaplication(project,pid):
    uploadfiles = UploadedFiles.objects.filter(project_id = pid) 
    loginfo(p=uploadfiles,label="uploadfiles")
    loginfo(p=project.score_application,label="project.score_application")
    for file_temp in uploadfiles:
        loginfo(p=file_temp,label="file_temp")
        loginfo(p=file_temp.name,label="file_temp.name")
        if u'学分申请' in file_temp.name:
            break
    else:
        project.score_application = False
    loginfo(p=project.score_application,label="project.score_application")
    project.save()
    loginfo(p=project.score_application,label="project.score_application")

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
def get_student_member(project):
    student_group = Student_Group.objects.filter(project = project)
    return ','.join([student.studentName for student in student_group])
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
