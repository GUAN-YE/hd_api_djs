# coding:utf-8
from libs.utils import ajax, ajax_json, ajax_try, Struct, db
from . import common
from com.com_user import need_teacher


@ajax_try([])
@need_teacher
def get_status(request):
    """
    @api {post}  /huodong/tea/task/status  返回剩余金币数量和是否可以领取的状态
    @apiGroup tea_coin
    @apiParamExample {json} 请求示例
        {}
    @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {
                    "status": 0,            #是否可以领取金币 0 不可以 1 可以 2 领取过
                    "num":2000              #剩余金币数量
                    }
            "response": "ok",
            "error": ""
        }

    :return:
    """

    user = request.user
    tea_unit_ids = [u.id for u in user.units]
    data = common.get_status(user)
    return ajax_json.jsonp_ok(request, data)


@ajax_try([])
@need_teacher
def get_coin(request):
    """
    @api {post} /huodong/tea/task/get/coin  领取金币
    @apiGroup tea_coin
    @apiParamExample {json} 请求示例
        {}
    @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": "",
            "response": "ok",
            "error": ""
        }
    """
    user_id = request.user_id
    num = db.tbkt_active.active_score_gift.select("end_num").get(active_id=14)
    if num.end_num == 0:
        return ajax_json.jsonp_fail(request, data=u"金币领完了")
    data = common.get_coin(user_id)
    return ajax_json.jsonp_ok(request, data)
