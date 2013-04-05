# coding: UTF-8
'''
Created on 2012-11-10

@author: tianwei
'''

import datetime
import random
import re,sha
import uuid

from django.conf import settings
from django.shortcuts import render_to_response
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.sites.models import get_current_site
from django.db import models
from const.models import UserIdentity 
from backend.logging import logger
from users.models import SchoolProfile
from const.models import SchoolDict
SHA1_RE = re.compile('^[a-f0-9]{40}$')      #Activation Key

class RegistrationManager(models.Manager):
    """
    Custom manager for ``RegistrationProfile`` model.
    
    The methods defined here provide shortcuts for account creation
    and activation (including generation and emailing of activation
    keys), and for cleaning out expired inactive accounts.    
    
    """
    def activate_user(self, activation_key):
        """
        Validate an activation key and activation the corresponding User if vaild.
        """
        if SHA1_RE.search(activation_key):
            try:
                profile = RegistrationProfile.objects.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False
            if not profile.activation_key_expired():
                user = profile.user
                user.is_active = True
                user.save()
                profile.activation_key = "ALREADY_ACTIVATED"
                profile.save()
                return user
        
        return False
    
    def create_inactive_user(self,request,
                             username,password,email,
                             Identity,send_email=True, profile_callback=None, **kwargs):
        """
        Create a new, inactive ``User``, generates a
        ``RegistrationProfile`` and email its activation key to the
        ``User``, returning the new ``User``.
        
        TODO: we will custom the USER
        
        """
        #如果存在用户的话不必进行新建只需对权限表进行操作即可，否则新建用户
        if User.objects.filter(email=email).count() == 0:
            new_user = User.objects.create_user(username, email, password)
            new_user.is_active = False
        else:
            new_user = User.objects.get(email=email)
            
        new_authority = UserIdentity.objects.get(identity=Identity)
        new_authority.auth_groups.add(new_user)
        new_user.save()
        new_authority.save()
        #如果存在用户的话则跳过
        if User.objects.filter(email=email).count():
            pass
        #否则则进行发送邮件激活码进行激活
        else:
            registration_profile = self.create_profile(new_user)
            registration_profile.save()
            #如果是学校注册 添加学校注册姓名
            if kwargs.has_key('school_name'):
                schoolObj = SchoolDict.objects.get(id = kwargs["school_name"])
                if SchoolProfile.objects.filter(school=schoolObj).count() == 0:
                    schoolProfileObj = SchoolProfile(school=schoolObj, userid =new_user)
                    schoolProfileObj.save()
                else:  
                    schoolProfileObj = SchoolProfile.objects.get(school=schoolObj)
                    schoolProfileObj.userid = new_user
                    schoolProfileObj.save()
            if profile_callback is not None:
                profile_callback(user=new_user)
    
            if send_email:
                from django.core.mail import send_mail
                subject = render_to_string('registration/activation_email_subject.txt',
                                           {'site':get_current_site(request),
                                            'username':username,
                                            'password':password})
                
                # Email subject *must not* contain newlines
                subject = ''.join(subject.splitlines())
                message = render_to_string('registration/activation_email.txt',
                                           {'activation_key':registration_profile.activation_key,
                                            'expiration_days':settings.ACCOUNT_ACTIVATION_DAYS,
                                            'site':"http://127.0.0.1:9999",
                                           'username':username,
                                           'password':password}
                                           )
                logger.error(message)          
                send_mail(subject,
                          message,
                          settings.DEFAULT_FROM_EMAIL,
                          [new_user.email])
        return new_user

    def create_profile(self,user):
        """
        Create a ``RegistrationProfile`` for a given 
        ``User``, and return the ``RegistrationProfile``.
        """
        salt= sha.new(str(random.random())).hexdigest()[:5]
        activation_key = sha.new(salt+user.username).hexdigest()
        
        return RegistrationProfile(user=user,
                           activation_key=activation_key)
            
    def delete_expired_users(self):
        """
        Remove expired instances of ``RegistrationProfile`` and their associated ``User``s.

        It is recommended that this method be executed regularly as
        part of your routine site maintenance; this application
        provides a custom management command which will call this
        method, accessible as ``manage.py cleanupregistration``.

        """
        for profile in self.all():
            if profile.activation_key_expired():
                user = profile.user
                if not user.is_active:
                    user.delete()

class RegistrationProfile(models.Model):
    """
    A simple profile which stores an activation key for use during user account registration
    """   
    user = models.ForeignKey(User,unique=True,verbose_name=_('user'))
    activation_key = models.CharField(_('activation key'), max_length=40)
    
    objects = RegistrationManager()
    
    class Meta:
        verbose_name = '激活码管理'
        verbose_name_plural = '激活码管理'
        
    def __unicode__(self):
        return u"Registration information for %s" % self.user
        
    def activation_key_expired(self):
        """
        Determine whether this ``RegistrationProfile``'s activation
        key has expired, returning a boolean -- ``True`` if the key
        has expired.
        """
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.activation_key == "ALREADY_ACTIVATED" or \
               (self.user.date_joined + expiration_date <= datetime.datetime.now())
               
    activation_key_expired.boolean = True 
