# Create your views here.
#
from school.models import *
from const.models import ProjectGrade
from django.http import Http404
from django.db.models import Q
from django.shortcuts import render
from backend.utility import convert2media_url, getContext
from const import PROJECT_GRADE_CHOICES, GRADE_NATION, DEFAULT_IMG_URL

GRADE_DICT = dict(PROJECT_GRADE_CHOICES)
def show_index(request):
    # nation_project = ProjectGrade.objects.get(grade=GRADE_NATION)
    # return render(request, 'introduction/show.html', {})
    project_page = request.GET.get('project_page')
    try:
        project_page = int(project_page)
    except:
        project_page = 1
    project_list = ProjectSingle.objects.all()
    #filter( \project_grade=nation_project)
    context = getContext(project_list, project_page, 'project', 8)
    if project_page != context["project_page"].number:
        raise Http404
    for project in context["project_list"]:
        imgs = project.uploadedfiles_set.filter( \
            Q(file_obj__iendswith="jpg") | \
            Q(file_obj__iendswith="png") )
        project.img = (imgs.count() and convert2media_url(imgs[0].file_obj.url)) or \
            DEFAULT_IMG_URL
    return render(request, 'introduction/show.html', context)
