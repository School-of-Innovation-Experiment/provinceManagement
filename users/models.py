# coding: UTF-8
'''
Created on 2012-11-10

@author: tianwei
'''
import uuid
from django.db import models
from django.contrib.auth.models import User
from const.models import *
from const import SCHOOL_USER, EXPERT_USER, ADMINSTAFF_USER, VISITOR_USER, STUDENT_USER, TEACHER_USER, EXPERT_GRADE_CHOICES

class AdminStaffProfile(models.Model):
    userid = models.ForeignKey(User, unique=True,
                               verbose_name="权限对应ID")
    jobs = models.CharField(max_length=50, blank=True, verbose_name="职务")
    is_finishing = models.BooleanField(null=False, default=False,
                                  verbose_name=u"允许结题")

    class Meta:
        verbose_name = "校级管理员"
        verbose_name_plural = "校级管理员"

    def __unicode__(self):
        return '%s' % (self.userid)

    def save(self, *args, **kwargs):
        super(AdminStaffProfile, self).save()
        auth, created = UserIdentity.objects.get_or_create(identity=ADMINSTAFF_USER)
        self.userid.identities.add(auth)


class SchoolProfile(models.Model):
    """
    User Profile Extend
    The Administrator can modified them in admin.page
    """
    address = models.CharField(max_length=100, blank=True, verbose_name="地址")
    school = models.ForeignKey(SchoolDict, unique=True, verbose_name="学院名称")
    name = models.CharField(blank=True, max_length=100,
                            verbose_name=u"姓名")

    userid = models.ForeignKey(User, unique=True, \
                               verbose_name="权限对应ID")
    is_applying = models.BooleanField(null=False, default=False,
                                  verbose_name=u"允许申请")
    is_finishing = models.BooleanField(null=False, default=False,
                                  verbose_name=u"允许结题")

    class Meta:
        verbose_name = "院级管理员"
        verbose_name_plural = "学院管理员"

    def __unicode__(self):
        return "%s(%s)"% (self.name, self.school.schoolName)

    def save(self, *args, **kwargs):
        super(SchoolProfile, self).save()
        auth, created = UserIdentity.objects.get_or_create(identity=SCHOOL_USER)
        self.userid.identities.add(auth)


class ExpertProfile(models.Model):
    userid = models.ForeignKey(User, unique=True,
                               verbose_name=u"权限对应ID")
    name = models.CharField(blank=True, max_length=100,
                            verbose_name=u"姓名")

    jobs = models.CharField(max_length=100, blank=True,
                            verbose_name=u"工作单位")
    assigned_by_school = models.ForeignKey(SchoolProfile, blank=True, null=True)
    assigned_by_adminstaff = models.ForeignKey(AdminStaffProfile, blank=True, null=True)
    grade = models.CharField(blank=False, max_length=30,
                             choices=EXPERT_GRADE_CHOICES,
                             verbose_name=u"评审项目级别")

    class Meta:
        verbose_name = "评审专家"
        verbose_name_plural = "评审专家"

    def __unicode__(self):
        return '%s(%s)' % (self.name, self.userid)

    def save(self, *args, **kwargs):
        super(ExpertProfile, self).save()
        auth, created = UserIdentity.objects.get_or_create(identity=EXPERT_USER)
        self.userid.identities.add(auth)

class TeacherProfile(models.Model):
    """
    User Profile Extend
    The Administrator can modified them in admin.page
    """
    userid = models.ForeignKey(User, unique=True,
                               verbose_name="权限对应ID")
    # school is a foreignkey to school `user`
    school = models.ForeignKey(SchoolProfile,
                               verbose_name="所属学院")
    name = models.CharField(blank=True, max_length=100,
                            verbose_name=u"姓名")
    telephone = models.CharField(blank=True, max_length=20,
                                 verbose_name=u"联系电话")
    titles = models.CharField(blank=True, max_length=20,
                              verbose_name=u"职称")
    jobs = models.CharField(max_length=100, blank=True,
                            verbose_name="工作单位")

    class Meta:
        verbose_name = "指导教师"
        verbose_name_plural = "指导教师"

    def __unicode__(self):
        return '%s(%s)' % (self.name, self.userid)

    def save(self, *args, **kwargs):
        super(TeacherProfile, self).save()
        auth, created = UserIdentity.objects.get_or_create(identity=TEACHER_USER)
        self.userid.identities.add(auth)


class StudentProfile(models.Model):
    """
    User Profile Extend
    The Administrator can modified them in admin.page
    """
    userid = models.ForeignKey(User, unique=True,
                                verbose_name="权限对应ID")
    teacher = models.ForeignKey(TeacherProfile,
                                verbose_name="指导教师")
    name = models.CharField(blank=True, max_length=100,
                            verbose_name=u"姓名")

    class Meta:
        verbose_name = "参赛学生账户"
        verbose_name_plural = "参赛学生账户"
    def __unicode__(self):
        return '%s(%s)' % (self.name, self.userid)
    def save(self, *args, **kwargs):
        super(StudentProfile, self).save()
        auth, created = UserIdentity.objects.get_or_create(identity=STUDENT_USER)
        self.userid.identities.add(auth)
