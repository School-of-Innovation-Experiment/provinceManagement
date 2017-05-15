#!python
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-05-11 18:21
# Last modified: 2017-05-15 15:38
# Filename: restore_project_code.py
# Description:
# coding: UTF-8
import sys
import os

sys.path.append(os.path.abspath('..'))

import MySQLdb

from django.core.management import setup_environ
import settings_production

setup_environ(settings_production)

from const import *
from school.models import *

year = 2016

conn = MySQLdb.connect(host='localhost', user='root', passwd='root',
                       port=3306, db='tmpProvinceManagement')
curs = conn.cursor()
fmt = 'select project_id, project_code from school_projectsingle where year={}'
query = fmt.format(year)
curs.execute(query)
id_codes = {}
for project_id, project_code in curs.fetchall():
    id_codes[project_id] = project_code

projs = ProjectSingle.objects.filter(year=year)
cnt = projs.count()
for idx, proj in enumerate(projs, 1):
    if idx % (cnt / 5) == 0:
        print '{:4d} / {:4d}'.format(idx, cnt)
    proj.project_code = id_codes[proj.project_id]
    proj.save()


