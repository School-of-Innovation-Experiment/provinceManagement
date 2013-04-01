# coding: UTF-8
'''
Created on 2013-03-27

@author: tianwei

Desc: some tool code snniper
'''
from settings import STATIC_URL, MEDIA_URL

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
    return STATIC_URL + raw_url[raw_url.find(MEDIA_URL)+len(MEDIA_URL):]
