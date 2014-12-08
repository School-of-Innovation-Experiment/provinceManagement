#coding=utf-8
import os, sys,re
from os.path import join
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form

from django.http import Http404
from django.utils import simplejson
from django.template.loader import render_to_string

from student.forms import StudentGroupForm, StudentGroupInfoForm,ProcessRecordForm
from student.models import Student_Group,StudentWeeklySummary
from school.models import ProjectSingle
from users.models import StudentProfile
from school.utility import *

from backend.logging import logger, loginfo
from backend.decorators import check_auth
from backend.utility import *

from const import MEMBER_NUM_LIMIT
from const import *

from django.shortcuts import get_object_or_404

def getProject(request):
    ok = check_auth(request.user, ADMINSTAFF_USER)
    ok = ok or check_auth(request.user, SCHOOL_USER)
    if ok == True:
        try:
            strUrl = request.META['HTTP_REFERER']
            pid = strUrl.split('/')[-1]
            loginfo(pid)
            project = ProjectSingle.objects.get(project_id = pid)
        except:
            raise Http404
    else :
        try:
            project = ProjectSingle.objects.get(student__userid=request.user)
        except:
            raise Http404
    return project


@dajaxice_register
def empty_file_set_check(request):
    status = "ok"
    if UploadedFiles.objects.filter(project_id__student__userid = request.user).count() == 0:
        status = 'empty'
    return simplejson.dumps({"status": status})

@dajaxice_register
def MemberChangeInfo(request, form, origin):
    # try:
    #     project = ProjectSingle.objects.get(student__userid=request.user)
    # except:
    #     raise Http404
    #sdfasdf

    project = getProject(request)

    stugroup_form = StudentGroupInfoForm(deserialize_form(form))
    if not stugroup_form.is_valid():
        ret = {'status': '1',
               'message': u"输入 有误，请重新输入"}
    else:
        email = stugroup_form.cleaned_data["email"]
        telephone = stugroup_form.cleaned_data["telephone"]
        classInfo = stugroup_form.cleaned_data["classInfo"]
        sex = stugroup_form.cleaned_data["sex"]
        nation = stugroup_form.cleaned_data["nation"]
        school = stugroup_form.cleaned_data["school"]
        school = SchoolDict.objects.get(id = int(school))
        major = stugroup_form.cleaned_data["major"]
        major = MajorDict.objects.get(id = int(major))
        grade = stugroup_form.cleaned_data["grade"]
        group = project.student_group_set
        for student in group.all():
            if student.studentId == origin:
                student.email = email
                student.telephone = telephone
                student.classInfo = classInfo
                student.sex = sex
                student.nation = nation
                student.school = school
                student.major = major
                student.grade = grade
                student.save()
                table = refresh_member_table(request)
                ret = {'status': '0', 'message': u"人员变更成功", 'table':table}
                break
        else:
            ret = {'status': '1', 'message': u"该成员不存在，请刷新页面"}
    return simplejson.dumps(ret)

@dajaxice_register
def MemberDelete(request, deleteId):
    # try:
    #     project = ProjectSingle.objects.get(student__userid=request.user)
    # except:
    #     raise Http404
    loginfo(deleteId)
    project = getProject(request)
    group = project.student_group_set
    for student in group.all():
        if student.studentId == deleteId:
            scorefile = student.scoreFile
            loginfo(p=scorefile,label="scorefile")
            if scorefile:
                delete_file(scorefile,project)
            student.delete()
            table = refresh_member_table(request)
            ret = {'status': '0', 'message': u"人员变更成功", 'table':table}
            break
    else:
        ret = {'status': '1', 'message': u"待删除成员不存在，请刷新页面"}
    return simplejson.dumps(ret)

@dajaxice_register
def MemberChange(request, form, origin):
    stugroup_form = StudentGroupForm(deserialize_form(form))
    if not stugroup_form.is_valid():
        ret = {'status': '2',
               'error_id': stugroup_form.errors.keys(),
               'message': u"输入有误，请重新输入"}
        print stugroup_form["student_id"]
    elif not origin: # 添加或更新成员
        ret = new_or_update_member(request, stugroup_form)
    else:  # 更换成员
        ret = change_member(request, stugroup_form, origin)
    return simplejson.dumps(ret)

@dajaxice_register
def recordChange(request, form):
    record_form = ProcessRecordForm(deserialize_form(form))
    if not record_form.is_valid():
        message = u"";
        if "weekId" in record_form.errors.keys():
            message += u"请填写周次！"
        if "recorder" in record_form.errors.keys():
            message += u"请填写项目记录人!"
        if "recordtext" in record_form.errors.keys():
            message += u"过程记录字数超过限制!"
        ret = {'status' : '2',
               'error_id':record_form.errors.keys(),
               'message': message}
    else:
        ret = new_or_update_record(request,record_form)
    return simplejson.dumps(ret)

@dajaxice_register
def GetStudentInfo(request, selectedId):
    try:
        project = ProjectSingle.objects.get(student__userid=request.user)
    except:
        raise Http404
    group = project.student_group_set
    for student in group.all():
        if student.studentId == selectedId:
            ret = {'status': '0', 'message': u"人员变更成功", 'table':table}
            break
    return simplejson.dumps(ret)

