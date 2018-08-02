# coding: utf-8
from django.conf.urls import url
from apps.yw_reading import views

urlpatterns = [
    url(r'^set_recording$', views.set_recording),            # 上传录音（学生端）
    url(r'^get_recording$', views.get_recording),            # 获取录音（学生端）
    url(r'^set_message$', views.set_message),            # 上传留言（学生端）
    url(r'^get_message$', views.get_message),            # 获取留言（学生端）
    url(r'^get_join_status$', views.get_join_status),            # 是否能参加活动（教师端）
    url(r'^index$', views.index),            # 活动首页（教师端）
    url(r'^get_paper$', views.get_paper),            # [教师端]获取当前年级下的试卷
    url(r'^view_paper$', views.view_paper),            # [教师端]预览试卷
    url(r'^send_sms$', views.send_sms),             #[教师端]发送试卷短信\
    url(r'^get_coin$', views.get_coin),            # 用户排名
]
