# coding: UTF-8

import os, sys, time
from django import forms

class StudentDispatchForm(forms.Form):
    student_password = forms.CharField(max_length=20, required=False,
           widget=forms.TextInput(attrs={'class':'span2','id':"student_password",'placeholder':u"默认密码：邮箱名字",'id':'student_password'})
           )
    student_email    = forms.EmailField(required=True,
           widget=forms.TextInput(attrs={'class':'span2','id':"student_mailbox",'placeholder':u"邮箱",'id':'student_email'})
           )


