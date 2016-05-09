# coding: UTF-8
'''
Created on 2013-3-29

@author: sytmac
'''

from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from adminStaff.forms import NumLimitForm, TimeSettingForm, SubjectCategoryForm, ExpertDispatchForm, SchoolDispatchForm, SchoolCategoryForm, ResetSchoolPasswordForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from adminStaff.models import  ProjectPerLimits, ProjectControl
from const.models import SchoolDict, NewsCategory, InsituteCategory, ProjectRecommendStatus
from const import *
from adminStaff.utils import DateFormatTransfer
from adminStaff.views import AdminStaffService
from school.models import *
from users.models import SchoolProfile, ExpertProfile
from news.models import News
import datetime
from backend.logging import logger, loginfo
from django.template.loader import render_to_string
from backend.utility import getContext
from school.utility import *

import random, math, datetime, time

@dajaxice_register
def ShowDelete(request, uid):
    show = ShowProjectSingle.objects.get(project_id = uid)
    show.delete()
    return ""

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

            # num_limit_form = forms.NumLimitForm()
            school_limit_num_list = AdminStaffService.SchoolLimitNumList()
            page = request.GET.get('page')

            context = getContext(school_limit_num_list, page, 'item', 0)
            table = render_to_string("adminStaff/widgets/projectlimitnumsettingsTable.html",
                           context)
            return simplejson.dumps(
                {'status':'1',
                 'table': table, 
                 'message':u'更新成功'})
        except SchoolProfile.DoesNotExist:
            return simplejson.dumps({'status':'0','message':u'更新失败，选定的学校没有进行注册'})
    else:
        return simplejson.dumps({'status':'0', 'id':form.errors.keys(),'message':u'输入错误'})

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
def RemoveExpert(request, email):
    """
    Remove the exist expert user from database
    """
    User.objects.get(email = email).delete()
    #ExpertProfile.objects.get(userid__email = email).delete()
    return simplejson.dumps({"status":"1"})

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
        name = email.split('@')[0]
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
def change_subject_grade(request, project_id, changed_grade,page,school_name):
    '''
    change subject grade secretly
    '''
    
    AdminStaffService.SubjectGradeChange(project_id, changed_grade)
    table = refresh_to_table(page,school_name)
    return simplejson.dumps({'status':'1','table':table})
@dajaxice_register
def Release_News(request):
    '''
    Release_News
    '''
    unsubjected = False
    subject_list = ProjectSingle.objects.all().order_by('school').exclude(school__schoolName=u'测试用学校')
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

@dajaxice_register
def refresh_alloc_table(request, insitute):
    subject_list = get_current_project_query_set().filter(insitute_id=insitute)
    page = request.GET.get("page")
    context = getContext(subject_list, page, 'subject', 0)
    table_html = render_to_string("adminStaff/widgets/subjectalloc_table.html", context)
    return simplejson.dumps({"table": table_html})
def refresh_to_table(page,school_name):
    if school_name == "None": school_name = None
   # subject_list = AdminStaffService.GetSubject_list(school = school_name)
    subject_list = get_current_project_query_set().filter(school = school_name)
    context = getContext(subject_list, page, 'item', 0) 
    context.update({"school_name": school_name})
    return render_to_string("adminStaff/widgets/subjectrating_table.html", context)   
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

@dajaxice_register
def ResetSchoolPassword(request, form):
    resetSchoolPassword_form = ResetSchoolPasswordForm(deserialize_form(form))
    if resetSchoolPassword_form.is_valid():
        password = resetSchoolPassword_form.cleaned_data["reset_password"]
        for register in SchoolProfile.objects.all():
            user = User.objects.get(username__exact = register.userid.username)
            if user:
                user.set_password(password)
                user.save()
        return simplejson.dumps({'status':'1', 'message':u"重置密码成功"})
    else:
        return simplejson.dumps({'status':'1', 'message':u"密码不能为空"})

