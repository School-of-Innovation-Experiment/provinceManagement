# coding: UTF-8

import os, sys, time
from django import forms
from const import *

class  MonthCommentForm(forms.Form):
    monthId    = forms.IntegerField(max_value=50,
                            required=True,
                            widget=forms.DateInput(attrs={'class':'studentchange span2 ','id':"monthId","onkeyup":"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}" ,
                            'onafterpaste':"if(this.value.length==1){this.value=this.value.replace(/[^1-9]/g,'')}else{this.value=this.value.replace(/\D/g,'')}"}),
                            )
    commenttext  = forms.CharField( max_length=300,
                            required=True,
                            widget=forms.Textarea(attrs={'class':'studentchange span8','id':"commenttext",'placeholder':u"评论意见"}),)

