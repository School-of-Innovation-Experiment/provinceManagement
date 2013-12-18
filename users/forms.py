# coding: UTF-8
'''
Created on 2013-03-04

@author: tianwei

Desc: This module contains Forms for users.views.
'''
import os
import sys
import time

from django import forms
from django.core.exceptions import PermissionDenied
from django.db import models
from django.forms.util import ErrorList
from django.contrib.auth import authenticate
from django.forms import ModelForm
from django.core.urlresolvers import reverse

from school.models import *
from users.models import *


class SchoolProfileForm(ModelForm):
    """
        User Profile settings form
    """
    class Meta:
        model = SchoolProfile
        exclude = ("userid", "school")
class TeacherProfileForm(ModelForm):
    """
        Teacher Profile settings form
    """
    class Meta:
        model = TeacherProfile
        exclude = ("userid","school")

class ExpertProfileForm(ModelForm):
    """
       Expert Profile settings form
    """
    class Meta:
        model = ExpertProfile
        exclude = ("userid")


class AdminStaffProfileForm(ModelForm):
    """
        AdminStaff Profile settings form
    """
    class Meta:
        model = AdminStaffProfile
        exclude = ("userid", )


class PasswordForm(forms.Form):
    """
        User change password form
    """
    old_password = forms.CharField(required=True,
                                   max_length=255,
                                   widget=forms.PasswordInput(attrs={"class": "input-xlarge"}))
    new_password = forms.CharField(required=True,
                                   min_length=1,
                                   max_length=255,
                                   widget=forms.PasswordInput(attrs={"class": "input-xlarge"}))
    new_password2 = forms.CharField(required=True,
                                    min_length=1,
                                    max_length=255,
                                    widget=forms.PasswordInput(attrs={"class": "input-xlarge"}))
    user = None

    def __init__(self, user, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs)
        self.user = user

    def clean(self):
        """
            self clean form data
        """
        password = self.cleaned_data.get("old_password", "").strip()
        new_password = self.cleaned_data.get("new_password", "").strip()
        new_password2 = self.cleaned_data.get("new_password2", "").strip()

        # check password from database
        user = authenticate(username=self.user.username,
                            password=password)

        if user is None:
            self._errors["old_password"] = ErrorList([u'Please input the corrected password!'])
            if self.cleaned_data.get("old_password", None) is not None:
                del self.cleaned_data["old_password"]

        # check newpassword twice
        if new_password != new_password2:
            self._errors["new_password2"] = ErrorList([u'The twiced password\
                cannot match!'])
            if self.cleaned_data.get("new_password2", None) is not None:
                del self.cleaned_data["new_password2"]

        return self.cleaned_data
