# coding: UTF-8

import os, sys, time
from django import forms
from const import *

class StudentDispatchForm(forms.Form):
    student_password = forms.CharField(max_length=20, required=False,
           widget=forms.TextInput(attrs={'class':'span2','id':"student_password",'placeholder':u"默认密码：邮箱名字",'id':'student_password'})
           )
    student_email    = forms.EmailField(required=True,
          widget=forms.TextInput(attrs={'class':'span2', 'placeholder':u"邮箱",'id':'student_email'})
           )
    category            = forms.ChoiceField(choices = PROJECT_CATE_CHOICES, 
           )
class  MonthCommentForm(forms.Form):
    monthId    = forms.IntegerField(max_value=50,
                            required=True,
                            widget=forms.DateInput(attrs={'class':'studentchange span2 ','id':"weekId","onkeyup":"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}" ,
                            'onafterpaste':"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}"}),
                            )
    commenttext  = forms.CharField( max_length=300,
                            required=True,
                            widget=forms.Textarea(attrs={'class':'studentchange span8','id':"recordtext",'placeholder':u"评论意见"}),)

