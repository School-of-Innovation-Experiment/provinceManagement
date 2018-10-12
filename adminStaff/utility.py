# coding: UTF-8

import os
import sys
import xlwt
import mimetypes
import zipfile
from const import *
from django.core.files.storage import default_storage
from django.contrib.auth.models import User
from django.core.servers.basehttp import FileWrapper
from django.http import HttpResponse, Http404
from django.core.files.storage import default_storage
from student.models import Student_Group
from school.models import *
from users.models import *
from backend.decorators import check_auth
from school.utility import get_current_project_query_set,get_manager
from backend.logging import logger, loginfo
from settings import TMP_FILES_PATH
from const import *
from django.db.models import Q
from adminStaff.forms import ProjectManageForm as AdminstaffProjectManageForm
from school.forms import ProjectManageForm as SchoolProjectManageForm
from dajaxice.utils import deserialize_form
def get_average_score_list(review_list):
    cnt_of_list = len(review_list)
    return [sum(a) / (cnt_of_list - a.count(0)) if cnt_of_list != a.count(0) else 0 for a in zip(*review_list)]
def info_xls_baseinformation_gen():
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')
    style = cell_style(horizontal=True,vertical=True)
    # generate header
    worksheet.write_merge(0, 0, 0, 10, '大连理工大学创新创业项目基本信息统计表',style)

    # generate body
    worksheet.write_merge(1, 1, 0, 0, '序号')
    worksheet.write_merge(1, 1, 1, 1, '项目编号')
    worksheet.col(1).width = len('项目编号') * 300
    worksheet.write_merge(1, 1, 2, 2, '项目名称')
    worksheet.col(2).width = len('项目名称') * 800
    worksheet.write_merge(1, 1, 3, 3, '项目级别')
    worksheet.write_merge(1, 1, 4, 4, '指导教师')
    worksheet.col(4).width = len('指导教师') * 200
    worksheet.write_merge(1, 1, 5, 5, '申报书')
    worksheet.write_merge(1, 1, 6, 6, '开题报告')
    worksheet.write_merge(1, 1, 7, 7, '中期检查表')
    worksheet.write_merge(1, 1, 8, 8, '结题报告')
    worksheet.write_merge(1, 1, 9, 9, '项目汇编')
    worksheet.write_merge(1, 1, 10, 10, '申请学分')
    worksheet.write_merge(1, 1, 11, 11, '是否结题')
    worksheet.col(11).width = len('是否结题') * 300
    worksheet.write_merge(1, 1, 12, 12, '负责人')
    worksheet.col(12).width = len('负责人') * 200
    worksheet.write_merge(1, 1, 13, 13, '负责人电话')
    worksheet.col(13).width = len('负责人电话') * 200
    worksheet.write_merge(1, 1, 14, 14, '负责人邮箱')
    worksheet.col(14).width = len('负责人邮箱') * 200
    worksheet.write_merge(1, 1, 15, 15, '所在院系')

    return worksheet, workbook

def info_xls_baseinformation(request,proj_set):
    """
    """
    def _format_number(i):
        i = str(i)
        i = '0' * (4-len(i)) + i
        return i

    # proj_set = ProjectSingle.objects.all()
    xls_obj, workbook = info_xls_baseinformation_gen()
    # _index = 1
    _number= 1
    for proj_obj in proj_set:
        proj_obj.file_application = check_fileupload(proj_obj.file_application)
        proj_obj.file_interimchecklist = check_fileupload(proj_obj.file_interimchecklist)
        proj_obj.file_summary = check_fileupload(proj_obj.file_summary)
        proj_obj.file_projectcompilation = check_fileupload(proj_obj.file_projectcompilation)
        proj_obj.score_application = check_scoreapplication(proj_obj.score_application)
        proj_obj.file_opencheck = check_fileupload(proj_obj.file_opencheck)
        get_expertscore(proj_obj)
        teammember = get_teammember(proj_obj)

        row = 1 + _number
        xls_obj.write(row, 0, str(_number))
        xls_obj.write(row, 1, unicode(proj_obj.project_unique_code))
        xls_obj.write(row, 2, unicode(proj_obj.title))
        xls_obj.write(row, 3, unicode(proj_obj.project_grade))
        xls_obj.write(row, 4, unicode(proj_obj.adminuser.get_name()))
        xls_obj.write(row, 5, unicode(proj_obj.file_application))
        xls_obj.write(row, 6, unicode(proj_obj.file_opencheck))
        xls_obj.write(row, 7, unicode(proj_obj.file_interimchecklist))
        xls_obj.write(row, 8, unicode(proj_obj.file_summary))
        xls_obj.write(row, 9, unicode(proj_obj.file_projectcompilation))
        xls_obj.write(row, 10, unicode(proj_obj.score_application))
        xls_obj.write(row, 11, unicode(proj_obj.over_status))
        xls_obj.write(row, 12, unicode(teammember['manager_name']))
        xls_obj.write(row, 13, unicode(teammember['telephone']))
        xls_obj.write(row, 14, unicode(teammember['email']))
        xls_obj.write(row, 15, unicode(proj_obj.school.get_school_name()))

        # _index += 1
        _number+= 1
    # write xls file
    save_path = os.path.join(TMP_FILES_PATH, "%s%s.xls" % (str(datetime.date.today().year+1), "年大连理工大学创新创业项目基本信息统计表"))
    workbook.save(save_path)
    return save_path

