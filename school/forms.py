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
from django.db.models import Q 
from django.forms.util import ErrorList
from django.forms import ModelForm
from django.core.urlresolvers import reverse

from school.models import *
from adminStaff.models import ProjectPerLimits
from users.models import SchoolProfile, TeacherProfile,StudentProfile
from student.models import Student_Group
from backend.logging import loginfo
from const import *

class SubjectGradeForm(forms.Form):
    subject_grade_choice = [grade for grade in PROJECT_GRADE_CHOICES if grade[0] == GRADE_INSITUTE or grade[0] == GRADE_SCHOOL]
    subject_grade_choice = tuple(subject_grade_choice)
    subject_grade   = forms.ChoiceField(choices=subject_grade_choice)

class InfoForm(ModelForm):
    """
        Project Basic info
    """
    def __init__(self, *args, **kwargs):
        self.pid = kwargs.pop('pid', None)
        if not self.pid:
            return
        project = ProjectSingle.objects.get(project_id=self.pid)
        student_group = Student_Group.objects.filter(project = project)
        member = []
        for temp_student in student_group:
             member.append(temp_student.studentName)
        memberlist=','.join(member)
        super(InfoForm, self).__init__(*args, **kwargs)
        self.fields['memberlist'].widget.attrs["value"] = memberlist

    memberlist = forms.CharField(
                           widget=forms.TextInput(attrs={'class':"school-display",'readonly':'readonly','placeholder': '请在“队员变更”标签中添加组员'}))
    class Meta:
        model = ProjectSingle
        #TODO: add css into widgets
       # exclude = ('project_id','school','adminuser','student','project_category',
       #            'year', 'project_grade', 'project_status', 'expert','project_code',"funds_total","funds_remain", "over_status", "file_application", "file_interimchecklist", "file_summary", "file_projectcompilation", "score_application", "recommend", "is_past", "over_status", "funds_total", "funds_remain", "project_code", )
        fields = ('title',)
        widgets={'title':forms.TextInput(attrs={'class':"school-display"}),
                 }
    def clean_title(self):
        print self.pid, "*"*1000
        title = self.cleaned_data['title']
        if ProjectSingle.objects.filter(title=title).exclude(project_id=self.pid).count():
            raise forms.ValidationError("标题已存在")
        return title
    def get_absolute_url(self):
        return reverse('student.views.application_report_view', args=(str(self.instance.project_id),))


class ApplicationReportForm(ModelForm):
    """
        Application Report Form
    """
    class Meta:
        model = PreSubmit
        exclude = ('project_id', 'content_id', )

        #TODO: add css into widgets
        widgets = {
                   'original':forms.Select(attrs={'class':'studentchange' }),
                   "background": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                       'style':'display:none',
                                                       'placeholder': '同类研究工作国内外研究现状与存在的问题等...',
                                                       'class': "fill-form"}),
                   "key_notes": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                      'style':'display:none',
                                                      'placeholder': '最关键的，最重要的，最核心的，最...',
                                                      'class': "fill-form"}),
                   "innovation": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                       'style':'display:none',
                                                       'placeholder': '说点什么不同的...',
                                                       'class': "fill-form"}),
                   "funds_plan": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                       'style':'display:none',
                                                       'placeholder': '材料费、资料费、版面费、专利费、调研费等如项目鉴定、学术论文、申请专利、获奖、推广应用等..如项目鉴定、学术论文、申请专利、获奖、推广应用等....',
                                                       'class': "fill-form"}),
                   "pre_results": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                        'style':'display:none',
                                                        'placeholder': '项目鉴定、学术论文、申请专利、获奖、推广应用等...',
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
                   "progress_plan": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                          'style':'display:none',
                                                          'placeholder':
                                                          '查阅资料、选题、自主设计项目研究方案、开题报告、实验研究、数据统计、处理与分析、研制开发、填写结题表、撰写研究论文和总结报告、参加结题答辩和成果推广等',
                                                          'class': "fill-form"}),
                   }

    def get_absolute_url(self):
        return reverse('student.views.application_report_view', args=(str(self.instance.project_id),))

class EnterpriseApplicationReportForm(ModelForm):
    """
        EnterpriseApplicationReportForm Report Form
    """
    class Meta:
        model = PreSubmitEnterprise

        exclude = ('project_id', 'content_id','enterpriseTeacher' )

        #TODO: add css into widgets
        widgets = {
                   'original':forms.Select(attrs={'class':'studentchange' }),
                   'maturity':forms.Select(attrs={'class':'studentchange' }),
                   "background": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                       'style':'display:none',
                                                       'placeholder': '团队各成员的知识背景，分工，指导教师，企业导师情况...',
                                                       'class': "fill-form"}),
                   "innovation": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                       'style':'display:none',
                                                      'placeholder': '产品介绍，产品技术水平，产品的新颖性、先进性和独特性，产品的竞争优势...',
                                                      'class': "fill-form"}),
                   "industry": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                     'style':'display:none',
                                                       'placeholder': '行业历史与前景，市场规模及增长趋势，行业竞争对手，未来市场销售预测...',
                                                       'class': "fill-form"}),
                   "product": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                    'style':'display:none',
                                                       'placeholder': '生产方式，生产材料，劳动力需求，设备需求，质量保证，生产成本...',
                                                       'class': "fill-form"}),
                   "funds_plan": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                       'style':'display:none',
                                                       'placeholder': '资金需求量、用途、使用计划，融资途径....',
                                                       'class': "fill-form"}),
                   "operating_mode": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                           'style':'display:none',
                                                       'placeholder': '合作计划，实施方案，机构设置，人员管理，销售策略等....',
                                                       'class': "fill-form"}),
                   "risk_management": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                            'style':'display:none',
                                                       'placeholder': '项目实施可能出现的风险及拟采取的控制措施....',
                                                       'class': "fill-form"}),
                   "financial_pred": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                           'style':'display:none',
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
                   }

    def get_absolute_url(self):
        return reverse('student.views.application_report_view', args=(str(self.instance.project_id),))

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
        return reverse('student.views.application_report_view', args=(str(self.instance.project_id),))

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
        return reverse('student.views.mid_report_view', args=(str(self.instance.project_id),))
