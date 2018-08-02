#coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: views.py
@time: 2018/1/31 14:17
"""

from libs.utils import ajax
def index(request):
    return ajax.jsonp_fail(request, message=u'no path, what are you doing!')