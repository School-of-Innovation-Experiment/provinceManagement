# coding: UTF-8
'''
Created on 2013-3-29

@author: sytmac
'''
import os, sys
from django.shortcuts import get_object_or_404
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from django.template.loader import render_to_string

#from adminStaff.forms import NumLimitForm, TimeSettingForm, SubjectCategoryForm, ExpertDispatchForm,SchoolDispatchForm,TemplateNoticeForm,FundsChangeForm,StudentNameForm, SchoolDictDispatchForm
from adminStaff.forms import *
from adminStaff.models import  ProjectPerLimits, ProjectControl,TemplateNoticeMessage
from const.models import SchoolDict, ProjectGrade, ApplyControl, OverStatus
from const import *
from adminStaff.utils import DateFormatTransfer
from adminStaff.views import AdminStaffService
from school.models import Project_Is_Assigned, InsituteCategory, ProjectSingle,ProjectFinishControl, PreSubmit, PreSubmitEnterprise
from users.models import SchoolProfile, AdminStaffProfile, StudentProfile
from news.models import News
from student.models import Funds_Group, Student_Group
from django.contrib.auth.models import User
from context import userauth_settings
from school.utility import get_recommend_limit,get_schooluser_project_modify_status,get_current_year, get_running_project_query_set
from django.db.models import Q

from const import *
import datetime
from backend.logging import logger, loginfo
from school.utility import get_current_project_query_set
from adminStaff.models import HomePagePic
from settings import IS_MINZU_SCHOOL, IS_DLUT_SCHOOL,MEDIA_URL,TMP_FILES_PATH
from adminStaff.utility import get_average_score_list,get_zipfiles_path
from adminStaff.utility import get_otherfiles_path
from backend.decorators import check_auth

def refresh_mail_table(request):
    email_list  = AdminStaffService.GetRegisterList(request)
    return render_to_string("adminStaff/widgets/email_table.html",
                            {"email_list": email_list})
def refresh_numlimit_table(request):
    school_limit_num_list = AdminStaffService.SchoolLimitNumList()
    return render_to_string("adminStaff/widgets/numlimit_table.html",
                            {'school_limit_list':school_limit_num_list})

@dajaxice_register
def NumLimit(request, form):
    form = NumLimitForm(deserialize_form(form))
    if form.is_valid():
        #school = SchoolProfile.objects.get(id=form.cleaned_data["school_name"])
        limited_num = form.cleaned_data["limited_num"]

        print form.cleaned_data['school_name']
        if form.cleaned_data["school_name"] == "-1": #处理所有学院的情况
            for school_obj in SchoolProfile.objects.all():
                if ProjectPerLimits.objects.filter(school = school_obj).count() == 0:
                    projectlimit = ProjectPerLimits(school = school_obj, number = limited_num)
                    projectlimit.save()
                else:
                    object = ProjectPerLimits.objects.get(school = school_obj)
                    minnum = ProjectSingle.objects.filter(Q(school = school_obj) & Q(is_past = False)).count()
                    object.number = max(limited_num, minnum)
                    object.save()
            table = refresh_numlimit_table(request)
            return simplejson.dumps({'status': '1', 'table': table, 'message': u'批量更新成功'})

        try:
            school_obj = SchoolProfile.objects.get(id=form.cleaned_data["school_name"])
            if  ProjectPerLimits.objects.filter(school=school_obj).count() == 0 :
                projectlimit = ProjectPerLimits(school=school_obj,
                                                number=limited_num)
                projectlimit.save()
            else:
                object = ProjectPerLimits.objects.get(school=school_obj)
                minnum = ProjectSingle.objects.filter(Q(school=school_obj)&Q(is_past=False)).count()
                if limited_num < minnum:
                    return simplejson.dumps({'status':'1',
                                             'message':u'更新失败,数量不得少于该学院已开始项目数量',})
                object.number = limited_num
                object.save()
            table = refresh_numlimit_table(request)
            return simplejson.dumps({'status':'1',
                                     'message':u'更新成功',
                                     'table':table})
        except SchoolDict.DoesNotExist:
            return simplejson.dumps({'status':'1','message':u'更新失败，选定的学校没有进行注册'})
    else:
        return simplejson.dumps({'id':form.errors.keys(),'message':u'输入错误'})

