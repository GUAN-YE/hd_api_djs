#coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: urls.py
@time: 2017/10/21 11:39
"""

from django.conf.urls import url
from apps.gift_active import views

# 金豆商城活动
urlpatterns = [
    url(r'^status$', views.p_status),                           # 用户是否参加过活动
    url(r'^join$', views.p_join),                           # 参加活动
]