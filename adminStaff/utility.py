#!/usr/local/bin/python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-04-20 16:04
# Last modified: 2017-04-20 16:04
# Filename: utility.py
# Description:
# coding: UTF-8

import os
import sys
import xlwt

from const import *

from django.contrib.auth.models import User
from student.models import Student_Group
from school.models import *
from users.models import *
from school.utility import *

from backend.logging import logger, loginfo
from settings import TMP_FILES_PATH

def info_xls_province_gen():
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')
    year = get_current_year()
    # generate header
    worksheet.write_merge(0, 0, 0, 19, str(year)+'年辽宁省大学生创新创业训练计划项目信息表')

    # generate body
    worksheet.write_merge(1, 4, 0, 0, '序号')
    worksheet.write_merge(1, 4, 1, 1, '学校')
    worksheet.col(1).width = len('学校') * 800
    worksheet.write_merge(1, 4, 2, 2, '项目编号')
    worksheet.col(2).width = len('项目编号') * 400    
    worksheet.write_merge(1, 4, 3, 3, '项目名称')
    worksheet.col(3).width = len('项目名称') * 800
    worksheet.write_merge(1, 4, 4, 4, '项目级别')
    worksheet.col(4).width = len('项目级别') * 256
    worksheet.write_merge(1, 4, 5, 5, '项目类型')
    worksheet.write_merge(1, 2, 6, 7, '项目负责人')
    worksheet.write_merge(3, 4, 6, 6, '姓名')
    worksheet.write_merge(3, 4, 7, 7, '学号')
    worksheet.write_merge(1, 4, 8, 8, '参与学生人数')
    worksheet.col(8).width = len('参与学生人数') * 256
    worksheet.write_merge(1, 4, 9, 9, '项目其他成员信息')
    worksheet.col(9).width = len('项目其他成员信息') * 256
    worksheet.write_merge(1, 2, 10, 11, '指导教师姓名')
    worksheet.write_merge(3, 4, 10, 10, '姓名')
    worksheet.write_merge(3, 4, 11, 11, '职称')
    worksheet.write_merge(1, 2, 12, 14, '项目经费（元）')
    worksheet.write_merge(3, 4, 12, 12, '总经费')
    worksheet.write_merge(3, 4, 13, 13, '财政拨款')
    worksheet.write_merge(3, 4, 14, 14, '校拨')
    worksheet.write_merge(1, 4, 15, 15, '项目所属一级学科')
    worksheet.col(15).width = len('项目所属一级学科') * 256
    worksheet.write_merge(1, 4, 16, 18, '项目简介（100字以内）')
    


    return worksheet, workbook

def info_xls(request):
    """
    """
    # def _format_index(i):
    #     i = str(i)
    #     i = '0' * (3-len(i)) + i
    #     return i

    def _format_number(i):
        i = str(i)
        i = '0' * (4-len(i)) + i
        return i

    # name_code = '2013' + request.user.username
    # loginfo(p=teammanager.first_name, label="get first_name")
    # school_prof = SchoolProfile.objects.get(userid=request.user)
    proj_set = get_current_project_query_set().order_by('school','project_grade').exclude(school__schoolName=u'测试用学校').exclude(project_code__isnull=True)
    proj_set = filter(lambda x: x.presubmit_set.all()[0].is_audited if x.project_category.category == CATE_INNOVATION else x.presubmitenterprise_set.all()[0].is_audited, proj_set)

    xls_obj, workbook = info_xls_province_gen()

    # _index = 1
    _number= 1
    for proj_obj in proj_set:
        teammember = get_studentmessage(proj_obj)       

        pro_type = PreSubmit if proj_obj.project_category.category == CATE_INNOVATION else PreSubmitEnterprise
        fin_type = ("15000", "5000", "10000") if proj_obj.financial_category.category == FINANCIAL_CATE_A else ("10000", "0", "10000")
        try:
            innovation = pro_type.objects.get(project_id=proj_obj.project_id)
        except Exception, err:
            loginfo(p=err, label="get innovation")
            loginfo(p=proj_obj.project_category.category, label="project category")
        # if _index==1:
        #     schoolname = proj_obj.school
        #     name_code = get_shcoolcode(schoolname)
        # if schoolname!=proj_obj.school:
        #     _index=1
        #     schoolname = proj_obj.school
        #     name_code = get_shcoolcode(schoolname)   

        row = 4 + _number
        xls_obj.write(row, 0, "%s" % _format_number(_number))
        xls_obj.write(row, 1, unicode(proj_obj.school))
        # xls_obj.write(row, 2, unicode(proj_obj.project_code[:9]+proj_obj.project_code[-3:]))
        xls_obj.write(row, 2, unicode(proj_obj.project_code))
        xls_obj.write(row, 3, unicode(proj_obj.title))
        xls_obj.write(row, 4, unicode(proj_obj.financial_category))
        xls_obj.write(row, 5, unicode(proj_obj.project_grade))
        xls_obj.write(row, 6, unicode(teammember['manager_name']))# 负责人
        xls_obj.write(row, 7, unicode(teammember['manager_studentid'])) # 学号
        xls_obj.write(row, 8, unicode(teammember['member_number'])) # 学生人数
        xls_obj.write(row, 9, unicode(teammember['othermember'])) # 项目其他成员
        xls_obj.write(row, 10, unicode(proj_obj.inspector))
        xls_obj.write(row, 11, unicode(proj_obj.inspector_title)) # 指导老师职称
        xls_obj.write(row, 12, fin_type[0]) # 经费
        xls_obj.write(row, 13, fin_type[1]) # 经费
        xls_obj.write(row, 14, fin_type[2]) # 经费
        xls_obj.write(row, 15, unicode(proj_obj.insitute))
        xls_obj.write_merge(row, row, 16, 18, unicode(innovation.proj_introduction)) # both enterprise and innovation has innovation attr

        # _index += 1
        _number+= 1
    # write xls file
    save_path = os.path.join(TMP_FILES_PATH, "%s%s.xls" % (str(datetime.date.today().year), "年辽宁省大学生创新创业训练计划项目信息表"))
    workbook.save(save_path)
    return save_path


