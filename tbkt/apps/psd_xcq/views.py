#coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: views.py
@time: 2017/3/20 11:16
"""

import datetime, time

from libs.utils.ajax import jsonp_ok, jsonp_fail
from . import common
from libs.utils import db
from libs.utils import ajax_json, ajax_try
from com.com_user import need_login
from com.com_cache import cache

PAGE_COUNT = 10
APP_ID = 37


# SCHOOL = [192037, 1304, 12466, 12465, 12464, 12463, 12467, 12444]
SCHOOL = 180795


@ajax_try({})
@need_login
def pds_share(request):
    """
    @api {post} /huodong/pds_xcq/share [活动]分享活动
    @apiGroup pds_xcq
    @apiParamExample {json} 请求示例
       {}
    @apiSuccessExample {json} 成功返回
       {
        "message": "",
        "next": "",
        "data": "不满足条件",  or   今天已经分享一次了 or 分享成功
        "response": "ok",
        "error": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """

    """
    平顶山新城区用户分享的积分的更新
    :param user:
    :param app_id:
    :return:
    :author: 张帅男
    """
    user = request.user
    if user.school_id != SCHOOL or user.grade_id != 4:
        return ajax_json.jsonp_ok(request, u'不满足条件')
    app_id = APP_ID
    school_id = user.school_id or 0
    school_id = int(school_id)
    nowt = time.time()
    if nowt >= 1525795199:
        return jsonp_ok(request, u'超过了活动时间')

    data = common.pds_share(user, app_id, school_id)

    return jsonp_ok(request, data)


@ajax_try({})
@need_login
def index(request):
    """
    @api {post} /huodong/pds_xcq/index [活动]活动首页
    @apiGroup pds_xcq
    @apiParamExample {json} 请求示例
       {}
    @apiSuccessExample {json} 成功返回
       {
        "message": "",
        "next": "",
        "data": {
            "score": 30,            # 积分
            "rank_no": 3            # 排名
        },
        "response": "ok",
        "error": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """

    """
    平顶山发作业活动首页
    :param request:
    :return:
    :author: 张帅男
    """

    user = request.user
    nowt = time.time()
    if user.school_id != SCHOOL or user.grade_id != 4:
        return ajax_json.jsonp_ok(request, u'不满足条件')
    app_id = APP_ID
    if nowt >= 1525795199:
        return jsonp_fail(request, u'超过了活动时间')

    data = common.index(user, app_id)
    return jsonp_ok(request, data)


@ajax_try({})
@need_login
def user_rank(request):
    """
    @api {post} /huodong/pds_xcq/user_rank [活动]用户排名
    @apiGroup pds_xcq
    @apiParamExample {json} 请求示例
       {"page_no": 0}           # 每次请求10条
    @apiSuccessExample {json} 成功返回
       {
        "message": "",
        "next": "",
           "data": {
        "rank": [
                {
                    "user_name": "张大帅",
                    "score": 30,
                    "class_name": "401班"
                },{},...
            ]
        },
        "response": "ok",
        "error": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """

    """
    用户排名
    :param request:
    :return:
    :author: 张嘉麒
    """
    user = request.user
    nowt = time.time()
    # 不满足条件
    if user.school_id != SCHOOL or user.grade_id != 4:
        return ajax_json.jsonp_ok(request, u'不满足条件')
    app_id = APP_ID
    if nowt >= 1525795199:
        return jsonp_fail(request, u'超过了活动时间')
    args = request.QUERY.casts(page_no=int)
    page_no = args.page_no or 0
    if page_no == 0:
        page_no = 1
    # 获取与用户排名
    data = common.user_rank(page_no, app_id)
    return ajax_json.jsonp_ok(request, data)