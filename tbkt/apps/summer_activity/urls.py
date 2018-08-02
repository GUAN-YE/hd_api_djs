# coding=utf-8
from django.conf.urls import include, url, patterns


urlpatterns = patterns(
    url(r'sapp/', include('apps.summer_activity.sapp.urls')),  # 学生端
    url(r'tapp/', include('apps.summer_activity.tapp.urls')),  # 教师端

)