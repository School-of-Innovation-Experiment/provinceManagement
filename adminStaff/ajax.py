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

from adminStaff.forms import NumLimitForm, TimeSettingForm, SubjectCategoryForm, ExpertDispatchForm, SchoolDispatchForm, SchoolDictDispatchForm,TemplateNoticeForm
from adminStaff.models import  ProjectPerLimits, ProjectControl,TemplateNoticeMessage
from const.models import SchoolDict
from const import *
from adminStaff.utils import DateFormatTransfer
from adminStaff.views import AdminStaffService
from school.models import Project_Is_Assigned, InsituteCategory
from users.models import SchoolProfile
from news.models import News
import datetime

def refresh_mail_table(request):
    email_list  = AdminStaffService.GetRegisterList()
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
        if password == "":
            password = email.split('@')[0]
        flag = AdminStaffService.sendemail(request, name, password, email,EXPERT_USER, expert_user=True)
        if flag:
            message = u"发送邮件成功"
            table = refresh_mail_table(request)
            return simplejson.dumps({'field':expert_form.data.keys(), 'status':'1', 'message':message, 'table':table})
        else:
            message = u"相同邮件已经发送，中断发送"
            return simplejson.dumps({'field':expert_form.data.keys(), 'status':'1', 'message':message})
    else:
        return simplejson.dumps({'field':expert_form.data.keys(),'error_id':expert_form.errors.keys(),'message':u"输入有误,请检查邮箱的合法性"})
@dajaxice_register
def SchoolDispatch(request, form):
    #dajax = Dajax()
    school_form = SchoolDictDispatchForm(deserialize_form(form))
    if school_form.is_valid():
        password = school_form.cleaned_data["school_password"]
        email = school_form.cleaned_data["school_email"]
        name = email
        school_name = school_form.cleaned_data["school_name"]
        if password == "":
            password = email.split('@')[0]
        flag = AdminStaffService.sendemail(request, name, password, email,SCHOOL_USER, school_name=school_name)
        if flag:
            message = u"发送邮件成功"
            table = refresh_mail_table(request)
            return simplejson.dumps({'field':school_form.data.keys(), 'status':'1', 'message':message, 'table': table})
        else:
            message = u"相同邮件已经发送，中断发送"
            return simplejson.dumps({'field':school_form.data.keys(), 'status':'1', 'message':message})
    else:
        return simplejson.dumps({'id':school_form.errors.keys(),'message':u"输入有误,请检查邮箱的合法性"})
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
    #dajax = Dajax()
    review_list = AdminStaffService.GetSubjectReviewList(project_id)

    return simplejson.dumps({'review_list':review_list})

@dajaxice_register
def change_subject_grade(request, project_id, changed_grade):
    '''
    change subject grade secretly
    '''
    AdminStaffService.SubjectGradeChange(project_id, changed_grade)
    return simplejson.dumps({'status':'1'})

@dajaxice_register
def TemnoticeChange(request):
    #temnotice_form=TemplateNoticeForm(deserialize_form(form))
    # if not temnotice_form.is_valid();
    #     ret = {'status': '2',
    #            'error_id': temnotice_form.errors.keys(),
    #            'message': u"输入有误，请重新输入"}
    # elif not origin: #添加模版消息
    #     ret = new_temnotice(request,temnotice_form)
    # else:  #添加模版消息
    #     ret = change_temnotice(request,temnotice_form,origin)
    ret = {'status': '2',
           'message': u"输入有误，请重新输入"}

    return simplejson.dumps(ret)

@dajaxice_register
def Release_News(request, html):
    '''
    Release_News
    '''
    title=datetime.datetime.today().year
    data = News(news_title =title.__str__()+'年创新项目级别汇总', news_content = html);
    data.save();


def new_temnotice(request,temnotice_form):
    title = temnotice_form.cleaned_data["title"]
    message = temnotice_form.cleaned_data["message"]

    # group = project.student_group_set

        # if group.count() == MEMBER_NUM_LIMIT[project.project_category.category]:
        #     ret = {'status': '1', 'message': u"人员已满，不可添加"}
        # else:
    # new_temnotice = TemplateNoticeMessage(  noticeId =3,
    #                                         title = title,
    #                                         message=message)
    # new_temnotice.save()
    table = refresh_member_table(request)
    ret = {'status': '0', 'message': u"添加成功", 'table':table}
    return ret
def refresh_temnotice_table(request):
    templatenotice_group = TemplateNoticeMessage.objects.all()
    templatenotice_group_form = TemplateNoticeForm()

    return render_to_string("adminStaff/widgets/notice_message_table.html",
                            {"templatenotice_group": templatenotice_group,
                             "templatenotice_group_form": templatenotice_group_form})