@dajaxice_register
def first_round_recommend(request):
    message = ""
    try:
        recommend_obj = SchoolRecommendRate.load()
        recommend_rate = recommend_obj.rate / 100.0
        
        exclude_schools = [u"东北大学", u"大连理工大学", u"大连海事大学", u"大连民族大学",]
        exclude_query_set = reduce(lambda x, y: x | y, [Q(school__schoolName = name) for name in exclude_schools])
        
        current_year = datetime.datetime.now().year
        result_set = []
        project_list = get_current_project_query_set().exclude(exclude_query_set).filter(year = current_year)
        for insitute in InsituteCategory.objects.all():
            category_project_list = project_list.filter(insitute_id = insitute)
            recommend_num = int(math.ceil(len(category_project_list) * recommend_rate))
            pending_list = []
            for project in category_project_list:
                score = sum(1 for item in Re_Project_Expert.objects.filter(project = project) if item.pass_p)
                pending_list.append((score, project))
            random.shuffle(pending_list)
            pending_list.sort(reverse = True)
            result_set.extend(pending_list[:recommend_num])
        for item in result_set:
            project = item[1]
            project.project_recommend_status = ProjectRecommendStatus.objects.get(status = RECOMMEND_FIRST_ROUND_PASSED)
            project.save()
        recommend_obj.firstRoundFinished = True
        recommend_obj.save()

        message = "ok"
    except:
        message = "fail"
    return simplejson.dumps({"message": message, })

@dajaxice_register
def second_round_start(request):
    message = ''
    try:
        expert_group = ExpertProfile.objects.filter(subject__category = "12")
        # category="12"为所有学科标为“全部”的专家
        project_list = list(get_current_project_query_set().filter(project_recommend_status__status = RECOMMEND_FIRST_ROUND_PASSED))
        
        score_project_set = {0:[], 1:[], 2:[], 3:[]}
        for project in project_list:
            score = Re_Project_Expert.objects.filter(project = project).filter(pass_p = True).count()
            score_project_set[score].append(project)
        
        print [len(score_project_set[i]) for i in xrange(4)]
        for i, expert in enumerate(expert_group):
            group_id = i / 3
            for cnt in xrange(4):
                for project in score_project_set[cnt][group_id::5]:
                    re_project_expert = Re_Project_Expert(project = project, expert = expert)
                    re_project_expert.save()
        recommend_obj = SchoolRecommendRate.load()
        recommend_obj.secondRoundStart = True
        recommend_obj.save()
        message = "ok"
    except:
        message = "fail"

    return simplejson.dumps({"message": message, })

@dajaxice_register
def second_round_recommend(request):
    message = ""
    try:
        recommend_obj = SchoolRecommendRate.load()
        recommend_rate = recommend_obj.rate / 100.0
        project_list = get_current_project_query_set().filter(project_recommend_status__status = RECOMMEND_FIRST_ROUND_PASSED)
        recommend_num = int(math.ceil(project_list.count() * recommend_rate))

        project_list = [(Re_Project_Expert.objects.filter(project = project).filter(pass_p = True).count(), project) for project in project_list]
        
        random.shuffle(project_list)
        project_list.sort(reverse = True)
        
        result_set = project_list[:recommend_num]
        
        print len(result_set)
        for (score, project) in result_set:
            project.project_recommend_status = ProjectRecommendStatus.objects.get(status = RECOMMEND_SECOND_ROUND_PASSED)
            project.save()

        recommend_obj.secondRoundFinished = True
        recommend_obj.save()

        message = "ok"
    except:
        message = "fail"

    return simplejson.dumps({"message": message, })

@dajaxice_register
def show_result(request):
    message = ""
    path = ""
    try:
        project_list = get_current_project_query_set().filter(project_recommend_status__status = RECOMMEND_SECOND_ROUND_PASSED)
        path = AdminStaffService.get_show_result_xls_path(request,project_list)
        print project_list.count()
        print path
        message = "ok"
    except:
        message = "fail"


    return simplejson.dumps({"message": message, 'path':path})
@dajaxice_register
def ResetUserPassword(request, form,uid):

    resetSchoolPassword_form = ResetSchoolPasswordForm(deserialize_form(form))
    print form
    if resetSchoolPassword_form.is_valid():
        password = resetSchoolPassword_form.cleaned_data["reset_password"]
        try:
            user = User.objects.get(id = uid)
            user.set_password(password)
            user.save()
        except Exception,e:
            print e
        return simplejson.dumps({'status':'1', 'message':u"重置密码成功"})
    else:
        return simplejson.dumps({'status':'0', 'message':u"密码不能为空"})


