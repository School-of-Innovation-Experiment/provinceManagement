# coding: UTF-8
from django import forms

class StudentGroupForm(forms.Form):
    student_id = forms.CharField(max_length=20,
                                 required=True,
                                 widget=forms.TextInput(attrs={'class':'studentchange span2','id':"student_id",'placeholder':u"学号"}),)
    student_name = forms.CharField(max_length=100,
                                 required=True,
                                 widget=forms.TextInput(attrs={'class':'studentchange span2','id':"student_name",'placeholder':u"姓名"}),)

class StudentGroupInfoForm(forms.Form):
    email = forms.EmailField(required=False,
                             widget=forms.TextInput(attrs={'class':'span2 studentchange', 'placeholder':u"邮箱",'id':'email'}))
    telephone = forms.CharField(max_length=20,
                                required=False,
                                widget=forms.TextInput(attrs={'class':'studentchange span2','id':"telephone",'placeholder':u"电话"}),)
    classInfo = forms.CharField(max_length=20,
                                required=False,
                                widget=forms.TextInput(attrs={'class':'studentchange span2','id':"student_id",'placeholder':u"班级"}),)
