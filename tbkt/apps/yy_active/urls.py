#coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: urls.py
@time: 2017/9/5 14:20
"""

from django.conf.urls import url
from apps.yy_active import views

# 英语常态活动s1赛季
urlpatterns = [
    url(r'add_score$', views.add_score),                        # 英语活动加减分
    url(r'get_question$', views.get_question)                   # 获取问题详情
]