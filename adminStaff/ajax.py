# coding: UTF-8
'''
Created on 2013-3-29

@author: sytmac
'''

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from django.template.loader import render_to_string

from adminStaff.forms import NumLimitForm, TimeSettingForm, SubjectCategoryForm, ExpertDispatchForm,SchoolDispatchForm,TemplateNoticeForm,FundsChangeForm,StudentNameForm
from adminStaff.models import  ProjectPerLimits, ProjectControl,TemplateNoticeMessage
from const.models import SchoolDict, ProjectGrade
from const import *
from adminStaff.utils import DateFormatTransfer
from adminStaff.views import AdminStaffService
from school.models import Project_Is_Assigned, InsituteCategory, ProjectSingle,ProjectFinishControl
from users.models import SchoolProfile, AdminStaffProfile
from news.models import News
from student.models import Funds_Group
from django.contrib.auth.models import User

from school.utility import get_recommend_limit

from const import *
import datetime
from backend.logging import logger, loginfo

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
        try:
            school_obj = SchoolProfile.objects.get(id=form.cleaned_data["school_name"])
            if  ProjectPerLimits.objects.filter(school=school_obj).count() == 0 :
                projectlimit = ProjectPerLimits(school=school_obj,
                                                number=limited_num)
                projectlimit.save()
            else:
                object = ProjectPerLimits.objects.get(school=school_obj)
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
        person_name = expert_form.cleaned_data["person_firstname"]
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
    #dajax = Dajax()
    school_form = SchoolDictDispatchForm(deserialize_form(form))
    if school_form.is_valid():
        password = school_form.cleaned_data["school_password"]
        email = school_form.cleaned_data["school_email"]
        name = email
        school_name = school_form.cleaned_data["school_name"]
        person_name = school_form.cleaned_data["person_firstname"]
        if password == "":
            password = email.split('@')[0]
        flag = AdminStaffService.sendemail(request, name, password,email,SCHOOL_USER, school_name=school_name,person_name = person_name)
        loginfo(flag)
        if flag:
            message = u"发送邮件成功"
            table = refresh_mail_table(request)
            return simplejson.dumps({'field':school_form.data.keys(), 'status':'1', 'message':message, 'table': table})
        else:
            message = u"相同邮件已经发送，中断发送"
            return simplejson.dumps({'field':school_form.data.keys(), 'status':'1', 'message':message})
    else:
        return simplejson.dumps({'id':school_form.errors.keys(),'message':u"输入有误"})
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
    review_list = AdminStaffService.GetSubjectReviewList(project_id)

    cnt_of_list = len(review_list)

    average_list = [sum(map(float, a)) / cnt_of_list for a in zip(*review_list)[1:]]
    return simplejson.dumps({'review_list':review_list, 'average_list': average_list})

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
    res = changed_grade == "nation" and "国家级" or "省级"
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
    title=datetime.datetime.today().year
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
        else:
            return simplejson.dumps({'flag':None,'message':u"项目年份未选择或是没有未结题项目"})
    else:
        projectcontrol_list=ProjectFinishControl.objects.filter(userid=user)
        projectcontrol_list.delete()
        adminObj.is_finishing=False
        adminObj.save()
    flag = adminObj.is_finishing
    return simplejson.dumps({'flag': flag})

@dajaxice_register
def fundsChange(request,form,name,pid):
    project_id = pid
    funds_form = FundsChangeForm(deserialize_form(form))
    if not funds_form.is_valid():
        ret = {'status': '2'}
    else:
        ret = new_or_update_funds(request,project_id,funds_form,name)
    return simplejson.dumps(ret)

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
        table = refresh_funds_table(request,pid)
        ret = {'status': '0', 'message': u"经费信息添加成功", 'table':table,
                            "funds_total":project.funds_total,
                            "funds_remain":project.funds_remain}
    else:
        ret = {'status': '1', 'message': u"无经费余额，无法添加经费明细，或经费总额不对"}
    return ret

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
            table = refresh_funds_table(request,pid)
            ret = {'status': '0', 'message': u"条目删除成功", 'table':table,
                            "funds_total":project.funds_total,
                            "funds_remain":project.funds_remain}
            break
    else:
        ret = {'status': '1', 'message': u"待删除条目不存在"}
    return simplejson.dumps(ret)

def refresh_funds_table(request,pid):

    funds_list    = Funds_Group.objects.filter(project_id = pid)

    return render_to_string("adminStaff/widgets/funds_table.html",
                            {"project_funds_list": funds_list})
