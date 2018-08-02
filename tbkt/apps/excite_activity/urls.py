#coding=utf-8

"""
@varsion: ??
@author: 张嘉麒
@file: urls.py
@time: 2017/12/12 17:30
"""

from django.conf.urls import url
from apps.excite_activity import views

# 激励教师抽奖活动
urlpatterns = [
    url(r'^ticket_num$', views.activity_num),                         # 用户抽奖券个数
    url(r'^coin_join_actitvity$', views.coin_join_activity),       # 用户使用金币参与抽奖
    url(r'^ticket_join_actitvity$', views.ticket_join_activity),     # 用户使用奖券参与抽奖
    url(r'^winning_list$', views.get_winning_list),                   # 获奖教师名单
    url(r'^activity_entrance$', views.get_activity_entrance),         # 活动入口
    url(r'^activity$', views.get_activity),                            # 获取活动详细信息
    url(r'^invite_teacher$', views.invite_teacher),                   # 邀请老师界面
    url(r'^invite_stu$', views.invite_stu),                            # 邀请学生接口
    url(r'^activity_list$', views.get_activity_list),                  # 获取正在进行的活动列表
    url(r'^submit_address$', views.submit_address),                  # 获取正在进行的活动列表
]