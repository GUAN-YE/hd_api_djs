# coding=utf-8

"""
@varsion: ??
@author: 张嘉麒
@file: urls.py
@time: 2017/12/12 17:30
"""
import datetime
import time

from apps.excite_activity import common
from com.com_user import need_login
from libs.utils import tbktapi
from libs.utils.ajax import jsonp_ok, jsonp_fail


def activity_num(request):
    """
        @api {get} /huodong/excite_activity/ticket_num [激励抽奖活动]用户抽奖券个数
        @apiGroup excite_activity
        @apiParamExample {json} 请求示例
           {
            }
        @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {
                "ticket_num":1     //该用户剩余的奖券数量
                "now_month":12     //当前月份
            },
            "response": "ok",
            "error": ""
        }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    """
    功能说明：                激励抽奖活动， 用户抽奖券个数
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张嘉麒                    2017-12-12
    """
    data = {}
    user_id = request.user_id
    if not user_id:
        return jsonp_fail(request, message=u'未获取到user_id')
    now_month, ticket_num = common.get_user_tickets(user_id)
    data['ticket_num'] = ticket_num
    data['now_month'] = now_month

    return jsonp_ok(request, data)


def coin_join_activity(request):
    """
        @api {post} /huodong/excite_activity/coin_join_actitvity [激励抽奖活动]用户使用金币参与抽奖
        @apiGroup excite_activity
        @apiParamExample {json} 请求示例
           {
            "excite_activity_id" : 1
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
    功能说明：                激励抽奖活动， 用户使用金币参与活动
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张嘉麒                    2017-12-12
    """
    args = request.loads() or request.QUERY.casts(excite_activity_id=int)
    excite_activity_id = args.excite_activity_id
    if not excite_activity_id:
        return jsonp_fail(request, message=u'参数不正确')
    user_id = request.user_id
    message = common.coin_join_actitvity(user_id, excite_activity_id)
    if message:
        return jsonp_fail(request, message=message)
    common.change_batch_id(request,excite_activity_id)
    return jsonp_ok(request, message=message)


def ticket_join_activity(request):
    """
        @api {post} /huodong/excite_activity/ticket_join_actitvity [激励抽奖活动]用户使用抽奖券参与抽奖
        @apiGroup excite_activity
        @apiParamExample {json} 请求示例
           {
            "excite_activity_id" : 1
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
    功能说明：                激励抽奖活动， 用户使用抽奖券参与活动
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张嘉麒                    2017-12-12
    """
    args = request.loads() or request.QUERY.casts(excite_activity_id=int)
    excite_activity_id = args.excite_activity_id
    if not excite_activity_id:
        return jsonp_fail(request, message=u'参数不正确')
    user_id = request.user_id
    message = common.ticket_join_actitvity(user_id, excite_activity_id)
    if message:
        return jsonp_fail(request, message=message)
    common.change_batch_id(request, excite_activity_id)
    return jsonp_ok(request, message=message)


def get_winning_list(request):
    """
        @api {get} /huodong/excite_activity/winning_list [激励抽奖活动]获取获奖教师名单
        @apiGroup excite_activity
        @apiParamExample {json} 请求示例
           {
            "excite_activity_id" : 1
            }
        @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": [
                {
                  "phone": "151****6670",
                  "school_name": "123",
                  "real_name": "钱学三"
                },
                {
                  "phone": "151****6670",
                  "school_name": "123",
                  "real_name": "钱学三"
                }
                {}，{}，{}......
              ],
            "response": "ok",
            "error": ""
        }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    """
    功能说明：                激励抽奖活动， 获取获奖教师名单
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张嘉麒                    2017-12-12
    """
    args = request.loads() or request.QUERY.casts(excite_activity_id=int)
    excite_activity_id = args.excite_activity_id
    if not excite_activity_id:
        return jsonp_fail(request, message=u'活动ID出了错')
    data = common.get_winning_list(excite_activity_id)

    return jsonp_ok(request, data)


def get_activity_entrance(request):
    """
        @api {get} /huodong/excite_activity/activity_entrance [激励抽奖活动]活动入口
        @apiGroup excite_activity
        @apiParamExample {json} 请求示例
           {

            }
        @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {
                "actitity_len" : 1             // 目前正在进行的活动数量
            },
            "response": "ok",
            "error": ""
        }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    """
    功能说明：                激励抽奖活动，入口按钮
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张嘉麒                    2017-12-12
    """
    data = {}
    actitity_len = common.get_activity_entrance()
    data['actitity_len'] = actitity_len

    return jsonp_ok(request, data)


def get_activity(request):
    """
        @api {get} /huodong/excite_activity/activity [激励抽奖活动]抽奖活动详情页面
        @apiGroup excite_activity
        @apiParamExample {json} 请求示例
           {
            "excite_activity_id" : 1
            }
        @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data" = {
                'open_person' : open_person,                //到达多少人开奖
                'had_join' : had_join,                //已经有多少人参与
                'had_lottery' : had_lottery,                //已经开奖的次数
                'lottery_rate' : lottery_rate,                //当前用户的中奖率
                'lottery_up' : lottery_up,                //使用奖券参与次数上限
                'had_use_ticket_join' : had_use_ticket_join,                //已经用奖券参与的用户的数量
            },
            "response": "ok",
            "error": ""
        }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    """
    功能说明：                激励抽奖活动，抽奖活动详情页面
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张嘉麒                    2017-12-12
    """
    args = request.loads() or request.QUERY.casts(excite_activity_id=int)
    excite_activity_id = args.excite_activity_id
    user_id = request.user_id
    if not excite_activity_id:
        return jsonp_fail(request, message=u'活动ID出了错')
    data = common.get_activity(excite_activity_id, user_id)
    return jsonp_ok(request, data)


