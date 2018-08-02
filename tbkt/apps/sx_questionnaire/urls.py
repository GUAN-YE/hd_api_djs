# coding:utf-8
from django.conf.urls import url
from . import view

urlpatterns = [
    url(r'^submit$', view.submit),  # 问卷调查提交
    url(r'^result$', view.result),  # 问卷调查结果页
    url(r'^status$', view.status),  # 查看是否已做
]

urlpatterns += [
    url(r'^download/detail$', view.detail),  # 问卷调查详情
    url(r'^download/detail_all$', view.detail_all),  # 问卷调查详情

]