def info_xls_expertscore_gen():
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')
    style = cell_style(horizontal=True,vertical=True)
    # generate header
    worksheet.write_merge(0, 0, 0, 10, '大连理工大学创新创业项目评分统计表',style)

    # generate body

    worksheet.write_merge(1, 1, 0, 0, '项目申报编号')
    worksheet.col(0).width = len('项目申报编号') * 200
    worksheet.write_merge(1, 1, 1, 1, '名称')
    worksheet.col(1).width = len('名称') * 800
    worksheet.write_merge(1, 1, 2, 2, '学院')
    worksheet.col(2).width = len('学院') * 800
    worksheet.write_merge(1, 1, 3, 3, '项目级别')
    worksheet.write_merge(1, 1, 4, 4, '指导教师')
    worksheet.col(3).width = len('指导教师') * 200
    worksheet.write_merge(1, 1, 5, 5, '项目选题意义')
    worksheet.write_merge(1, 1, 6, 6, '科技研究价值')
    worksheet.write_merge(1, 1, 7, 7, '项目创新之处')
    worksheet.write_merge(1, 1, 8, 8, '项目可行性')
    worksheet.write_merge(1, 1, 9, 9, '预期成果')
    worksheet.write_merge(1, 1, 10, 10, '指导教师科研能力')
    worksheet.write_merge(1, 1,11, 11, '总分')
    return worksheet, workbook

def info_xls_expertscore(request,proj_set):
    """
    """
    def _format_number(i):
        i = str(i)
        i = '0' * (4-len(i)) + i
        return i

    xls_obj, workbook = info_xls_expertscore_gen()

    # _index = 1
    _number= 1
    for proj_obj in proj_set:
        scorelist=get_expertscore(proj_obj)

        row = 1 + _number
        xls_obj.write(row, 0, unicode(proj_obj.project_code))
        xls_obj.write(row, 1, unicode(proj_obj.title))
        xls_obj.write(row, 2, unicode(proj_obj.school.school))
        xls_obj.write(row, 3, unicode(proj_obj.project_grade))
        xls_obj.write(row, 4, unicode(proj_obj.adminuser.get_name()))
        xls_obj.write(row, 5, unicode(scorelist[0]))
        xls_obj.write(row, 6, unicode(scorelist[1]))
        xls_obj.write(row, 7, unicode(scorelist[2]))
        xls_obj.write(row, 8, unicode(scorelist[3]))
        xls_obj.write(row, 9, unicode(scorelist[4]))
        xls_obj.write(row, 10, unicode(scorelist[5]))
        xls_obj.write(row, 11, unicode(scorelist[6]))



        # _index += 1
        _number+= 1
    # write xls file
    save_path = os.path.join(TMP_FILES_PATH, "%s%s.xls" % (str(datetime.date.today().year+1), "年大连理工大学创新创业项目评分统计表"))
    workbook.save(save_path)
    return save_path

def info_xls_summaryinnovate_gen():
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')
    style = cell_style(horizontal=True,vertical=True)

    # generate header
    worksheet.write_merge(0, 0, 0, 10, '大连理工大学大学生创新训练项目汇总表(%s年)' % str(datetime.date.today().year+1),style)

    # generate body
    worksheet.write_merge(1, 1, 0, 0, '序号')
    worksheet.write_merge(1, 1, 1, 1, '学生姓名')
    worksheet.col(1).width = len('学生姓名')*200
    worksheet.write_merge(1, 1, 2, 2, '学号')
    worksheet.col(2).width = len('学号')*400
    worksheet.write_merge(1, 1, 3, 3, '班级')
    worksheet.col(3).width = len('班级')*300
    worksheet.write_merge(1, 1, 4, 4, '项目名称')
    worksheet.col(4).width = len('项目名称')*800
    worksheet.write_merge(1, 1, 5, 5, '指导教师')
    worksheet.col(5).width = len('指导教师')*200
    worksheet.write_merge(1, 1, 6, 6, '职称')
    worksheet.write_merge(1, 1, 7, 7, '所在院系')
    worksheet.write_merge(1, 1, 8, 10, '备注')
    return worksheet, workbook

