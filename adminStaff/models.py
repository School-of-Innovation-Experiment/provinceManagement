# coding: UTF-8
'''
Created on 2013-03-28

@author: tianwei

Desc: Province Admin staff
'''

from uuid import uuid4

from django.db import models

from const.models import *
from school.models import *
from users.models import *


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
    school = models.OneToOneField(SchoolProfile)
    number = models.IntegerField(blank=False)

    class Meta:
        verbose_name = "时间节点控制"
        verbose_name_plural = "时间节点控制"


class ReviewTask(models.Model):
    review_id = models.CharField(max_length=50, blank=False, unique=True,
                                 primary_key=True, default=uuid4(),
                                 verbose_name="题目唯一ID")
    project_id = models.ForeignKey(ProjectSingle)
    experter = models.ForeignKey(ExperterProfile)
    comments = models.TextField(blank=False, verbose_name="评价")
    scores = models.IntegerField(blank=False, verbose_name="评分百分制")

    class Meta:
        verbose_name = "评审任务"
        verbose_name_plural = "评审任务"

    def __unicode__(self):
        return self.project_id.title
