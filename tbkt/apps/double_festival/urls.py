# coding:utf-8
"""
@author: lvyang
@time: 2017/12/14
"""
from django.conf.urls import url
from . import views

urlpatterns = [
    url('^info$', views.p_info),  # 用户信息
    url('^prop/news$', views.p_news),  # 道具 详情
    url('^prop/demand$', views.p_demand),  # 索要道具
    url('^prop/give$', views.p_give),  # 赠送道具
    url('^prop/openBox$', views.p_open),  # 打开宝箱获得奖品
    url('^prop/gain$', views.p_gain),  # 完成作业获得道具

    url('^stu/class_stu$', views.p_class_stu),  # 学生
    url('^stu/verify$', views.p_verify),  # 确认用户为邀请用户
    url('^stu/open_invite', views.p_open_subject),  # 开通接口

]
