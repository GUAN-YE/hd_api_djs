#coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: views.py
@time: 2017/9/5 14:20
"""

import time
import datetime

from com import com_user
from apps.active import common
from libs.utils import db, Struct, get_ling_time, format_url
from libs.utils.ajax import jsonp_ok
from com.com_user import need_login

ITEM = ["ballon", "mouse", "test", "receive"]

ACTIVE_ID = 3  # 英语常态活动 s1赛季
PAGE_COUNT = 20

def user_rank(request):
    """
    @api {post} /huodong/yy/normal/rank [英语常态活动]用户排名
    @apiGroup yy_normal
    @apiParamExample {json} 请求示例
       {}
    @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {
                "rank_info": [
                    {
                         "portrait": "https://file.m.tbkt.cn/upload_media/portrait/2017/03/06/20170306102941170594.png",
                        "score": 190,
                        "user_id": 2465828,
                        "school_name": "创恒中学",
                        "real_name": "小张"
                    }
                ]
            },
            "response": "ok",
            "error": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    """
    功能说明：                用户排名
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-9-5
    """
    page_no = request.QUERY.get('page_no', 1)
    page_no = max(int(page_no), 1)

    rank = common.get_active_rank(ACTIVE_ID, page_no, PAGE_COUNT)
    user_dict = com_user.users_info([int(r.user_id) for r in rank])
    for r in rank:
        r.real_name = user_dict.get(r.user_id).get("real_name")
        r.school_name = user_dict.get(r.user_id).get("school_name")
        r.portrait = format_url(user_dict.get(r.user_id).get("portrait"))
    return jsonp_ok(request, {"rank": rank})

@need_login
def index(request):
    """
        @api {post} /huodong/yy/normal/index [英语常态活动]首页
        @apiGroup yy_normal
        @apiParamExample {json} 请求示例
           {}
        @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {
                "score": 210,
                "rank_no": 1
            },
            "response": "ok",
            "error": ""
        }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
        """
    """
    功能说明：                活动首页 目前是实时更新
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-9-5
    """
    user_id = request.user_id
    data = common.get_user_rank(ACTIVE_ID, user_id)
    return jsonp_ok(request, data)

def tasks(request):
    """
        @api {post} /huodong/yy/normal/tasks [英语常态活动]每日任务完成情况
        @apiGroup yy_normal
        @apiParamExample {json} 请求示例
           {}
        @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {
                "test": 0,
                "receive": 0,
                "status": 0,
                "mouse": 0,
                "ballon": 0,
                "time_def": "13:42:07",
            },
            "response": "ok",
            "error": ""
        }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
        """
    """
    功能说明：                每日任务, 实时更新
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-9-5
    """
    user_id = request.user_id

    ling_time = get_ling_time()  # 每天凌晨的时间

    # 当天各个模块完成的次数
    sql = """
        SELECT item_no, COUNT(id) as count FROM active_score_user_detail
        WHERE user_id = %s AND active_id = %s AND add_date > %s GROUP BY item_no;
        """ % (user_id, ACTIVE_ID, ling_time)

    result = db.tbkt_active.fetchall_dict(sql)
    data = {}
    for key in ITEM:
        data[key] = 0
    for r in result:
        data[r.item_no] = r.count
    data["status"] = request.user.openstatus(9)
    # data["time_def"] = get_time_difference()
    return jsonp_ok(request, data)

def add_score(user_id, active_id, item_no, add_user, city, unit_id):
    """
    功能说明：                英语常态活动加减积分
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-9-11
    """
    if int(city) == 411200:
        return
    if active_id != 3:
        return
    if item_no not in ITEM:
        return
    common.update_score(user_id, active_id, item_no, add_user, city, unit_id, is_open=0)
    return


def get_time_difference():
    """
    功能说明：                获取现在时间到第二天凌晨的时间差
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-9-13
    """
    now = datetime.datetime.now()                                                       # 现在的时间
    today = now.today()
    ming = datetime.datetime(today.year, today.month, today.day + 1, 0, 0, 0)           # 明天凌晨的时间
    return str(ming-now)[:-7]
