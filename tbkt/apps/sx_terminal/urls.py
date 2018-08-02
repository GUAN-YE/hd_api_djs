# coding: utf-8
from django.conf.urls import url
from apps.sx_terminal import view, send_task

# 数学期末活动
urlpatterns = [
    url(r'^paper/list$', view.hd_book_papers),                # 试卷列表
    url(r'^paper/send/task$', send_task.p_give_web),          # 发作业
]