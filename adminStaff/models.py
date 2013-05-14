# coding: UTF-8
'''
Created on 2013-03-28

@author: tianwei

Desc: Province Admin staff
'''

import uuid

from django.db import models

from const import PROJECT_STATUS_CHOICES
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
    school = models.OneToOneField(SchoolProfile, verbose_name=u"学校名称", unique=True)
    number = models.IntegerField(blank=False, verbose_name=u"总申请数量上限")
    a_cate_number = models.IntegerField(blank=False, verbose_name=u"甲类项目数量上限")

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
