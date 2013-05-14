# coding: UTF-8
'''
Created on 2013-3-28

@author: sytmac
'''
from datetime import *
from django import  forms
from adminStaff.models import ProjectControl
from const import PROJECT_GRADE_CHOICES
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
                                         widget=forms.TextInput(attrs={'id':"a_limited_num"}
                           ))
    b_limited_num   = forms.IntegerField(required=True,
                                         widget=forms.TextInput(attrs={'id':"b_limited_num"}
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