@dajaxice_register
def DeadlineSettings(request, form):
    #dajax = Dajax()
    form = TimeSettingForm(deserialize_form(form))
    if form.is_valid():
        # get cleaned_data
        psd = form.data["pre_start_date"]
        ped = form.data["pre_end_date"]
        fsd = form.data["final_start_date"]
        fed = form.data["final_end_date"]
        psdr = form.data["pre_start_date_review"]
        pedr = form.data["pre_end_date_review"]
        fsdr = form.data["final_start_date_review"]
        fedr = form.data["final_end_date_review"]
        try:
            object = ProjectControl.objects.get()
            object.pre_start_day = psd
            object.pre_end_day = ped
            object.final_start_day = fsd
            object.final_end_day = fed
            object.pre_start_day_review = psdr
            object.pre_end_day_review = pedr
            object.final_start_day_review = fsdr
            object.final_end_day_review = fedr
            object.save()
        except:
            return simplejson.dumps({'field':form.data.keys(),'error_id':form.errors.keys(),'message':u"输入数据有误格式为YYYY-MM-DD"})
        return simplejson.dumps({'field':form.data.keys(),'status':'1','message':u'更新成功'})
        #return simplejson.dumps({'field':form.data["pre_start_date"],'id':form,'status':'1','message':u'更新成功'})
    else:
        return simplejson.dumps({'field':form.data.keys(),'error_id':form.errors.keys(),'message':u"输入有误"})

@dajaxice_register
def  ExpertDispatch(request, form):
    #dajax = Dajax()
    expert_form =  ExpertDispatchForm(deserialize_form(form))
    if expert_form.is_valid():
        password = expert_form.cleaned_data["expert_password"]
        email = expert_form.cleaned_data["expert_email"]
        name = email
        person_name = expert_form.cleaned_data["expert_personname"]
        if password == "":
            password = email.split('@')[0]
        flag = AdminStaffService.sendemail(request, name, password, email,EXPERT_USER, expert_user=True,person_name=person_name)
        if flag:
            message = u"发送邮件成功"
            table = refresh_mail_table(request)
            return simplejson.dumps({'field':expert_form.data.keys(), 'status':'1', 'message':message, 'table':table})
        else:
            message = u"相同邮件已经发送，中断发送"
            return simplejson.dumps({'field':expert_form.data.keys(), 'status':'1', 'message':message})
    else:
        return simplejson.dumps({'field':expert_form.data.keys(),'error_id':expert_form.errors.keys(),'message':u"输入有误"})


@dajaxice_register
def SchoolDispatch(request, form):
    school_form = SchoolDictDispatchForm(deserialize_form(form))
    if school_form.is_valid():
        uid = school_form.cleaned_data['school_uid']
        email = school_form.cleaned_data["school_email"]
        school_name = school_form.cleaned_data["school_name"]
        person_name = school_form.cleaned_data["school_personname"]
        username = 'A_{}'.format(uid.strip(' '))
        flag = AdminStaffService.sendemail(
            request, username, None, email, SCHOOL_USER,
            school_name=school_name, person_name=person_name)
        if flag:
            message = u"发送邮件成功"
            table = refresh_mail_table(request)
            return simplejson.dumps({
                'field': school_form.data.keys(),
                'status': '1',
                'message': message,
                'table': table})
        else:
            message = u"相同邮件已经发送或内部错误"
            return simplejson.dumps({
                'field': school_form.data.keys(),
                'status': '1',
                'message': message})
    else:
        return simplejson.dumps({
            'field': school_form.data.keys(),
            'error_id': school_form.errors.keys(),
            'message': u"输入有误"})


