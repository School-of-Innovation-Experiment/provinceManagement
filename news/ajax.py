from django.utils import simplejson
from django.template.loader import render_to_string
from django.template import RequestContext
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from django.shortcuts import render_to_response
from news.models import News
from news.views import getContext

@dajaxice_register(method='GET')
def news_turn_page(request, news_page, news_search):
    news_page = (news_page.isdigit() and int(news_page)) or 1
    news_list = (news_search and \
                     News.objects.filter(news_title__icontains=news_search)) \
                     or News.objects.order_by('-news_date')
    # news_page = request.GET.get('news_page')
    context = getContext(news_list, news_page, 'news')
    # return render_to_response(request, 'home/ajax/_news_list.html', context)
    html = render_to_string('home/ajax/_news_list.html',
                            context,
                            context_instance=RequestContext(request))
    return simplejson.dumps({'html':html})

@dajaxice_register(method='GET')
def docs_turn_page(request, docs_page, docs_search):
    docs_page = (docs_page.isdigit() and int(docs_page)) or 1
    docs_list = (docs_search and \
                     News.objects.filter(news_document__icontains=docs_search)) \
                     or News.objects.exclude(news_document=u'')
    context = getContext(docs_list, docs_page, 'docs')
    html = render_to_string('home/ajax/_docs_list.html',
                            context,
                            context_instance=RequestContext(request))
    return simplejson.dumps({'html':html})

@dajaxice_register(method='GET')
def docs_search_page(request, docs_input):
    docs_list = News.objects.filter(news_document__icontains=docs_input)
    context = getContext(docs_list, 1, 'docs')
    html = render_to_string('home/ajax/_docs_list.html',
                            context,
                            context_instance=RequestContext(request))
    return simplejson.dumps({'html':html})

@dajaxice_register(method='GET')
def news_search_page(request, news_input):
    news_list = News.objects.filter(news_title__icontains=news_input)
    context = getContext(news_list, 1, 'news')
    html = render_to_string('home/ajax/_news_list.html',
                            context,
                            context_instance=RequestContext(request))
    return simplejson.dumps({'html':html})