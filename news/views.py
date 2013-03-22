# coding: UTF-8
'''
Created on 2013-03-17

@author: Tianwei

Desc: news view with Tinymce
'''

from django import forms
from django.contrib.flatpages.models import FlatPage
from django.shortcuts import render

from tinymce.widgets import TinyMCE

class FlatPageForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCE(attrs={'cols':80, 'rows':30}))

    class Meta:
        model = FlatPage


def testmce(request):
    if request.method == "POST":
        form = FlatPageForm(request.POST)
    else:
        form = FlatPageForm()

    data = {'form': form}

    return render(request, 'news/test.html', data)
