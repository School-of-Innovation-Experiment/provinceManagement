# coding: UTF-8
'''
Created on 2013-03-17

@author: Tianwei

Desc: news view with Tinymce
'''
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, render_to_response

from news.models import News
from django.template import Context, loader
from django.http import HttpResponse
import datetime

def get_news_content(news_id = None):
    if news_id: #get news which id equal to news_id
        news_content = News.objects.get(id = news_id)
    else: # get latest news
        news_content = (News.objects.count() and News.objects.order_by('-news_date')[0]) or None
    context = {
        'news_content' : news_content,
        }
    return context

def index(request):
    the_latest_news = get_news_content()['news_content']
    the_latest_news = the_latest_news or News(id =  -1, news_title = 'haha', news_content = 'yeshi haha', news_date = datetime.datetime.today)
    context = Context({
            'the_latest_news': the_latest_news,
            })
    return render(request, 'home/index.html', context)

def read_news(request, news_id):
    context = Context({
            'news': get_news_content(news_id)['news_content']
            })
    return render(request, 'home/news-content.html', context)

PAGE_NEWS = 20
def list_news(request):
    news_list = News.objects.all()
    paginator = Paginator(news_list, PAGE_NEWS)

    page = request.GET.get('page')
    try:
        news_page = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        news_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        news_page = paginator.page(paginator.num_pages)
    news_list = list(news_page.object_list)
    for news_index in xrange(len(news_list)):
        news_list[news_index].index = news_index + 1 # .__dict__.update(dict)
    return render(request, 'home/news-list.html', \
                  Context({"news_page": news_page,
                           "news_list": news_list,}))
