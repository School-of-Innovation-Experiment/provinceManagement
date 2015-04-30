# coding: UTF-8
'''
Created on 2013-3-28

@author: sytmac
'''
from datetime import *
from django import  forms
from django.db.models import Q
from adminStaff.models import ProjectControl
from school.models import ProjectSingle
from const import *
from const.models import SchoolDict, PROJECT_CATE_CHOICES, ProjectCategory, InsituteCategory


class ExpertDispatchForm(forms.Form):
    insitute_choice_list = []
    insitute_list = InsituteCategory.objects.all()
    for object in insitute_list:
        insitute_choice_list.append((object.id, object.get_category_display()))
    insitute_tuple = tuple(insitute_choice_list)

    expert_password = forms.CharField(max_length=20, required=False,
    widget=forms.TextInput(attrs={'class':'span2','id':"expert_password",'placeholder':u"默认密码：邮箱名字",'id':'expert_password'}
                           ),
)
    expert_email    = forms.EmailField(required=True,
    widget=forms.TextInput(attrs={'class':'span2','id':"expert_mailbox",'placeholder':u"邮箱",'id':'expert_email'}
                           ))
    expert_insitute = forms.ChoiceField(required=True,choices=insitute_tuple
                                        )
    person_firstname = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'span2','id':"person_firstname",'placeholder':u"负责人"}))
class SchoolDispatchForm(forms.Form):
    SCHOOL_CHOICE_list = []
    school_list        = SchoolDict.objects.all()
    for object in school_list:
        SCHOOL_CHOICE_list.append((object.id, object.schoolName))
    SCHOOL_CHOICE = tuple(SCHOOL_CHOICE_list)
    school_password = forms.CharField(max_length=20, required=False,
    widget=forms.TextInput(attrs={'class':'span2','id':"school_password",'placeholder':u"默认密码：邮箱名字",'id':'school_password'}
                           ),
)
    school_email    = forms.EmailField(required=True,
    widget=forms.TextInput(attrs={'class':'span2','id':"school_mailbox",'placeholder':u"邮箱",'id':'school_email'}
                           ))
    school_name     = forms.ChoiceField(required=True,choices=SCHOOL_CHOICE)
    person_firstname = forms.CharField(required=False,widget=forms.TextInput(attrs={'class':'span2','id':"person_firstname",'placeholder':u"负责人"}))
    def __init__(self, *args, **kwargs):
        super(SchoolDispatchForm, self).__init__(*args, **kwargs)
        SCHOOL_CHOICE_list = []
        school_list = SchoolDict.objects.all()
        for obj in school_list:
            SCHOOL_CHOICE_list.append((obj.id, obj.schoolName))
        SCHOOL_CHOICE = tuple(SCHOOL_CHOICE_list)
        self.fields["school_name"].choices = SCHOOL_CHOICE

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
    school_list        = SchoolDict.objects.all()
    for object in school_list:
        SCHOOL_CHOICE_list.append((object.id, object.schoolName))
    SCHOOL_CHOICE = tuple(SCHOOL_CHOICE_list)
    school_name   = forms.ChoiceField(choices=SCHOOL_CHOICE)
    a_limited_num   = forms.IntegerField(required=True,
                                         widget=forms.TextInput(attrs={'id':"a_limited_num", 'class': 'span2'}
                           ))
    b_limited_num   = forms.IntegerField(required=True,
                                         widget=forms.TextInput(attrs={'id':"b_limited_num", 'class': 'span2'}
                                                          ))

class SubjectCategoryForm(forms.Form):
    category_choice_list = []
    category_list = ProjectCategory.objects.all()
    for object in category_list:
        category_choice_list.append((object.id, object.category))
    category_tuple =  tuple(category_choice_list)
    category_choice = forms.ChoiceField(choices=category_tuple)

class SubjectInsituteForm(forms.Form):
    insitute_choice_list = []
    insitute_list = InsituteCategory.objects.all()
    for object in insitute_list:
        insitute_choice_list.append((object.id, object.get_category_display()))
    insitute_tuple = tuple(insitute_choice_list)
    insitute_choice = forms.ChoiceField(choices=insitute_tuple, widget=forms.Select(attrs={"onchange":"is_assigned();"}))

class SchoolCategoryForm(forms.Form):
    SCHOOL_CHOICE_list = []
    school_list        = SchoolDict.objects.all()
    for object in school_list:
        SCHOOL_CHOICE_list.append((object.id, object.schoolName))
    SCHOOL_CHOICE = tuple(SCHOOL_CHOICE_list)
    school_choice   = forms.ChoiceField(choices=SCHOOL_CHOICE)

