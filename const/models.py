#!/usr/bin/python
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-11-26 14:30
# Last modified: 2017-03-13 16:36
# Filename: models.py
# Description:
# coding: UTF-8
'''
Created on 2013-03-27

@author: tianwei

Desc: dict table
'''

from django.db import models
from django.contrib.auth.models import User

from const import NEWS_CATEGORY_CHOICES
from const import NEWS_CATEGORY_ANNOUNCEMENT
from const import OVER_STATUS_CHOICES
from const import OVER_STATUS_NOTOVER
from const import AUTH_CHOICES, VISITOR_USER
from const import PROJECT_CATE_CHOICES, CATE_UN
from const import PROJECT_GRADE_CHOICES, GRADE_UN
from const import PROJECT_STATUS_CHOICES, STATUS_FIRST
from const import PROJECT_INNOVATION_ORIGIN_CHOICES
from const import PROJECT_ENTERPRISE_ORIGIN_CHOICES, PROJECT_ENTERPRISE_MATURITY_CHOICES
from const import MAJOR_CHOICES
from const import DEPARTMENT_CODE
from backend.utility import search_tuple
from django.contrib.auth.models import User

class MajorDict(models.Model):
    major = models.CharField(blank=True, null=True, max_length=100, choices=MAJOR_CHOICES, unique=True,
                             verbose_name=u"专业")
    class Meta:
        verbose_name = "专业列表"
        verbose_name_plural = "专业列表"

    def __unicode__(self):
        return self.get_major_display()

class SchoolDict(models.Model):
    """
    Schoold name dict
    """
    schoolName = models.CharField(max_length=200, blank=False, unique=True,
                                  verbose_name="学院名称")
    school_code = models.CharField(max_length=10, blank=True, null=True, choices=DEPARTMENT_CODE,
                                   verbose_name=u'学院代码')

    class Meta:
        verbose_name = "学院列表"
        verbose_name_plural = "学院列表"

    def __unicode__(self):
        return self.schoolName


class ProjectCategory(models.Model):
    """
    Project category: Innovation, enterprise, ...
    """
    category = models.CharField(max_length=30, blank=False, unique=True,
                                choices=PROJECT_CATE_CHOICES, default=CATE_UN,
                                verbose_name="项目类型")

    class Meta:
        verbose_name = "项目类型"
        verbose_name_plural = "项目类型"

    def __unicode__(self):
        return self.get_category_display()


class InsituteCategory(models.Model):
    """
    Insitute Category: software, math, ...
    """
    category = models.CharField(max_length=200, blank=False, unique=True,
                                verbose_name="所属学科学院")

    class Meta:
        verbose_name = "学院学科"
        verbose_name_plural = "学院学科"

    def __unicode__(self):
        return self.category

class UserIdentity(models.Model):
    """
    Login User identity: AdminStaff, AdminSystem, Expert, SchoolTeam, visitor,
    Teacher, Student
    """
    identity = models.CharField(max_length=50, blank=False, unique=True,
                                choices=AUTH_CHOICES, default=VISITOR_USER,
                                verbose_name="身份级别")
    auth_groups = models.ManyToManyField(User, related_name="identities")

    class Meta:
        verbose_name = "登录权限"
        verbose_name_plural = "登录权限"

    def __unicode__(self):
        return self.get_identity_display()


class ProjectGrade(models.Model):
    """
    Project grade: Nation, Province
    """
    grade = models.CharField(max_length=20, blank=False, unique=True,
                             choices=PROJECT_GRADE_CHOICES, default=GRADE_UN,
                             verbose_name="项目级别")

    class Meta:
        verbose_name = "项目级别"
        verbose_name_plural = "项目级别"

    def __unicode__(self):
        return self.get_grade_display()


