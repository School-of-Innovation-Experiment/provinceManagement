# Create your views here.
#
from school.models import *
from django.db.models import Q
from django.shortcuts import render
from backend.utility import convert2media_url
Q(question__startswith='What')

DEFAULT_IMG_URL = ""
def show_index(request):
    projects = ProjectSingle.objects.all()
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
