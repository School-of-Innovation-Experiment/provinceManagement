from django.utils import simplejson
from django.template.loader import render_to_string
from django.template import RequestContext
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from django.shortcuts import render_to_response
from backend.utility import getContext, convert2media_url
from school.models import ProjectSingle
from django.db.models import Q
from const.__init__ import DEFAULT_IMG_URL

@dajaxice_register(method='GET')
def project_turn_page(request, project_page, project_search):
    try:
        project_page = int(project_page)
    except:
        project_page = 1
    project_list = (project_search and \
                     ProjectSingle.objects.filter(title__icontains=project_search)) \
                     or ProjectSingle.objects.all()
    for project in project_list:
        imgs = project.uploadedfiles_set.filter( \
            Q(file_obj__iendswith="jpg") | \
            Q(file_obj__iendswith="png") )
        project.img = (imgs.count() and convert2media_url(imgs[0].file_obj.url)) or \
            DEFAULT_IMG_URL
    context = getContext(project_list, project_page, 'project')
    html = render_to_string('introduction/ajax/_show_list.html',
                            context,
                            context_instance=RequestContext(request))
    return simplejson.dumps({'html':html})