def info_result_xls(request,project_list):
    """
    """
    # def _format_index(i):
    #     i = str(i)
    #     i = '0' * (3-len(i)) + i
    #     return i

    def _format_number(i):
        i = str(i)
        i = '0' * (4-len(i)) + i
        return i

    # name_code = '2013' + request.user.username
    # loginfo(p=teammanager.first_name, label="get first_name")
    # school_prof = SchoolProfile.objects.get(userid=request.user)
    proj_set = project_list
    xls_obj, workbook = info_xls_province_gen()

    # _index = 1
    _number= 1
    for proj_obj in proj_set:
        teammember = get_studentmessage(proj_obj)       

        pro_type = PreSubmit if proj_obj.project_category.category == CATE_INNOVATION else PreSubmitEnterprise
        fin_type = ("15000", "5000", "10000") if proj_obj.financial_category.category == FINANCIAL_CATE_A else ("10000", "0", "10000")
        try:
            innovation = pro_type.objects.get(project_id=proj_obj.project_id)
        except Exception, err:
            loginfo(p=err, label="get innovation")
            loginfo(p=proj_obj.project_category.category, label="project category")
        # if _index==1:
        #     schoolname = proj_obj.school
        #     name_code = get_shcoolcode(schoolname)
        # if schoolname!=proj_obj.school:
        #     _index=1
        #     schoolname = proj_obj.school
        #     name_code = get_shcoolcode(schoolname)   

        row = 4 + _number
        xls_obj.write(row, 0, "%s" % _format_number(_number))
        xls_obj.write(row, 1, unicode(proj_obj.school))
        xls_obj.write(row, 2, unicode(proj_obj.project_code))
        xls_obj.write(row, 3, unicode(proj_obj.title))
        xls_obj.write(row, 4, unicode(proj_obj.financial_category))
        xls_obj.write(row, 5, unicode(proj_obj.project_category))
        xls_obj.write(row, 6, unicode(teammember['manager_name']))# 负责人
        xls_obj.write(row, 7, unicode(teammember['manager_studentid'])) # 学号
        xls_obj.write(row, 8, unicode(teammember['member_number'])) # 学生人数
        xls_obj.write(row, 9, unicode(teammember['othermember'])) # 项目其他成员
        xls_obj.write(row, 10, unicode(proj_obj.inspector))
        xls_obj.write(row, 11, unicode(proj_obj.inspector_title)) # 指导老师职称
        xls_obj.write(row, 12, fin_type[0]) # 经费
        xls_obj.write(row, 13, fin_type[1]) # 经费
        xls_obj.write(row, 14, fin_type[2]) # 经费
        xls_obj.write(row, 15, unicode(proj_obj.insitute))
        xls_obj.write_merge(row, row, 16, 18, unicode(innovation.proj_introduction)) # both enterprise and innovation has innovation attr

        # _index += 1
        _number+= 1
    # write xls file
    save_path = os.path.join(TMP_FILES_PATH, "%s%s.xls" % (str(datetime.date.today().year), "年辽宁省大学生创新创业训练计划评审项目信息表"))
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


