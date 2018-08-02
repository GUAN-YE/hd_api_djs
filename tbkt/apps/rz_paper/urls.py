#coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: urls.py
@time: 2017/12/20 17:32
"""


from django.conf.urls import url
from apps.rz_paper import views

# 金豆商城活动
urlpatterns = [
    url(r'^status$', views.p_status),                           # 试卷完成状态
    url(r'^do_paper$', views.do_paper),                         # 做英语试卷
    url(r'^submit_paper$', views.submit_paper),                 # 英语试卷提交
    url(r'^paper_result$', views.paper_result),                 # 英语试卷结果
    url(r'^paper_result_detail$', views.paper_result_detail),   # 英语试卷详细结果
]