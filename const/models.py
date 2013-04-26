# coding: UTF-8
'''
Created on 2013-03-27

@author: tianwei

Desc: dict table
'''

from django.db import models
from django.contrib.auth.models import User

from const import AUTH_CHOICES, VISITOR_USER
from const import PROJECT_CATE_CHOICES, CATE_UN
from const import PROJECT_GRADE_CHOICES, GRADE_UN
from const import PROJECT_STATUS_CHOICES, STATUS_FIRST
from const import PROJECT_INNOVATION_ORIGIN_CHOICES
from const import PROJECT_ENTERPRISE_ORIGIN_CHOICES, PROJECT_ENTERPRISE_MATURITY_CHOICES
from backend.utility import search_tuple
from django.contrib.auth.models import User


class SchoolDict(models.Model):
    """
    Schoold name dict
    """
    schoolName = models.CharField(max_length=200, blank=False, unique=True,
                                  verbose_name="学院名称")

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
        verbose_name = "项目来源"
        verbose_name_plural = "项目来源"

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
        verbose_name = "项目来源"
        verbose_name_plural = "项目来源"

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
