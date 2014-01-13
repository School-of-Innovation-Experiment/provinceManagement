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

def info_xls_baseinformation_gen():
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

def info_xls_baseinformation(request):
    """
    """
    def _format_number(i):
        i = str(i)
        i = '0' * (4-len(i)) + i
        return i

    proj_set = ProjectSingle.objects.all()
    xls_obj, workbook = info_xls_baseinformation_gen()

    # _index = 1
    _number= 1
    for proj_obj in proj_set:
        proj_obj.file_application = check_fileupload(proj_obj.file_application)
        proj_obj.file_interimchecklist = check_fileupload(proj_obj.file_interimchecklist)
        proj_obj.file_summary = check_fileupload(proj_obj.file_summary)
        proj_obj.file_projectcompilation = check_fileupload(proj_obj.file_projectcompilation)
        proj_obj.score_application = check_scoreapplication(proj_obj.score_application)
        get_expertscore(proj_obj)

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

def info_xls_expertscore_gen():
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')

    # generate header
    worksheet.write_merge(0, 0, 0, 19, '大连民族学院创新创业项目评分统计表')

    # generate body
    worksheet.write_merge(1, 1, 0, 0, '项目申报编号')
    worksheet.col(0).width = len('项目申报编号') * 200
    worksheet.write_merge(1, 1, 1, 1, '名称')
    worksheet.col(1).width = len('名称') * 800
    worksheet.write_merge(1, 1, 2, 2, '项目级别')
    worksheet.write_merge(1, 1, 3, 3, '指导教师')
    worksheet.col(3).width = len('指导教师') * 200
    worksheet.write_merge(1, 1, 4, 4, '项目选题意义')
    worksheet.write_merge(1, 1, 5, 5, '科技研究价值')
    worksheet.write_merge(1, 1, 6, 6, '项目创新之处')
    worksheet.write_merge(1, 1, 7, 7, '项目可行性')
    worksheet.write_merge(1, 1, 8, 8, '预期成果')
    worksheet.write_merge(1, 1, 9, 9, '指导教师科研能力')
    worksheet.write_merge(1, 1,10, 10, '总分')
    return worksheet, workbook

def info_xls_expertscore(request):
    """
    """
    def _format_number(i):
        i = str(i)
        i = '0' * (4-len(i)) + i
        return i

    proj_set = ProjectSingle.objects.all()
    xls_obj, workbook = info_xls_expertscore_gen()

    # _index = 1
    _number= 1
    for proj_obj in proj_set:
        scorelist=get_expertscore(proj_obj)

        row = 1 + _number
        xls_obj.write(row, 0, unicode(proj_obj.project_code)) 
        xls_obj.write(row, 1, unicode(proj_obj.title)) 
        xls_obj.write(row, 2, unicode(proj_obj.project_grade)) 
        xls_obj.write(row, 3, unicode(proj_obj.adminuser.get_name())) 
        xls_obj.write(row, 4, unicode(scorelist[0])) 
        xls_obj.write(row, 5, unicode(scorelist[1])) 
        xls_obj.write(row, 6, unicode(scorelist[2]))
        xls_obj.write(row, 7, unicode(scorelist[3])) 
        xls_obj.write(row, 8, unicode(scorelist[4]))  
        xls_obj.write(row, 9, unicode(scorelist[5])) 
        xls_obj.write(row, 10, unicode(scorelist[6])) 


        # _index += 1
        _number+= 1
    # write xls file
    save_path = os.path.join(TMP_FILES_PATH, "%s%s.xls" % (str(datetime.date.today().year), "年大连民族学院创新创业项目评分统计表"))
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
                
def get_expertscore(proj_obj):
    """
        get expert score
    """  

    project_id = proj_obj.project_id
    review_list = getSubjectReviewList(project_id)

    cnt_of_list = len(review_list)
    average_list = [sum(map(float, a)) / cnt_of_list for a in zip(*review_list)[1:]]
    loginfo(p=average_list,label="average_list")
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
            loginfo(p=obj_list,label="obj_list")
            review_list.append(obj_list)
        if review_list == []:
            inital_list = [u""]
            inital_list.extend([0.0]*7)
            review_list.append(inital_list)
        loginfo(p=review_list,label="review_list")
        return review_list