def info_xls_summaryinnovate(request,proj_set):
    """
    """
    def _format_number(i):
        i = str(i)
        i = '0' * (4-len(i)) + i
        return i
    print CATE_INNOVATION
    proj_set = proj_set.filter(project_category__category = CATE_INNOVATION)
    xls_obj, workbook = info_xls_summaryinnovate_gen()
    style = cell_style(horizontal=True,vertical=True)

    # _index = 1
    row = 1
    number = 0
    for proj_obj in proj_set:
        number += 1
        studentlist=get_students(proj_obj)
        row_project_start = row + 1
        for student in studentlist:
            row += 1
            xls_obj.write(row, 1, unicode(student.studentName))
            xls_obj.write(row, 2, unicode(student.studentId))
            xls_obj.write(row, 3, unicode(student.classInfo))
        if row_project_start > row :
            row = row_project_start
        xls_obj.write_merge(row_project_start,row,0,0,str(number),style)
        xls_obj.write_merge(row_project_start,row,4,4,unicode(proj_obj.title),style)
        xls_obj.write_merge(row_project_start,row,5,5,unicode(proj_obj.adminuser.get_name()),style)
        xls_obj.write_merge(row_project_start,row,6,6,unicode(proj_obj.adminuser.titles),style)
        xls_obj.write_merge(row_project_start,row,7,7,unicode(proj_obj.school.get_school_name()),style)
        xls_obj.write_merge(row_project_start,row,8,10)
        # _index += 1
    # write xls file
    save_path = os.path.join(TMP_FILES_PATH, "%s%s.xls" % (str(datetime.date.today().year+1), "年大连理工大学大学生创新训练项目汇总表"))
    workbook.save(save_path)
    return save_path

def info_xls_summaryresearch_gen():
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')
    style = cell_style(horizontal=True,vertical=True)

    # generate header
    worksheet.write_merge(0, 0, 0, 10, '大连理工大学大学生科研训练项目汇总表(%s年)' % str(datetime.date.today().year+1),style)

    # generate body
    worksheet.write_merge(1, 1, 0, 0, '序号')
    worksheet.write_merge(1, 1, 1, 1, '学生姓名')
    worksheet.col(1).width = len('学生姓名')*200
    worksheet.write_merge(1, 1, 2, 2, '学号')
    worksheet.col(2).width = len('学号')*400
    worksheet.write_merge(1, 1, 3, 3, '班级')
    worksheet.col(3).width = len('班级')*300
    worksheet.write_merge(1, 1, 4, 4, '项目名称')
    worksheet.col(4).width = len('项目名称')*800
    worksheet.write_merge(1, 1, 5, 5, '指导教师')
    worksheet.col(5).width = len('指导教师')*200
    worksheet.write_merge(1, 1, 6, 6, '职称')
    worksheet.write_merge(1, 1, 7, 7, '所在院系')
    worksheet.write_merge(1, 1, 8, 10, '备注')
    return worksheet, workbook

def info_xls_summaryresearch(request,proj_set):
    """
    """
    def _format_number(i):
        i = str(i)
        i = '0' * (4-len(i)) + i
        return i
    print CATE_RESEARCH
    proj_set = proj_set.filter(project_category__category = CATE_RESEARCH)
    xls_obj, workbook = info_xls_summaryresearch_gen()
    style = cell_style(horizontal=True,vertical=True)

    # _index = 1
    row = 1
    number = 0
    for proj_obj in proj_set:
        number += 1
        studentlist=get_students(proj_obj)
        row_project_start = row + 1
        for student in studentlist:
            row += 1
            xls_obj.write(row, 1, unicode(student.studentName))
            xls_obj.write(row, 2, unicode(student.studentId))
            xls_obj.write(row, 3, unicode(student.classInfo))
        if row_project_start > row :
            row = row_project_start
        xls_obj.write_merge(row_project_start,row,0,0,str(number),style)
        xls_obj.write_merge(row_project_start,row,4,4,unicode(proj_obj.title),style)
        xls_obj.write_merge(row_project_start,row,5,5,unicode(proj_obj.adminuser.get_name()),style)
        xls_obj.write_merge(row_project_start,row,6,6,unicode(proj_obj.adminuser.titles),style)
        xls_obj.write_merge(row_project_start,row,7,7,unicode(proj_obj.school.get_school_name()),style)
        xls_obj.write_merge(row_project_start,row,8,10)
        # _index += 1
    # write xls file
    save_path = os.path.join(TMP_FILES_PATH, "%s%s.xls" % (str(datetime.date.today().year+1), "年大连理工大学大学生科研训练项目汇总表"))
    workbook.save(save_path)
    return save_path

