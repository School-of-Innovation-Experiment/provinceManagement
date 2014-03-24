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
from const import *
from student.models import Student_Group

class InfoForm(ModelForm):
    """
        Project Basic info
    """
    def __init__(self, *args, **kwargs):
        pid = kwargs.pop('pid', None)
        if not pid:
            return
        project = ProjectSingle.objects.get(project_id=pid)
        student_group = Student_Group.objects.filter(project = project)
        member = []
        for temp_student in student_group:
             member.append(temp_student.studentName)
        memberlist=','.join(member)
        super(InfoForm, self).__init__(*args, **kwargs)
        self.fields['memberlist'].widget.attrs["value"] = memberlist

    memberlist = forms.CharField(
                           widget=forms.TextInput(attrs={'class':"school-display",'readonly':'readonly','placeholder': '请在“团队成员”标签中添加组员'}))    
    class Meta:
        model = ProjectSingle
        #TODO: add css into widgets
        exclude = ('project_id', 'adminuser', 'school', 'student','project_category','financial_category',
                   'year', 'project_grade', 'project_status', 'expert','members','project_code')
        widgets={'title':forms.TextInput(attrs={'class':"school-display"}),
                 'inspector':forms.TextInput(attrs={'class':"school-display"}),
                 'inspector_title':forms.TextInput(attrs={'class':"school-display"}),
                 'telephone':forms.TextInput(attrs={'class':"school-display"}),
                 'email':forms.TextInput(attrs={'class':"school-display"}),
                 'im':forms.TextInput(attrs={'class':"school-display"}),
                 'insitute':forms.Select(attrs={'class':"school-display"}),
                 'keywords':forms.TextInput(attrs={'class':"school-display"}),
                 }

    def get_absolute_url(self):
        return reverse('school.views.application_report_view', args=(str(self.instance.project_id),))


class ApplicationReportForm(ModelForm):
    """
        Application Report Form
    """
    class Meta:
        model = PreSubmit
        exclude = ('project_id', 'content_id','is_audited', )

        #TODO: add css into widgets
        widgets = {
                   'original':forms.Select(attrs={'class':'student' }),
                   "background": forms.Textarea(attrs={'rows': 8, 'cols': 100,
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
                   "proj_introduction":forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                          'placeholder':
                                                          '项目内容简介（100字以内）',
                                                          'class': "fill-form"}),
                   }

    def get_absolute_url(self):
        return reverse('school.views.application_report_view', args=(str(self.instance.project_id),))

class EnterpriseApplicationReportForm(ModelForm):
    """
        EnterpriseApplicationReportForm Report Form
    """
    class Meta:
        model = PreSubmitEnterprise

        exclude = ('project_id', 'content_id','enterpriseTeacher','is_audited',)

        #TODO: add css into widgets
        widgets = {
                   'original':forms.Select(attrs={'class':'student' }),
                   'maturity':forms.Select(attrs={'class':'student' }),
                   "background": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                       'placeholder': '团队各成员的知识背景，分工，指导教师，企业导师情况...',
                                                       'class': "fill-form"}),
                   "innovation": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                      'placeholder': '产品介绍，产品技术水平，产品的新颖性、先进性和独特性，产品的竞争优势...',
                                                      'class': "fill-form"}),
                   "industry": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                       'placeholder': '行业历史与前景，市场规模及增长趋势，行业竞争对手，未来市场销售预测...',
                                                       'class': "fill-form"}),
                   "product": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                       'placeholder': '生产方式，生产材料，劳动力需求，设备需求，质量保证，生产成本...',
                                                       'class': "fill-form"}),
                   "funds_plan": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                       'placeholder': '资金需求量、用途、使用计划，融资途径....',
                                                       'class': "fill-form"}),
                   "operating_mode": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                       'placeholder': '合作计划，实施方案，机构设置，人员管理，销售策略等....',
                                                       'class': "fill-form"}),
                   "risk_management": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                       'placeholder': '项目实施可能出现的风险及拟采取的控制措施....',
                                                       'class': "fill-form"}),
                   "financial_pred": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                       'placeholder': '未来三年或五年的销售收入、利润、资产回报率等....',
                                                       'class': "fill-form"}),
                   "inspector_comments": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                               'placeholder': '指导教师推荐语',
                                                               'class': "fill-form"}),
                   "instutite_comments": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                            'placeholder': '学院推荐语',
                                                            'class': "fill-form"}),
                   "school_comments": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                            'placeholder': '学校推荐语',
                                                            'class': "fill-form"}),
                   "proj_introduction":forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                          'placeholder':
                                                          '项目内容简介（100字以内）',
                                                          'class': "fill-form"}),                   
                   }

    def get_absolute_url(self):
        return reverse('school.views.application_report_view', args=(str(self.instance.project_id),))

