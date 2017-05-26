#!/usr/local/bin/python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-05-26 14:16
# Last modified: 2017-05-26 14:28
# Filename: expert_generate.py
# Description:
# coding: UTF-8
import sys
import os

from random import randint

sys.path.append(os.path.abspath('..'))

from django.core.management import setup_environ
import settings_dev

setup_environ(settings_dev)

from django.contrib.auth.models import User
from const import *
from const.models import InsituteCategory
from users.models import ExpertProfile

institute = InsituteCategory.objects.get(category=INSITUTE_CATEGORY_CHOICES[12][0])
experts_users = []
experts = []

for i in xrange(1, 19):
    username = '2017{:03d}'.format(i)
    password = str(randint(10000, 99999))
    user = User.objects.create_user(username=username, password=password)
    user.save()
    expert = ExpertProfile(userid=user, group=2017, subject=institute)
    expert.save()
    print '专家帐号创建成功\t用户名:%s\t密码:%s\t类别:%s\t组号:%02d' % (username, password, institute, 2017)