@dajaxice_register
def judge_is_assigned(request, school):
    '''
    to judge if the projects that belong to the certain insitute has been assigned
    '''
    try:
        schoolObj = SchoolProfile.objects.get(id=int(school))
    except SchoolProfile.DoesNotExist:
        return simplejson.dumps({'flag':None,'message':u"SchoolProfile 数据不完全，请联系管理员更新数据库"})
    try:
        obj = Project_Is_Assigned.objects.get(school = schoolObj)
    except Project_Is_Assigned.DoesNotExist:
        return simplejson.dumps({'flag':None,'message':u"Project_Is_Assigned 数据不完全，请联系管理员更新数据库"})
    return simplejson.dumps({'flag':obj.is_assigned})

@dajaxice_register
def get_subject_review_list(request, project_id):
    '''
    to get subject evaluate list through project_id
    '''
    if check_auth(user = request.user, authority = SCHOOL_USER):
        identity = SCHOOL_USER
    else:
        identity = ADMINSTAFF_USER

    review_list = AdminStaffService.GetSubjectReviewList(project_id, identity)
    average_list = get_average_score_list(review_list)

    data = {"review_list": review_list,
            "average_list": average_list,
            }
    table = render_to_string("adminStaff/widgets/review_table.html", data)
    return simplejson.dumps({"table": table})

@dajaxice_register
def change_subject_recommend(request, project_id, changed_grade):
    """
    change the recommend state of single project
    """
    val = int(changed_grade)
    project = ProjectSingle.objects.get(project_id = project_id)
    school = SchoolProfile.objects.get(userid = request.user)
    exit_status = '1'
    res = ''
    if val == 1:
        res = "已推荐"
        if project.recommend:
            exit_status = '1'
        else:
            remaining = get_recommend_limit(school)[1]
            if remaining:
                project.recommend = True
                project.project_grade = ProjectGrade.objects.get(grade = GRADE_UN)
                project.save()
            else:
               exit_status = '0'
    else:
        res = val and "未推荐（学院级）" or "未推荐（校级）"
        change_to = val and GRADE_INSITUTE or GRADE_SCHOOL
        project.recommend = False
        project.project_grade = ProjectGrade.objects.get(grade = change_to)
        project.save()
    remaining = str(get_recommend_limit(school)[1])
    return simplejson.dumps({'status': exit_status, 'res': res, 'remaining': remaining})

@dajaxice_register
def change_subject_grade(request, project_id, changed_grade):
    '''
    change subject grade secretly
    '''
    AdminStaffService.SubjectGradeChange(project_id, changed_grade)
    project = ProjectSingle.objects.get(project_id = project_id)
    res = project.project_grade.get_grade_display()
    return simplejson.dumps({'status':'1', 'res':res})

@dajaxice_register
def change_project_overstatus(request, project_id, changed_overstatus):
    '''
    change project overstatus
    '''
    choices = dict(OVER_STATUS_CHOICES)
    if changed_overstatus in choices:
        AdminStaffService.ProjectOverStatusChange(project_id, changed_overstatus)
        res = choices[changed_overstatus]
    else:
        res = "操作失败，请重试"
    return simplejson.dumps({'status':'1', 'res':res})
@dajaxice_register
def change_project_unique_code(request, project_id,project_unique_code):
    '''
    change project_unique_code
    '''
    res = AdminStaffService.ProjectUniqueCodeChange(project_id, project_unique_code)
    return simplejson.dumps({'status':'1', 'res':res})

@dajaxice_register
def Release_Excel(request,exceltype,project_manage_form):
    path = AdminStaffService.get_xls_path(request,exceltype,project_manage_form)
    loginfo(p=path,label="path")
    return simplejson.dumps({'path':path})

@dajaxice_register
def get_news_list(request, uid):

    logger.info("sep delete news"+"**"*10)
    # check mapping relation
    try:
        delnews=News.objects.get(id=uid)
        if request.method == "POST":
            delnews.delete()
            return simplejson.dumps({"is_deleted": True,
                    "message": "delete it successfully!",
                    "uid": str(uid)})
        else:
            return simplejson.dumps({"is_deleted": False,
                                     "message": "Warning! Only POST accepted!"})
    except Exception, err:
        logger.info(err)

