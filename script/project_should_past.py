# coding: UTF-8
import sys
import os

sys.path.append(os.path.abspath('..'))
from django.core.management import setup_environ
import settings_dev
setup_environ(settings_dev)

from school import *
from school.models import *
from users import *
from users.models import *

school_name = raw_input('请输入欲查询学校名称: ')
school_profile = SchoolProfile.objects.get(school__schoolName=school_name)
if not school_profile:
    print '未找到该学校,请查证后再输入'
assert school_profile

year = raw_input('请输入当前年份: ')
if not 2000 < year < 2100:
    print '请输入正确年份'
assert year

emails = StudentProfile.objects.filter(school=school_profile).filter(projectsingle__is_past=False)
error_emails = filter(lambda x: x.projectsingle.year != year, emails)
for item in error_emails:
    print '%s:%s' % (item.projectsingle.title, item)