class ProjectStatus(models.Model):
    """
    Project status: review, submit, result
    """
    status = models.CharField(max_length=50, blank=False, unique=True,
                              choices=PROJECT_STATUS_CHOICES,
                              default=STATUS_FIRST,
                              verbose_name="项目状态")

    class Meta:
        verbose_name = "项目状态"
        verbose_name_plural = "项目状态"

    def __unicode__(self):
        return self.get_status_display()

class ProjectOrigin(models.Model):
    """
    Project Origin for innovation
    """
    origin = models.CharField(blank=False, null=False, unique=True, max_length=5,
                                 choices=PROJECT_INNOVATION_ORIGIN_CHOICES, \
                                 default = "0",
                                 verbose_name="项目来源")
    class Meta:
        verbose_name = "创新项目来源"
        verbose_name_plural = "创新项目来源"

    def __unicode__(self):
        return self.get_origin_display()

class ProjectEnterpriseOrigin(models.Model):
    """
    Project Origin for innovation
    """
    origin = models.CharField(blank=False, null=False, unique=True, max_length=5,
                                 choices=PROJECT_ENTERPRISE_ORIGIN_CHOICES, \
                                 default = "0",
                                 verbose_name="项目来源")
    class Meta:
        verbose_name = "创业类项目来源"
        verbose_name_plural = "创业类项目来源"

    def __unicode__(self):
        return self.get_origin_display()

class ProjectEnterpriseMaturity(models.Model):
    """
    Project Origin for innovation
    """
    maturity = models.CharField(blank=False, null=False, unique=True, max_length=5,
                                choices=PROJECT_ENTERPRISE_MATURITY_CHOICES, \
                                default = "0",
                                verbose_name="项目技术成熟度")
    class Meta:
        verbose_name = "项目技术成熟度"
        verbose_name_plural = "项目技术成熟度"

    def __unicode__(self):
        return self.get_maturity_display()

class NewsCategory(models.Model):
    """
    """
    category = models.CharField(blank=False, null=False, unique=True, max_length=20,
                                choices=NEWS_CATEGORY_CHOICES, \
                                default=NEWS_CATEGORY_ANNOUNCEMENT ,
                                verbose_name=u"新闻类型")
    class Meta:
        verbose_name = "新闻类型"
        verbose_name_plural = "新闻类型"

    def __unicode__(self):
        return self.get_category_display()

class OverStatus(models.Model):
    """
    """
    status = models.CharField(blank=False, null=False, unique=True, max_length=20,
                                choices=OVER_STATUS_CHOICES, \
                                default=OVER_STATUS_NOTOVER ,
                                verbose_name=u"项目结束状态")
    class Meta:
        verbose_name = "项目结束状态"
        verbose_name_plural = "项目结束状态"

    def __unicode__(self):
        return self.get_status_display()

class SchoolRecommendRate(models.Model):
    """
    """
    rate = models.FloatField(default=0)
    class Meta:
        verbose_name = "项目结束状态"
        verbose_name_plural = "项目结束状态"

    def __unicode__(self):
        return self.get_status_display()


    #def mysave(self, *args, **kwargs):
        #self.__class__.objects.exclude(id=self.id).delete()
    #    super(SchoolRecommendRate, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        """
        """
        try: return cls.objects.get()
        except: return cls()


class ApplyControl(models.Model):
    """
    Project apply control.

    Before project is applied, this should be tested, if any of department and
    school apply control is forbidden, then application should fail, due to 
    history reasons, deparment apply control will be in SchoolProfile rather
    than here, so this is just for school admin currently.

    Author: David
    """
    origin = models.ForeignKey(SchoolDict, null=True, blank=True,
                               verbose_name="设置来源")
    is_applying = models.BooleanField(null=False, default=True,
                                      verbose_name=u"允许申请")
    class Meta:
        verbose_name = u'项目申请控制'
        verbose_name_plural = u'项目申请控制'

    def __unicode__(self):
        return '{}:{}'.format(self.origin or 'ADMIN', self.is_applying)