def info_xls_summaryentrepreneuship_gen():
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')
    style = cell_style(horizontal=True,vertical=True)

    # generate header
    worksheet.write_merge(0, 0, 0, 13, '大连理工大学大学生创业训练项目汇总表(%s年)' % str(datetime.date.today().year),style)

    # generate body
    worksheet.write_merge(1, 1, 0, 0, '序号')
    worksheet.write_merge(1, 1, 1, 1, '学生姓名')
    worksheet.col(1).width = len('学生姓名')*200
    worksheet.write_merge(1, 1, 2, 2, '学号')
    worksheet.col(2).width = len('学号')*400
    worksheet.write_merge(1, 1, 3, 3, '班级')
    worksheet.col(3).width = len('班级')*300
    worksheet.write_merge(1, 1, 4, 4, '项目名称')
    worksheet.col(4).width = len('项目名称') * 800
    worksheet.write_merge(1, 1, 5, 5, '项目类别（创业训练或创业实践）')
    worksheet.write_merge(1, 1, 6, 6, '指导教师')
    worksheet.col(6).width = len('指导教师')*200
    worksheet.write_merge(1, 1, 7, 7, '职称')
    worksheet.write_merge(1, 1, 8, 8, '企业导师')
    worksheet.col(8).width = len('企业导师')*200
    worksheet.write_merge(1, 1, 9, 9, '单位/职称')
    worksheet.write_merge(1, 1, 10, 10, '所在院系')
    worksheet.write_merge(1, 1, 11, 13, '备注')
    return worksheet, workbook

def info_xls_summaryentrepreneuship(request,proj_set):
    """
    """
    def _format_number(i):
        i = str(i)
        i = '0' * (4-len(i)) + i
        return i
    proj_set = proj_set.filter(
        project_category__category__in=(CATE_ENTERPRISE_EE, CATE_ENTERPRISE))
    xls_obj, workbook = info_xls_summaryentrepreneuship_gen()
    style = cell_style(horizontal=True,vertical=True)

    # _index = 1
    row = 1
    number = 0
    for proj_obj in proj_set:
        row_project_start = row + 1
        number += 1
        studentlist=get_students(proj_obj)
        try:
            pre = PreSubmitEnterprise.objects.get(project_id=proj_obj.project_id)
            teacher_enterprise = Teacher_Enterprise.objects.filter(id=pre.enterpriseTeacher_id)
        except Exception, e:
            print e
        finally:
            teacher_enterprise = Teacher_Enterprise()
        for student in studentlist:
            row += 1
            xls_obj.write(row, 1, unicode(student.studentName))
            xls_obj.write(row, 2, unicode(student.studentId))
            xls_obj.write(row, 3, unicode(student.classInfo))
        if row_project_start > row :
            row = row_project_start
        xls_obj.write_merge(row_project_start,row,0,0,unicode(number),style)
        xls_obj.write_merge(row_project_start,row,4,4,unicode(proj_obj.title),style)
        xls_obj.write_merge(row_project_start,row,5,5,unicode(proj_obj.project_category),style)
        xls_obj.write_merge(row_project_start,row,6,6,unicode(proj_obj.adminuser.get_name()),style)
        xls_obj.write_merge(row_project_start,row,7,7,unicode(proj_obj.adminuser.titles),style)
        xls_obj.write_merge(row_project_start,row,8,8,unicode(teacher_enterprise.name),style)
        xls_obj.write_merge(row_project_start,row,9,9,unicode(teacher_enterprise.jobs)+'/'+unicode(teacher_enterprise.titles),style)
        xls_obj.write_merge(row_project_start,row,10,10,unicode(proj_obj.school.get_school_name()),style)
        xls_obj.write_merge(row_project_start,row,11,13)
        # _index += 1
    # write xls file
    save_path = os.path.join(TMP_FILES_PATH, "%s%s.xls" % (str(datetime.date.today().year+1), "年大连理工大学大学生创业训练项目汇总表"))
    workbook.save(save_path)
    return save_path


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

def get_expertscore(proj_obj):
    """
        get expert score
    """

    project_id = proj_obj.project_id
    review_list = getSubjectReviewList(project_id)

    cnt_of_list = len(review_list)
    # average_list = [sum(map(float, a)) / cnt_of_list for a in zip(*review_list)[1:]]
    average_list = [sum(map(float, a)) / len(filter(bool, a)) if len(filter(bool, a)) else 0 for a in zip(*review_list)[1:]]
    #loginfo(p=average_list,label="average_list")
    return average_list



def getSubjectReviewList(project_id):
        review_obj_list = Re_Project_Expert.objects.filter(project=project_id).all()
        review_list = []
        for obj in review_obj_list:
            obj_list = [obj.comments, obj.score_significant,
                        obj.score_value, obj.score_innovation,
                        obj.score_practice, obj.score_achievement,
                        obj.score_capacity,]
            obj_list.append(sum(map(float, obj_list[1:])))
            review_list.append(obj_list)
        if review_list == []:
            inital_list = [u""]
            inital_list.extend([0.0]*7)
            review_list.append(inital_list)
       # loginfo(p=review_list,label="review_list")
        return review_list

def cell_style(horizontal,vertical):
    """
    为CELL添加水平居中和垂直居中
    """
    alignment = xlwt.Alignment()
    if horizontal:
        alignment.horz = xlwt.Alignment.HORZ_CENTER
    elif vertical:
        alignment.vert = xlwt.Alignment.VERT_CENTER
    style = xlwt.XFStyle() # Create Style
    style.alignment = alignment # Add Alignment to Style
    return style

