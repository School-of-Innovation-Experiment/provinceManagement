# coding: UTF-8
'''
Created on 2013-4-17

@author: sytmac
'''

from dajax.core import Dajax
from django.contrib.auth.models import User
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from django.http import Http404
from school.models import ProjectSingle,Teacher_Enterprise,PreSubmitEnterprise
from school.forms import StudentDispatchForm
from school.views import Send_email_to_student, Count_email_already_exist, school_limit_num
from const.models import SchoolDict, ProjectCategory, FinancialCategory, InsituteCategory
from const import *
import datetime
from backend.logging import logger, loginfo
from school.utility import *
from users.models import SchoolProfile, StudentProfile
from student.forms import StudentGroupForm, StudentGroupInfoForm
from student.models import Student_Group
from django.template.loader import render_to_string

@dajaxice_register
def  StudentDispatch(request, form):
    #dajax = Dajax()
    student_form =  StudentDispatchForm(deserialize_form(form))
    if student_form.is_valid():
        password = student_form.cleaned_data["student_password"]
        email = student_form.cleaned_data["student_email"]
        financial_cate = student_form.cleaned_data["proj_cate"]
        person_firstname = student_form.cleaned_data["person_firstname"]
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

            flag = Send_email_to_student(request, name, person_firstname,password, email,STUDENT_USER, financial_cate=financial_cate)
            if flag:
                message = u"发送邮件成功"
                remaining_activation_times -= 1
                return simplejson.dumps({'field':student_form.data.keys(), 'status':'1', 'message':message,'remaining_activation_times':remaining_activation_times})
            else:
                message = u"邮件发送失败，请重新发送"
                return simplejson.dumps({'field':student_form.data.keys(), 'status':'1', 'message':message,'remaining_activation_times':remaining_activation_times})
    else:
        logger.info("Form Valid Failed"+"**"*10)
        logger.info(student_form.errors)
        logger.info("--"*10)
        return simplejson.dumps({'field':student_form.data.keys(),'error_id':student_form.errors.keys(),'message':u"输入有误,请检查后重新发送"})

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

@dajaxice_register
def StudentDeleteConsistence(request, uid):
    """
    Delete student in history file list
    """
    logger.info("sep delete student"+"**"*10)
    # check mapping relation
    try:
        delstudent=User.objects.get(id=uid)
        studentpro=StudentProfile.objects.get(user_id=uid)
        project=ProjectSingle.objects.get(student_id=studentpro.id)
        presubmitenterprise = PreSubmitEnterprise.objects.get(project_id_id=project.project_id)
        delteacher_enterprise=Teacher_Enterprise.objects.get(id=presubmitenterprise.enterpriseTeacher_id)
        if request.method == "POST":
            schooluser=request.user
            school=User.objects.get(username=schooluser)
            schoolpro=SchoolProfile.objects.filter(userid_id=school.id)
            if schoolpro:              
                if studentpro.school_id==schoolpro[0].id:
                    delstudent.delete()
                    delteacher_enterprise.delete()
                    return simplejson.dumps({"is_deleted": True,
                                 "message": "delete it successfully!",
                                 "uid": str(uid)})
        else:
            return simplejson.dumps({"is_deleted": False,
                                 "message": "Warning! Only POST accepted!"})
    except Exception, err:
        logger.info(err)

@dajaxice_register
def MemberChangeInfo(request, form, origin):
    loginfo(p=origin, label="origin")
    try:
        project = ProjectSingle.objects.get(student__user_id=request.user)
    except:
        raise Http404
    stugroup_form = StudentGroupInfoForm(deserialize_form(form))
    loginfo(p=stugroup_form, label="stugroup_form")
    if not stugroup_form.is_valid():
        ret = {'status': '1',
               'message': u"输入有误，请重新输入"}
    else:
        email = stugroup_form.cleaned_data["email"]
        telephone = stugroup_form.cleaned_data["telephone"]
        classInfo = stugroup_form.cleaned_data["classInfo"]
        student_id= stugroup_form.cleaned_data["student_id"]
        group = project.student_group_set
        for student in group.all():
            if student.studentId == origin :
                print "save successfully"
                student.email = email
                student.telephone = telephone
                student.classInfo = classInfo
                student.studentId = student_id
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
        project = ProjectSingle.objects.get(student__user_id=request.user)
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
    print 'MemberChange'
    loginfo(p=origin, label="origin")
    stugroup_form = StudentGroupForm(deserialize_form(form))
    if not stugroup_form.is_valid():
        ret = {'status': '2',
               'error_id': stugroup_form.errors.keys(),
               'message': u"输入有误，请重新输入"}
    elif not origin: # 添加或更新成员
        print 'add new member'
        ret = new_or_update_member(request, stugroup_form)
    else:  # 更换成员
        ret = change_member(request, stugroup_form, origin)
    return simplejson.dumps(ret)

def change_member(request, stugroup_form, origin):
    student_id = stugroup_form.cleaned_data["student_id"]
    student_name = stugroup_form.cleaned_data["student_name"]
    try:
        project = ProjectSingle.objects.get(student__user_id=request.user)
    except:
        raise Http404

    group = project.student_group_set
    managerid=StudentProfile.objects.get(id=project.student_id) #得到负责人的信息
    teammanager = User.objects.get(id=managerid.user_id)
    if filter(lambda x:x==student_id, [student.studentId for student in group.all()]):
        return {'status': '1', 'message': u"替换成员已存在队伍中，请选择删除"}

    loginfo(p=teammanager.first_name,label="teammanager.first_name")
    loginfo(p=student_name,label="student_name")    
    for student in group.all():
        if student.studentId == origin:
            # 如果是更改负责人的信息时需要将first_name内容更新
            if  student.studentName == teammanager.first_name:
                teammanager.first_name = student_name
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
    print "new_or_update_member"
    student_id = stugroup_form.cleaned_data["student_id"]
    student_name = stugroup_form.cleaned_data["student_name"]
    try:
        project = ProjectSingle.objects.get(student__user_id=request.user)
        loginfo(p=project,label='project')
    except:
        raise Http404

    managerid=StudentProfile.objects.get(id=project.student_id) #得到负责人的信息
    teammanager = User.objects.get(id=managerid.user_id)
    group = project.student_group_set
    loginfo(p=group, label="group")
    loginfo(p=teammanager.first_name,label="teammanager first_name")
    loginfo(p=student_name,label="student_name")    
    for student in group.all():
        if student.studentId == student_id:
            if  student.studentName == teammanager.first_name:
                teammanager.first_name = student_name
                teammanager.save()
                loginfo(p=teammanager.first_name,label="teammanager first_name")
                loginfo(p=student_name,label="student_name") 
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
                                        project=project)
            new_student.save()
            table = refresh_member_table(request)
            ret = {'status': '0', 'message': u"人员添加成功", 'table':table}
    return  ret

def refresh_member_table(request):
    student_account = StudentProfile.objects.get(user_id = request.user)
    project = ProjectSingle.objects.get(student=student_account)
    student_group = Student_Group.objects.filter(project = project)
    student_group_info_form = StudentGroupInfoForm()

    return render_to_string("school/widgets/member_group_table.html",
                            {"student_group": student_group,
                             "student_group_info_form": student_group_info_form})