# coding:utf-8
"""
@author: lvyang
@time: 2017/12/14
"""
from apps.double_festival import common
from com.com_user import need_login
from libs.utils import ajax, tbktapi


@need_login
def p_info(request):
    """
    @api /huodong/sd/info [双但活动]首页学生获奖信息
    @apiGroup sd
    @apiParamExample {json} 请求示例
       {}
    @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {
                 "invite_prop":{   # 通过邀请获得
                    '圣诞鞋':2,
                    '圣诞手套':2
                 }
                "open_prop": "通过开通获得圣诞鞋", # 开通获得奖品，没有为 ""
                "user_props": [     # 用户奖品列表
                    {
                        "item_no": "shoe",
                        "num": 1,
                        "name": "圣诞鞋"
                    }
                ]
            },
            "response": "ok",
            "error": ""
        }
    """
    # 判断开通是否加过奖品
    user = request.user
    # 查看邀请信息
    open_prop = common.open_prop(user)
    invite_prop = common.check_invite(user)
    # 返回用户道具数量
    user_props = common.get_user_props(user.id)
    data = dict(open_prop=open_prop, user_props=user_props, invite_prop=invite_prop)
    return ajax.ajax_ok(data)


@need_login
def p_news(request):
    """
    @api /huodong/sd/prop/news [双但活动]道具 详情
    @apiGroup sd
    @apiParamExample {json} 请求示例
       {}
    @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {
                "news": [ # 赠送详情
                            {
                                "status": 0,
                                "item_no": "clothes",
                                "user_id": 520403,
                                "name": "圣诞衣服",
                                "date": "12月18日 15:42:07",
                                "add_user": 591113,
                                "msg": "中学生同学向你索要",
                                "id": 7,
                                "add_time": 1513582927
                            },
                            {
                                "status": 1,    0 ：未赠送  1：以赠送
                                "item_no": "hat",
                                "user_id": 520403,
                                "name": "圣诞帽子",
                                "date": "12月18日 15:46:15",
                                "add_user": 591113,
                                "msg": "中学生同学向你索要",
                                "id": 8,
                                "add_time": 1513583175
                            }
                    ],
                "detail": [ #获得道具详情
                    {
                        "add_date": 1513559167,
                        "date": "12月18日 09:06:07",
                        "item_no": "open_prop"
                    }
                ]
            },
            "response": "ok",
            "error": ""
        }
    """
    user_id = request.user_id
    # 道具信息
    props_detail = common.user_props_detail(user_id)
    # 索要和赠送 的消息
    props_news = common.user_props_news(user_id)
    data = dict(detail=props_detail, news=props_news)
    return ajax.ajax_ok(data)


@need_login
def p_demand(request):
    """
    @api /huodong/sd/prop/demand [双但活动]索要道具道具
    @apiGroup sd
    @apiParamExample {json} 请求示例
       {
       prop_item:'shoe'  #索要道具
       stu_id :123   # 被索要道具用户id
       }
    @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {},
            "response": "ok",
            "error": ""
        }
    """
    user = request.user
    args = request.QUERY.casts(prop_item=unicode, stu_id=int)
    prop_item = args.prop_item
    stu_id = args.stu_id
    if not prop_item or not stu_id:
        return ajax.ajax_fail(error=u'缺少道具标识')
    if not common.any_open_status(user.id):
        return ajax.ajax_fail(error=u'开通用户才能索要')
    # 索要奖品
    common.demand_props(user, stu_id, prop_item)
    return ajax.ajax_ok()


@need_login
def p_give(request):
    """
    @api /huodong/sd/prop/give [双但活动]赠送道具
    @apiGroup sd
    @apiParamExample {json} 请求示例
       {
       prop_item:'shoe'  #赠送道具
       stu_id :123   # 被赠送道具用户id
       new_id:123  # 消息id
       }
    @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {},
            "response": "ok",
            "error": ""
        }
    """

    user = request.user
    args = request.QUERY.casts(prop_item=unicode, stu_id=int, new_id=int)
    # 道具标识
    prop_item = args.prop_item
    stu_id = args.stu_id
    new_id = args.new_id
    if not prop_item or not stu_id:
        return ajax.ajax_fail(error=u'缺少道具标识')
    if not common.any_open_status(user.id):
        return ajax.ajax_fail(error=u'开通用户才能赠送')
    if user.id == stu_id:
        return ajax.ajax_fail(error=u'不能赠送给自己')
    # 赠送奖品
    success, why = common.give_props(user, stu_id, prop_item, new_id)
    if not success:
        return ajax.ajax_fail(error=why)
    return ajax.ajax_ok()


