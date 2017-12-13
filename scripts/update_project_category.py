# coding: UTF-8
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