class OpenReportForm(ModelForm):
    """
      open form
    """
    class Meta:
        model = OpenSubmit
        exclude = ('project_id', 'content_id', )
        widgets = {"content": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                                'placeholder':'研究内容，写1000字就行...',
                                                                'class':"fill-form"},),
                   "study_achievement": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                                'placeholder': '已完成的前期研究工作和成果, 写1000字就行...',
                                                                'class': "fill-form"}),
                   "next_plan_target": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                                'placeholder':'下一阶段计划及预期达到目标, 写1000字就行...',
                                                                'class': "fill-form"}),
                   "inspector_comments": forms.Textarea(attrs={'rows': 8, 'cols': 100,
                                                       'placeholder':'指导教师意见,  写200字就行...',
                                                       'class': "fill-form"}),
                   }



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
 #                  "achievement_objects": forms.Textarea(attrs={'rows': 12, 'cols': 100,
 #                                                                'placeholder':'名称、完成人、完成时间、详细信息等...',
 #                                                               'class': "fill-form"}),
 #                  "papers": forms.Textarea(attrs={'rows': 12, 'cols': 100,
 #                                                  'placeholder':'题目、作者、期刊、发表时间、录用时间...',
 #                                                  'class': "fill-form"}),
 #                  "patents": forms.Textarea(attrs={'rows': 12, 'cols': 100,
 #                                                   'placeholder':'专利名称、申请者、专利号、批准时间...',
 #                                                   'class': "fill-form"}),
 #                  "tech_competitions": forms.Textarea(attrs={'rows': 12, 'cols': 100,
 #                                                             'placeholder':'竞赛名称、参加人、获奖名称、获奖等级...',
 #                                                             'class': "fill-form"}),
                   }

    def get_absolute_url(self):
        return reverse('student.views.final_report_view', args=(str(self.instance.project_id),))

class TechCompetitionForm(forms.Form):
    """
        TechCompetitionForm in FinalReportForm
    """
    class Meta:
        model = TechCompetition
        #TODO: add css into widgets
        exclude = ('project_id', 'content_id')
        widgets={ 'title':forms.TextInput(attrs={'class':"school-display"}),
                  'members':forms.TextInput(attrs={'class':"school-display"}),
                  'competition_name':forms.TextInput(attrs={'class':"school-display"}),
                  'competition_grade':forms.TextInput(attrs={'class':"school-display"}),
                 }


    def get_absolute_url(self):
        return reverse('student.views.final_report_view', args=(str(self.instance.project_id),))
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
        TEACHER_CHOICE_list = [(-1, "所有指导教师")]
        teacher_list        = TeacherProfile.objects.filter(school=school)
        for obj in teacher_list:
            TEACHER_CHOICE_list.append((obj.id, obj.userid.username))
        TEACHER_CHOICE = tuple(TEACHER_CHOICE_list)
        self.fields["teacher_name"].choices = TEACHER_CHOICE

class ProjectManageForm(forms.Form):
    project_grade_choice = [grade for grade in PROJECT_GRADE_CHOICES if grade[0] not in (GRADE_UN,GRADE_CITY)]
    project_grade_choice = list(project_grade_choice)
    project_grade_choice.insert(0,('-1',u"级别"))
    # project_isover_choice = [(-1,"结题管理"),(0,"未结题"),(1,"已结题")]
    # project_isover_choice = tuple(project_isover_choice)
    project_overstatus_choice = list(OVER_STATUS_CHOICES)
    project_overstatus_choice = tuple([(-1, u"结题状态")] + project_overstatus_choice)
    project_grade = forms.ChoiceField(choices=project_grade_choice)
    project_year = forms.ChoiceField() 
    # project_isover = forms.ChoiceField(choices=project_isover_choice)
    project_overstatus = forms.ChoiceField(choices=project_overstatus_choice)
    teacher_student_name = forms.CharField(max_length = 20,
                                    required=False,
                                    widget=forms.TextInput(attrs={'class':'span2','id':'name','placeholder':u"输入需要筛选的老师或学生名字"}),)
    def __init__(self, *args, **kwargs):
        school = kwargs.pop('school', None)
        super(ProjectManageForm, self).__init__(*args, **kwargs)
        loginfo(p=school,label="school")
        if not school:
            return
        project_list = ProjectSingle.objects.filter(Q(school_id=school))
        yearlist = []
        for temp in project_list:
            if (temp.year, str(temp.year)+"年") not in yearlist:
              yearlist.append((temp.year, str(temp.year)+"年"))
        YEAR_CHOICE = list(yearlist)
        YEAR_CHOICE.insert(0,('-1',u"年份"))
        loginfo(p=YEAR_CHOICE,label="YEAR_CHOICE")
        self.fields['project_year'].choices = YEAR_CHOICE