def get_students(project):
    project_id = project.project_id
    studentlist = Student_Group.objects.filter(project=project_id).order_by('-is_manager')
    return studentlist


def info_xls_province_gen():
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')

    # generate header
    worksheet.write_merge(0, 0, 0, 19, '大连理工大学大学生创新创业训练计划项目信息汇总表')

    # generate body
    worksheet.write_merge(1, 4, 0, 0, '序号')
    worksheet.write_merge(1, 4, 1, 1, '学院')
    worksheet.col(1).width = len('学院') * 800
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
    worksheet.write_merge(1, 2, 12, 13, '项目经费（元）')
    worksheet.write_merge(3, 4, 12, 12, '总经费')
    worksheet.write_merge(3, 4, 13, 13, '剩余经费')
    worksheet.write_merge(1, 4, 14, 14, '一级学科代码')
    worksheet.write_merge(1, 4, 15, 19, '项目简介（100字以内）')

    return worksheet, workbook

def info_xls_projectsummary(request,proj_set):
    """
    """

    def _format_number(i):
        i = str(i)
        i = '0' * (4-len(i)) + i
        return i
    proj_set = proj_set.order_by('school','project_grade')
    xls_obj, workbook = info_xls_province_gen()

    _number= 1
    for proj_obj in proj_set:
        teammember = get_teammember(proj_obj)

        pro_type = PreSubmit if proj_obj.project_category.category == CATE_INNOVATION else PreSubmitEnterprise
        try:
            innovation = pro_type.objects.get(project_id=proj_obj.project_id)
        except Exception, err:
            loginfo(p=err, label="get innovation")
            loginfo(p=proj_obj.project_category.category, label="project category")

        row = 4 + _number
        xls_obj.write(row, 0, "%s" % _format_number(_number))
        xls_obj.write(row, 1, unicode(proj_obj.school.school))
        xls_obj.write(row, 2, unicode(proj_obj.project_unique_code))
        xls_obj.write(row, 3, unicode(proj_obj.title))
        xls_obj.write(row, 4, unicode(proj_obj.project_grade))
        xls_obj.write(row, 5, unicode(proj_obj.project_category))
        xls_obj.write(row, 6, unicode(teammember['manager_name']))# 负责人
        xls_obj.write(row, 7, unicode(teammember['manager_studentid'])) # 学号
        xls_obj.write(row, 8, unicode(teammember['count'])) # 学生人数
        xls_obj.write(row, 9, unicode(teammember['memberlist'])) # 项目其他成员
        xls_obj.write(row, 10, unicode(proj_obj.adminuser.get_name()))
        xls_obj.write(row, 11, unicode(proj_obj.adminuser.titles)) # 指导老师职称
        xls_obj.write(row, 12, unicode(proj_obj.funds_total)) # 总经费
        xls_obj.write(row, 13, unicode(proj_obj.funds_remain)) # 剩余经费
        if proj_obj.presubmit_set.all() and proj_obj.presubmit_set.all()[0].subject:
            xls_obj.write(row, 14, unicode(proj_obj.presubmit_set.all()[0].subject.subject)) # 一级学科代码
        xls_obj.write_merge(row, row, 15, 19, unicode(innovation.innovation)) # both enterprise and innovation has innovation attr

        # _index += 1
        _number+= 1
    # write xls file
    save_path = os.path.join(TMP_FILES_PATH, "%s%s.xls" % (str(datetime.date.today().year+1), "年大连理工大学大学生创新创业训练计划项目信息汇总表"))
    workbook.save(save_path)
    return save_path

def info_xls_scoreapplication_gen():
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')

    # generate header
    worksheet.write_merge(0, 0, 0, 19, '大连理工大学大学生创新创业训练计划项目学分认定表')

    # generate body
    worksheet.write_merge(1, 1, 0, 0, '项目级别')
    worksheet.write_merge(1, 1, 1, 1, '项目编号')
    worksheet.write_merge(1, 1, 2, 2, '项目名称')
    worksheet.write_merge(1, 1, 3, 3, '指导教师')
    worksheet.write_merge(1, 1, 4, 4, '学生姓名')
    worksheet.write_merge(1, 1, 5, 5, '学号')
    worksheet.write_merge(1, 1, 6, 6, '是否认定学分')
    worksheet.write_merge(1, 1, 7, 7, '学生签字')
    return worksheet, workbook

