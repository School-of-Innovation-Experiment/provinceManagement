# coding: UTF-8
import sys
import os

sys.path.append(os.path.abspath('..'))

from django.core.management import setup_environ
import settings_dev

setup_environ(settings_dev)

from django.contrib.auth.models import User
from const import *
from const.models import InsituteCategory
from users.models import ExpertProfile

institutes = InsituteCategory.objects.exclude(category=INSITUTE_CATEGORY_CHOICES[12][0])
experts_users = []
experts = []

for i in xrange(0, 60):
    group = i / 3 + 1
    institute = institutes[i/5]
    username = '2016%02d%d' % (group, i % 3 + 1)
    password = 'expert'+username
    user = User.objects.create_user(username=username, password=password)
    user.save()
    expert = ExpertProfile(userid=user, group=group, subject=institute)
    expert.save()
    print '专家帐号创建成功\t用户名:%s\t密码:%s\t类别:%s\t组号:%02d' % (username, password, institute, group)
