# coding: utf-8
from django.conf.urls import url
from apps.psd_xcq import views

urlpatterns = [
    url(r'^share$', views.pds_share),            # 分享活动
    url(r'^index', views.index),            # 活动首页
    url(r'^user_rank', views.user_rank),            # 用户排名
]
