# coding: UTF-8
'''
Created on 2012-11-10

@author: tianwei
'''
import uuid
from django.db import models
from django.contrib.auth.models import User

from const.models import *
from const import SCHOOL_USER, EXPERT_USER, ADMINSTAFF_USER, VISITOR_USER, STUDENT_USER

class SchoolProfile(models.Model):
    """
    User Profile Extend
    The Administrator can modified them in admin.page
    """
    address = models.CharField(max_length=100, blank=True, verbose_name="地址")
    school = models.ForeignKey(SchoolDict, unique=True, verbose_name="学校名称")
    userid = models.ForeignKey(User, unique=True,
                               verbose_name="权限对应ID")

    class Meta:
        verbose_name = "参赛学校"
        verbose_name_plural = "参赛学校"

    def __unicode__(self):
        return self.school.schoolName
    def get_name(self):
        return "%s(%s)" % (self.userid.first_name,self.school.schoolName) 

    def save(self, *args, **kwargs):
        super(SchoolProfile, self).save()
        auth, created = UserIdentity.objects.get_or_create(identity=SCHOOL_USER)
        self.userid.identities.add(auth)


class ExpertProfile(models.Model):
    userid = models.ForeignKey(User, unique=True,
                               verbose_name="权限对应ID")
    subject = models.ForeignKey(InsituteCategory, verbose_name="相关学科")
    jobs = models.CharField(max_length=100, blank=True,
                            verbose_name="工作单位")
    numlimit = models.IntegerField(blank=True, null=True, default=0,
                                   verbose_name="甲类国家级项目上限")
    numlimit_b = models.IntegerField(blank=True, null=True, default=0,
                                   verbose_name="乙类国家级项目上限")
    group = models.IntegerField(blank=True, null=True, default=-1,
                                   verbose_name="组号")
    class Meta:
        verbose_name = "评审专家"
        verbose_name_plural = "评审专家"

    def __unicode__(self):
        return '%s' % (self.userid)

    def save(self, *args, **kwargs):
        super(ExpertProfile, self).save()
        auth, created = UserIdentity.objects.get_or_create(identity=EXPERT_USER)
        self.userid.identities.add(auth)


class StudentProfile(models.Model):
    """
    school student profile
    """
    user = models.ForeignKey(User, unique=True)
    school = models.ForeignKey(SchoolProfile)

    class Meta:
        verbose_name = "参赛学生"
        verbose_name_plural = "参赛学生"

    def __unicode__(self):
        return '%s' % (self.user)

    def save(self, *args, **kwargs):
        super(StudentProfile, self).save()
        auth, created = UserIdentity.objects.get_or_create(identity=STUDENT_USER)
        self.user.identities.add(auth)


class AdminStaffProfile(models.Model):
    userid = models.ForeignKey(User, unique=True,
                               verbose_name="权限对应ID")
    jobs = models.CharField(max_length=50, blank=True, verbose_name="职务")

    class Meta:
        verbose_name = "省级管理员"
        verbose_name_plural = "省级管理员"

    def __unicode__(self):
        return '%s' % (self.userid)

    def save(self, *args, **kwargs):
        super(AdminStaffProfile, self).save()
        auth, created = UserIdentity.objects.get_or_create(identity=ADMINSTAFF_USER)
        self.userid.identities.add(auth)