@dajaxice_register
def TemNoticeChange(request,form,origin):
    temnotice_form=TemplateNoticeForm(deserialize_form(form))
    if not temnotice_form.is_valid():
        ret = {'status': '2',
               'error_id': temnotice_form.errors.keys(),
               'message': u"输入有误，请重新输入"}
    elif not origin: #添加模版消息
        ret = new_temnotice(request,temnotice_form)
    else:  #添加模版消息
        ret = change_temnotice(request,temnotice_form,origin)
    return simplejson.dumps(ret)

@dajaxice_register
def Release_News(request, html):
    '''
    Release_News
    '''
    title=datetime.datetime.today().year + 1
    data = News(news_title =title.__str__()+'年创新项目级别汇总', news_content = html);
    data.save();
@dajaxice_register
def TemNoticeDelete(request, deleteId):
    group = TemplateNoticeMessage.objects.all()
    for temnotice in group.all():
        if temnotice.id == deleteId:
            temnotice.delete()
            table = refresh_temnotice_table(request)
            ret = {'status': '0', 'message': u"模版消息删除成功", 'table':table}
            break
    else:
        ret = {'status': '1', 'message': u"待删除模版消息不存在，请刷新页面"}
    return simplejson.dumps(ret)

def new_temnotice(request,temnotice_form):
    title = temnotice_form.cleaned_data["title"]
    message = temnotice_form.cleaned_data["message"]
    group = TemplateNoticeMessage.objects.all()
    if group.count() == TEMPLATE_NOTICE_MESSAGE_MAX:
        ret = {'status': '1', 'message': u"模版消息已满，不可添加"}
    else:
        new_temnotice = TemplateNoticeMessage(  noticeId =3,
                                                title = title,
                                                message=message)
        new_temnotice.save()
        table = refresh_temnotice_table(request)
        ret = {'status': '0', 'message': u"模版消息添加成功", 'table':table}
    return ret

def refresh_temnotice_table(request):
    templatenotice_group = TemplateNoticeMessage.objects.all()
    templatenotice_group_form = TemplateNoticeForm()
    _range = 1
    for i in templatenotice_group:
        i.iid = _range
        _range += 1

    return render_to_string("adminStaff/widgets/notice_message_table.html",
                            {"templatenotice_group": templatenotice_group,
                             "templatenotice_group_form": templatenotice_group_form})

def change_temnotice(request, temnotice_form, origin):
    title = temnotice_form.cleaned_data["title"]
    message = temnotice_form.cleaned_data["message"]
    group = TemplateNoticeMessage.objects.all()
    selectId = int(origin)
    for temnotice in group.all():
        if temnotice.id == selectId:
            temnotice.title = title
            temnotice.message = message
            temnotice.save()
            table = refresh_temnotice_table(request)
            ret = {'status': '0', 'message': u"模版消息变更成功", 'table':table}
            break
    else:
        ret = {'status': '1', 'message': u"输入有误，请刷新后重新输入"}
    return ret

@dajaxice_register
def finish_control(request,year_list):
    try:
        adminObj = AdminStaffProfile.objects.get(userid = request.user)
    except AdminStaffProfile.DoesNotExist:
        return simplejson.dumps({'flag':None,'message':u"AdminStaffProfile 数据不完全，请联系管理员更新数据库"})
    user = User.objects.get(id=adminObj.userid_id)
    year_finishing_list = []
    if adminObj.is_finishing ==False:
        if year_list != []:
            for temp in year_list:
                projectcontrol=ProjectFinishControl()
                projectcontrol.userid=user
                projectcontrol.project_year=temp
                projectcontrol.save()
            adminObj.is_finishing=True
            adminObj.save()
            flag = True

            projectfinish = ProjectFinishControl.objects.filter(userid =user.id)
            for finishtemp in projectfinish :
                if finishtemp.project_year not in year_finishing_list:
                    year_finishing_list.append(finishtemp.project_year)
            year_finishing_list = sorted(year_finishing_list)
        else:
            return simplejson.dumps({'flag':None,'message':u"项目年份未选择或是没有未结题项目"})
    else:
        projectcontrol_list=ProjectFinishControl.objects.filter(userid=user)
        projectcontrol_list.delete()
        adminObj.is_finishing=False
        adminObj.save()
    flag = adminObj.is_finishing
    return simplejson.dumps({'flag': flag,'year_finishing_list':year_finishing_list})

