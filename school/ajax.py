# coding: UTF8
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register
from dajaxice.utils import deserialize_form
from django.utils import simplejson
from const.models import SchoolDict
from const import *
from adminStaff.utils import DateFormatTransfer
from adminStaff.views import AdminStaffService
from school.models import Project_Is_Assigned, InsituteCategory
from users.models import SchoolProfile
from news.models import News
import datetime
from school.forms import TeacherDispatchForm, TeacherNumLimitForm

@dajaxice_register
def NumLimit(request, form):
    dajax = Dajax()
    form = TeacherNumLimitForm(deserialize_form(form))
    if form.is_valid():
        teacher_obj = TeacherProfile.objects.get(id=form.cleaned_data["teacher_name"])
        limited_num = form.cleaned_data["limited_num"]
        try:
            if  TeacherProjectPerLimits.objects.filter(teacher=teacher_obj).count() == 0 :
                projectlimit = TeacherProjectPerLimits(teacher=teacher_obj,
                                                       number=limited_num)
                projectlimit.save()
            else:
                object = ProjectPerLimits.objects.get(teacher=teacher_obj)
                object.number = limited_num
                object.save()
            return simplejson.dumps({'status':'1','message':u'更新成功'})
        except TeacherProfile.DoesNotExist:
            return simplejson.dumps({'status':'1','message':u'更新失败，选定的指导老师没有进行注册'})
    else:
        return simplejson.dumps({'id':form.errors.keys(),'message':u'输入错误'})


@dajaxice_register
def  TeacherDispatch(request, form):
    #dajax = Dajax()
    teacher_form =  TeacherDispatchForm(deserialize_form(form))
    if teacher_form.is_valid():
        password = teacher_form.cleaned_data["teacher_password"]
        email = teacher_form.cleaned_data["teacher_email"]
        # school = teacher_form.cleaned_data["teacher_school"]
        school = request.user.schoolprofile_set.get()
        name = email
        if password == "":
            password = email.split('@')[0]
        flag = AdminStaffService.sendemail(request, name, password, email,TEACHER_USER, teacher_school=school)
        if flag:
            message = u"发送邮件成功"
            return simplejson.dumps({'field':teacher_form.data.keys(), 'status':'1', 'message':message})
        else:
            message = u"相同邮件已经发送，中断发送"
            return simplejson.dumps({'field':teacher_form.data.keys(), 'status':'1', 'message':message})
    else:
        return simplejson.dumps({'field':teacher_form.data.keys(),'error_id':teacher_form.errors.keys(),'message':u"输入有误,请检查邮箱的合法性"})
