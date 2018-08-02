# coding=utf-8
from django.conf.urls import url
from apps.summer2018 import views


urlpatterns = [
    url(r'^math2/paper/scan$', views.r_math2_paper),     # 初中试卷扫一扫
    url(r'^math2/paper/ask$',  views.r_math2_paper_explain),     # 初中试卷扫一扫
]