def invite_teacher(request):
    """
        @api {post} /huodong/excite_activity/invite_teacher [激励抽奖活动]邀请老师用来获得抽奖券
        @apiGroup excite_activity
        @apiParamExample {json} 请求示例
           {
            "phone_num" : 13303330333
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
    功能说明：                邀请老师用来获得抽奖券
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张嘉麒                    2017-12-12
    """
    args = request.loads() or request.QUERY.casts(phone_num=int)
    phone_num = args.phone_num
    if not phone_num:
        return jsonp_fail(request, message=u'缺少手机号')
    user = request.user
    user_id = request.user_id
    message = common.send_sms(phone_num, user_id, request, user)
    if message:
        return jsonp_fail(request, message=message)
    message = u'邀请成功'
    return jsonp_ok(request, message=message)


def invite_stu(request):
    """
        @api {post} /huodong/excite_activity/invite_stu [激励抽奖活动]将邀请学生的信息存到数据库
        @apiGroup excite_activity
        @apiParamExample {json} 请求示例
           {
            "stu_id" : "10000,10001,10002,10003,10004"
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
    功能说明：                将邀请学生的信息存到数据库
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张嘉麒                    2017-12-13
    """
    args = request.loads() or request.QUERY.casts(stu_id=str)
    stu_id = args.stu_id
    user_id = request.user_id
    if not user_id:
        return jsonp_fail(request, message=u'缺少user_id')
    if not stu_id:
        return jsonp_fail(request, message=u'缺少stu_id')
    message = common.create_stu_invite_data_to_mysql(stu_id, user_id)
    if message:
        return jsonp_fail(request, message=message)
    message = u'添加stu数据成功'
    return jsonp_ok(request, message=message)


def get_activity_list(request):
    """
        @api {get} /huodong/excite_activity/activity_list [激励抽奖活动]目前正在进行的活动列表
        @apiGroup excite_activity
        @apiParamExample {json} 请求示例
           {
            }
        @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {
                active_data:[
                {
                  "id": "***",                   //活动id
                  "name": "***",               //活动名称
                  "url": "***",                 //图片url
                  "open_person": "***"          //开奖人次
                  "strat_time_month": "***"    //开奖月份
                  "start_time_date": "***"      //开奖日期
                  "strat_time_year": "***"      //开奖年份
                   "sign_gold": "***"          //参与金币
                  "end_time_month": "***"    //结束月份
                  "end_time_date": "***"      //结束日期
                  "end_time_year": "***"       //结束年份
                  'original_price' : 'original_price'    //商品原价
                  'tea_num':1   //参与教师数量
                  'type' ：1   // 0金币，奖券都可以，1，仅限奖券参与
                 },
              ],
                winner_data:[# 获奖信息
                ]
              }
            "response": "ok",
            "error": ""
        }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    """
    功能说明：                激励抽奖活动， 目前正在进行的活动列表
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张嘉麒                    2017-12-27
    """
    user_id = request.user_id
    if not user_id:
        return jsonp_fail(request, message=u'请先登录')
    active_data = common.get_activeity_list()
    winner_data = []
    if not active_data:
        winner_data = common.last_month_winning()

    data = dict(winner_data=winner_data, active_data=active_data)
    return jsonp_ok(request, data)


@need_login
def submit_address(request):
    """
        @api {get} /huodong/excite_activity/submit_address [激励抽奖活动]填写中奖信息
        @apiGroup excite_activity
        @apiParamExample {json} 请求示例
           {
                excita_id:1 活动id,
                address: 地址
                phone: 手机号
                addressee: 收件人姓名
            }
        @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": "",
            "response": "ok",
            "error": ""
        }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    user_id = request.user_id
    args = request.QUERY.casts(excita_id=int, address=unicode, phone=unicode, addressee=unicode)
    if not all(args.values()):
        return jsonp_fail(request, error=u'参数不正确')
    if not args.phone.isdigit() or not len(args.phone) == 11:
        return jsonp_fail(request, error=u'手机号不正确')
    err = common.submit_winner_info(user_id, args.excita_id, args.address, args.addressee, args.phone)
    if err:
        return jsonp_fail(request, error=err)
    return jsonp_ok(request)