# coding:utf-8
"""
活动学生端视图
"""
from apps.active.common import update_score
from . import common
from libs.utils import ajax, ajax_try
from com.com_user import need_login

STU_ACTIVE_ID = 8
SIGN = 'stu_sign'
SHARD = 'stu_share'


@ajax_try({})
@need_login
def r_sign(request):
    """
    @api /huodong/sx/normal/stu/sign [数学常态活动]学生签到 
    @apiGroup math_normal
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "msg": "签到获取60积分"
        },
        "response": "ok",
        "error": ""
    }
    @apiSuccessExample {json} 其他返回
    {
        "message": "已签到",
        "next": "",
        "data": "",
        "response": "fail",
        "error": ""
    }
    """
    user = request.user
    return ajax.jsonp_fail(request, message='活动已结束！')
    if user.is_teacher or int(user.city) !=411200:
        return ajax.jsonp_fail(request, message='教师不能参与学生签到！')
    status, msg = common.stu_sign(user, STU_ACTIVE_ID, SIGN)
    if not status:
        return ajax.jsonp_fail(request, message=msg, data='')
    return ajax.jsonp_ok(request, {'msg': msg})


@ajax_try({})
@need_login
def r_share(request):
    """
    @api /huodong/sx/normal/stu/share [数学常态活动]学生分享
    @apiGroup math_normal
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": "",
        "response": "ok",
        "error": ""
    }
    """
    user = request.user
    if user.is_teacher or int(user.city) !=411200:
        return ajax.jsonp_fail(request, message='教师不能参与学生分享！')
    if not common.get_user_share(user.id, STU_ACTIVE_ID, SHARD):
        return ajax.jsonp_fail(request)
    is_open = 0 #user.openstatus(2)
    update_score(user.id, STU_ACTIVE_ID, SHARD, user.city, user.unit.id, is_open)
    return ajax.jsonp_ok(request)
