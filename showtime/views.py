# Create your views here.
#
from school.models import *
from const.models import ProjectGrade
from django.http import Http404
from django.db.models import Q
from django.shortcuts import render
from backend.utility import convert2media_url, getContext
from const import PROJECT_GRADE_CHOICES, GRADE_NATION, DEFAULT_IMG_URL
from const.models import SchoolDict, ProjectGrade

GRADE_DICT = dict(PROJECT_GRADE_CHOICES)

def show_index(request):
    project_page = request.GET.get('project_page')

    search_school = request.GET.get('search_school')
    search_year = request.GET.get('search_year')
    search_grade = request.GET.get('search_grade')

    try:
        project_page = int(project_page)
    except:
        project_page = 1

    q1 = (search_year and Q(year=search_year)) or None
    q2 = (search_school and Q(school=search_school)) or None
    q3 = (search_grade and Q(project_grade=search_grade)) or None
    qset = filter(lambda x: x != None, [q1, q2, q3])
    if qset :
        qset = reduce(lambda x, y: x & y, qset)
        project_list = ProjectSingle.objects.filter(qset)
    else:
        project_list = ProjectSingle.objects.all()

    context = getContext(project_list, project_page, 'project', 8)
    if project_page != context["project_page"].number:
        raise Http404
    for project in context["project_list"]:
        imgs = project.uploadedfiles_set.filter( \
            Q(file_obj__iendswith="jpg") | \
            Q(file_obj__iendswith="png") )
        project.img = (imgs.count() and convert2media_url(imgs[0].file_obj.url)) or \
            DEFAULT_IMG_URL

    school_list = SchoolDict.objects.all()
    grade_list = ProjectGrade.objects.all()

    context["schools"] = school_list
    context["grades"] = grade_list

    context["search_school"] = search_school
    context["search_year"] = search_year
    context["search_grade"] = search_grade

    return render(request, 'introduction/show.html', context)
