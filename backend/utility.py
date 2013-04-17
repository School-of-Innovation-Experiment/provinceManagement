# coding: UTF-8
'''
Created on 2013-03-27

@author: tianwei

Desc: some tool code snniper
'''
import uuid
from settings import STATIC_URL, MEDIA_URL
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from const.__init__ import PAGE_ELEMENTS
def search_tuple(src, target):
    """
    search value in tuple
    """
    if src is None:
        return None

    for item in src:
        if item[0] == target:
            return item[1]

    return None


def convert2media_url(raw_url):
    """
    convert filefield's default url-string to media url
    example:
    convert:http://127.0.0.1:8000/media/tmp/process_file/2013/04/01/bike.jpg
    to:/static/tmp/process_file/2013....
    """
    return raw_url
    #return STATIC_URL + raw_url[raw_url.find(MEDIA_URL)+len(MEDIA_URL):]

def getContext(contentList, page=1, name="context", page_elems=PAGE_ELEMENTS):
    """
    分页：
    contenList:分页内容,集合类型
    page:页码
    name:根据name获得对应的上下文名，分别为:
        #{name}_page:Page对象,默认"context_page"
        #{name}_list:第page页元素集合,默认"context_list"
    """
    paginator = Paginator(contentList, page_elems)
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

def make_uuid():
    """
    make uuid
    """
    return str(uuid.uuid4())
