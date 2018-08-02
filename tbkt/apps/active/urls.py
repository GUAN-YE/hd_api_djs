#coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: urls.py
@time: 2017/9/5 11:30
"""

from django.conf.urls import url
from apps.active import views

# 学生完成练习加分
urlpatterns = [
    url(r'^actives_info$', views.p_actives),                         # 得到用户所有满足条件的活动
    url(r'^active_status$', views.p_active_status),                 # 判断用户是否参加某个活动
    url(r'^add_score$', views.p_update_score),                      # 活动加减分
]