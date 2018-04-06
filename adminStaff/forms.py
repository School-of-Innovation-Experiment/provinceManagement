# coding: UTF-8
'''
Created on 2013-3-28

@author: sytmac
'''
from datetime import *
from django import  forms
from django.db.models import Q 
from django.core import exceptions
from backend.logging import loginfo
from adminStaff.models import ProjectControl
from const import *
from users.models import *
from school.models import *
from student.models import Student_Group
from school.utility import get_yearlist_forform
from const.models import SchoolDict, PROJECT_CATE_CHOICES, ProjectCategory #, InsituteCategory
class ExpertDispatchForm(forms.Form):
    expert_password = forms.CharField(max_length=20, required=False,
                                      widget=forms.TextInput(attrs={'class':'span2','id':"expert_password",'placeholder':u"默认密码：邮箱名字",'id':'expert_password'}),)
    expert_email    = forms.EmailField(required=True,
                                       widget=forms.TextInput(attrs={'class':'span2','id':"expert_mailbox",'placeholder':u"邮箱",'id':'expert_email'}))
    expert_personname = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'span2','id':"expert_personname",'placeholder':u"专家姓名"}))

class SchoolDictDispatchForm(forms.Form):
    SCHOOL_CHOICE_list = []
    school_list        = SchoolDict.objects.all()
    for obj in school_list:
        SCHOOL_CHOICE_list.append((obj.id, obj.schoolName))
    SCHOOL_CHOICE = tuple(SCHOOL_CHOICE_list)
    school_password = forms.CharField(max_length=20, required=False,
                                      widget=forms.TextInput(attrs={'class':'span2','id':"school_password",'placeholder':u"默认密码：邮箱名字",'id':'school_password'}
                           ),
)
    school_email    = forms.EmailField(required=True,
                                       widget=forms.TextInput(attrs={'class':'span2','placeholder':u"邮箱",'id':'school_email'}
                           ))
    school_name     = forms.ChoiceField(required=True,choices=SCHOOL_CHOICE)
    school_personname = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'span2','id':"school_personname",'placeholder':u"学院管理员"}))
    def __init__(self, *args, **kwargs):
        super(SchoolDictDispatchForm, self).__init__(*args, **kwargs)
        SCHOOL_CHOICE_list = []
        school_list        = SchoolDict.objects.all()
        for obj in school_list:
            SCHOOL_CHOICE_list.append((obj.id, obj.schoolName))
        SCHOOL_CHOICE = tuple(SCHOOL_CHOICE_list)
        self.fields["school_name"].choices = SCHOOL_CHOICE

# WARNING!! maybe delete this form, DONOT use it!
class SchoolDispatchForm(forms.Form):
    SCHOOL_CHOICE_list = []
    school_list        = SchoolProfile.objects.all()
    for obj in school_list:
        SCHOOL_CHOICE_list.append((obj.id, obj.school))
    SCHOOL_CHOICE = tuple(SCHOOL_CHOICE_list)
    school_password = forms.CharField(max_length=20, required=False,
                                      widget=forms.TextInput(attrs={'class':'span2','id':"school_password",'placeholder':u"默认密码：邮箱名字",'id':'school_password'}
                           ),
)
    school_email    = forms.EmailField(required=True,
                                       widget=forms.TextInput(attrs={'class':'span2','placeholder':u"邮箱",'id':'school_email'}
                           ))
    school_name     = forms.ChoiceField(required=True,choices=SCHOOL_CHOICE)
    school_personname = forms.CharField(required=True,
                                       widget=forms.TextInput(attrs={'class':'span2','id':"school_personname",'placeholder':u"学院管理员"}))

class StudentDispatchForm(forms.Form):
    student_email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'span2',
            'placeholder': u"邮箱",
            'id': 'student_email'}))
    category = forms.ChoiceField(choices=PROJECT_CATE_CHOICES)
    student_personname = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'span2',
            'id': "student_personname",
            'placeholder': u"学生姓名"}))
    student_uid = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'span2',
            'id': "teacher_id",
            'placeholder': u"学生学号"}))

    def clean_student_uid(self):
        uid = self.cleaned_data['student_uid']
        if '_' in uid:
            raise exceptions.ValidationError(u'学号不能包含特殊字符')
        return uid

