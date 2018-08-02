# coding:utf-8
"""
教师发作业领金币活动
2018年3月21日-2018年4月2号
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'status$', views.get_status),  #
    url(r'get/coin$', views.get_coin),  # 剩余金币数量
]
