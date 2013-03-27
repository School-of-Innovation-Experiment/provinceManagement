# coding: UTF-8
'''
Created on 2013-03-27

@author: tianwei

Desc: some tool code snniper
'''


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