def scored_xls_gen():
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')
    year = get_current_year()

    worksheet.write_merge(0, 0, 0, 23, str(year)+"年辽宁省大学生创新创业训练计划评审得分汇总表")
    worksheet.write_merge(1, 4, 0, 0, '立项年份')
    worksheet.write_merge(1, 4, 1, 1, '省（区、市）')
    worksheet.write_merge(1, 4, 2, 2, '高校代码')
    worksheet.write_merge(1, 4, 3, 3, '高校名称')
    worksheet.write_merge(1, 4, 4, 4, '项目编号')
    worksheet.write_merge(1, 4, 5, 5, '项目名称')
    worksheet.write_merge(1, 4, 6, 6, '项目类型')
    worksheet.write_merge(1, 4, 7, 7, '项目负责人姓名')
    worksheet.write_merge(1, 4, 8, 8, '项目负责人学号')
    worksheet.write_merge(1, 4, 9, 9, '参与学生人数')
    worksheet.write_merge(1, 4, 10, 10, '项目其他成员信息')
    worksheet.write_merge(1, 4, 11, 11, '指导教师姓名')
    worksheet.write_merge(1, 4, 12, 12, '指导教师职称')
    worksheet.write_merge(1, 4, 13, 13, '财政拨款（元）')
    worksheet.write_merge(1, 4, 14, 14, '校拨（元）')
    worksheet.write_merge(1, 4, 15, 15, '总经费（元）')
    worksheet.write_merge(1, 4, 16, 16, '项目所属一级学科')
    worksheet.write_merge(1, 4, 17, 17, '项目简介（200字以内）')
    worksheet.write_merge(1, 4, 18, 18, '评分小组')
    worksheet.write_merge(1, 2, 19, 21, '专家评分')
    worksheet.write_merge(3, 4, 19, 19, '专家1')
    worksheet.write_merge(3, 4, 20, 20, '专家2')
    worksheet.write_merge(3, 4, 21, 21, '专家3')
    worksheet.write_merge(1, 4, 22, 22, '平均分')
    worksheet.write_merge(1, 4, 23, 23, '排名')

    worksheet.col(3).width = len('学校') * 600
    worksheet.col(4).width = len('项目编号') * 300
    worksheet.col(5).width = len('项目名称') * 800

    return worksheet, workbook


def scored_result_xls(request, sorted_list):
    xls_obj, workbook = scored_xls_gen()
    row = 5
    for index, group in enumerate(sorted_list):
        group_index = index+1
        for item_index, item in enumerate(group):
            rating = item_index+1
            proj, score1, score2, score3, total_score = item
            school = proj.school.schoolprofile_set.all()[0]
            students = proj.student_group_set.all()
            charge_student = students[0]
            members = students[1:]
            presubmit_type = PreSubmit if proj.project_category.category == CATE_INNOVATION else PreSubmitEnterprise
            presubmit = presubmit_type.objects.get(project_id=proj.project_id)
            xls_obj.write(row, 0, unicode(proj.year)) 
            xls_obj.write(row, 1, '辽宁省')
            xls_obj.write(row, 2, unicode(school.userid))
            xls_obj.write(row, 3, unicode(school.school))
            xls_obj.write(row, 4, unicode(proj.project_code[:9]+proj.project_code[-3:]))
            #xls_obj.write(row, 4, unicode(proj.project_code))
            xls_obj.write(row, 5, unicode(proj.title))
            xls_obj.write(row, 6, unicode(proj.project_category))
            xls_obj.write(row, 7, unicode(charge_student.studentName))
            xls_obj.write(row, 8, unicode(charge_student.studentId))
            xls_obj.write(row, 9, unicode(students.count()))
            xls_obj.write(row, 10, unicode(','.join(map(lambda x: x.studentName+'('+x.studentId+')', members))))
            xls_obj.write(row, 11, unicode(proj.inspector))
            xls_obj.write(row, 12, unicode(proj.inspector_title))
            xls_obj.write(row, 13, '10000')
            xls_obj.write(row, 14, '5000')
            xls_obj.write(row, 15, '15000')
            xls_obj.write(row, 16, unicode(proj.project_category))
            xls_obj.write(row, 17, unicode(presubmit.proj_introduction))
            xls_obj.write(row, 18, unicode(group_index))
            xls_obj.write(row, 19, '%.3f' % score1)
            xls_obj.write(row, 20, '%.3f' % score2)
            xls_obj.write(row, 21, '%.3f' % score3)
            xls_obj.write(row, 22, '%.3f' % (sum([score1, score2, score3])/3))
            xls_obj.write(row, 23, unicode(rating))
            row += 1
    save_path = os.path.join(
        TMP_FILES_PATH,
        "%s%s.xls" % (str(datetime.date.today().year),
                      "年辽宁省大学生创新创业训练计划评审得分汇总表"))
    workbook.save(save_path)
    return save_path
