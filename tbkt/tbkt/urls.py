# coding=utf-8
"""tbkt URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.conf import settings
from tbkt import views

urlpatterns = [
    url(r'^apidoc/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.APIDOC_DIR}),  # 接口文档
]

urlpatterns += [
    url(r'huodong/', include('apps.urls')),
    url(r'^system/', include('apps.system.urls')),
]

urlpatterns += [
    url(r'^$', views.index),

]