class TeacherDispatchForm(forms.Form):
    teacher_email = forms.EmailField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'span2',
            'placeholder': u"邮箱",
            'id':'teacher_email'}))
    teacher_personname = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'span2',
            'id': "teacher_personname",
            'placeholder': u"指导教师姓名"}))
    teacher_uid = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'span2',
            'id': "teacher_id",
            'placeholder': u"指导教师工号"}))

    def clean_teacher_uid(self):
        uid = self.cleaned_data['teacher_uid']
        if '_' in uid:
            raise exceptions.ValidationError(u'工号不能包含特殊字符')
        return uid


class TimeSettingForm(forms.Form):
    pre_start_date = forms.DateField(required=True,widget=forms.DateInput(attrs={ 'class':'span2','id':'pre_start_date',"data-date-format":"yyyy-mm-dd"}))
    pre_end_date = forms.DateField(required=True,widget=forms.DateInput(attrs={'class':'span2','id':'pre_end_date',"data-date-format":"yyyy-mm-dd"}))
    final_start_date = forms.DateField(widget=forms.DateInput(attrs={ 'class':'span2','id':'final_start_date',"data-date-format":"yyyy-mm-dd"}))
    final_end_date = forms.DateField(widget=forms.DateInput(attrs={ 'class':'span2','id':'final_end_date',"data-date-format":"yyyy-mm-dd"}))
    pre_start_date_review = forms.DateField(widget=forms.DateInput(attrs={ 'class':'span2','id':'pre_start_date_review',"data-date-format":"yyyy-mm-dd"}))
    pre_end_date_review = forms.DateField(widget=forms.DateInput(attrs={ 'class':'span2','id':'pre_end_date_review',"data-date-format":"yyyy-mm-dd"}))
    final_start_date_review = forms.DateField(widget=forms.DateInput(attrs={'class':'span2','id':'final_start_date_review',"data-date-format":"yyyy-mm-dd"}))
    final_end_date_review = forms.DateField(widget=forms.DateInput(attrs={'class':'span2','id':'final_end_date_review',"data-date-format":"yyyy-mm-dd"}))
    def clean(self):
        cleaned_data = super(TimeSettingForm,self).clean()
        psd = cleaned_data.get("pre_start_date")
        ped = cleaned_data.get("pre_end_date")
        fsd = cleaned_data.get("final_start_date")
        fed = cleaned_data.get("final_end_date")
        psdr = cleaned_data.get("pre_start_date_review")
        pedr = cleaned_data.get("pre_end_date_review")
        fsdr = cleaned_data.get("final_start_date_review")
        fedr = cleaned_data.get("final_end_date_review")
        if not (psd == None or \
            ped == None or \
            fsd == None or \
            fed == None or \
            psdr == None or \
            pedr == None or \
            fsdr == None or \
            fedr == None):
                if psd > ped :
                    msg = u"初期提交起止时间有误，请重新设置PROJECT_GRADE_CHOICES"
                    self._errors['pre_start_date'] = self.error_class([msg])
                    self._errors['pre_end_date'] = self.error_class([msg])
                elif fsd > fed:
                    msg = u"结题报告起止时间有误，请重新设置"
                    self._errors['final_start_date'] = self.error_class([msg])
                    self._errors['final_end_date'] = self.error_class([msg])
                elif psdr > pedr:
                    msg = u"项目初审起止时间有误，请重新设置"
                    self._errors['pre_start_date_review'] = self.error_class([msg])
                    self._errors['pre_end_date_review'] = self.error_class([msg])
                elif fsdr > fedr:
                    msg = u"项目终止起止时间有误，请重新设置"
                    self._errors['final_start_date_review'] = self.error_class([msg])
                    self._errors['final_end_date_review'] = self.error_class([msg])
