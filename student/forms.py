# coding: UTF-8
from django import forms
from const import *
from const.models import *

class StudentGroupForm(forms.Form):
    student_id = forms.CharField(max_length=20,
                                 required=True,
                                 widget=forms.TextInput(attrs={'class':'studentchange span2','id':"student_id",'placeholder':u"学号","onkeyup":"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}" ,'onafterpaste':"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}"}),)
    student_name = forms.CharField(max_length=100,
                                   required=True,
                                   widget=forms.TextInput(attrs={'class':'studentchange span2','id':"student_name",'placeholder':u"姓名"}),)

class StudentGroupInfoForm(forms.Form):
    SCHOOL_CHOICES_list = []
    school_list        = SchoolDict.objects.all()
    for obj in school_list:
        SCHOOL_CHOICES_list.append((obj.id, obj.schoolName))
    SCHOOL_CHOICE = tuple(SCHOOL_CHOICES_list)

    MAJOR_CHOICES_list = []
    major_list        = MajorDict.objects.all()
    major_list = sorted(major_list, key = lambda i: int(i.major))
    for obj in major_list:
        MAJOR_CHOICES_list.append((obj.id, obj.__unicode__()))
    MAJOR_CHOICE = tuple(MAJOR_CHOICES_list)
    email = forms.EmailField(required=False,
                             widget=forms.TextInput(attrs={'class':'span2 studentchange', 'placeholder':u"邮箱",'id':'email'}))
    telephone = forms.CharField(max_length=20,
                                required=False,
                                widget=forms.TextInput(attrs={'class':'studentchange span2','id':"telephone",'placeholder':u"电话"}),)
    classInfo = forms.CharField(max_length=20,
                                required=False,
                                widget=forms.TextInput(attrs={'class':'studentchange span2','id':"student_id",'placeholder':u"班级"}),)
    sex = forms.ChoiceField(choices = SEX_CHOICES,
                            required=True,)
                          # widget=forms.TextInput(attrs={'class':'studentchange span2','id':"student_sex",'placeholder':u"性别"}),)
    nation = forms.CharField(max_length=20,
                             required=True,
                             widget=forms.TextInput(attrs={'class':'studentchange span2','id':"student_nation",'placeholder':u"民族"}),)
    school = forms.ChoiceField(choices = SCHOOL_CHOICE,
                               required=False,)
                             # widget=forms.TextInput(attrs={'class':'studentchange span2','id':"student_school",'placeholder':u"学院"}),)
    major = forms.ChoiceField(choices = MAJOR_CHOICE,
                            required=True,)
                            # widget=forms.TextInput(attrs={'class':'studentchange span2','id':"student_major",'placeholder':u"专业"}),)
    grade = forms.CharField(max_length=20,
                            required=True,
                            widget=forms.TextInput(attrs={'class':'studentchange span2','id':"student_grade",'placeholder':u"年级"}),)


class ProcessRecordForm(forms.Form):
    weekId    = forms.IntegerField(max_value=200,
                                       required=True,
                                       widget=forms.DateInput(attrs={'class':'studentchange span2 ','id':"weekId","onkeyup":"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}" ,'onafterpaste':"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}"}),
        )
    recorder    = forms.CharField( max_length=30,
                                   required=True,
                                   widget=forms.TextInput(attrs={'class':'studentchange span2','id':"recorder",'placeholder':u""}),)
    recordtext  = forms.CharField( max_length=300,
                                   required=True,
                                   widget=forms.Textarea(attrs={'class':'studentchange span8','id':"recordtext",'placeholder':u"过程记录"}),)
