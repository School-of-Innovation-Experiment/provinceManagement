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
class ProcessRecordForm(forms.Form):
    weekId    = forms.IntegerField(max_value=50,
                            required=True,
                            widget=forms.DateInput(attrs={'class':'studentchange span2 ','id':"weekId","onkeyup":"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}" ,
                            'onafterpaste':"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}"}),
                            )
    recorder    = forms.CharField( max_length=30,
                            required=True,
                            widget=forms.TextInput(attrs={'class':'studentchange span2','id':"recorder",'placeholder':u""}),)
    recordtext  = forms.CharField( max_length=300,
                            required=True,
                            widget=forms.Textarea(attrs={'class':'studentchange span8','id':"recordtext",'placeholder':u"过程记录"}),)