class NumLimitForm(forms.Form):
    SCHOOL_CHOICE_list = []
    school_list        = SchoolProfile.objects.all()
    for obj in school_list:
        SCHOOL_CHOICE_list.append((obj.id, obj.school))
    SCHOOL_CHOICE = tuple(SCHOOL_CHOICE_list)
    school_name   = forms.ChoiceField(choices=SCHOOL_CHOICE)
    limited_num   = forms.IntegerField(required=True,
                                       widget=forms.TextInput(attrs={'id':"limited_num"}
                           ) )
    def __init__(self, *args, **kwargs):
        super(NumLimitForm, self).__init__(*args, **kwargs)
        
        SCHOOL_CHOICE_list = [(-1, "所有学部学院")]
        #学院项目数量设定特殊添加，待debug

        school_list        = SchoolProfile.objects.all()
        for obj in school_list:
            SCHOOL_CHOICE_list.append((obj.id, obj.school))
        SCHOOL_CHOICE = tuple(SCHOOL_CHOICE_list)
        # school_name   = forms.ChoiceField(choices=SCHOOL_CHOICE)
        self.fields["school_name"].choices = SCHOOL_CHOICE

class SubjectCategoryForm(forms.Form):
    category_choice_list = []
    category_list = ProjectCategory.objects.all()
    for object in category_list:
        category_choice_list.append((object.id, object.category))
    category_tuple =  tuple(category_choice_list)
    category_choice = forms.ChoiceField(choices=category_tuple)

class SubjectInsituteForm(forms.Form):
    school_choice_list = []
    school_list = SchoolProfile.objects.all()
    for object in school_list:
        school_choice_list.append((object.id, object.school))
    school_tuple = tuple(school_choice_list)
    school_choice = forms.ChoiceField(choices=school_tuple, widget=forms.Select(attrs={"onchange":"is_assigned();"}))

class SchoolCategoryForm(forms.Form):
    SCHOOL_CHOICE_list = []
    school_list        = SchoolProfile.objects.all()
    for object in school_list:
        SCHOOL_CHOICE_list.append((object.id, object.school))
    SCHOOL_CHOICE = tuple(SCHOOL_CHOICE_list)
    school_choice   = forms.ChoiceField(choices=SCHOOL_CHOICE)
    def __init__(self, *args, **kwargs):
        super(SchoolCategoryForm, self).__init__(*args, **kwargs)
        SCHOOL_CHOICE_list = [(-1, u"显示所有学部学院")]
        school_list        = SchoolProfile.objects.all()
        for object in school_list:
            SCHOOL_CHOICE_list.append((object.id, object.school))
        SCHOOL_CHOICE = tuple(SCHOOL_CHOICE_list)
        self.fields["school_choice"].choices = SCHOOL_CHOICE

class SubjectGradeForm(forms.Form):
    subject_grade_choice =  [grade for grade in PROJECT_GRADE_CHOICES if grade[0] != GRADE_CITY]
    subject_grade_choice = tuple(subject_grade_choice)
    subject_grade   = forms.ChoiceField(choices=subject_grade_choice)

class TemplateNoticeForm(forms.Form):
    title =forms.CharField( max_length=30,
                            required=True,
                            widget=forms.TextInput(attrs={'class':'templatenotice span12','id':"title",'placeholder':u"项目记录人"}),)
    message =forms.CharField( max_length=300,
                            required=True,
                            widget=forms.Textarea(attrs={'class':'templatenotice span12','id':"message",'placeholder':u"内容"}),)

class FundsChangeForm(forms.Form):
    fnuds_datetime = forms.CharField(max_length = 100,
                                    required=False,
                                    widget=forms.TextInput(attrs={'class':'span2 fundschange','id':'funds_datetime','placeholder':datetime.datetime,
                                        'cols':"6"}),)    
    student_name = forms.CharField(max_length = 100,
                                    required=False,
                                    widget=forms.TextInput(attrs={'class':'span2 fundschange','id':'student_name','placeholder':u""}),)    
    funds_amount = forms.FloatField(
                                    required=False,
                                    widget=forms.TextInput(attrs={'class':'span2 fundschange','id':'funds_amount','placeholder':u""}),)    
    funds_detail = forms.CharField(max_length = 100,
                                    required=False,
                                    widget=forms.Textarea(attrs={'class':'span4 fundsTextarea','id':'funds_detail','placeholder':u"报销明细",
                                                                    'rows':"3",'cols':"20"}),)    
    funds_total = forms.FloatField(
                                    required=False,
                                    widget=forms.TextInput(attrs={'class':'span2 fundschange','id':'funds_remaining','placeholder':u"初始化/修改明细填写"}),) 

