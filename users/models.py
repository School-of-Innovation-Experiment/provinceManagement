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
    user = models.OneToOneField(User)
    school = models.ForeignKey(SchoolDict)
    identity = models.ForeignKey(UserIdentity)

    class Meta:
        verbose_name = "参赛学校"
        verbose_name_plural = "参赛学校"

    def __unicode__(self):
        return '%s' % (self.user)


class ExperterProfile(models.Model):
    user = models.OneToOneField(User)
    subject = models.FileField(InsituteCategory)
    identity = models.ForeignKey(UserIdentity)

    class Meta:
        verbose_name = "评审专家"
        verbose_name_plural = "评审专家"

    def __unicode__(self):
        return '%s' % (self.user)


class AdminStaffProfile(models.Model):
    user = models.OneToOneField(User)
    identity = models.ForeignKey(UserIdentity)

    class Meta:
        verbose_name = "省级管理员"
        verbose_name_plural = "省级管理员"

    def __unicode__(self):
        return '%s' % (self.user)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        SchoolProfile.objects.create(user=instance)
        ExperterProfile.objects.create(user=instance)
        AdminStaffProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
    
