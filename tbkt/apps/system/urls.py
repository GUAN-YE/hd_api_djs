# coding: utf-8
from django.conf.urls import include, url, patterns

urlpatterns = patterns('apps.system.views',
    (r"^version$", "p_version"),  # 检查新版
    (r"^ping$", "p_ping"),  # 检查网站可用性
    (r"^info$", "p_info"),  # 系统信息
    (r"^download/(?P<type>\d+)$", "p_download"),  # APK下载地址
    (r"^bump_version$", "p_bump_version"),  # 版本升级
    (r"^active_info$", "f"),  # 是否开通活动权限
    (r"^blocks$", "p_blocks"),  # 模块展示接口
    (r"^platforms$", "p_platforms"),  # 平台列表接口
)