class StudentNameForm(forms.Form):
    STUDENT_CHOICE_list = []
    student_list        = Student_Group.objects.all();
    for object in student_list:
        STUDENT_CHOICE_list.append((object.studentId, object.studentName))
    STUDENT_CHOICE = tuple(STUDENT_CHOICE_list)
    student_choice   = forms.ChoiceField(choices=STUDENT_CHOICE)
    def __init__(self, *args, **kwargs):
        pid = kwargs.pop('pid', None)
        if not pid:
            return
        project = ProjectSingle.objects.get(project_id=pid)
        student_list = Student_Group.objects.filter(project = project)

        super(StudentNameForm, self).__init__(*args, **kwargs)
        STUDENT_CHOICE_list = [(-1, u"选择学生姓名")]
        # student_list        = Student_Group.objects.all()
        for object in student_list:
            STUDENT_CHOICE_list.append((object.studentId, object.studentName))
        STUDENT_CHOICE = tuple(STUDENT_CHOICE_list)
        self.fields["student_choice"].choices = STUDENT_CHOICE



class ProjectManageForm(forms.Form):
    project_grade_choice = [grade for grade in PROJECT_GRADE_CHOICES if grade[0] != GRADE_CITY and grade[0] != GRADE_UN]
    project_grade_choice = list(project_grade_choice)
    project_grade_choice.insert(0,('-1',u"级别"))
    loginfo(p=project_grade_choice,label="project_grade_choice")
    # project_isover_choice = [(-1, "结题状态"),(0,"未结题"),(1,"已结题")]
    # project_isover_choice = tuple(project_isover_choice)

    project_overstatus_choice = list(OVER_STATUS_CHOICES)
    project_overstatus_choice = tuple([(-1, u"结题状态")] + project_overstatus_choice)

    project_scoreapplication_choice = [(-1, "学分申请状态"),(0,"未申请"),(1,"已申请")]
    project_scoreapplication_choice = tuple(project_scoreapplication_choice)
    project_grade = forms.ChoiceField(choices=project_grade_choice)
    project_year = forms.ChoiceField()
    #project_isover = forms.ChoiceField(choices=project_isover_choice)
    project_overstatus = forms.ChoiceField(choices=project_overstatus_choice)
    project_scoreapplication = forms.ChoiceField(choices=project_scoreapplication_choice)
    
    project_category_choice = [(-1, u'项目类型')] + list(PROJECT_CATE_CHOICES)
    project_category = forms.ChoiceField(choices=project_category_choice)

    SCHOOL_CHOICE_list = []
    school_list        = SchoolProfile.objects.all()
    for object in school_list:
        SCHOOL_CHOICE_list.append((object.id, object.school))
    SCHOOL_CHOICE = tuple(SCHOOL_CHOICE_list)
    project_school = forms.ChoiceField(choices=SCHOOL_CHOICE)
    teacher_student_name = forms.CharField(max_length = 20,
                                    required=False,
                                    widget=forms.TextInput(attrs={'class':'span2','id':'name','placeholder':u"输入需要筛选的老师或学生名字"}),)
    def __init__(self, *args, **kwargs):
        super(ProjectManageForm, self).__init__(*args, **kwargs)
        project_list = ProjectSingle.objects.all()
        yearlist = get_yearlist_forform(project_list)
        loginfo(p = yearlist,label="yearlist")
        YEAR_CHOICE = list(yearlist)
        YEAR_CHOICE.insert(0,('-1',u"年份"))
        self.fields['project_year'].choices = YEAR_CHOICE
        SCHOOL_CHOICE_list = [(-1, u"显示所有学部学院")]
        school_list     = SchoolProfile.objects.all()
        for object in school_list:
            SCHOOL_CHOICE_list.append((object.id, object.school))
        SCHOOL_CHOICE = tuple(SCHOOL_CHOICE_list)
        self.fields["project_school"].choices = SCHOOL_CHOICE  


# class Sync_form(forms.Form):
#     Sync_username =forms.CharField(
#                             required=True,widget=forms.TextInput(attrs={'id':"Sync_username"}),)
#     Sync_passeword =forms.CharField(
# 							required=True,
#                             widget=forms.TextInput(attrs={'id':"Sync_password"}),)
class Sync_form(forms.Form):
    Sync_username = forms.CharField(required=True,widget=forms.TextInput(attrs={'id':"Sync_username"}),)
    Sync_passeword = forms.CharField(required=True,widget=forms.TextInput(attrs={'id':"Sync_password"}),)
