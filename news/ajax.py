from django.utils import simplejson
from django.template.loader import render_to_string
from django.template import RequestContext
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from django.shortcuts import render_to_response
from django.db.models import Q
from news.models import News
from const.models import *
from backend.utility import getContext
import datetime

@dajaxice_register(method='GET')
def news_turn_page(request, news_page, news_search, news_cate):
    try:
        news_page = int(news_page)
    except:
        news_page = 1
    news_list = (news_search and \
                 News.objects.filter(news_category__category=news_cate).filter(news_title__icontains=news_search)) \
        or News.objects.filter(news_category__category=news_cate).order_by('-news_date')
    context = getContext(news_list, news_page, 'news')
    context["news_cate"] = NewsCategory.objects.get(category=news_cate)
    html = render_to_string('home/ajax/_news_list.html',
                            context,
                            context_instance=RequestContext(request))
    return simplejson.dumps({'html':html})

@dajaxice_register(method='GET')
def docs_turn_page(request, docs_page, docs_search):
    try:
        docs_page = int(docs_page)
    except:
        docs_page = 1
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
    docs_list = News.objects.exclude(news_document=u""). \
        filter(Q(news_document__icontains=docs_input)\
                                        & Q(news_date__gte=datetime.date.today()-datetime.timedelta(365)))
    context = getContext(docs_list, 1, 'docs')
    html = render_to_string('home/ajax/_docs_list.html',
                            context,
                            context_instance=RequestContext(request))
    return simplejson.dumps({'html':html})

@dajaxice_register(method='GET')
def news_search_page(request, news_input):
    news_list = News.objects. \
        filter(news_date__gte=datetime.date.today()-datetime.timedelta(365)). \
        filter(Q(news_title__icontains=news_input) |
               Q(news_content__icontains=news_input))
    context = getContext(news_list, 1, 'news')
    html = render_to_string('home/ajax/_news_list.html',
                            context,
                            context_instance=RequestContext(request))
    return simplejson.dumps({'html':html})
