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
from users.models import *


class SearchForm(forms.Form):
    """
        Search form for school statistics
    """
    SCHOOL_CHOICE = tuple([(o.school.id, o.school.schoolName) for o in SchoolProfile.objects.all()])
    schoolName = forms.ChoiceField(choices=SCHOOL_CHOICE,widget=forms.Select(attrs={'class':'search-input'}))