class SubjectGradeForm(forms.Form):
    subject_grade_choice =   PROJECT_GRADE_CHOICES
    subject_grade   = forms.ChoiceField(choices=subject_grade_choice)
class ResetSchoolPasswordForm(forms.Form):
    reset_password = forms.CharField(max_length=20, required=True,
                                     widget=forms.TextInput(attrs={'class':'span2','id':"reset_school_password",'placeholder':u"请输入要重置的密码",'id':'reset_password_text'}
                                    ),)


class ProjectManageForm(forms.Form):
    project_cate_choice = list(PROJECT_CATE_CHOICES)
    project_cate_choice.insert(0,('-1',u"项目类型"))
    financial_cate_choice = list(FINANCIAL_CATE_CHOICES)
    financial_cate_choice.insert(0,('-1',u"类型(甲/乙类)"))
    project_grade_choice = list(PROJECT_GRADE_CHOICES)
    project_grade_choice.insert(0,('-1',u"评审级别"))
    project_status_choice = list(PROJECT_STATUS_CHOICES)
    project_status_choice.insert(0,('-1',u"当前状态"))
    project_cate       = forms.ChoiceField(choices =project_cate_choice)
    financial_cate     = forms.ChoiceField(choices =financial_cate_choice)
    project_grade      = forms.ChoiceField(choices =project_grade_choice)
    project_status     = forms.ChoiceField(choices =project_status_choice)
    project_year       = forms.ChoiceField()
    title_teacher_name = forms.CharField(max_length = 40,
                                    required=False,
                                    widget=forms.TextInput(attrs={'class':'span2','id':'name','placeholder':u"输入需要筛选的老师名字或项目名称"}),)
    def __init__(self, *args, **kwargs):
        super(ProjectManageForm, self).__init__(*args, **kwargs)
        YEAR_CHOICE = [(pro['year'],pro['year'])  for pro in ProjectSingle.objects.order_by('year').values('year').distinct()]
        YEAR_CHOICE.insert(0,('-1',u"年份"))
        self.fields['project_year'].choices = YEAR_CHOICE
    def get_url_para(self):
        url_para = []
        url_para.append(u'project_cate='      +unicode(self.cleaned_data['project_cate'      ]) )
        url_para.append(u'financial_cate='    +unicode(self.cleaned_data['financial_cate'    ]) )
        url_para.append(u'project_grade='     +unicode(self.cleaned_data['project_grade'     ]) )
        url_para.append(u'project_status='    +unicode(self.cleaned_data['project_status'    ]) )
        url_para.append(u'project_year='      +unicode(self.cleaned_data['project_year'      ]) )
        url_para.append(u'title_teacher_name='+unicode(self.cleaned_data['title_teacher_name']) )
        return u'&'.join(url_para)
    def set_selected(self,request):
        self.fields['project_cate'      ].initial =request.GET.get('project_cate'      ) or "-1"
        self.fields['financial_cate'    ].initial =request.GET.get('financial_cate'    ) or "-1"
        self.fields['project_grade'     ].initial =request.GET.get('project_grade'     ) or "-1"
        self.fields['project_status'    ].initial =request.GET.get('project_status'    ) or "-1"
        self.fields['project_year'      ].initial =request.GET.get('project_year'      ) or "-1"
        self.fields['title_teacher_name'].initial =request.GET.get('title_teacher_name') or ""

    def get_qset(self):
        project_cate       = self.cleaned_data['project_cate']
        financial_cate     = self.cleaned_data['financial_cate']
        project_grade      = self.cleaned_data['project_grade']
        project_status     = self.cleaned_data['project_status']
        project_year       = self.cleaned_data['project_year']
        title_teacher_name = self.cleaned_data['title_teacher_name']
        if project_cate       =="-1":
            project_cate       =""
        if financial_cate     =="-1":
            financial_cate     =""
        if project_grade      =="-1":
            project_grade      =""
        if project_status     =="-1":
            project_status     =""
        if project_year       =="-1":
            project_year       =""
        q0 =(project_cate       and Q( project_category__category   = project_cate   ))or None
        q1 =(financial_cate     and Q( financial_category__category = financial_cate ))or None
        q2 =(project_grade      and Q( project_grade__grade         = project_grade  ))or None
        q3 =(project_status     and Q( project_status__status       = project_status ))or None
        q4 =(project_year       and Q( year                         = project_year   ))or None
        if title_teacher_name:
            q5_1 = Q(title__contains = title_teacher_name)
            q5_2 = Q(inspector__contains = title_teacher_name)
            q5 = reduce(lambda x,y: x|y , [q5_1,q5_2])
        else:
            q5=None
        qset = filter(lambda x:x!=None,[q0,q1,q2,q3,q4,q5])
        if qset:
            qset=reduce(lambda x,y: x&y ,qset)
        return qset