class Teacher_EnterpriseForm(ModelForm):
    """
        Teacher_EnterpriseForm in ApplicationReportForm
    """
    class Meta:
        model = Teacher_Enterprise
        #TODO: add css into widgets
        exclude=('id')
        widgets={
                  'name':forms.TextInput(attrs={'class':"school-display"}),
                  'telephone':forms.TextInput(attrs={'class':"school-display"}),
                  'titles':forms.TextInput(attrs={'class':"school-display"}),
                  'jobs':forms.TextInput(attrs={'class':"school-display"}),
                 }

    def get_absolute_url(self):
        return reverse('school.views.application_report_view', args=(str(self.instance.project_id),))

class MidReportForm(ModelForm):
    """
        Mid Form
    """
    class Meta:
        model = MidSubmit
        exclude = {"project_id", "content_id"}
        widgets = {"process": forms.Textarea(attrs={'rows': 13, 'cols': 100,
                                                                'placeholder':'项目进展情况，写1000字就行...',
                                                                'class':"fill-form"},),
                   "achievement_summary": forms.Textarea(attrs={'rows': 13, 'cols': 100,
                                                                'placeholder':'研究成果概述，写1000字就行...',
                                                                'class':"fill-form"},),
                   "next_plan": forms.Textarea(attrs={'rows': 13, 'cols': 100,
                                                                'placeholder':'下一阶段工作计划，写1000字就行...',
                                                                'class':"fill-form"},),
                   "achievement": forms.Textarea(attrs={'rows': 13, 'cols': 100,
                                                                'placeholder':'主要成果（成果名称，参与者，发表时间，发表刊物等）',
                                                                'class':"fill-form"},),
                   "inspector_comments": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                                'placeholder': '指导教师推荐语',
                                                                'class': "fill-form"}),
                 }
    def get_absolute_url(self):
        return reverse('school.views.mid_report_view', args=(str(self.instance.project_id),))

class FinalReportForm(ModelForm):
    """
        Final Form
    """
    class Meta:
        model = FinalSubmit
        #TODO: add css into widgets
        exclude = ('project_id', 'content_id','is_audited' )
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

class StudentDispatchForm(forms.Form):
    student_password = forms.CharField(max_length=20, required=False,
                                       widget=forms.TextInput(attrs={'class':'span2','id':"student_password",'placeholder':u"默认密码：邮箱名字",'id':'student_password'}
                           ),
)
    student_email    = forms.EmailField(required=True,
                                        widget=forms.TextInput(attrs={'class':'span2','id':"student_mailbox",'placeholder':u"邮箱",'id':'student_email'}
                           ))
    proj_cate = forms.ChoiceField(required=True,choices=FINANCIAL_CATE_CHOICES, initial=FINANCIAL_CATE_UN,widget=forms.Select(attrs={'class':'studispatch'}))
    person_firstname = forms.CharField(required=True,widget=forms.TextInput(attrs={'class':'studispatch','id':"person_firstname",'placeholder':u"负责人"}))
