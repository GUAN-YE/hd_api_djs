#coding=utf-8

"""
@varsion: ??
@author: 张嘉麒
@file: urls.py
@time: 2017/12/12 17:30
"""

from django.conf.urls import url
from apps.winter_activity import views

# 寒假活动
urlpatterns = [
    url(r'^activity_entrance$', views.get_activity_entrance),        # 总的活动入口
    url(r'^get_user_match$', views.get_user_match),                  # 成语、诗词pk模块选择对手、获取信息
    url(r'^r_get_poetry$', views.r_get_poetry),                      # 诗词pk模块资源接口
    url(r'^r_get_idiom$', views.r_get_idiom),                        # 成语pk模块资源接口
    url(r'^post_pk_details$', views.post_pk_details),               # 成语、诗词pk模块结果入库
    url(r'^happy_arena$', views.happy_arena),                        # 欢乐竞技场入口
    url(r'^post_happy_pk_details$', views.post_happy_pk_details),    # 欢乐竞技场PK结果入库
    url(r'^heroes$', views.heroes),                                   # 英雄榜
    url(r'^my_things$', views.my_things),                             # 我的很多东西
    url(r'^happy_ranking$', views.happy_ranking),                     # 欢乐榜
    url(r'^invite_get_power$', views.invite_get_power),               # 邀请获得能量接口
    url(r'^use_props$', views.use_props),                             # 使用道具
    url(r'^coin_power_detail$', views.get_user_coin_power_detail),    # 获取积分能量值明细
]