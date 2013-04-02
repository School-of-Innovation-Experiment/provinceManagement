# Create your views here.
#
from school.models import *
from const.models import ProjectGrade
from django.db.models import Q
from django.shortcuts import render
from backend.utility import convert2media_url
from const import PROJECT_GRADE_CHOICES, GRADE_NATION

GRADE_DICT = dict(PROJECT_GRADE_CHOICES)
DEFAULT_IMG_URL = ""
def show_index(request):
    nation_project = ProjectGrade.objects.get(grade=GRADE_NATION)
    projects = ProjectSingle.objects.filter( \
        project_grade=nation_project)
    for project in projects:
        imgs = project.uploadedfiles_set.filter( \
            Q(file_obj__iendswith="jpg") | \
            Q(file_obj__iendswith="png") )
        project.img = (imgs.count() and convert2media_url(imgs[0].file_obj.url)) or \
            DEFAULT_IMG_URL
    context = {
        "projects": projects,
        }
    return render(request, 'introduction/show.html', context)
