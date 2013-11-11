# coding: UTF-8
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

from const import MEMBER_NUM_LIMIT
from const import *
@dajaxice_register
def MemberChangeInfo(request, form, origin):
    try:
        project = ProjectSingle.objects.get(student__userid=request.user)
    except:
        raise Http404
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
    try:
        project = ProjectSingle.objects.get(student__userid=request.user)
    except:
        raise Http404
    group = project.student_group_set
    for student in group.all():
        if student.studentId == deleteId:
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
    elif not origin: # 添加或更新成员
        ret = new_or_update_member(request, stugroup_form)
    else:  # 更换成员
        ret = change_member(request, stugroup_form, origin)
    return simplejson.dumps(ret)

@dajaxice_register
def recordChange(request, form):
    record_form = ProcessRecordForm(deserialize_form(form))
    if not record_form.is_valid():
        ret = {'status' : '2',
               'error_id':record_form.errors.keys(),
               'message': u"输入有误，请重新输入"}
    else:
        ret = new_or_update_record(request,record_form)
    return simplejson.dumps(ret)

@dajaxice_register
def GetStudentInfo(request, selectedId):
    if check_auth()
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

    loginfo("3" * 10)
    
    if check_auth(request.user, SCHOOL_USER):
        try:
            project = ProjectSingle.objects.get(project_id = pid)
        except:
            raise Http404
    else :
        try:
            project = ProjectSingle.objects.get(student__userid=request.user)
        except:
            raise Http404


        
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
    try:
        project = ProjectSingle.objects.get(student__userid=request.user)
    except:
        raise Http404
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
    student_account = StudentProfile.objects.get(userid = request.user)
    project = ProjectSingle.objects.get(student=student_account)
    student_group = Student_Group.objects.filter(project = project)
    student_group_info_form = StudentGroupInfoForm()

    for student in student_group:
        student.sex = student.get_sex_display()

    return render_to_string("student/widgets/member_group_table.html",
                            {"student_group": student_group,
                             "student_group_info_form": student_group_info_form})

def new_or_update_record(request, record_form):
    record_weekId   = record_form.cleaned_data["weekId"]
    record_recorder = record_form.cleaned_data["recorder"]
    record_text     = record_form.cleaned_data["recordtext"]
    try:
        project = ProjectSingle.objects.get(student__userid=request.user)
    except:
        raise Http404
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
    student_account = StudentProfile.objects.get(userid = request.user)
    project = ProjectSingle.objects.get(student=student_account)
    record_group    = StudentWeeklySummary.objects.filter(project = project).order_by("weekId")
    record_group_info_form = ProcessRecordForm()

    return render_to_string("student/widgets/record_group_table.html",
                            {"record_group": record_group})
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


    