def info_xls_scoreapplication(request,proj_set):
    """
    """

    def _format_number(i):
        i = str(i)
        i = '0' * (4-len(i)) + i
        return i
    proj_set = proj_set.filter(score_application = True).order_by('school','project_grade')
    xls_obj, workbook = info_xls_scoreapplication_gen()

    _number= 2
    for proj_obj in proj_set:
        stu_set = proj_obj.student_group_set.all()
        for stu in stu_set:
            xls_obj.write(_number, 0, unicode(proj_obj.project_grade))
            xls_obj.write(_number, 1, unicode(proj_obj.project_unique_code))
            xls_obj.write(_number, 2, unicode(proj_obj.title))
            xls_obj.write(_number, 3, unicode(proj_obj.adminuser.get_name()))
            xls_obj.write(_number, 4, unicode(stu.studentName))
            xls_obj.write(_number, 5, unicode(stu.studentId))
            xls_obj.write(_number, 6, "是")
            xls_obj.write(_number, 7,)
            _number+= 1
    # write xls file
    save_path = os.path.join(TMP_FILES_PATH, "%s%s.xls" % (str(datetime.date.today().year+1), "年大连理工大学大学生创新创业训练计划项目学分认定表"))
    workbook.save(save_path)
    return save_path


def get_teammember(project):
    """
        get teammanager's name and student_id
    """
    teammember = {'manager_name':'','manager_studentid':'','memberlist':'','count':0,'telephone':'','email':''}
    #loginfo(p=teammember,label="teammember")
    student_Group=Student_Group.objects.filter(project_id=project.project_id)
    #print project.title
   # loginfo(p=student_Group,label="student_Group")
    if student_Group.count() > 0:
        manager = get_manager(project)
        teammember['telephone'] = manager.telephone
        teammember['manager_name'] = manager.studentName
        teammember['email'] = manager.email
        teammember['manager_studentid'] = manager.studentId
        teammember['memberlist'],teammember['count'] = get_memberlist(manager.studentId,student_Group)
    return teammember

def get_memberlist(manager_studentid,student_Group):
    """
        get other members
    """
    memberlist=[]
    for student in student_Group.all():
        if student.studentId != manager_studentid:
            member=student.studentName+"("+student.studentId+")"
            memberlist.append(member)
    count=len(memberlist)+1
    memberlist=','.join(memberlist)
    return memberlist,count

def get_projectlist(request,project_manage_form):
    """
    根据身份筛选项目
    返回：QuerySet对象
    """
    if check_auth(user=request.user, authority=ADMINSTAFF_USER):
        project_manage_form = AdminstaffProjectManageForm(deserialize_form(project_manage_form))
        proj_set = projectFilterList(request,project_manage_form)
        proj_set =  proj_set.order_by('project_unique_code','school','adminuser')
    elif check_auth(user=request.user, authority=SCHOOL_USER):
        school = SchoolProfile.objects.get(userid=request.user)
        project_manage_form = SchoolProjectManageForm(deserialize_form(project_manage_form),school = school)
        proj_set = projectFilterList(request,project_manage_form)
        proj_set = proj_set.filter(school_id=school).order_by('-year','adminuser')
    return proj_set
def file_download_gen(request,fileid = None):
    """
    按照前台的文件名，在下载文件时对文件名进行修改，不改变存储文件的名称
    """
    try:
        uploadfile = UploadedFiles.objects.get(file_id = fileid)
        project = uploadfile.project_id
        filename = project.project_unique_code + project.title + uploadfile.name
        currenturl = os.path.dirname(os.path.abspath('__file__'))
        fileurl = str(uploadfile.file_obj)
        filepath = currenturl+'/media/'+fileurl
        filename =  filename.encode('GBK')
        wrapper = FileWrapper(open(filepath,'rb'))
    except UploadedFiles.DoesNotExist,err:
        loginfo(p = err , label = "err")
        raise Http404

    filetype = "." + uploadfile.file_type
    content_type = mimetypes.guess_type(filepath)[0]
    loginfo(p=content_type,label = "content_type")
    response = HttpResponse(wrapper, mimetype='content_type')
    response['Content-Disposition'] = "attachment; filename= %s%s" % (filename,str(filetype))
    return response

def fix_bad_flag(proj_set):
    for pro_temp in proj_set:
        uploadfiles = UploadedFiles.objects.filter(project_id_id = pro_temp)
        for filetmp in uploadfiles:
            if default_storage.exists(filetmp.file_obj.path):
                if filetmp.name == u"申报书" and not pro_temp.file_application:
                    pro_temp.file_application = True
                if filetmp.name == u"开题报告" and not pro_temp.file_opencheck:
                    pro_temp.file_opencheck = True
                if filetmp.name == u"中期检查表" and not pro_temp.file_interimchecklist:
                    pro_temp.file_interimchecklist = True
                if filetmp.name == u"结题报告" and not pro_temp.file_summary:
                    pro_temp.file_summary = True
                if filetmp.name == u"项目汇编" and not pro_temp.file_projectcompilation:
                    pro_temp.file_projectcompilation = True
        pro_temp.save()


