# Create your views here.
#
from school.models import *
from const.models import ProjectGrade
from django.db.models import Q
from django.shortcuts import render
from backend.utility import convert2media_url
from const import PROJECT_GRADE_CHOICES, GRADE_NATION, DEFAULT_IMG_URL

GRADE_DICT = dict(PROJECT_GRADE_CHOICES)
def show_index(request):
    # nation_project = ProjectGrade.objects.get(grade=GRADE_NATION)
    project_list = ProjectSingle.objects.all()[:8]
    #filter( \project_grade=nation_project)
    for project in project_list:
        imgs = project.uploadedfiles_set.filter( \
            Q(file_obj__iendswith="jpg") | \
            Q(file_obj__iendswith="png") )
        project.img = (imgs.count() and convert2media_url(imgs[0].file_obj.url)) or \
            DEFAULT_IMG_URL
    context = {
        "project_list": project_list,
        }
    return render(request, 'introduction/show.html', context)