@dajaxice_register
def FundsDelete(request,delete_id,pid):
    delete_id = int(delete_id)
    try:
        project = ProjectSingle.objects.get(project_id = pid)
    except:
        raise Http404
    group = project.funds_group_set
    for funds in group.all():
        if funds.id == delete_id:
            project.funds_remain = project.funds_remain + funds.funds_amount
            funds.delete()
            project.save()
            table = refresh_funds_table(request,project)
            ret = {'status': '0', 'message': u"条目删除成功", 'table':table,
                            "funds_total":project.funds_total,
                            "funds_remain":project.funds_remain}
            break
    else:
        ret = {'status': '1', 'message': u"待删除条目不存在"}
    return simplejson.dumps(ret)

@dajaxice_register
def fundsChange(request,form,name,pid):
    project_id = pid
    funds_form = FundsChangeForm(deserialize_form(form))
    if not funds_form.is_valid():
        ret = {'status': '2'}
    else:
        ret = new_or_update_funds(request,project_id,funds_form,name)
    return simplejson.dumps(ret)
@dajaxice_register
def set_recommend_rate(request, set_val):
    message = ""
    try:
        set_val = float(set_val)
        if set_val < 0 or set_val > 100: raise
    except:
        message = "wrong input"
        return simplejson.dumps({'message': message})
    recommend_rate_obj = SchoolRecommendRate.load()
    recommend_rate_obj.rate = set_val
    recommend_rate_obj.save()
    return simplejson.dumps({'message': message, 'set_val': str(set_val)})

def new_or_update_funds(request,pid,funds_form,name):
    funds_studentname   = name#funds_form.cleaned_data["student_choice"]
    funds_amount        = funds_form.cleaned_data["funds_amount"]
    funds_detail        = funds_form.cleaned_data["funds_detail"]
    funds_total         = funds_form.cleaned_data["funds_total"]
    try:
        project = ProjectSingle.objects.get(project_id = pid)
    except:
        raise Http404
    group = Funds_Group.objects.filter(project_id = pid)
    num = Funds_Group.objects.filter(project_id = pid).count()
    cost = funds_amount
    for funds in group.all():
        cost = cost + funds.funds_amount
    loginfo(cost)
    if funds_total != None:
        project.funds_total = funds_total
    if project.funds_total >= cost :
        new_funds = Funds_Group(
                      project_id = project,
                      student_name = funds_studentname,
                      funds_amount = funds_amount,
                      funds_detail = funds_detail,
                      )
        new_funds.save()
        project.funds_remain = project.funds_total - cost
        project.save()
        table = refresh_funds_table(request,project)
        ret = {'status': '0', 'message': u"经费信息添加成功", 'table':table,
                            "funds_total":project.funds_total,
                            "funds_remain":project.funds_remain}
    else:
        ret = {'status': '1', 'message': u"无经费余额，无法添加经费明细，或经费总额不对"}
    return ret
def refresh_funds_table(request,project):
    funds_list = Funds_Group.objects.filter(project_id = project.project_id)
    context = userauth_settings(request)
    context["project_funds_list"] = funds_list
    context['is_addFundDetail'] = get_schooluser_project_modify_status(project)
    return render_to_string("widgets/fund/fund_table.html",
                            context)

@dajaxice_register
def FileDeleteConsistence(request, fid):
    """
    Delete files in history file list
    """
    logger.info("sep delete files"+"**"*10)
    # check mapping relation
    f = get_object_or_404(HomePagePic, id=fid)

    if request.method == "POST":
        try:
            os.remove(f.pic_obj.url)
            f.delete()
        except: pass
        return simplejson.dumps({"is_deleted": True,
                                 "message": "delete it successfully!",
                                 "fid": str(fid)})
    else:
        return simplejson.dumps({"is_deleted": False,
                                 "message": "Warning! Only POST accepted!"})
