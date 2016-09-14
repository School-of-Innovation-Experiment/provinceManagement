#!/usr/bin/python
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-09-13 11:06
# Last modified: 2016-09-14 11:56
# Filename: models.py
# Description:
# coding: UTF-8
'''
Created on 2013-03-28

@author: tianwei

Desc: Province Admin staff
'''

import uuid
import os, sys

from django.db import models

from const import PROJECT_STATUS_CHOICES
from const.models import *
from school.models import *
from users.models import *

from django.contrib.auth.models import User

import settings


class ProjectControl(models.Model):
    """
    Project date control
    """
    pre_start_day = models.DateField(blank=False,
                                     verbose_name="申请报告提交开始时间")
    pre_end_day = models.DateField(blank=False,
                                   verbose_name="申请报告提交结束时间")
    pre_start_day_review = models.DateField(blank=False,
                                            verbose_name="项目初审开始时间")
    pre_end_day_review = models.DateField(blank=False,
                                          verbose_name="项目初审结束时间")
    final_start_day = models.DateField(blank=False,
                                       verbose_name="结题报告提交开始时间")
    final_end_day = models.DateField(blank=False,
                                     verbose_name="结题报告提交结束时间")
    final_start_day_review = models.DateField(blank=False,
                                              verbose_name="项目终审开始时间")
    final_end_day_review = models.DateField(blank=False,
                                            verbose_name="项目终审结束时间")
    def now_status(self):
        now = datetime.date.today()
        statuss_list =  [(self.pre_end_day, PROJECT_STATUS_CHOICES[0]),
                         (self.final_end_day, PROJECT_STATUS_CHOICES[2]),
                         (self.final_end_day_review, PROJECT_STATUS_CHOICES[3]) ]
        for i in range(len(statuss_list)):
            if now < statuss_list[i][0]:
                return statuss_list[i][1][1], (statuss_list[i][0] - now) .days
            return "", 0

    class Meta:
        verbose_name = "时间节点控制"
        verbose_name_plural = "时间节点控制"


class ProjectPerLimits(models.Model):
    """
    Project apply number limits
    """
    school = models.OneToOneField(SchoolProfile, verbose_name="学校名称", unique=True)
    number = models.IntegerField(blank=False, verbose_name="申请数量上限")

    class Meta:
        verbose_name = "申请数量限制"
        verbose_name_plural = "申请数量限制"

    def __unicode__(self):
        return self.school.school.schoolName + str(self.number)
class NoticeMessage(models.Model):
    '''
    约定:
    传给专家的信息以__expert__开头
    传给学校的信息以__school__开头
    '''
    noticedatetime = models.DateTimeField(blank=True, default=datetime.datetime.now)
    noticemessage = models.CharField(blank=True, max_length=600)

class TemplateNoticeMessage(models.Model):
    """docstring for NoticeMessageTemplate"""
    noticeId    = models.DecimalField(blank =False,max_digits=19, decimal_places=2)
    title       = models.CharField(blank=False,max_length=30)
    message     = models.CharField(blank=True,max_length=600)

class HomePagePic(models.Model):
    """
    """
    pic_obj = models.FileField(upload_to=settings.HOMEPAGE_PIC_PATH,
                               verbose_name="文件对象")
    name = models.CharField(max_length=100, blank=False,
                            verbose_name="文件名称")
    uploadtime = models.DateTimeField(blank=True, null=True,
                                      verbose_name="上传时间")
    file_size = models.CharField(max_length=50, blank=True, null=True,
                                 default=None, verbose_name="文件大小")
    file_type = models.CharField(max_length=50, blank=True, null=True,
                                 default=None, verbose_name="文件类型")
    class Meta:
        verbose_name = "首页图片上传"
        verbose_name_plural = "首页图片上传"

    def __unicode__(self):
        return self.name
    def file_name(self):
        return os.path.basename(self.file_obj.name)
