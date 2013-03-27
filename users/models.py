# -*- coding: UTF-8 -*-
'''
Created on 2012-11-10

@author: tianwei
'''
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from const.models import *


class SchoolProfile(models.Model):
    """
    User Profile Extend
    The Administrator can modified them in admin.page
    """
    address = models.CharField(max_length=100, blank=True)
    school = models.ForeignKey(SchoolDict, unique=True)
    userid = models.ForeignKey(User, unique=True)

    class Meta:
        verbose_name = "参赛学校"
        verbose_name_plural = "参赛学校"

    def __unicode__(self):
        return '%s' % (self.userid)


class ExpertProfile(models.Model):
    userid = models.ForeignKey(User, unique=True)
    subject = models.ForeignKey(InsituteCategory)
    jobs = models.CharField(max_length=100, blank=True,
                            verbose_name="工作单位")

    class Meta:
        verbose_name = "评审专家"
        verbose_name_plural = "评审专家"

    def __unicode__(self):
        return '%s' % (self.userid)


class AdminStaffProfile(models.Model):
    userid = models.ForeignKey(User, unique=True)
    jobs = models.CharField(max_length=50, blank=False, verbose_name="职务")

    class Meta:
        verbose_name = "省级管理员"
        verbose_name_plural = "省级管理员"

    def __unicode__(self):
        return '%s' % (self.userid)


class AuthorityRelation(models.Model):
    userid = models.ForeignKey(User)
    authority = models.ForeignKey(UserIdentity)

    class Meta:
        unique_together = (("userid", "authority"),)
        verbose_name = "权限信息"
        verbose_name_plural = "权限信息"

    def __unicode__(self):
        return '%s' % (self.userid)

