# coding: UTF-8
from django import forms
from django.contrib.admin import widgets
from const import NEWS_MAX_LENGTH
from school.models import ShowProjectSingle

class ShowForm(forms.ModelForm):
    class Meta:
        model = ShowProjectSingle
        exclude = {'project_id', }
        widgets = {
    'title': forms.TextInput(attrs={'class':'span5','id':"news_title",'placeholder':u"项目名称"}),
    'school': forms.Select(attrs={'class':'span5','id':"news_title",'placeholder':u"高校名称"}),
    'teacher': forms.TextInput(attrs={'class':'span5','id':"news_title",'placeholder':u"指导教师"}),
    'members': forms.TextInput(attrs={'class':'span8','id':"news_title",'placeholder':u"团队负责人"}),
    'keywords': forms.TextInput(attrs={'class':'span8','id':"news_title",'placeholder':u"关键字"}),
    'background': forms.Textarea(attrs={'style': 'width: 800px', }),
    'result_overview': forms.Textarea(attrs={'style': 'width: 800px', })
        }



