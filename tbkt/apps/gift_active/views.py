#coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: views.py
@time: 2017/10/21 11:40
"""
from apps.gift_active import common
from libs.utils.ajax import jsonp_ok, jsonp_fail

def p_join(request):
    """
        @api {post} /huodong/gift_active/join [金豆商城活动]参加活动
        @apiGroup gift_active
        @apiParamExample {json} 请求示例
           {
            "active_id": 1
            }
        @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {
            },
            "response": "ok",
            "error": ""
        }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    """
    功能说明：                金豆商城活动， 参加活动
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-10-21
    """
    args = request.loads() or request.QUERY.casts(active_id=int)
    active_id = int(args.active_id or 0)
    if not active_id:
        return jsonp_fail(request, message=u'参数不正确')
    user_id = request.user_id
    message = common.join_active(user_id, active_id)
    if message:
        return jsonp_fail(request, message=message)
    return jsonp_ok(request, message=message)


def p_status(request):
    """
        @api {post} /huodong/gift_active/status [金豆商城活动]用户是否参加活动
        @apiGroup gift_active
        @apiParamExample {json} 请求示例
           {
            "active_id": 1
            }
        @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {
                "status": 1             # 0 没有参加过， 1 参加过
                "active_num": 0         # 0 参与人数为0  n 参与人数为n
            },
            "response": "ok",
            "error": ""
        }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    """
    功能说明：                金豆商城活动， 用户是否参加活动
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张嘉麒                    2017-11-07
    """
    data = {}
    args = request.loads() or request.QUERY.casts(active_id=int)
    active_id = int(args.active_id or 0)
    if not active_id:
        data['status'] = 0
        return jsonp_fail(request, message=u'参数不正确')
    user_id = request.user_id
    status = common.active_status(user_id, active_id)
    data['status'] = status
    active_count_num = common.active_count(active_id)
    data['active_num'] = active_count_num

    return jsonp_ok(request, data)