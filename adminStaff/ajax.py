# coding: UTF-8
'''
Created on 2013-3-29

@author: sytmac
'''

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from adminStaff.forms import NumLimitForm, TimeSettingForm, SubjectCategoryForm, ExpertDispatchForm, SchoolDispatchForm
from adminStaff.models import  ProjectPerLimits, ProjectControl
from const.models import SchoolDict, NewsCategory
from const import *
from adminStaff.utils import DateFormatTransfer
from adminStaff.views import AdminStaffService
from school.models import Project_Is_Assigned, InsituteCategory ,ProjectSingle
from users.models import SchoolProfile
from news.models import News
import datetime
from backend.logging import logger, loginfo
from django.template.loader import render_to_string

@dajaxice_register
def NumLimit(request, form):
    dajax = Dajax()
    form = NumLimitForm(deserialize_form(form))
    if form.is_valid():
        school = SchoolDict.objects.get(id=form.cleaned_data["school_name"])
        a_limited_num = form.cleaned_data["a_limited_num"]
        b_limited_num = form.cleaned_data["b_limited_num"]
        try:
            school_obj = SchoolProfile.objects.get(school=school)
            if  ProjectPerLimits.objects.filter(school=school_obj).count() == 0 :
                projectlimit = ProjectPerLimits(school=school_obj,
                                                number=a_limited_num + b_limited_num,
                                                a_cate_number=a_limited_num)
                projectlimit.save()
            else:
                object = ProjectPerLimits.objects.get(school=school_obj)
                object.number = a_limited_num + b_limited_num
                object.a_cate_number = a_limited_num
                object.save()
            return simplejson.dumps({'status':'1','message':u'更新成功'})
        except SchoolProfile.DoesNotExist:
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
def ExpertImport(request, form):
    """
	Import Expert Profile directly without email
	"""
    expert_form = ExpertDispatchForm(deserialize_form(form))
    if expert_form.is_valid():
        password = expert_form.cleaned_data["expert_password"]
        email = expert_form.cleaned_data["expert_email"]
        insitute = expert_form.cleaned_data["expert_insitute"]
        name = email
        person_firstname = expert_form.cleaned_data["person_firstname"]
        if password == "":
            password = email.split('@')[0]
        flag = AdminStaffService.sendemail(request, name, person_firstname,password, email,EXPERT_USER, False, expert_insitute=insitute)
        if flag:
            message = u"导入成功"
            return simplejson.dumps({'field':expert_form.data.keys(), 'status':'1', 'message':message})
        else:
            message = u"相同权限用户已经存在，中断导入"
            return simplejson.dumps({'field':expert_form.data.keys(), 'status':'1', 'message':message})
    else:
        return simplejson.dumps({'field':expert_form.data.keys(),'error_id':expert_form.errors.keys(),'message':u"输入有误,请检查邮箱的合法性"})

@dajaxice_register
def  ExpertDispatch(request, form):
    expert_form =  ExpertDispatchForm(deserialize_form(form))
    if expert_form.is_valid():
        password = expert_form.cleaned_data["expert_password"]
        email = expert_form.cleaned_data["expert_email"]
        insitute = expert_form.cleaned_data["expert_insitute"]
        name = email
        person_firstname = expert_form.cleaned_data["person_firstname"]
        if password == "":
            password = email.split('@')[0]
        flag = AdminStaffService.sendemail(request, name, person_firstname,password, email,EXPERT_USER, expert_insitute=insitute)
        if flag:
            message = u"发送邮件成功"
            return simplejson.dumps({'field':expert_form.data.keys(), 'status':'1', 'message':message})
        else:
            message = u"相同邮件已经发送，中断发送"
            return simplejson.dumps({'field':expert_form.data.keys(), 'status':'1', 'message':message})
    else:
        return simplejson.dumps({'field':expert_form.data.keys(),'error_id':expert_form.errors.keys(),'message':u"输入有误,请检查邮箱的合法性"})
@dajaxice_register
def SchoolDispatch(request, form):
    #dajax = Dajax()
    school_form = SchoolDispatchForm(deserialize_form(form))
    if school_form.is_valid():
        password = school_form.cleaned_data["school_password"]
        email = school_form.cleaned_data["school_email"]
        name = email
        school_name = school_form.cleaned_data["school_name"]
        person_firstname = school_form.cleaned_data["person_firstname"]
        if password == "":
            password = email.split('@')[0]
        flag = AdminStaffService.sendemail(request, name, person_firstname,password, email,SCHOOL_USER, school_name=school_name)
        if flag:
            message = u"发送邮件成功"
            return simplejson.dumps({'field':school_form.data.keys(), 'status':'1', 'message':message})
        else:
            message = u"相同邮件已经发送，中断发送"
            return simplejson.dumps({'field':school_form.data.keys(), 'status':'1', 'message':message})
    else:
        return simplejson.dumps({'id':school_form.errors.keys(),'message':u"输入有误,请检查邮箱的合法性"})
@dajaxice_register
def judge_is_assigned(request,insitute):
    '''
    to judge if the projects that belong to the certain insitute has been assigned
    '''
    #dajax = Dajax()
    #query database
    try:
        insobj = InsituteCategory.objects.get(id=insitute)
    except InsituteCategory.DoesNotExist:
        return simplejson.dumps({'flag':None,'message':u"InstituteCategory 数据不完全，请更新数据库"})
    try:
        obj = Project_Is_Assigned.objects.get(insitute = insobj)
    except Project_Is_Assigned.DoesNotExist:
        return simplejson.dumps({'flag':None,'message':u"Project_Is_Assigned 数据不完全，请更新数据库"})
    return simplejson.dumps({'flag':obj.is_assigned})

@dajaxice_register
def get_subject_review_pass_p_list(request, project_id):
    '''
    to get subject evaluate list through project_id
    '''
    #dajax = Dajax()
    review_list = AdminStaffService.GetSubjectReviewPassPList(project_id)

    return simplejson.dumps({'review_list':review_list})

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
def Release_News(request):
    '''
    Release_News
    '''
    unsubjected = False
    subject_list = ProjectSingle.objects.all().order_by('school')
    for project in subject_list:
        if project.project_grade.grade == GRADE_UN:
            unsubjected = False
            break

    if unsubjected:
        release = False
    else:
        html = refresh_member_table(subject_list)
        release = True
        title=datetime.datetime.today().year
        data = News(news_title =title.__str__()+'年创新项目级别汇总', news_content = html,
                     news_category=NewsCategory.objects.get(category=NEWS_CATEGORY_ANNOUNCEMENT))
        data.save()        
    loginfo(p=release,label="release")
    return simplejson.dumps({'release':release})

def refresh_member_table(projectlist):

    return render_to_string("adminStaff/widgets/releasenews.html",
                            {"subject_list": projectlist})

@dajaxice_register
def Release_Excel(request):
    path = AdminStaffService.get_xls_path(request)
    loginfo(p=path,label="what")
    return simplejson.dumps({'path':path})

@dajaxice_register
def get_news_list(request,uid):

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
    

 