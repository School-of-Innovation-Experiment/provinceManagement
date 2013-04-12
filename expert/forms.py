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
        exclude = ('project', 'expert', )
        widgets = {'comments': forms.Textarea(attrs={'class': "fill-form", 'rows': "6", 
                                                      'placeholder': "给这个项目提点意见或建议吧。。。"}),
                   'score_innovation': forms.TextInput(attrs={'class':'input-small', 'placeholder':'0-100分'}),
                   'score_practice': forms.TextInput(attrs={'class':'input-small', 'placeholder':'0-100分'}),
                   'score_funny': forms.TextInput(attrs={'class':'input-small', 'placeholder':'0-100分'}),
                   }
