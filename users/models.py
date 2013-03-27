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


class UserProfile(models.Model):
    """
    User Profile Extend
    The Administrator can modified them in admin.page
    """
    user = models.OneToOneField(User)
    machinecode = models.CharField(max_length = 100)
    agentID = models.CharField(max_length = 40,default = uuid.uuid4(),unique=True)         #When the userProfile is created,agentId will be created automatically.
    workunit = models.CharField(max_length = 2000,blank=True)
    address  = models.CharField(max_length = 2000,blank=True)
    telephone = models.CharField(max_length = 100, blank=True)
    
    def __unicode__(self):
        return '%s' %(self.user)
    

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
    subject = models.ForeignKey(InsituteCategory)
    identity = models.ForeignKey(UserIdentity)
    workunit = models.CharField(max_length=100, blank=True,
                                verbose_name="工作单位")

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
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User) 
