# coding: UTF-8
'''
Created on 2013-03-28

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
from users.models import SchoolProfile


class InfoForm(ModelForm):
    """
        Project Basic info
    """
    class Meta:
        model = ProjectSingle
        #TODO: add css into widgets
        exclude = ('project_id', 'adminuser', 'school',
                   'year', 'project_grade', 'project_status')
        widgets={'title':forms.TextInput(attrs={'class':"school-display"}),
                 'inspector':forms.TextInput(attrs={'class':"school-display"}),
                 'telephone':forms.TextInput(attrs={'class':"school-display"}),
                 'email':forms.TextInput(attrs={'class':"school-display"}),
                 'im':forms.TextInput(attrs={'class':"school-display"}),
                 'members':forms.TextInput(attrs={'class':"school-display"}),
                 'original':forms.TextInput(attrs={'class':"school-display"}),
                 'project_category':forms.Select(attrs={'class':"school-display"}),
                 'insitute':forms.Select(attrs={'class':"school-display"}),             
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
        widgets = {"background": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                       'placeholder': '同类研究工作国内外研究现状与存在的问题等...',
                                                       'class': "fill-form"}),
                   "key_notes": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                      'placeholder': '最关键的，最重要的，最核心的，最...',
                                                      'class': "fill-form"}),
                   "innovation": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                       'placeholder': '说点什么不同的...',
                                                       'class': "fill-form"}),
                   "funds_plan": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                       'placeholder': '材料费、资料费、版面费、专利费、调研费等如项目鉴定、学术论文、申请专利、获奖、推广应用等..如项目鉴定、学术论文、申请专利、获奖、推广应用等....',
                                                       'class': "fill-form"}),
                   "pre_results": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                        'placeholder': '项目鉴定、学术论文、申请专利、获奖、推广应用等...',
                                                        'class': "fill-form"}),
                   "inspector_comments": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                               'placeholder': '指导教师推荐语',
                                                               'class': "fill-form"}),
                   "school_comments": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                            'placeholder': '学校推荐语',
                                                            'class': "fill-form"}),
                   "progress_plan": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                          'placeholder':
                                                          '查阅资料、选题、自主设计项目研究方案、开题报告、实验研究、数据统计、处理与分析、研制开发、填写结题表、撰写研究论文和总结报告、参加结题答辩和成果推广等',
                                                          'class': "fill-form"}),
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
                                                                'class':"fill-form"},),
                   "achievement_fashion": forms.Textarea(attrs={'rows': 2, 'cols': 100,
                                                                'placeholder': '一句话就行...',
                                                                'class': "fill-form"}),
                   "inspector_comments": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                                'placeholder':'指导教师对项目评价...',
                                                                'class': "fill-form"}),
                   "school_comments": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                       'placeholder':'学校对项目评价...',
                                                       'class': "fill-form"}),
                   "achievement_objects": forms.Textarea(attrs={'rows': 12, 'cols': 100,
                                                                'placeholder':'名称、完成人、完成时间、详细信息等...',
                                                                'class': "fill-form"}),
                   "papers": forms.Textarea(attrs={'rows': 12, 'cols': 100,
                                                   'placeholder':'题目、作者、期刊、发表时间、录用时间...',
                                                   'class': "fill-form"}),
                   "patents": forms.Textarea(attrs={'rows': 12, 'cols': 100,
                                                    'placeholder':'专利名称、申请者、专利号、批准时间...',
                                                    'class': "fill-form"}),
                   "tech_competitions": forms.Textarea(attrs={'rows': 12, 'cols': 100,
                                                              'placeholder':'竞赛名称、参加人、获奖名称、获奖等级...',
                                                              'class': "fill-form"}),
                   }

    def get_absolute_url(self):
        return reverse('school.views.final_report_view', args=(str(self.instance.project_id),))