def change_member(request, stugroup_form, origin):
    student_id = stugroup_form.cleaned_data["student_id"]
    student_name = stugroup_form.cleaned_data["student_name"]

    project = getProject(request)

    group = project.student_group_set
    if filter(lambda x:x==student_id, [student.studentId for student in group.all()]):
        return {'status': '1', 'message': u"替换成员已存在队伍中，请选择删除"}
    for student in group.all():
        if student.studentId == origin:
            student.studentName = student_name
            student.studentId = student_id
            student.save()
            table = refresh_member_table(request)
            ret = {'status': '0', 'message': u"人员变更成功", 'table':table}
            break
    else: # new student
        ret = {'status': '1', 'message': u"输入有误，请刷新后重新输入"}
    return ret



def new_or_update_member(request, stugroup_form):

    student_id = stugroup_form.cleaned_data["student_id"]
    student_name = stugroup_form.cleaned_data["student_name"]
    loginfo(request.user)
    if not re.match('^[0-9]+$',student_id):
        return {'status': '1', 'message': u"学号只能输入数字"}
    project = getProject(request)
    group = project.student_group_set
    for student in group.all():
        if student.studentId == student_id:
            student.studentName = student_name
            student.save()
            table = refresh_member_table(request)
            ret = {'status': '0', 'message': u"人员信息更新成功", 'table':table}
            break
    else: # new student
        if group.count() == MEMBER_NUM_LIMIT[project.project_category.category]:
            ret = {'status': '1', 'message': u"人员已满，不可添加"}
        elif sum(student_id in [student.studentId for student in project.student_group_set.all()] for project in get_running_project_query_set()):
            ret = {'status': '1', 'message': u"相同学号已存在于其它正在进行的项目中"}
        else:
            new_student = Student_Group(studentId = student_id,
                                        studentName = student_name,
                                        classInfo = "",
                                        project=project)
            new_student.save()
            table = refresh_member_table(request)
            ret = {'status': '0', 'message': u"人员添加成功", 'table':table}
    return ret

def refresh_member_table(request):
    #student_account = StudentProfile.objects.get(userid = request.user)
    project = getProject(request)
    student_group = Student_Group.objects.filter(project = project)
    student_group_info_form = StudentGroupInfoForm()

    for student in student_group:
        student.sex_val = student.sex
        student.sex = student.get_sex_display()
    # loginfo(p=student_group_info_form,label ="test")
    return render_to_string("student/widgets/member_group_table.html",
                            {"student_group": student_group,
                             "student_group_info_form": student_group_info_form})

def new_or_update_record(request, record_form):
    record_weekId   = record_form.cleaned_data["weekId"]
    record_recorder = record_form.cleaned_data["recorder"]
    record_text     = record_form.cleaned_data["recordtext"]

    project = getProject(request)

    group = project.studentweeklysummary_set
    for record in group.all():
        if record.weekId == record_weekId:
            record.summary  = record_text
            record.recorder = record_recorder
            record.save()
            table = refresh_record_table(request)
            ret = {'status': '0', 'message': u"过程记录更新成功", 'table':table}
            break
    else:
        if group.count() == PROGRESS_RECORD_MAX:
            ret = {'status': '1', 'message': u"过程记录已满，不可添加"}
        else:
            new_record = StudentWeeklySummary( weekId    = record_weekId,
                                  summary   = record_text,
                                  recorder  = record_recorder,
                                  project=project)
            new_record.save()
            table = refresh_record_table(request)
            ret = {'status': '0', 'message': u"过程记录添加成功", 'table':table}
    return ret
def refresh_record_table(request):
    project = getProject(request)
    record_group    = StudentWeeklySummary.objects.filter(project = project).order_by("weekId")
    record_group_info_form = ProcessRecordForm()

    return render_to_string("student/widgets/record_group_table.html",
                            {"record_group": record_group})
@dajaxice_register
def RecordDelete(request,deleteWeekId):
    project = getProject(request)
    group = project.studentweeklysummary_set
    deleteWeekId = int(deleteWeekId)
    for weekSummary in group.all():
        if weekSummary.weekId == deleteWeekId:
            weekSummary.delete()
            table = refresh_record_table(request)
            ret = {'status': '0', 'message': u"过程记录删除成功", 'table':table}
            break
    else:
        ret = {'status': '1', 'message': u"所要删除过程记录不存在，请刷新页面"}
    return simplejson.dumps(ret)
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
        delete_file(f,p)
        return simplejson.dumps({"is_deleted": True,
                                 "message": "delete it successfully!",
                                 "fid": str(fid)})
    else:
        return simplejson.dumps({"is_deleted": False,
                                 "message": "Warning! Only POST accepted!"})

@dajaxice_register
def SetManager(request,studentid):
    """
        set studnet manager
    """
    loginfo(p=studentid,label="studentid")
    try:
        newmanager = Student_Group.objects.get(id = studentid)
        oldmanager = Student_Group.objects.filter(project_id = newmanager.project_id,is_manager=True)
        if oldmanager:
            oldmanager[0].is_manager = False
            oldmanager[0].save()
        newmanager.is_manager = True
        newmanager.save()
        project = ProjectSingle.objects.get(project_id = newmanager.project_id)
        users_student = project.student
        users_student.name = newmanager.studentName
        users_student.save()
        table = refresh_member_info_table(request)
        return simplejson.dumps({'table':table,'message':u'负责人设定成功','flag':True})
    except Exception, e:
        logger.info(e)
        return simplejson.dumps({'message':u'负责人不存在','flag':False})


def refresh_member_info_table(request):
    project = getProject(request)
    lock = project.recommend or (project.project_grade.grade != GRADE_UN)
    student_group = Student_Group.objects.filter(project = project)

    for student in student_group:
        student.sex_val = student.sex
        student.sex = student.get_sex_display()
    return render_to_string("student/widgets/member_info_table.html",
                            {
                                "student_group": student_group,
                                "lock":lock,
                            })