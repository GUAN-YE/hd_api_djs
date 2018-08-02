#coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: urls.py
@time: 2017/9/5 14:20
"""

from django.conf.urls import url
from apps.yy_normal import views

# 英语常态活动s1赛季
urlpatterns = [
    url(r'^rank$', views.user_rank),                           # 用户排名
    url(r'^index$', views.index),                              # 首页
    url(r'^tasks$', views.tasks),                              # 每日任务
]