@dajaxice_register
def auto_ranking(request):
    message = ""
    project_set = list(get_current_project_query_set().select_related('school'))
    project_set.sort(key = lambda x: (x.school.school.schoolName,
                                      x.project_category.category,
                                      x.adminuser.name))
    school_codes = {}
    for p in project_set:
        school_codes[p.school] = p.school.school.school_code

    project_control = ProjectControl.objects.all()[0]
    year = project_control.pre_start_day.year

    id_fmt = '{:04d}{}{}{:02d}{:04d}'

    for i, p in enumerate(project_set, start=1):
        p.project_unique_code = id_fmt.format(year + 1, DUT_code, school_codes[p.school], p.project_category.id, i)
        p.save()
    return simplejson.dumps({"message": message})

@dajaxice_register
def student_code_project_query(request, student_code):
    """
    根据学生的学号查询与之相关的进行中项目
    """
    message = ""
    project = [project for project in get_running_project_query_set() if project.student_group_set.filter(studentId = student_code)]
    if project:
        #按照逻辑，每个学号只能存在于一个正在进行中项目，所以直接获取project[0]即可
        message = 'ok'
        table_html = render_to_string("adminStaff/widgets/project_table.html", {"proj_list": project, "IS_DLUT_SCHOOL": IS_DLUT_SCHOOL,"IS_DELETE_TABLE": False, "IS_MINZU_SCHOOL": IS_MINZU_SCHOOL})
        return simplejson.dumps({"message": message, "table": table_html})
    else:
        message = "not found"
        return simplejson.dumps({"message": message})

"""
def student_code_project_query(request, student_code):

    message = ""
    project = [project for project in get_running_project_query_set() if project.student_group_set.filter(studentId = student_code)]
    if project:
        #按照逻辑，每个学号只能存在于一个正在进行中项目，所以直接获取project[0]即可
        message = 'ok'
        table_html = render_to_string("adminStaff/widgets/project_table.html", {"item": project[0], "IS_DLUT_SCHOOL": IS_DLUT_SCHOOL, "IS_MINZU_SCHOOL": IS_MINZU_SCHOOL})
"""


@dajaxice_register
def delete_project_query(request, delete_info):
    """
    根据学生的学号查询与之相关的进行中项目
    """
    loginfo(p=delete_info,label="delete_info")
    message = ""
    project_list = ProjectSingle.objects.filter(Q(adminuser__name__icontains = delete_info.strip(' ')))
    if project_list:
        #按照逻辑，每个学号只能存在于一个正在进行中项目，所以直接获取project[0]即可
        message = 'ok'
        table_html = render_to_string("adminStaff/widgets/project_table.html", {"proj_list": project_list, "IS_DLUT_SCHOOL": IS_DLUT_SCHOOL, "IS_DELETE_TABLE": True,"IS_MINZU_SCHOOL": IS_MINZU_SCHOOL})
        return simplejson.dumps({"message": message, "table": table_html})
    else:
        message = "not found"
        return simplejson.dumps({"message": message})

@dajaxice_register
def changeyear_project_query(request, changeyear_info):
    """
    根据学生的学号查询与之相关的进行中项目
    """
    loginfo(p=changeyear_info,label="changeyear_info")
    message = ""
    subject_grade_form = SubjectGradeForm()
    project_list = ProjectSingle.objects.filter(Q(adminuser__name = changeyear_info),
        Q(project_category__category = 'research'))
    if project_list:
        #按照逻辑，每个学号只能存在于一个正在进行中项目，所以直接获取project[0]即可
        message = 'ok'
        table_html = render_to_string("adminStaff/widgets/project_change_year_and_grade.html", {"proj_list": project_list, "IS_DLUT_SCHOOL": IS_DLUT_SCHOOL, "IS_DELETE_TABLE": True,"IS_MINZU_SCHOOL": IS_MINZU_SCHOOL, 'subject_grade_form': subject_grade_form})
        return simplejson.dumps({"message": message, "table": table_html})
    else:
        message = "not found"
        return simplejson.dumps({"message": message})

@dajaxice_register
def changeyear_project_id(request, pid, year):
    """
    根据学生的学号查询与之相关的进行中项目
    """
    loginfo(p=pid,label="pid")
    message = ""
    try:
        project = ProjectSingle.objects.get(Q(project_id = pid))
        project.year = int(year)
        project.save()
        message = 'ok'
        return simplejson.dumps({"message": message, "pid": pid, "year": year})
    except Exception, e:
        print e
        message = "not found"
        return simplejson.dumps({"message": message})

