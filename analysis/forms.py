# coding: UTF-8
'''
Created on 2013-04-17

@author: tianwei

Desc: Search form.
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

from const.models import *


class SearchForm(ModelForm):
    """
        Search form for school statistics
    """
    class Meta:
        model = SchoolDict
        #TODO: add css into widgets
        exclude = ('id', )
        widgets = {'schoolName': forms.Select(attrs={'class': "school-display"}), }
