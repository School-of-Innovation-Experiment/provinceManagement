# -*- coding: UTF-8 -*-
'''
Created on 2012-11-10

@author: tianwei
'''
import uuid
from django.db import models
from django.contrib.auth.models import User

from const.models import *


class AuthorityRelation(models.Model):
    userid = models.ForeignKey(User,verbose_name="用户ID")
    authority = models.ForeignKey(UserIdentity, verbose_name="访问权限")

    class Meta:
        unique_together = (("userid", "authority"),)
        verbose_name = "权限信息"
        verbose_name_plural = "权限信息"

    def __unicode__(self):
        return '%s' % (self.userid)


class SchoolProfile(models.Model):
    """
    User Profile Extend
    The Administrator can modified them in admin.page
    """
    address = models.CharField(max_length=100, blank=True, verbose_name="地址")
    school = models.ForeignKey(SchoolDict, unique=True, verbose_name="学校名称")
    userid = models.ForeignKey(AuthorityRelation, unique=True,
                               verbose_name="权限对应ID")

    class Meta:
        verbose_name = "参赛学校"
        verbose_name_plural = "参赛学校"

    def __unicode__(self):
        return self.school.schoolName


class ExpertProfile(models.Model):
    userid = models.ForeignKey(AuthorityRelation, unique=True,
                               verbose_name="权限对应ID")
    subject = models.ForeignKey(InsituteCategory, verbose_name="相关学科")
    jobs = models.CharField(max_length=100, blank=True,
                            verbose_name="工作单位")

    class Meta:
        verbose_name = "评审专家"
        verbose_name_plural = "评审专家"

    def __unicode__(self):
        return '%s'(self.userid)


class AdminStaffProfile(models.Model):
    userid = models.ForeignKey(AuthorityRelation, unique=True,
                               verbose_name="权限对应ID")
    jobs = models.CharField(max_length=50, blank=False, verbose_name="职务")

    class Meta:
        verbose_name = "省级管理员"
        verbose_name_plural = "省级管理员"

    def __unicode__(self):
        return '%s' % (self.userid)