@dajaxice_register
def delete_project_id(request, pid):
    """
    根据学生的学号查询与之相关的进行中项目
    """
    loginfo(p=pid,label="pid")
    message = ""
    try:
        project = ProjectSingle.objects.get(Q(project_id = pid))
        student = project.student
        user = student.userid
        user.delete()
        message = 'ok'
        return simplejson.dumps({"message": message, "pid": pid})
    except Exception, e:
        print e
        message = "not found"
        return simplejson.dumps({"message": message})

from base64 import b64encode as b64en
from adminStaff.utility import get_manager
import jsonrpclib
import simplejson
from settings import RPC_SITE
@dajaxice_register
def project_sync(request,project_sync_list,username,password):
    def get_projsingle_dict(proj_single):
        ret = {}
        student_user = proj_single.student.userid
        ret['student_username'] = b64en(student_user.username)
        # ret['student_username'] = b64en('lpyiou@qq.com')
        ret['student_person_firstname'] = b64en(student_user.first_name)
        ret['student_email'] = b64en(student_user.email)
        # ret['student_email'] = b64en('lpyiou@qq.com') #test
        ret['student_password'] = b64en(student_user.email.split('@')[0])
        # ret['student_password'] = b64en('lpyiou')
        ret['project_category'] = proj_single.project_category.category

        team = get_manager(proj_single)
        ret['email'] = student_user.email
        ret['project_code'] = proj_single.project_unique_code
        ret['telephone'] = team['telephone']
        ret['im'] = ''
        ret['inspector'] = proj_single.adminuser.name
        ret['inspector_title'] = proj_single.adminuser.titles
        ret['members'] = team['memberlist']
        for attr in projsingle_attrs:
            ret[attr] = getattr(proj_single, attr)
        return ret
    def get_presubmit_dict(proj_single):
        presubmit = PreSubmit.objects.get(project_id=proj_single)
        ret = {}
        ret['origin'] = presubmit.original.origin
        for attr in presubmit_attrs:
            ret[attr] = getattr(presubmit, attr)
        return ret
    def get_presubmitenterprise_dict(proj_single):
        presubmitenterprise = PreSubmitEnterprise.objects.get(project_id=proj_single)
        ret = {}
        ret['origin'] = presubmitenterprise.original.origin
        ret['maturity'] = presubmitenterprise.maturity.maturity
        ret['enterprise_teacher_name'] = presubmitenterprise.enterpriseTeacher.name
        ret['enterprise_teacher_telephone'] = presubmitenterprise.enterpriseTeacher.telephone
        ret['enterprise_teacher_titles'] = presubmitenterprise.enterpriseTeacher.titles
        ret['enterprise_teacher_jobs'] = presubmitenterprise.enterpriseTeacher.jobs
        for attr in presubmitenterprise_attrs:
            ret[attr] = getattr(presubmitenterprise, attr)
        return ret
    projsingle_attrs = ['project_id', 'title', 'year']
    # fk: project_id, original, maturity, enterpriseTeacher
    presubmitenterprise_attrs = ['background', 'innovation', 'industry', 'product', 'funds_plan',
                                 'operating_mode', 'risk_management', 'financial_pred', 'inspector_comments',
                                 'school_comments']
    # fk: project_id, original
    presubmit_attrs = ['background', 'key_notes', 'innovation', 'progress_plan', 'funds_plan',
                       'pre_results', 'inspector_comments', 'school_comments']
    dict_obj = {'username': b64en(username), 'password': b64en(password), 'projects': []}
    for proj in project_sync_list:
        try:
            proj_single = ProjectSingle.objects.get(project_id=proj)
        except:
            print "proj %s not exist!" % proj
            return simplejson.dumps({'status':'1', 'result': u"项目 %s 不存在" % proj_single.title})
        proj_dict = get_projsingle_dict(proj_single)
        try:
            if proj_single.project_category.category == CATE_INNOVATION:
                proj_dict['presubmit_type'] = 'presubmit'
                proj_dict.update(get_presubmit_dict(proj_single))
            else:
                proj_dict['presubmit_type'] = 'presubmitenterprise'
                proj_dict.update(get_presubmitenterprise_dict(proj_single))
        except:
            return simplejson.dumps({'status':'1', 'result': u"项目 %s 申请书存在问题 !" % proj_single.title})
        dict_obj['projects'].append(proj_dict)
    try:
        server = jsonrpclib.Server(RPC_SITE)
        result = server.SyncProjects(simplejson.dumps(dict_obj))
        loginfo(result)
    except:
        return simplejson.dumps({'status':'1', 'result': '省级版服务器异常，请稍后再试'})
    return simplejson.dumps({'status':'0', 'result': result})

