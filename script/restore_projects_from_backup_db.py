#!/usr/local/bin/python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-06-26 08:38
# Last modified: 2017-06-26 08:45
# Filename: restore_projects_from_backup_db.py
# Description:
import sys
import os

sys.path.append(os.path.abspath('..'))
from django.core.management import setup_environ
import settings_dev
setup_environ(settings_dev)

from school.models import *

adminuser_id = None  # Which school's projects try to restore

# 1. Fetch projects info from backup database
# e.g. ProjectSingle.objects.using('backup_db_name').filter(...)

pass

# 2. Save project's related objects w.r.t its' dependencies to default database.
# e.g. user.save()  # save() will automatically save to default db

pass
