#coding: utf-8
"""
简单封装了http接口的远程调用

用法:
api = Hub(request)
api.com.get('/account/profile')
"""
import logging

import requests
from django.conf import settings
from libs.utils import Struct


class Proxy:
    def __init__(self, urlroot, headers=None, cookies=None):
        """
        :param urlroot: 平台接口根路径(比如 http://mapi.m.jxtbkt.com)
        :param headers: 自定义头部字典
        :param cookies: 自定义cookie字典
        """
        self.urlroot = urlroot
        self.headers = headers or {}
        self.cookies = cookies or {}

    def post(self, path, data=None, json=None, **kwargs):
        """Sends a POST request.

        :param path: 接口路径(比如 "/account/profile")
        :param data: (optional) Dictionary, bytes, or file-like object to send in the body.
        :param json: (optional) json data to send in the body.
        :param kwargs: 可选参数, 比如timeout, cookies, headers...
        :return: 成功返回同步课堂ajax格式的字典, 比如:
            {
                "message": "",
                "next": "",
                "data": {},
                "response": "ok",
                "error": ""
            }
            失败返回None
        """
        url = self.urlroot + path
        if self.headers:
            if 'headers' in kwargs:
                headers = self.headers.copy()
                headers.update(kwargs['headers'])
            else:
                headers = self.headers
            kwargs['headers'] = headers
        if self.cookies:
            if 'cookies' in kwargs:
                cookies = self.cookies.copy()
                cookies.update(kwargs['cookies'])
            else:
                cookies = self.cookies
            kwargs['cookies'] = cookies
        r = requests.post(url, data, json, **kwargs)
        if r.status_code != 200:
            logging.warning('tbktapi.post %s' % r.status_code)
            return
        return Struct(r.json())

    def get(self, path, params=None, **kwargs):
        """Sends a GET request.

        :param path: 接口路径(比如 "/account/profile")
        :param params: (optional) Dictionary or bytes to be sent in the query string.
        :param json: (optional) json data to send in the body.
        :param kwargs: 可选参数, 比如timeout, cookies, headers...
        :return: 成功返回同步课堂ajax格式的字典, 比如:
            {
                "message": "",
                "next": "",
                "data": {},
                "response": "ok",
                "error": ""
            }
        """
        url = self.urlroot + path
        if self.headers:
            if 'headers' in kwargs:
                headers = self.headers.copy()
                headers.update(kwargs['headers'])
            else:
                headers = self.headers
            kwargs['headers'] = headers
        if self.cookies:
            if 'cookies' in kwargs:
                cookies = self.cookies.copy()
                cookies.update(kwargs['cookies'])
            else:
                cookies = self.cookies
            kwargs['cookies'] = cookies
        r = requests.get(url, params, **kwargs)
        assert r.status_code == 200, r.status_code
        return Struct(r.json())


class Hub:
    def __init__(self, request=None, headers=None, cookies=None):
        """
        :param request: django.http.HttpRequest对象
            如果request不为空, 意味着每次调用都携带登录状态
        :param headers: 自定义公共头部字典
        :param cookies: 自定义公共cookie字典
        """
        self.headers = headers or {}
        self.cookies = cookies or {}
        if request:
            token = request.QUERY.get(settings.SESSION_COOKIE_NAME) or request.META.get('HTTP_TBKT_TOKEN') or request.COOKIES.get('tbkt_token')
            self.cookies['tbkt_token'] = token


    def __getattr__(self, alias):
        """
        :param alias: 接口服务器别名
            公共接口: com
            银行接口: bank
        :return: RPC代理对象
        """
        assert alias in settings.API_URLROOT, alias
        urlroot = settings.API_URLROOT[alias]
        if not settings.DEBUG:
            self.headers['Host'] = urlroot[urlroot.find("//") + 2:]
            self.headers['Platform'] = 'hd_api_dj'
            urlroot = settings.TBKT_HOST
        return Proxy(urlroot, self.headers, self.cookies)
