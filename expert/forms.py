# coding: UTF-8
'''
Created on 2013-04-03

@author: tianwei

Desc: Review form.
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


class ReviewForm(ModelForm):
    """
        Project Basic info
    """
    class Meta:
        model = Re_Project_Expert
        #TODO: add css into widgets
        exclude = ('project', 'expert', 'is_assign_by_adminStaff', )
        widgets = {'comments': forms.Textarea(attrs={'class': "fill-form", 'rows': "6", 
                                                      'placeholder': "给这个项目提点意见或建议吧。。。"}),
                   'score_significant': forms.TextInput(attrs={'class':'input-small', 'placeholder':'0-100分',"onkeyup":"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}" ,'onafterpaste':"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}"}),
                   'score_value': forms.TextInput(attrs={'class':'input-small', 'placeholder':'0-100分',"onkeyup":"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}" ,'onafterpaste':"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}"}),
                   'score_innovation': forms.TextInput(attrs={'class':'input-small', 'placeholder':'0-100分',"onkeyup":"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}" ,'onafterpaste':"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}"}),
                   'score_practice': forms.TextInput(attrs={'class':'input-small', 'placeholder':'0-100分',"onkeyup":"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}" ,'onafterpaste':"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}"}),
                   'score_achievement': forms.TextInput(attrs={'class':'input-small', 'placeholder':'0-100分',"onkeyup":"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}" ,'onafterpaste':"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}"}),
                   'score_capacity': forms.TextInput(attrs={'class':'input-small', 'placeholder':'0-100分',"onkeyup":"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}" ,'onafterpaste':"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}"}),
                   }
    def clean(self):
        #TODO still have several bug
        clean_data = super(ReviewForm, self).clean()
        msg = u"得分输入有误(为负数或超过上限)，请重新输入"
        if 0 > clean_data.get('score_significant') or clean_data.get('score_significant') > 15:
            self._errors["score_significant"] = self.error_class([msg])

        if 0 > clean_data.get('score_value') or clean_data.get('score_value') > 20:
            self._errors["score_value"] = self.error_class([msg])

        if 0 > clean_data.get('score_innovation') or clean_data.get('score_innovation') > 25:
            self._errors["score_innovation"] = self.error_class([msg])

        if 0 > clean_data.get('score_practice') or clean_data.get('score_practice') > 20:
            self._errors["score_practice"] = self.error_class([msg])

        if 0 > clean_data.get('score_achievement') or clean_data.get('score_achievement') > 10:
            self._errors["score_achievement"] = self.error_class([msg])

        if 0 > clean_data.get('score_capacity') or clean_data.get('score_capacity') > 10:
            self._errors["score_capacity"] = self.error_class([msg])

        return clean_data