def projectFilterList(request,project_manage_form):
    if project_manage_form.is_valid():
        project_grade = project_manage_form.cleaned_data["project_grade"]
        project_year =  project_manage_form.cleaned_data["project_year"]
        project_overstatus = project_manage_form.cleaned_data["project_overstatus"]
        project_scoreapplication = "-1"
        project_school = "-1"
        project_category= "-1"
        if check_auth(user=request.user, authority=ADMINSTAFF_USER):
            project_category = project_manage_form.cleaned_data['project_category']
            project_scoreapplication = project_manage_form.cleaned_data["project_scoreapplication"]
            project_school = project_manage_form.cleaned_data["project_school"]
        project_teacher_student_name = project_manage_form.cleaned_data["teacher_student_name"]
        loginfo(project_teacher_student_name)
        # qset = AdminStaffService.get_filter(project_grade,project_year,project_isover,project_scoreapplication)
        qset = get_filter(project_grade, project_year, project_overstatus,
            project_teacher_student_name, project_category, project_scoreapplication,
            project_school)
        if qset :
            qset = reduce(lambda x, y: x & y, qset)
            # if project_grade == "-1" and project_scoreapplication == "-1":
            #     pro_list = ProjectSingle.objects.filter(qset).exclude(Q(project_grade__grade=GRADE_INSITUTE) or Q(project_grade__grade=GRADE_SCHOOL) or Q(project_grade__grade=GRADE_UN))
            # else:
            pro_list = ProjectSingle.objects.filter(qset)
        else:
            pro_list = ProjectSingle.objects.all()
    else:
        print  project_manage_form.errors
    #loginfo(p=qset,label="qset")
    return pro_list

##
# TODO: fixed the `isover` to over status

def get_filter(project_grade,project_year,project_overstatus, project_teacher_student_name, project_category, project_scoreapplication = "-1",project_school= "-1"):
    if project_grade == "-1":
        project_grade=''
    if project_year == '-1':
        project_year=''
    # if project_isover == '-1':
    #     project_isover=''
    if project_overstatus == '-1':
        project_overstatus=''
    if project_category == '-1':
        project_category=''
    if project_scoreapplication == '-1':
        project_scoreapplication=''
    if project_school  == '-1':
        project_school = '';
    q1 = (project_year and Q(year=project_year)) or None
    # q2 = (project_isover and Q(is_over=project_isover)) or None
    q2 = (project_overstatus and Q(over_status__status=project_overstatus)) or None
    q3 = (project_grade and Q(project_grade__grade=project_grade)) or None
    # if project_grade in [GRADE_NATION,GRADE_PROVINCE]:
    #     q3 = (Q(project_grade__grade = GRADE_NATION)|Q(project_grade__grade= GRADE_PROVINCE))
    q4 = (project_scoreapplication and Q(score_application=project_scoreapplication)) or None
    q5 = (project_school and Q(school_id = project_school)) or None
    q6 = (project_teacher_student_name and (Q(adminuser__name__contains = project_teacher_student_name) | Q(student__name__contains = project_teacher_student_name))) or None
    q7 = (project_category and Q(project_category__category = project_category)) or None
    qset = filter(lambda x: x != None, [q1, q2, q3, q4, q5, q6, q7])
    return qset

def get_zipfiles_path(request,filetype,project_manage_form):
    proj_set = get_projectlist(request,project_manage_form)
    save_path = os.path.join(TMP_FILES_PATH, "%s%s.zip" % ("大连理工大学大学生创新训练项目",FILE_TYPE_DICT[filetype]+"压缩包"))
    f = zipfile.ZipFile(save_path,'w',zipfile.ZIP_DEFLATED)
    for pro_obj in proj_set:
        upfile = pro_obj.uploadedfiles_set.filter(name = FILE_TYPE_DICT[filetype])
        if upfile:
            upfile_obj = upfile[0]
            if default_storage.exists(upfile_obj.file_obj):
                newname = pro_obj.project_unique_code + pro_obj.title + upfile_obj.name + '.' + upfile_obj.file_type
                f.write(upfile_obj.file_obj.path,newname)
    f.close()
    return save_path


def get_otherfiles_path(request, project_manage_form):
    proj_set = get_projectlist(request, project_manage_form)
    save_path = os.path.join(
        TMP_FILES_PATH, '大连理工大学大学生创新训练项目项目相关文件压缩包.zip')
    f = zipfile.ZipFile(save_path, 'w', zipfile.ZIP_DEFLATED)
    for pro_obj in proj_set:
        upfiles = pro_obj.uploadedfiles_set.exclude(
            Q(name=FILE_TYPE_DICT['application'])|
            Q(name=FILE_TYPE_DICT['opencheck'])|
            Q(name=FILE_TYPE_DICT['midcheck'])|
            Q(name=FILE_TYPE_DICT['summary'])|
            Q(name=FILE_TYPE_DICT['projectcompilation'])|
            Q(name__contains=u'学分申请表'))
        for upfile in upfiles:
            if default_storage.exists(upfile.file_obj):
                newname = pro_obj.project_unique_code + pro_obj.title + upfile.name + '.' + upfile.file_type
                f.write(upfile.file_obj.path,newname)
    f.close()
    return save_path


