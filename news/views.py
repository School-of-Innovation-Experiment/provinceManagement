# coding: UTF-8
'''
Created on 2013-03-17

@author: Tianwei

Desc: news view with Tinymce
'''
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render #, render_to_response

from news.models import News
from django.template import Context #, loader
from django.http import HttpResponse, Http404
from backend.utility import getContext, getSchoolsPic
import datetime, os
from const import *

def get_news(news_id = None):
    if news_id: #get news which id equal to news_id
        try:
            news_content = News.objects.get(id = news_id)
        except:
            raise Http404
    else: # get latest news
        news_content = (News.objects.count() and News.objects.order_by('-news_date')[0]) or None
    return news_content

def index(request):
    news_announcement = News.objects.filter(news_category__category=NEWS_CATEGORY_ANNOUNCEMENT)
    news_policy = News.objects.filter(news_category__category=NEWS_CATEGORY_POLICY)
    news_outstanding = News.objects.filter(news_category__category=NEWS_CATEGORY_OUTSTANDING)
    news_others = News.objects.filter(news_category__category=NEWS_CATEGORY_OTHERS)
    context = getContext(news_announcement, 1, "news_announcement")
    context.update(getContext(news_policy, 1, "news_policy"))
    context.update(getContext(news_outstanding, 1, "news_outstanding"))
    context.update(getContext(news_others, 1, "news_others"))
    return render(request, 'home/index.html', context)


def index_new(request):
    names = getSchoolsPic()
    context = {"schools_name_list": names}
    return render(request, "home/new-homepage.html", context)


def read_news(request, news_id):
    context = Context({
            'news': get_news(news_id),
            })
    return render(request, 'home/news-content.html', context)

def list_news(request):
    news_list = News.objects.order_by('-news_date')
    news_page = request.GET.get('news_page')

    docs_list = news_list.exclude(news_document=u'')
    docs_page = request.GET.get('docs_page')

    context = getContext(news_list, news_page, 'news')
    context.update(getContext(docs_list, docs_page, 'docs'))
    return render(request, 'home/news-list.html', \
                  Context(context))

BUF_SIZE = 262144
def download_news_doc(request, news_id):
    news_doc_name = get_news(news_id).news_document.path
    def readFile(fn, buf_size=BUF_SIZE):
        f = open(fn, "rb")
        while True:
            _c = f.read(buf_size)
            if _c:
                yield _c
            else:
                break
        f.close()
    response = HttpResponse(readFile(news_doc_name), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(news_doc_name).encode("UTF-8") #NOTICE: the file must be unicode
    return response
