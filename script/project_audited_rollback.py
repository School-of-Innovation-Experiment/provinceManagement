# coding: UTF-8
import sys
import os

sys.path.append(os.path.abspath('..'))
from django.core.management import setup_environ
import settings_dev
setup_environ(settings_dev)

from const import *
from school import *
from school.models import *
from users import *
from users.models import *

while True:
    project_code = raw_input("请输入欲回退审核状态项目编号(输入N或者n退出):")
    if project_code == 'N' or project_code == 'n':
        break
    try:
        project = ProjectSingle.objects.get(project_code=project_code)
    except Exception, e:
        print '未查询到相关信息,错误信息如下:'
        print e
        continue
    print '查询到项目:', project
    check = raw_input('确认修改(Y或N)?:')
    if check == 'Y':
        presubmit = PreSubmit.objects.get(project_id=project) if\
            project.project_category.category == CATE_INNOVATION else \
            PreSubmitEnterprise.objects.get(project_id=project)
        presubmit.is_audited = False
        presubmit.save()

        presubmit = PreSubmit.objects.get(project_id=project) if\
            project.project_category.category == CATE_INNOVATION else \
            PreSubmitEnterprise.objects.get(project_id=project)
        print '修完完成，当前状态:', presubmit.is_audited
    else:
        pass
