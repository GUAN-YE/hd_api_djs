# coding=utf-8

from django.conf.urls import include, url, patterns
urlpatterns = patterns('',
    url(r'^s/', include('apps.sx_summer.stu.urls')),             # 学生活动相关
    url(r'^t/', include('apps.sx_summer.tea.urls')),             # 教师活动相关
)
