# coding: UTF-8
'''
Created on 2013-03-17

@author: Tianwei

Desc: news view with Tinymce
'''

from django.shortcuts import render

from news.models import News
from django.template import Context, loader
from django.http import HttpResponse
import datetime

def get_news_content(news_id = None):
    if news_id: #get news which id equal to news_id
        news_content = News.objects.get(id = news_id)
    else: # get latest news
        news_content = (News.objects.count() and News.objects.order_by('news_datetime')[0]) or None
    context = {
        'news_content' : news_content,
        }
    return context

def index(request):
    the_latest_news = get_news_content()['news_content']
    the_latest_news = the_latest_news or News(id =  -1, news_title = 'haha', news_content = 'yeshi haha', news_datetime = datetime.datetime.now)
    context = Context({
            'the_latest_news': the_latest_news,
            })
    return render(request, 'home/index.html', context)

def read_news(request, news_id):
    context = Context({
            'news': get_news_content(news_id)['news_content']
            })
    return render(request, 'home/news-content.html', context)
