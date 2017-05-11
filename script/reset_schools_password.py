#!python
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-05-11 18:21
# Last modified: 2017-05-11 18:33
# Filename: reset_schools_password.py
# Description:
# coding: UTF-8
import sys
import os
import random

sys.path.append(os.path.abspath('..'))

from django.core.management import setup_environ
import settings_dev

setup_environ(settings_dev)

from django.contrib.auth.models import User
from const import *
from users.models import SchoolProfile

schools = SchoolProfile.objects.all()
with open('school_passwords.txt', 'w') as f:
    for school in schools:
        school_name = school.school
        user = school.userid
        new_passwd = str(random.randrange(10000, 100000))
        user.set_password(new_passwd)
        f.write('{} {} {}\n'.format(school_name, user.username, new_passwd))
        user.save()
