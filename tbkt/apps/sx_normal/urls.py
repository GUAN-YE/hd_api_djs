# coding:utf-8
"""
2017数学常态活动
映射路径
"""
from django.conf.urls import url
from stu import views as stu_views
import views as com_views

# 学生
urlpatterns = [
    url(r'stu/sign$', stu_views.r_sign),                     # 签到
    url(r'stu/share$', stu_views.r_share),                   # 分享
]

# 活动公用方法
urlpatterns += [
    url(r'^com/info$', com_views.r_info),                   # 用户积分详情
    url(r'score/detail$', com_views.r_score_detail),   # 用户积分信息
    url(r'class/ranks$', com_views.r_class_rank),      # 积分排名
    url(r'award/display$', com_views.r_award_info),    # 奖品静态展示

    # 河南活动未下线，三门峡活动暂不用
    url(r'award/winner$', com_views.r_award_winner),   # 奖品静态展示
    url(r'score/ranks$', com_views.r_score_rank),  # 积分排名

]