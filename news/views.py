#!/usr/local/bin/python3
# coding: UTF-8
# Author: David
# Email: youchen.du@gmail.com
# Created: 2016-12-21 09:05
# Last modified: 2016-12-21 09:05
# Filename: views.py
# Description:
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
from settings import IS_DLUT_SCHOOL, IS_MINZU_SCHOOL
from backend.utility import getContext, convert2media_url
import datetime, os
from settings import IS_DLUT_SCHOOL, IS_MINZU_SCHOOL, STATIC_URL, MEDIA_URL
from adminStaff.models import HomePagePic
from const import *
from const.models import *

def get_news(news_id = None):
    if news_id: #get news which id equal to news_id
        try:
            news_content = News.objects.get(id = news_id)
        except:
            raise Http404
    else: # get latest news
        news_content = (News.objects.count() and News.objects.order_by('-news_date')[0]) or None
    return news_content


def index_context(request):
    '''
    for index_new
    '''
    news_announcement = News.objects.filter(news_category__category=NEWS_CATEGORY_ANNOUNCEMENT).order_by('-news_date')
    news_policy = News.objects.filter(news_category__category=NEWS_CATEGORY_POLICY).order_by('-news_date')
    news_outstanding = News.objects.filter(news_category__category=NEWS_CATEGORY_OUTSTANDING).order_by('-news_date')
    news_others = News.objects.filter(news_category__category=NEWS_CATEGORY_OTHERS).order_by('-news_date')
    context = getContext(news_announcement, 1, "news_announcement")
    context.update(getContext(news_policy, 1, "news_policy"))
    context.update(getContext(news_outstanding, 1, "news_outstanding"))
    context.update(getContext(news_others, 1, "news_others"))

    context.update(
        getContext(
            News.objects.exclude(news_document=u'').order_by('-news_date'), \
                1, 'news_docs'))
    return context
    # return render(request, 'home/index.html', context)

def index_new(request):
    # names = getSchoolsPic()
    # context = {"schools_name_list": names}
    context = {}
    def convert_url(raw_url):
        return MEDIA_URL + raw_url[raw_url.find(MEDIA_URL)+len(MEDIA_URL):]
    homepage_pic = HomePagePic.objects.all()
    flag = True
    for pic in homepage_pic:
        pic.url = convert_url(pic.pic_obj.url)
        print pic.url
        if flag:
            pic.active = True
            flag = False
        else: pic.active = False
    context.update({
        'homepage_pic': homepage_pic,
    })
    context.update(
        getContext(
            News.objects.exclude(news_document=u'')[:5], \
                1, 'homepage_docs'))
    context.update(index_context(request))
    news_cate = {}
    news_cate["news_category_announcement"] = NEWS_CATEGORY_ANNOUNCEMENT
    news_cate["news_category_policy"] = NEWS_CATEGORY_POLICY
    news_cate["news_category_others"] = NEWS_CATEGORY_OTHERS
    news_cate["news_category_outstanding"] = NEWS_CATEGORY_OUTSTANDING
    news_cate["news_category_documents"] = NEWS_CATEGORY_DOCUMENTS
    context.update(news_cate)
    return render(request, "home/new-homepage.html", context)

def read_news(request, news_id):
    news = get_news(news_id)
    news_cate = news.news_category
    context = Context({
        'news': news,
        'news_cate':news_cate,
        'IS_DLUT_SCHOOL':IS_DLUT_SCHOOL,
        'IS_MINZU_SCHOOL':IS_MINZU_SCHOOL,
    })

    html = 'home/news-content.html' if IS_MINZU_SCHOOL else 'home/news-content-new.html'
    return render(request, html, context)

def list_news_by_cate(request, news_cate):
    try:
        if news_cate == NEWS_CATEGORY_DOCUMENTS:
            news_list = News.objects.exclude(news_document=u'').order_by('-news_date')
        else:
            news_list = News.objects.filter(news_category__category=news_cate).order_by('-news_date')
            news_cate = NewsCategory.objects.get(category=news_cate)
    except:
        raise Http404
    news_page = request.GET.get('news_page')
    context = getContext(news_list, news_page, 'news')
    if not news_cate == NEWS_CATEGORY_DOCUMENTS:
        context["news_cate"] = news_cate
        context['%s_active' % news_cate.category] = 'active'
    return render(request, 'home/news-list-by-cate.html', \
                  Context(context))

def index(request):
    if IS_DLUT_SCHOOL: return index_new(request)
    def convert_url(raw_url):
        return STATIC_URL + raw_url[raw_url.find(MEDIA_URL)+len(MEDIA_URL):]
    the_latest_news = get_news()
    the_latest_news = the_latest_news or News(id =  -1, news_title = '...', news_content = '无最新内容', news_date = datetime.datetime.today)
    homepage_pic = HomePagePic.objects.all()
    flag = True
    for pic in homepage_pic:
        pic.url = convert_url(pic.pic_obj.url)
        print pic.url
        if flag:
            pic.active = True
            flag = False
        else: pic.active = False
    context = {
        'the_latest_news': the_latest_news,
        'IS_DLUT_SCHOOL': IS_DLUT_SCHOOL,
        'IS_MINZU_SCHOOL': IS_MINZU_SCHOOL,
        'homepage_pic': homepage_pic,
    }
    context.update(
        getContext(
            News.objects.exclude(news_document=u'')[:5], \
                1, 'homepage_docs'))
    news_count = News.objects.count()
    if news_count >= 5:
        news_list = News.objects.order_by('-news_date')[:5]
    else:
        news_list = News.objects.order_by('-news_date')[:news_count]
    context.update(
        getContext(news_list, \
                   1, 'homepage_news'))
    return render(request, 'home/index.html', context)

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
