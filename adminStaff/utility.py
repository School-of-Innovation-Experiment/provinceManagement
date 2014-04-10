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

def get_average_score_list(review_list):
    cnt_of_list = len(review_list)
    return [sum(a) / (cnt_of_list - a.count(0)) for a in zip(*review_list)[1:]]
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
    worksheet.write_merge(1, 1, 5, 5, '开题报告')
    worksheet.write_merge(1, 1, 6, 6, '中期检查表')
    worksheet.write_merge(1, 1, 7, 7, '结题验收表')
    worksheet.write_merge(1, 1, 8, 8, '项目汇编')
    worksheet.write_merge(1, 1, 9, 9, '申请学分')
    worksheet.write_merge(1, 1, 10, 10, '是否结题')
    worksheet.col(10).width = len('是否结题') * 300
    worksheet.write_merge(1, 1, 11, 11, '负责人电话')
    worksheet.col(11).width = len('负责人电话') * 200
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
        proj_obj.file_opencheck = check_fileupload(proj_obj.file_opencheck)
        get_expertscore(proj_obj)
        teammember = get_manager(proj_obj)

        row = 1 + _number
        xls_obj.write(row, 0, unicode(proj_obj.project_code)) 
        xls_obj.write(row, 1, unicode(proj_obj.title)) 
        xls_obj.write(row, 2, unicode(proj_obj.project_grade)) 
        xls_obj.write(row, 3, unicode(proj_obj.adminuser.get_name())) 
        xls_obj.write(row, 4, unicode(proj_obj.file_application))
        xls_obj.write(row, 5, unicode(proj_obj.file_opencheck))  
        xls_obj.write(row, 6, unicode(proj_obj.file_interimchecklist)) 
        xls_obj.write(row, 7, unicode(proj_obj.file_summary))
        xls_obj.write(row, 8, unicode(proj_obj.file_projectcompilation)) 
        xls_obj.write(row, 9, unicode(proj_obj.score_application))  
        xls_obj.write(row, 10, unicode(proj_obj.over_status)) 
        xls_obj.write(row, 11, unicode(teammember['telephone']))


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

def project_excel():
    pass

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
    average_list = [sum(map(float, a)) / len(filter(bool, a)) for a in zip(*review_list)[1:]]
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

def info_xls_province_gen():
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('sheet1')

    # generate header
    worksheet.write_merge(0, 0, 0, 19, '大连民族学院大学生创新创业训练计划项目信息汇总表')

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
    worksheet.write_merge(1, 4, 14, 18, '项目简介（100字以内）')

    return worksheet, workbook

def info_xls_projectsummary(request):
    """
    """

    def _format_number(i):
        i = str(i)
        i = '0' * (4-len(i)) + i
        return i

    proj_set = ProjectSingle.objects.all().order_by('school','project_grade')
    xls_obj, workbook = info_xls_province_gen()

    # _index = 1
    _number= 1
    for proj_obj in proj_set:
        teammember = get_manager(proj_obj)

        pro_type = PreSubmit if proj_obj.project_category.category == CATE_INNOVATION else PreSubmitEnterprise
        loginfo(p=proj_obj.title, label="project category") 
        innovation = pro_type.objects.get(project_id=proj_obj.project_id)

        row = 4 + _number
        xls_obj.write(row, 0, "%s" % _format_number(_number))
        xls_obj.write(row, 1, unicode(proj_obj.school.school))
        xls_obj.write(row, 2, unicode(proj_obj.project_code))
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
        xls_obj.write_merge(row, row, 14, 18, unicode(innovation.innovation)) # both enterprise and innovation has innovation attr

        # _index += 1
        _number+= 1
    # write xls file
    save_path = os.path.join(TMP_FILES_PATH, "%s%s.xls" % (str(datetime.date.today().year), "年大连民族学院大学生创新创业训练计划项目信息汇总表"))
    workbook.save(save_path)
    return save_path


def get_manager(project):
    """
        get teammanager's name and student_id
    """
    teammember = {'manager_name':'None','manager_studentid':'None','memberlist':'None','count':0,'telephone':'',}
    loginfo(p=teammember,label="teammember")
    student_Group=Student_Group.objects.filter(project_id=project.project_id)
    loginfo(p=student_Group,label="student_Group")
    if student_Group.count() > 0:
        manager = student_Group[0]
        teammember['manager_name'] = manager.studentName
        teammember['telephone'] = manager.telephone
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

def get_projectlist(request):
    """
    根据身份筛选项目
    返回：QuerySet对象
    """
    if check_auth(user=request.user, authority=ADMINSTAFF_USER):
        proj_set = ProjectSingle.objects.all()
    elif check_auth(user=request.user, authority=SCHOOL_USER):
        school = SchoolProfile.objects.get(userid=request.user)
        proj_set = ProjectSingle.objects.filter(school_id=school)
    return proj_set
