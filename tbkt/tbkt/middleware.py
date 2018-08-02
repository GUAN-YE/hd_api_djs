#!/usr/bin/env python
# coding=utf-8
import logging, traceback
import simplejson as json
import time

from com.com_cache import cache
from libs.utils.common import casts, loads

from libs.utils import auth

from django.http import QueryDict, HttpRequest, HttpResponse
from com import com_sys, com_user
from django.conf import settings
from libs.utils.ajax import ajax_fail

SESSION_KEY = '_auth_user_id'

log = logging.getLogger('common.middleware')


def get_userid(request):
    """
    从cookie中获取user_id, 失败返回None
    """
    if not hasattr(request, '_userid'):
        token = request.QUERY.get(settings.SESSION_COOKIE_NAME) or request.META.get('HTTP_TBKT_TOKEN') or request.COOKIES.get(settings.SESSION_COOKIE_NAME)
        if token and cache.disable_token.get(token):
            return
        r = auth.decode_token(token)
        request._userid = r['user_id'] if r else None
        request._expire = expire = r['expire'] if r else None
        # 如果token过期时间到一半就续签
        if expire and time.time() >= expire - settings.SESSION_COOKIE_AGE / 2:
            request._newtoken = auth.create_token(request._userid)
    return request._userid


def get_user(request):
    """
    调取公共接口 获取用户信息
    """
    if not hasattr(request, '_user'):
        user_id = get_userid(request)
        request._user = com_user.get_user(request, user_id) if user_id else None
    return request._user

# 给request.GET, request.POST, request.QUERY注入新方法
QueryDict.casts = casts

HttpRequest.user_id = property(get_userid)
HttpRequest.user = property(get_user)
HttpRequest.loads = loads


class AuthenticationMiddleware(object):
    def process_request(self, request):
        try:
            return self._process_request(request)
        except:
            exc = traceback.format_exc()
            log.error(exc)
            if settings.DEBUG:
                print exc

    def cross_domain(self, request, response=None):
        """
        添加跨域头
        """
        origin = request.META.get('HTTP_ORIGIN', '*')
        if request.method == 'OPTIONS' and not response:
            response = HttpResponse()
        if not response:
            return
        response['Access-Control-Allow-Origin'] = origin
        response['Access-Control-Allow-Methods'] = 'GET,POST'
        response['Access-Control-Allow-Credentials'] = 'true'
        response['Access-Control-Allow-Headers'] = 'x-requested-with,content-type,Tbkt-Token,App-Type'
        response['Access-Control-Max-Age'] = '1728000'
        return response

    def _process_request(self, request):

        # REQUEST过期, 使用QUERY代替
        query = request.GET.copy()
        query.update(request.POST)
        # 把body参数合并到QUERY
        try:
            body = json.loads(request.body)
            query.update(body)
        except:
            pass
        request.QUERY = query

        r = self.cross_domain(request)
        if r:
            return r

        # 检查新版本
        app_type = request.META.get('HTTP_APP_TYPE')
        if app_type:
            request._app_version = com_sys.get_app_version(app_type)

    def process_response(self, request, response):
        # 更新token
        if getattr(request, '_newtoken', None):
            auth.login_response(response, request._newtoken)
        # 添加跨域头
        self.cross_domain(request, response)
        # 查询新版本
        if getattr(request, '_app_version', None):
            response['App-Version'] = json.dumps(request._app_version)
        return response


    def process_exception(self, request, exception):
        """
        功能说明:view函数抛出异常处理
        -------------------------------
        修改人     修改时间
        --------------------------------
        徐威      2013-07-17
        """
        path = str(request.path)

        # 如果请求的路径为 js css 文件 不处理
        if path.startswith('/site_media/'):
            return None
        if path.startswith('/media/'):
            return None
        # 如果请求的路径为 js css 文件 不处理
        if path.startswith('/theme_media/'):
            return None
        # 如果请求的路径为 js css 文件 不处理
        if path.startswith('/upload_media/'):
            return None

        exc = traceback.format_exc()
        if settings.DEBUG:
            print exc
        log.error(exc)

        return ajax_fail(error="500", message=u"抱歉，服务器开小差了，请联系客服12556185")
