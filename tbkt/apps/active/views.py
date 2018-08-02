#coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: views.py
@time: 2017/9/5 11:31
"""
from apps.active import common
from libs.utils.ajax import jsonp_ok, jsonp_fail

def p_actives(request):
    """
    @api {post} /huodong/active/actives_info [活动]满足用户条件的活动
    @apiGroup active
    @apiParamExample {json} 请求示例
       {}
    @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": [
                {
                    "extend": {},
                    "banner_url": "",
                    "banner_end": "2017-10-31 23:59:59",
                    "name": "英语常态活动(S1赛季)",
                    "banner_begin": "2017-09-11 17:21:31",
                    "is_open": 1,       1 表示能加分， 2 表示不能加分
                    "begin_url": "",
                    "active_id": 3
                }, {}, {},....
            ],
            "response": "ok",
            "error": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    """
    功能说明：                得到用户所有满足条件的活动
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-9-11
    """
    user = request.user
    data = common.get_actives(user)
    return jsonp_ok(request, data)

def p_active_status(request):
    """
    @api {post} /huodong/active/active_status [活动]用户某个活动是否能加分
    @apiGroup active
    @apiParamExample {json} 请求示例
       {
        "active_id": 3
       }
    @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {
                "status": 1             # 1 能加分， 2 不能加分,只显示排行
            },
            "response": "ok",
            "error": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    """
    功能说明：                判断用户参加的这个活动是否属于加分的活动
    参数：active_id    参数活动的id
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-9-11
    """
    args = request.loads() or request.QUERY.casts(active_id=int)  # 参加活动的id
    active_id = args.active_id or ""
    user = request.user
    status = common.get_active_status(user, active_id)
    data = {}
    data["status"] = 2
    if status:
        data["status"] = 1
    return jsonp_ok(request, data)

def p_update_score(request):
    """
    @api {post} /huodong/active/add_score [活动]活动加减分
    @apiGroup active
    @apiParamExample {json} 请求示例
       {
            "user_id": 2465828,             # 要加分的用户id
            "active_id": 3,                 # 活动id
            "item_no": "mouse"              # 活动加减分规则标识
            "city": 4500000,                # 省，市, 区
            "unit_id": ""                   # 班级
            "is_open":                      # 用户开通状态 0:未开通， 1: 开通
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
    功能说明：                活动加减分
    参数：item_no, 要加减分的学习模块或作业模块, 英文名
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-9-11
    """
    args = request.loads() or request.QUERY.casts(user_id=int, active_id=int, item_no=str, city=str, unit_id=int, grade_id=int, is_open=int)
    item_no = args.item_no or ""
    user_id = args.user_id or 0
    active_id = args.active_id or 0
    city = args.city or 0
    unit_id = args.unit_id or 0
    grade_id = args.grade_id or 0
    is_open = int(args.is_open or 0)

    add_user_id = request.user.id

    if not item_no:
        return jsonp_fail(request, message="no item_no")

    if not user_id:
        return jsonp_fail(request, message="no active_user_id")

    if not active_id:
        return jsonp_fail(request, message="no active_id")

    common.update_score(user_id, active_id, item_no, add_user_id, city, unit_id, is_open,grade_id)
    return jsonp_ok(request)