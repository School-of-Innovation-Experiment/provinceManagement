# coding: UTF-8
'''
Created on 2013-03-17

@author: Tianwei

Desc: news view with Tinymce
'''
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, render_to_response

from news.models import News
from const import NEWS_DOCS_NULL
from django.template import Context, loader
from django.http import HttpResponse

import datetime, os

def get_news(news_id = None):
    if news_id: #get news which id equal to news_id
        news_content = News.objects.get(id = news_id)
    else: # get latest news
        news_content = (News.objects.count() and News.objects.order_by('-news_date')[0]) or None
    return news_content

PAGE_NEWS = 20
def getContext(contentList, page, name, page_news=PAGE_NEWS):
    paginator = Paginator(contentList, page_news)
    try:
        _page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        _page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        _page = paginator.page(paginator.num_pages)
    _list = list(_page.object_list)
    for _index in xrange(len(_list)):
        _list[_index].list_index = _index + 1 # .__dict__.update(dict)
    return {'%s_page' % name: _page,
            '%s_list' % name: _list}

def index(request):
    the_latest_news = get_news()
    the_latest_news = the_latest_news or News(id =  -1, news_title = 'haha', news_content = 'yeshi haha', news_date = datetime.datetime.today)
    context = {
            'the_latest_news': the_latest_news,
            }
    context.update(
        getContext(
            News.objects.exclude(news_document=NEWS_DOCS_NULL)[:5], \
                1, 'homepage_docs'))
    return render(request, 'home/index.html', context)

def read_news(request, news_id):
    context = Context({
            'news': get_news(news_id)
            })
    return render(request, 'home/news-content.html', context)

def list_news(request):
    news_list = News.objects.order_by('-news_date')
    news_page = request.GET.get('news_page')

    docs_list = news_list.exclude(news_document=NEWS_DOCS_NULL)
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
