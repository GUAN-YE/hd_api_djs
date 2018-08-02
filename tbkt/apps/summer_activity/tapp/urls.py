# coding=utf-8

from django.conf.urls import url, patterns
from apps.summer_activity.tapp import views

urlpatterns = patterns('',
                       url(r'^yuyue', views.yuyue),  # 预约
                       url(r'^share', views.share),  # 分享积分
                       url(r'^ranking', views.ranking),  # 排行
                       url(r'^see_score', views.score),  # 积分详情
                       url(r'^award', views.award_name),  # 获奖名单
                       url(r'^send_homework', views.send_homework),  # 获奖名单
                       url(r'^send_open', views.send_open),  # 获奖名单
                       )