@dajaxice_register
def download_zipfiles(request,filetype,project_manage_form):
    if filetype == 'other_files':
        path = get_otherfiles_path(request, project_manage_form)
    else:
        path = get_zipfiles_path(request,filetype,project_manage_form)
    path = MEDIA_URL + "tmp" + path[len(TMP_FILES_PATH):]
    return simplejson.dumps({'path':path})


@dajaxice_register
def applicaton_control(request):
    ac, _ = ApplyControl.objects.get_or_create(origin=None)
    ac.is_applying = False if ac.is_applying else True
    ac.save()
    flag = ac.is_applying
    return simplejson.dumps({'flag': flag})


@dajaxice_register
def auto_finish(request, year_list):
    os_ov = OverStatus.objects.get(status=OVER_STATUS_NORMAL)
    no_nov = OverStatus.objects.get(status=OVER_STATUS_NOTOVER)
    for year in year_list:
        try:
            pros = ProjectSingle.objects.filter(
                year=year, over_status=no_nov)
            pros.update(over_status=os_ov)
        except Exception, e:
            loginfo(e)
            return simplejson.dumps({'flag': 1})
    return simplejson.dumps({'flag':'0', 'auto_finished': year_list})


@dajaxice_register
def switch_category(request, pid, cname):
    ret = {'status': -1}
    try:
        project = ProjectSingle.objects.get(project_unique_code=pid)
    except ProjectSingle.DoesNotExist, e:
        loginfo(e)
        try:
            project = Student_Group.objects.get(studentId=pid).project
            if not project:
                raise ProjectSingle.DoesNotExist
        except (Student_Group.DoesNotExist, ProjectSingle.DoesNotExist), e:
            loginfo(e)
            ret['status'] = 1
    finally:
        if ret['status'] == 1:
            return simplejson.dumps(ret)
    try:
        cate = ProjectCategory.objects.get(category=cname)
    except ProjectCategory.DoesNotExist, e:
        loginfo(e)
        ret['status'] = 2
        return simplejson.dumps(ret)
    if project.project_category.category.startswith('enterprise') and\
            not cate.category.startswith('enterprise'):
        loginfo('Wrong switch')
        ret['status'] = 3
        return simplejson.dumps(ret)
    elif not project.project_category.category.startswith('enterprise') and\
            cate.category.startswith('enterprise'):
        ret['status'] = 4
        return simplejson.dumps(ret)
    project.project_category = cate
    project.save()
    return simplejson.dumps({'status': 0})

@dajaxice_register
def change_all_grade(request):
    """
    修改所有等级为未指定的项目的等级为校级
    """
    try:
        project = ProjectSingle.objects.filter(project_grade__grade=GRADE_UN)
        for p in project:
            p.project_grade = ProjectGrade.objects.get(grade=GRADE_SCHOOL)
            p.save()
        message = '修改成功！'
        return simplejson.dumps({"message": message})
    except Exception, e:
        print e
        message = "修改失败！"
        return simplejson.dumps({"message": message})

@dajaxice_register
def change_pass(request, username):
    """
    校级管理员重置用户密码
    """
    user = User.objects.filter(username = username)
    if user:
        user = user[0]
        user.set_password('123456')
        user.save()
        return simplejson.dumps({"has_changed": True})
    return simplejson.dumps({"has_changed": False})