@need_login
def p_open(request):
    """
    @api /huodong/sd/prop/openBox [双但活动]开启宝箱
    @apiGroup sd
    @apiParamExample {json} 请求示例
       {}
    @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {
                gift:"方特门票一张"
            },
            "response": "ok",
            "error": ""
        }
    """
    user = request.user
    # 开启宝箱
    gift, error = common.open_box(user)
    if error:
        return ajax.ajax_fail(error)
    return ajax.ajax_ok({'gift': gift})


@need_login
def p_gain(request):
    """
    @api /huodong/sd/prop/gain [双但活动]完成作业获得宝箱
    @apiGroup sd
    @apiParamExample {json} 请求示例
       {
       work_type:1     # 作业类型   1在线作业, 2: 每日任务 3: 诗词大战    4: 同步习题
       }
    @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {
                "prop": "获得圣诞手套"
            },
            "response": "ok",
            "error": ""
        }
    """

    user = request.user
    args = request.QUERY.casts(work_type=int)
    work_type = args.work_type
    if not work_type:
        return ajax.ajax_fail(u'缺少type值')
    if user.is_teacher:
        return ajax.ajax_fail(u'教师不能参与')
    # 做作业获得
    prop, error = common.award_props(user, work_type)
    if error:
        return ajax.ajax_fail(error)
    return ajax.ajax_ok({'prop': prop})


@need_login
def p_class_stu(request):
    """
    @api /huodong/sd/stu/class_stu [双但活动]班级学生
    @apiGroup sd
    @apiParamExample {json} 请求示例
       {}
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": [
            {
                "pinyin": "bm",
                "initial": "b",
                "id": 2754348,
                "name": "宝马"
            },
            {
                "pinyin": "ddd",
                "initial": "d",
                "id": 7314774,
                "name": "得得得"
            },
            {
                "pinyin": "hh",
                "initial": "h",
                "id": 2022858,
                "name": "呵呵"
            },
            {
                "pinyin": "lqm",
                "initial": "l",
                "id": 7497502,
                "name": "刘启明"
            },
            {
                "pinyin": "xxxs",
                "initial": "x",
                "id": 608898,
                "name": "小小学生"
            },
        ],
        "response": "ok",
        "error": ""
    }
    """
    user = request.user
    stu = common.get_unit_stu(user)
    return ajax.ajax_ok(stu)


def p_verify(request):
    """
    @api /huodong/sd/stu/verify [双但活动]确认用户信息
    @apiGroup sd
    @apiParamExample {json} 请求示例
       {
       invite_user_id：456 #邀请人
       phone:135000000,
       name:张三
       }
    @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {
                "token": "MzEzMzk0OX0wNDA1MDg1MTg4fTA0MDcxODE1OTk",
                "open_info": [
                    {
                        "status": 0,
                        "pay_type": 2,
                        "subject_id": 2,
                        "cancel_date": "",
                        "open_date": "1970-01-01 08:00:00"
                    },
                    {
                        "status": 0,
                        "pay_type": 0,
                        "subject_id": 5,
                        "cancel_date": "",
                        "open_date": ""
                    },
                    {
                        "status": 0,
                        "pay_type": 0,
                        "subject_id": 9,
                        "cancel_date": "",
                        "open_date": ""
                    }
                ]
            },
            "response": "ok",
            "error": ""
        }
    """

    args = request.QUERY.casts(invite_user_id=int, phone=str, name=unicode)
    phone = args.phone
    name = args.name
    user_id = args.invite_user_id
    if not user_id or not phone or not name:
        return ajax.ajax_fail(u'缺少参数')
    data, error = common.verify_user(user_id, phone, name)
    if error:
        return ajax.ajax_fail(message=error)
    return ajax.ajax_ok(data)


@need_login
def p_open_subject(request):
    """
    @api /huodong/sd/stu/open_invite [双但活动]请邀开通接口
    @apiGroup sd
    @apiParamExample {json} 请求示例
       {
       invite_user_id：456 #邀请人
       sn_code:123
       subject_id：2,5,9   开通学科
       }
    @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {},
            "response": "ok",
            "error": ""
        }
    """
    user = request.user
    args = request.QUERY.casts(subject_id=str, sn_code=int, invite_user_id=int)
    subject_id = args.subject_id
    sn_code = args.sn_code
    invite_user_id = args.invite_user_id
    if not subject_id or not sn_code or not invite_user_id:
        return ajax.ajax_fail(u'缺少参数')
    success, why = common.invite_open(request, user, subject_id, sn_code, invite_user_id)
    if not success:
        return ajax.ajax_fail(why)
    return ajax.ajax_ok()
