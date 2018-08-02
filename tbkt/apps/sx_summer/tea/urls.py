# coding=utf-8

from django.conf.urls import include, url, patterns
from . import post

urlpatterns = patterns('',
                       url(r'^rank$', post.p_rank),  # 积分排行
                       url(r'^rank_unit', post.p_unit_rank),  # 班级内学生排行

                       url(r'^user_rank$', post.get_user_info),  # 用户名次分数
                       url(r'^detail$', post.p_score_detail),  # 分数详情

                       url(r'^send_sms$', post.p_send_sms),
                       url(r'^send_open$', post.p_send_open),

                       url(r'^award', post.p_award),

                       )
