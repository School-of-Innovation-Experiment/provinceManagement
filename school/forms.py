# coding: UTF8
'''
Created on 20130328

@author: tianwei

Desc: Application Form and final report form.
'''
import os
import sys
import time

from django import forms
from django.core.exceptions import PermissionDenied
from django.db import models
from django.forms.util import ErrorList
from django.forms import ModelForm
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from const.models import *
from school.models import *
from adminStaff.models import ProjectPerLimits
from users.models import SchoolProfile

# coding: UTF8
'''
Created on 20130328

@author: tianwei

Desc: Application Form and final report form.
'''
import os
import sys
import time

from django import forms
from django.core.exceptions import PermissionDenied
from django.db import models
from django.forms.util import ErrorList
from django.forms import ModelForm
from django.core.urlresolvers import reverse

from school.models import *
from adminStaff.models import ProjectPerLimits
from users.models import SchoolProfile, TeacherProfile,StudentProfile


class InfoForm(ModelForm):
    """
        Project Basic info
    """
    class Meta:
        model = ProjectSingle
        #TODO: add css into widgets
        exclude = ('project_id','school','adminuser','student',
                   'year', 'project_grade', 'project_status', 'expert')
        widgets={'title':forms.TextInput(attrs={'class':"schooldisplay"}),
                 'telephone':forms.TextInput(attrs={'class':"schooldisplay"}),
                 'email':forms.TextInput(attrs={'class':"schooldisplay"}),
                 'im':forms.TextInput(attrs={'class':"schooldisplay"}),
                 'members':forms.TextInput(attrs={'class':"schooldisplay"}),
                 'project_category':forms.Select(attrs={'class':"schooldisplay"}),
                 }

    def get_absolute_url(self):
        return reverse('school.views.application_report_view', args=(str(self.instance.project_id),))


class ApplicationReportForm(ModelForm):
    """
        Application Report Form
    """
    class Meta:
        model = PreSubmit
        exclude = ('project_id', 'content_id', )

        #TODO: add css into widgets
        widgets = {
                   "original" :forms.Textarea(attrs={'rows': 2, 'cols': 100,
                                                       'placeholder': '学生自选，学生的积累和兴趣   学生自选，教师的科研项目   教师帮选，教师的科研项目',
                                                       'class': "fillform"}),
                   "background": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                       'placeholder': '同类研究工作国内外研究现状与存在的问题等...',
                                                       'class': "fillform"}),
                   "key_notes": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                      'placeholder': '最关键的，最重要的，最核心的，最...',
                                                      'class': "fillform"}),
                   "innovation": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                       'placeholder': '说点什么不同的...',
                                                       'class': "fillform"}),
                   "funds_plan": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                       'placeholder': '材料费、资料费、版面费、专利费、调研费等如项目鉴定、学术论文、申请专利、获奖、推广应用等..如项目鉴定、学术论文、申请专利、获奖、推广应用等....',
                                                       'class': "fillform"}),
                   "pre_results": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                        'placeholder': '项目鉴定、学术论文、申请专利、获奖、推广应用等...',
                                                        'class': "fillform"}),
                   "inspector_comments": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                               'placeholder': '指导教师推荐语',
                                                               'class': "fillform"}),
                   "school_comments": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                            'placeholder': '学校推荐语',
                                                            'class': "fillform"}),
                   "progress_plan": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                          'placeholder':
                                                          '查阅资料、选题、自主设计项目研究方案、开题报告、实验研究、数据统计、处理与分析、研制开发、填写结题表、撰写研究论文和总结报告、参加结题答辩和成果推广等',
                                                          'class': "fillform"}),
                   }

    def get_absolute_url(self):
        return reverse('school.views.application_report_view', args=(str(self.instance.project_id),))