def info_xls_certificates_gen():
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')

    # generate header
    worksheet.write_merge(0, 0, 0, 5, '大连理工大学大学生创新创业训练计划项目获得证书学生名单')

    # generate body
    worksheet.write_merge(1, 1, 0, 0, '项目级别')
    worksheet.write_merge(1, 1, 1, 1, '项目编号')
    worksheet.write_merge(1, 1, 2, 2, '项目名称')
    worksheet.write_merge(1, 1, 3, 3, '指导教师')
    worksheet.write_merge(1, 1, 4, 4, '学生姓名')
    worksheet.write_merge(1, 1, 5, 5, '学号')
    return worksheet, workbook


def info_xls_certificates(request, proj_set):
    """
    """

    # proj_set = proj_set.filter(over_status__status=OVER_STATUS_NORMAL)
    xls_obj, workbook = info_xls_certificates_gen()

    row_num = 2

    for proj_obj in proj_set:
        stu_set = proj_obj.student_group_set.all()
        for stu in stu_set:
            xls_obj.write(row_num, 0, unicode(proj_obj.project_grade))
            xls_obj.write(row_num, 1, unicode(proj_obj.project_unique_code))
            xls_obj.write(row_num, 2, unicode(proj_obj.title))
            xls_obj.write(row_num, 3, unicode(proj_obj.adminuser.get_name()))
            xls_obj.write(row_num, 4, unicode(stu.studentName))
            xls_obj.write(row_num, 5, unicode(stu.studentId))
            row_num += 1
    # write xls file
    save_path = os.path.join(TMP_FILES_PATH, "%s%s.xls" % (str(datetime.date.today().year+1), "年大连理工大学大学生创新创业训练计划项目获得证书学生名单"))
    workbook.save(save_path)
    return save_path


def info_xls_achievements_gen():
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')

    # generate header
    worksheet.write_merge(0, 0, 0, 5, '大连理工大学大学生创新创业训练计划项目结题验收表项目成果汇总')

    # generate body
    worksheet.write_merge(1, 1, 0, 0, '项目级别')
    worksheet.write_merge(1, 1, 1, 1, '项目编号')
    worksheet.write_merge(1, 1, 2, 2, '项目名称')
    worksheet.write_merge(1, 1, 3, 3, '指导教师')
    worksheet.write_merge(1, 1, 4, 4, '成果形式')
    worksheet.write_merge(1, 1, 5, 5, '成果类别')
    worksheet.write_merge(1, 1, 6, 6, '相关名称')
    worksheet.write_merge(1, 1, 7, 7, '相关人员')
    worksheet.write_merge(1, 1, 8, 8, '附加信息1')
    worksheet.write_merge(1, 1, 9, 9, '附加信息2')
    worksheet.write_merge(1, 1, 10, 10, '成果类别')
    worksheet.write_merge(1, 1, 11, 11, '相关名称')
    worksheet.write_merge(1, 1, 12, 12, '相关人员')
    worksheet.write_merge(1, 1, 13, 13, '附加信息1')
    worksheet.write_merge(1, 1, 14, 14, '附加信息2')
    worksheet.write_merge(1, 1, 15, 15, '成果类别')
    worksheet.write_merge(1, 1, 16, 16, '相关名称')
    worksheet.write_merge(1, 1, 17, 17, '相关人员')
    worksheet.write_merge(1, 1, 18, 18, '附加信息1')
    worksheet.write_merge(1, 1, 19, 19, '附加信息2')
    worksheet.write_merge(1, 1, 20, 20, '成果类别')
    worksheet.write_merge(1, 1, 21, 21, '相关名称')
    worksheet.write_merge(1, 1, 22, 22, '相关人员')
    worksheet.write_merge(1, 1, 23, 23, '附加信息1')
    worksheet.write_merge(1, 1, 24, 24, '附加信息2')

    return worksheet, workbook


def info_xls_achievements(request, proj_set):
    xls_obj, workbook = info_xls_achievements_gen()

    row = 2
    for proj in proj_set:
        achievements = proj.achievementobjects_set.all()
        if not achievements:
            continue
        xls_obj.write(row, 0, unicode(proj.project_grade))
        xls_obj.write(row, 1, unicode(proj.project_unique_code))
        xls_obj.write(row, 2, unicode(proj.title))
        xls_obj.write(row, 3, unicode(proj.adminuser.get_name()))
        xls_obj.write(row, 4, unicode(proj.finalsubmit_set.all()[0].achievement_fashion))
        col = 5
        for item in achievements:
            xls_obj.write(row, col, unicode(item.get_category_display()))
            xls_obj.write(row, col+1, unicode(item.title))
            xls_obj.write(row, col+2, unicode(item.member))
            xls_obj.write(row, col+3, unicode(item.addition1))
            xls_obj.write(row, col+4, unicode(item.addition2))
            col += 5
        row += 1
    save_path = os.path.join(TMP_FILES_PATH, "%s%s.xls" % (str(datetime.date.today().year+1), "年大连理工大学大学生创新创业训练计划项目结题验收表项目成果汇总"))
    workbook.save(save_path)
    return save_path
