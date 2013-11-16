# coding: UTF-8

import os
import sys
import xlwt

from const import *

from django.contrib.auth.models import User
from student.models import Student_Group
from school.models import *
from users.models import *

from backend.logging import logger, loginfo
from settings import TMP_FILES_PATH

def info_xls_province_gen():
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')

    # generate header
    worksheet.write_merge(0, 0, 0, 19, '大连民族学院创新创业项目基本信息统计表')

    # generate body
    worksheet.write_merge(1, 1, 0, 0, '项目申报编号')
    worksheet.col(0).width = len('项目申报编号') * 200
    worksheet.write_merge(1, 1, 1, 1, '名称')
    worksheet.col(1).width = len('名称') * 800
    worksheet.write_merge(1, 1, 2, 2, '项目级别')
    worksheet.write_merge(1, 1, 3, 3, '指导教师')
    worksheet.col(3).width = len('指导教师') * 200
    worksheet.write_merge(1, 1, 4, 4, '申报书')
    worksheet.write_merge(1, 1, 5, 5, '中期检查表')
    worksheet.write_merge(1, 1, 6, 6, '结题验收表')
    worksheet.write_merge(1, 1, 7, 7, '项目汇编')
    worksheet.write_merge(1, 1, 8, 8, '申请学分')
    worksheet.write_merge(1, 1, 9, 9, '是否结题')
    worksheet.col(9).width = len('是否结题') * 300
    return worksheet, workbook

def info_xls(request,exceltype):
    """
    """
    def _format_number(i):
        i = str(i)
        i = '0' * (4-len(i)) + i
        return i

    proj_set = ProjectSingle.objects.all()
    xls_obj, workbook = info_xls_province_gen()

    # _index = 1
    _number= 1
    for proj_obj in proj_set:
        # manager_name,manager_id = get_manager(proj_obj)
        # memberlist,count = get_memberlist(manager_name,proj_obj)

        # pro_type = PreSubmit if proj_obj.project_category.category == CATE_INNOVATION else PreSubmitEnterprise
        # fin_type = ("15000", "5000", "10000") if proj_obj.financial_category.category == FINANCIAL_CATE_A else ("10000", "0", "10000")
        # try:
        #     innovation = pro_type.objects.get(project_id=proj_obj.project_id)
        # except Exception, err:
        #     loginfo(p=err, label="get innovation")
        #     loginfo(p=proj_obj.project_category.category, label="project category") 
        proj_obj.file_application = check_fileupload(proj_obj.file_application)
        proj_obj.file_interimchecklist = check_fileupload(proj_obj.file_interimchecklist)
        proj_obj.file_summary = check_fileupload(proj_obj.file_summary)
        proj_obj.file_projectcompilation = check_fileupload(proj_obj.file_projectcompilation)
        proj_obj.score_application = check_scoreapplication(proj_obj.score_application)

        row = 1 + _number
        xls_obj.write(row, 0, unicode(proj_obj.project_code)) 
        xls_obj.write(row, 1, unicode(proj_obj.title)) 
        xls_obj.write(row, 2, unicode(proj_obj.project_grade)) 
        xls_obj.write(row, 3, unicode(proj_obj.adminuser.get_name())) 
        xls_obj.write(row, 4, unicode(proj_obj.file_application)) 
        xls_obj.write(row, 5, unicode(proj_obj.file_interimchecklist)) 
        xls_obj.write(row, 6, unicode(proj_obj.file_summary))
        xls_obj.write(row, 7, unicode(proj_obj.file_projectcompilation)) 
        xls_obj.write(row, 8, unicode(proj_obj.score_application))  
        xls_obj.write(row, 9, unicode(proj_obj.over_status)) 


        # _index += 1
        _number+= 1
    # write xls file
    save_path = os.path.join(TMP_FILES_PATH, "%s%s.xls" % (str(datetime.date.today().year), "年大连民族学院创新创业项目基本信息统计表"))
    workbook.save(save_path)
    return save_path


def get_manager(project):
    """
        get teammanager's name and student_id
    """
    managerid=StudentProfile.objects.get(id=project.student_id)
    teammanager = User.objects.get(id=managerid.user_id)
    manager_name = teammanager.first_name
    manager_studentid = ""
    group = project.student_group_set
    for student in group.all():
        if student.studentName == manager_name:
            manager_studentid = student.studentId
            loginfo(p=manager_studentid,label="manager_studentid")
    return manager_name , manager_studentid
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

def get_shcoolcode(school_id):
    school_prof = SchoolProfile.objects.get(school_id=school_id)
    schooluser=User.objects.get(id=school_prof.userid_id)
    school_code = '2013'+schooluser.username
    return school_code

def check_fileupload(check_obj):
    """
        fileupload check
    """
    if check_obj == True:
        return u"已上传"
    else:
        return u"未上传"

def check_scoreapplication(check_obj):
    """
        coreapplication check
    """
    if check_obj == True:
        return u"申请学分"
    else:
        return u""    