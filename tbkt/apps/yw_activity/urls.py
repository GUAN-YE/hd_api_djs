# coding=utf-8

from django.conf.urls import include, url, patterns
urlpatterns = patterns('',
    url(r'^s/', include('apps.yw_activity.stu.urls')),             # 学生活动相关
    url(r'^t/', include('apps.yw_activity.tea.urls')),             # 教师活动相关
)
