# coding: utf-8
from django.conf.urls import url
from apps.end_term import views

urlpatterns = [
    url(r'^book/select$', views.p_list),          # 获取活动教材下的教材

]