@dajaxice_register
def Expert_Project_Assign(request, group_num=20,
                          expert_per_group=3, project_per_group=134):
    # experts filter
    # TODO: experts order by category if required
    experts = ExpertProfile.objects.exclude(Q(group=-1) | Q(group=0))
    expert_group = [experts.filter(group=i+1) for i in xrange(group_num)]
    for index, group in enumerate(expert_group):
        if len(group) != expert_per_group:
            response = '检测到第 %d 组专家数量与要求数量不一致\n期望数量:%d\n'\
                % (index+1, expert_per_group)
            response += '实际数量:%d\n请联系系统管理员处理' % len(group)
            return HttpResponse(response)
    # projects filter and order by category
    projects = get_current_project_query_set().exclude(
        Q(school__schoolName=u'大连理工大学')
        | Q(school__schoolName=u'东北大学')
        | Q(school__schoolName=u'大连海事大学')
        | Q(school__schoolName=u'大连民族大学')).order_by(
            'project_category',
            'project_id')
    expect_num = group_num*project_per_group
    actual_num = projects.count()
    if actual_num != expect_num:
        response = '项目数量与专家数量不匹配,请联系系统管理员处理\n'
        response += '期望项目数量: %d\n实际项目数量: %d' % (expect_num, actual_num)
        return HttpResponse(response)
    assigned_count = 0
    actual_assign_count = 0
    for index, project in enumerate(projects):
        if index == expect_num:
            break
        group = index / project_per_group
        if group == group_num:
            break
        for expert in expert_group[group]:
            proj_assign, created = Re_Project_Expert.objects.get_or_create(
                project=project,
                expert=expert)
            proj_assign.save()
            if created:
                actual_assign_count += 1
            assigned_count += 1
    response = '项目评审成功分配\n专家数量:%d\n项目数量:%d\n' % (
        experts.count(), projects.count())
    response += '本次实际分配数量:%d\n已分配数量:%d' % (
        actual_assign_count, assigned_count)
    return HttpResponse(response)


@dajaxice_register
def scored_result(request, group_num=20, expert_per_group=3,
                  project_per_group=134, forced=False):
    experts = ExpertProfile.objects.exclude(Q(group=-1) | Q(group=0))
    expert_groups = [experts.filter(group=i+1) for i in xrange(group_num)]
    project_groups = [
        map(lambda y: y.project, x[0].re_project_expert_set.all())
        for x in expert_groups]
    if not forced:
        for index, pg in enumerate(project_groups):
            for proj in pg:
                all_scores = proj.re_project_expert_set.all()
                scored_num = all_scores.filter(pass_p=True).count()
                unscored_experts = map(lambda x: x.expert.userid.username,
                                       all_scores.filter(pass_p=False))
                if scored_num != expert_per_group:
                    experts = reduce(lambda x, y: x+'\n'+y, unscored_experts)
                    response = u'第 %d 组中项目<%s>存在未评分,对应专家为:\n'\
                        % (index+1, proj)
                    response += experts+u'\n请查证。'
                    return simplejson.dumps(
                        {'status': 'ERROR',
                         'message': response})
    sorted_project_groups = [
        map(lambda proj: (proj,
            proj.re_project_expert_set.all()[0].score,
            proj.re_project_expert_set.all()[1].score,
            proj.re_project_expert_set.all()[2].score,
            reduce(lambda i, j: i+j,
                   map(lambda x: x.score, proj.re_project_expert_set.all()))),
            pg)
        for pg in project_groups]
    for spg in sorted_project_groups:
        spg.sort(key=lambda x: x[4], reverse=True)
    sorted_project_groups = map(lambda x: x[:50], sorted_project_groups)
    path = AdminStaffService.get_scored_result_xls_path(
        request,
        sorted_project_groups)
    return simplejson.dumps({'status': 'SUCCESS', 'path': path})