class FinalReportForm(ModelForm):
    """
        Final Form
    """
    class Meta:
        model = FinalSubmit
        #TODO: add css into widgets
        exclude = ('project_id', 'content_id', )
        widgets = {"achievement_summary": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                                'placeholder':'项目完成情况，写200字就行...',
                                                                'class':"fillform"},),
                   "achievement_fashion": forms.Textarea(attrs={'rows': 2, 'cols': 100,
                                                                'placeholder': '一句话就行...',
                                                                'class': "fillform"}),
                   "inspector_comments": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                                'placeholder':'指导教师对项目评价...',
                                                                'class': "fillform"}),
                   "school_comments": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                       'placeholder':'学校对项目评价...',
                                                       'class': "fillform"}),
                   "achievement_objects": forms.Textarea(attrs={'rows': 12, 'cols': 100,
                                                                'placeholder':'名称、完成人、完成时间、详细信息等...',
                                                                'class': "fillform"}),
                   "papers": forms.Textarea(attrs={'rows': 12, 'cols': 100,
                                                   'placeholder':'题目、作者、期刊、发表时间、录用时间...',
                                                   'class': "fillform"}),
                   "patents": forms.Textarea(attrs={'rows': 12, 'cols': 100,
                                                    'placeholder':'专利名称、申请者、专利号、批准时间...',
                                                    'class': "fillform"}),
                   "tech_competitions": forms.Textarea(attrs={'rows': 12, 'cols': 100,
                                                              'placeholder':'竞赛名称、参加人、获奖名称、获奖等级...',
                                                              'class': "fillform"}),
                   }

    def get_absolute_url(self):
        return reverse('school.views.final_report_view', args=(str(self.instance.project_id),))

class StudentDispatchForm(forms.Form):
    student_password = forms.CharField(max_length=20, required=False,
                                       widget=forms.TextInput(attrs={'class':'span2','id':"student_password",'placeholder':u"默认密码：邮箱名字",'id':'student_password'}
                           ),
)
    student_email    = forms.EmailField(required=True,
                                        widget=forms.TextInput(attrs={'class':'span2','id':"student_mailbox",'placeholder':u"邮箱",'id':'student_email'}
                           ))

class TeacherDispatchForm(forms.Form):
    teacher_password = forms.CharField(max_length=20, required=False,
                                       widget=forms.TextInput(attrs={'class':'span2','placeholder':u"默认密码：邮箱名字", 'id':'teacher_password'}))
    teacher_email    = forms.EmailField(required=True,
                                        widget=forms.TextInput(attrs={'class':'span2', 'placeholder':u"邮箱", 'id':'teacher_email'}))
class ExpertDispatchForm(forms.Form):
    expert_password = forms.CharField(max_length=20, required=False,
    widget=forms.TextInput(attrs={'class':'span2','id':"expert_password",'placeholder':u"默认密码：邮箱名字",'id':'expert_password'}
                           ))
    expert_email    = forms.EmailField(required=True,
    widget=forms.TextInput(attrs={'class':'span2','id':"expert_mailbox",'placeholder':u"邮箱",'id':'expert_email'}))

class TeacherNumLimitForm(forms.Form):
    TEACHER_CHOICE_list = []
    teacher_list        = TeacherProfile.objects.all()
    for obj in teacher_list:
        TEACHER_CHOICE_list.append((obj.id, obj.userid.username))
    TEACHER_CHOICE = tuple(TEACHER_CHOICE_list)

    teacher_name   = forms.ChoiceField(choices=TEACHER_CHOICE,)
                                       # widget=forms.Select(attrs={'id': "teacher_name"}))
    limited_num   = forms.IntegerField(required=True,
                                       widget=forms.TextInput(attrs={'id':"limited_num"}))
    # user is a User object
    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(TeacherNumLimitForm, self).__init__(*args, **kwargs)
        if not request:
            return
        school = SchoolProfile.objects.get(userid=request.user)
        TEACHER_CHOICE_list = []
        teacher_list        = TeacherProfile.objects.filter(school=school)
        for obj in teacher_list:
            TEACHER_CHOICE_list.append((obj.id, obj.userid.username))
        TEACHER_CHOICE = tuple(TEACHER_CHOICE_list)
        self.fields["teacher_name"].choices = TEACHER_CHOICE
