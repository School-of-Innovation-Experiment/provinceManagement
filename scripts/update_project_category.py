#!/usr/local/bin/python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2017-03-16 09:13
# Last modified: 2017-03-16 09:27
# Filename: update_project_category.py
# Description:
from .school.models import ProjectSingle
from .const.models import ProjectCategory
titles = []
with open('project_names.txt', 'r') as f:
    for line in f:
        title = line.strip()
        titles.append(title)

cate = ProjectCategory.objects.get(category='research')

projs = []
for title in titles:
    proj = ProjectSingle.objects.get(title__istartswith=title)
    proj.project_category = cate
    proj.save()
