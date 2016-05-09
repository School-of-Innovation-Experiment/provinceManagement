# coding: UTF-8
import sys
import os
import random

sys.path.append(os.path.abspath('..'))

from django.core.management import setup_environ
import settings_dev

setup_environ(settings_dev)

from django.contrib.auth.models import User
from django.db.models import Q

from const import *
from const.models import *
from users.models import *
from school.models import *

experts = ExpertProfile.objects.exclude(Q(group=0) | Q(group=-1))

for expert in experts:
    re_project_experts = Re_Project_Expert.objects.filter(Q(expert=expert))
    for rpe in re_project_experts:
        rpe.score = random.randint(1, 100)
        rpe.pass_p = True
        rpe.save()
    print '专家 %s 模拟打分完毕' % expert
