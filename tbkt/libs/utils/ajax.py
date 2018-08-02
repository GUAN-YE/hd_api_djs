# coding: utf-8
import json as simplejson
from json.encoder import JSONEncoder
import datetime

from django.conf import settings
from django.http import HttpResponse


class XJSONEncoder(JSONEncoder):
    """
    JSON扩展: 支持datetime和date类型
    """
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')
        else:
            return JSONEncoder.default(self, o)


class SimpleAjaxException(Exception):
    pass


def ajax_data(response_code, data=None, error=None, next=None, message=None):
    """if the response_code is true, then the data is set in 'data',
    if the response_code is false, then the data is set in 'error'
    """
    r = dict(response='ok', data=data, error='', next='', message='')
    if response_code is True or response_code.lower() in ('ok', 'yes', 'true'):
        r['response'] = 'ok'
    else:
        r['response'] = 'fail'
    if data is not None:
        r['data'] = data
    if error:
        r['error'] = error
    if next:
        r['next'] = next
    if message:
        r['message'] = message
    return r


def ajax_ok_data(data='', next=None, message=None):
    return ajax_data('ok', data=data, next=next, message=message)


def ajax_fail_data(error='', data=None, next=None, message=None):
    return ajax_data('fail', data=data, error=error, next=next, message=message)


def json_response(data):
    r = HttpResponse(simplejson.dumps(data, cls=XJSONEncoder, encoding='utf-8'))
    r['Content-Type'] = 'application/json'
    return r


def ajax_ok(data='', next=None, message=None):
    """
    return a success response
    """
    return json_response(ajax_ok_data(data, next, message))


def ajax_fail(error='', data=None, next=None, message=None):
    """
    return an error response
    """
    return json_response(ajax_fail_data(error, data, next, message))


def jsonp_response(callback, data):
    data = simplejson.dumps(data, cls=XJSONEncoder, encoding='utf-8')
    data = "%s(%s)" % (callback, data)
    r = HttpResponse(data)
    r['Content-Type'] = 'application/javascript'
    return r


def add_headers(request, body):
    """添加一些底层信息"""
    # 更新token
    if getattr(request, '_newtoken', None):
        body['tbkt_token'] = request._newtoken
    # 查询新版本
    if getattr(request, '_app_version', None):
        body['app_version'] = request._app_version


def jsonp_ok(request, data='', next=None, message=None):
    """
    return a success response
    """
    body = ajax_ok_data(data, next, message)
    add_headers(request, body)

    callback = request.GET.get('callback')
    if callback:
        return jsonp_response(callback, body)
    else:
        return json_response(body)


def jsonp_fail(request, error='', data=None, next=None, message=None):
    """
    return an error response
    """
    body = ajax_fail_data(error, data, next, message)
    add_headers(request, body)

    callback = request.GET.get('callback')
    if callback:
        return jsonp_response(callback, body)
    else:
        r = json_response(body)
        #r.status_code = 400
        return r

