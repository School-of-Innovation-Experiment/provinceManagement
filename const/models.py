# coding: UTF-8
'''
Created on 2013-03-27

@author: tianwei

Desc: dict table
'''

from django.db import models


class SchoolDict(models.Model):
    """
    Schoold name dict
    """
    schoolName = models.CharField(max_length=200, blank=False, unique=True)

    class Meta:
        verbose_name = "学校列表"
        verbose_name_plural = "学校列表"

    def __unicode__(self):
        return self.schoolName


class ProjectCategory(models.Model):
    """
    Project category: Innovation, enterprise, ...
    """
    category = models.CharField(max_length=30, blank=False, unique=True)

    class Meta:
        verbose_name = "项目类型"
        verbose_name_plural = "项目类型"

    def __unicode__(self):
        return self.category


class InsituteCategory(models.Model):
    """
    Insitute Category: software, math, ...
    """
    category = models.CharField(max_length=200, blank=False, unique=True)

    class Meta:
        verbose_name = "学院学科"
        verbose_name_plural = "学院学科"

    def __unicode__(self):
        return self.category

class UserIdentity(models.Model):
    """
    Login User identity: AdminStaff, AdminSystem, Expert, SchoolTeam, visitor,
    """
    identity = models.CharField(max_length=50, blank=False, unique=True)

    class Meta:
        verbose_name = "登录权限"
        verbose_name_plural = "登录权限"

    def __unicode__(self):
        return self.identity

class ProjectGrade(models.Model):
    """
    Project grade: Nation, Province
    """
    grade = models.CharField(max_length=20, blank=False, unique=True)

    class Meta:
        verbose_name = "项目级别"
        verbose_name_plural = "项目级别"


class ProjectStatus(models.Model):
    """
    Project status: review, submit, result
    """
    status = models.CharField(max_length=50, blank=False, unique=True)

    class Meta:
        verbose_name = "项目级别"
        verbose_name_plural = "项目级别"
