# -*- coding: utf-8 -*-
__author__ = 'Sam'
__date__ = '2018/10/24 14:16'
import hashlib


def get_md5(url):
    '''
    获取md5
    '''

    #判断传进来的字符是否是unicode,转换为utf8
    if isinstance(url, str):
        url = url.encode("utf-8")

    m = hashlib.md5()
    m.update(url)

    return m.hexdigest()