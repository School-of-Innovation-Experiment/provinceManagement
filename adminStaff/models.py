# coding: UTF-8
'''
Created on 2013-03-28

@author: tianwei

Desc: Province Admin staff
'''

import uuid

from django.db import models

from const.models import *
from school.models import *
from users.models import *

from django.contrib.auth.models import User


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

    class Meta:
        verbose_name = "时间节点控制"
        verbose_name_plural = "时间节点控制"


class ProjectPerLimits(models.Model):
    """
    Project apply number limits
    """
    school = models.OneToOneField(SchoolProfile, verbose_name="学校名称",
                                  unique=True)
    number = models.IntegerField(blank=False, verbose_name="申请数量上限")

    class Meta:
        verbose_name = "申请数量限制"
        verbose_name_plural = "申请数量限制"

    def __unicode__(self):
        return self.school.school.schoolName + str(self.number)


class ReviewTask(models.Model):
    """
    Review Task assign
    """
    review_id = models.CharField(max_length=50, blank=False, unique=True,
                                 primary_key=True, default=str(uuid.uuid4()),
                                 verbose_name="题目唯一ID")
    project_id = models.ForeignKey(ProjectSingle)
    experter = models.ForeignKey(ExpertProfile)
    comments = models.TextField(blank=False, verbose_name="评价")
    scores = models.IntegerField(blank=False, verbose_name="评分百分制")

    #TODO: maybe we should extent scores field.

    class Meta:
        verbose_name = "评审任务"
        verbose_name_plural = "评审任务"

    def __unicode__(self):
        return self.project_id.title
