# coding=utf-8
from django.conf.urls import url
from apps.summer_activity.sapp import views



# 2018暑假活动
urlpatterns = [
    url(r'^yw_index$', views.yw_index),          # 语文暑假活动首页
    url(r'^service_time$', views.service_time),          # 返回服务器时间
    url(r'^invite_stu$', views.invite_stu),          # 邀请学生界面
    url(r'^do_invite$', views.do_invite),          # 邀请学生
    url(r'^get_ask_message$', views.get_ask_message),  # 我的碎片消息----消息
    url(r'^get_debris_message$', views.get_debris_message),  # 我的碎片消息----碎片记录
    url(r'^get_unit_student$', views.get_unit_student),  # 赠送和索取获取班级下所有学生
    url(r'^give_debris$', views.give_debris),  # 赠送碎片
    url(r'^ask_for_debris$', views.ask_for_debris),  # 索取碎片
    url(r'^ask_for_debris$', views.do_invite),  # 邀请学生
    url(r'^open_box$', views.open_box),  # 开宝箱
    url(r'^get_rank$', views.get_rank),  # 获取排行榜
]