# coding=utf-8

from apps.summer_activity.sapp import common
from com.com_user import need_login
from libs.utils import ajax, ajax_try

PHASE_1_START_TIME = 0
PHASE_1_END_TIME = 9699999999
PHASE_2_START_TIME = 0
PHASE_2_END_TIME = 0

@ajax_try({})
@need_login
def service_time(request):
    """
        @api {post} /huodong/summer_activity/sapp/service_time [暑假活动]获取服务器时间
        @apiGroup summer2018
        @apiParamExample {json} 请求示例
           {}
        @apiSuccessExample {json} 成功返回
           {
            "message": "",
            "next": "",
            "data": 123456789  # 服务器时间
            "response": "ok",
            "error": ""
            }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """

    """
    暑假活动首页

    """
    data = int(time.time())
    return ajax.jsonp_ok(request, data)


@ajax_try({})
@need_login
def yw_index(request):
    """
    @api {post} /huodong/summer_activity/sapp/yw_index [暑假活动]语文活动首页
    @apiGroup summer2018
    @apiParamExample {json} 请求示例
       {
            subject_id : 2 5 9
        }
    @apiSuccessExample {json} 成功返回
       {
        "message": "",
        "next": "",
        "data": {
            "phase" : 1      # 1.2 为 1 2阶段         3.4  为第一阶段结束和第二阶段结束页面
            "open_num" : 1,   # 开启次数
            "rank" : '500+' ,  # 当前排名  （均为字符串数据）
            "box_status" : {"copper":0, "sliver":0, "gold":1},   # 用户宝箱状态    0不可开启   1可开启  2已开启
            "user_debris" :  {"hat":0, "shoe":0, "background":0, "pants":0, "cloth":0}    # 用户碎片状态  hat 帽子 shoe鞋子  background背景   pants  裤子 cloth 衣服
            "open_live" : [
                            {"user_id":123456, "user_name": "张三", "debris": "cloth", "add_time": "14:58:59", "remark": "gold"},
                            {"user_id":123456, "user_name": "张三", "debris": "cloth", "add_time": "14:58:59", "remark": "gold"},
                            # 开启实况
                            ...
                            ]
            "message_num" : 10    # 消息数目
            "mission" : "yw_reading"   //英语为'打地鼠'  '同步习题'   '口语流利说'   '情景对话'   '课本点读机'  '单词学习'  '爆破气球'    数学为 sx_test  sx_knowledge
        }
        "response": "ok",
        "error": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """

    """
    暑假活动首页

    """
    subject_id = 5
    nowt = int(time.time())
    if nowt < PHASE_1_START_TIME:
        return ajax.jsonp_fail(request, message=u'活动未开启')
    elif nowt < PHASE_1_END_TIME:
        phase = 1
    elif nowt < PHASE_2_START_TIME:
        phase = 3
    elif nowt < PHASE_2_END_TIME:
        phase = 2
    else:
        phase = 4
    user = request.user
    if phase in (1,2):
        data = common.yw_index(user, subject_id, phase)
    else:
        #  增加排行榜接口
        data = []
    return ajax.jsonp_ok(request, data)


@ajax_try({})
@need_login
def invite_stu(request):
    """
       @api {post} /huodong/summer_activity/sapp/invite_stu [暑假活动]邀请页面
       @apiGroup summer2018
       @apiParamExample {json} 请求示例
          {
            "subject_id" : 2       // 2代表数学  5 代表语文   9 代表英语
          }
       @apiSuccessExample {json} 成功返回
          {
           "message": "",
           "next": "",
           "data": [
                    { "user_id":123, "real_name":"张三"， "portrait":"很长很长的头像地址"   },
                    { "user_id":123, "real_name":"张三"， "portrait":"很长很长的头像地址"   },
                    { "user_id":123, "real_name":"张三"， "portrait":"很长很长的头像地址"   },
           ]
           "response": "ok",
           "error": ""
           }
       @apiSuccessExample {json} 失败返回
          {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
   """

    """
    暑假活动首页

    """
    args = request.QUERY.casts(subject_id=int)
    subject_id = args.subject_id or 0
    if not subject_id:
        return ajax.jsonp_fail(request, message=u'参数错误')
    nowt = int(time.time())
    if nowt < PHASE_1_START_TIME:
        return ajax.jsonp_fail(request, message=u'活动未开启')
    elif nowt < PHASE_1_END_TIME:
        phase = 1
    elif nowt < PHASE_2_START_TIME:
        phase = 3
    elif nowt < PHASE_2_END_TIME:
        phase = 2
    else:
        phase = 4
    if phase in (3,4):
        return ajax.jsonp_fail(request, message=u'活动未开启')
    user = request.user
    data = common.invite(user, subject_id, phase)
    return ajax.jsonp_ok(request, data)


@ajax_try({})
@need_login
def do_invite(request):
    """
       @api {post} /huodong/summer_activity/sapp/do_invite [暑假活动]邀请学生
       @apiGroup summer2018
       @apiParamExample {json} 请求示例
          {
            "subject_id" : 2       // 2代表数学  5 代表语文   9 代表英语
            "user_id" : 123456
          }
       @apiSuccessExample {json} 成功返回
          {
           "message": "",
           "next": "",
           "data": ""
           "response": "ok",
           "error": ""
           }
       @apiSuccessExample {json} 失败返回
          {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
   """

    """
    暑假活动首页

    """
    args = request.QUERY.casts(subject_id=int, user_id=int)
    subject_id = args.subject_id or 0
    invite_id = args.user_id or 0
    if not subject_id or not invite_id:
        return ajax.jsonp_fail(request, message=u'参数错误')
    nowt = int(time.time())
    if nowt < PHASE_1_START_TIME:
        return ajax.jsonp_fail(request, message=u'活动未开启')
    elif nowt < PHASE_1_END_TIME:
        phase = 1
    elif nowt < PHASE_2_START_TIME:
        phase = 3
    elif nowt < PHASE_2_END_TIME:
        phase = 2
    else:
        phase = 4
    if phase in (3,4):
        return ajax.jsonp_fail(request, message=u'活动未开启')
    user = request.user
    data = common.do_invite(user, subject_id, phase, invite_id)
    if data:
        return ajax.jsonp_fail(request, message=data)
    return ajax.jsonp_ok(request, data)


@ajax_try({})
@need_login
def get_ask_message(request):
    """
          @api {post} /huodong/summer_activity/sapp/get_ask_message [暑假活动]我的碎片消息----消息
          @apiGroup summer2018
          @apiParamExample {json} 请求示例
             {
               "subject_id" : 2       // 2代表数学  5 代表语文   9 代表英语
               "p" : 1                // 页数  从1 开始
             }
          @apiSuccessExample {json} 成功返回
             {
              "message": "",
              "next": "",
              "data": [
                       { "ask_for_user":123, "real_name":"张三"， "add_time":"12月11日" , "ask_thing": "cloth"  },
                       { "ask_for_user":123, "real_name":"张三"， "add_time":"12月11日", "ask_thing": "cloth"   },
                       { "ask_for_user":123, "real_name":"张三"， "add_time":"12月11日"  , "ask_thing": "cloth" },
              ]
              "response": "ok",
              "error": ""
              }
          @apiSuccessExample {json} 失败返回
             {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
      """

    """
   我的碎片消息----消息
    """
    args = request.QUERY.casts(subject_id=int, p=int)
    subject_id = args.subject_id or 0
    page = args.p or 0
    if not subject_id or not page:
        return ajax.jsonp_fail(request, message=u'参数错误')
    nowt = int(time.time())
    if nowt < PHASE_1_START_TIME:
        return ajax.jsonp_fail(request, message=u'活动未开启')
    elif nowt < PHASE_1_END_TIME:
        phase = 1
    elif nowt < PHASE_2_START_TIME:
        phase = 3
    elif nowt < PHASE_2_END_TIME:
        phase = 2
    else:
        phase = 4
    if phase in (3, 4):
        return ajax.jsonp_fail(request, message=u'活动未开启')
    user = request.user
    data = common.get_ask_message(user, subject_id, phase, page)
    return ajax.jsonp_ok(request, data)


@ajax_try({})
@need_login
def get_debris_message(request):
    """
          @api {post} /huodong/summer_activity/sapp/get_debris_message [暑假活动]我的碎片消息----碎片记录
          @apiGroup summer2018
          @apiParamExample {json} 请求示例
             {
               "subject_id" : 2       // 2代表数学  5 代表语文   9 代表英语
               "p" : 1                // 页数  从1 开始
             }
          @apiSuccessExample {json} 成功返回
             {
              "message": "",
              "next": "",
              "data": [

              ]
              "response": "ok",
              "error": ""
              }
          @apiSuccessExample {json} 失败返回
             {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
      """

    """
   我的碎片消息----碎片记录
    """
    args = request.QUERY.casts(subject_id=int, p=int)
    subject_id = args.subject_id or 0
    page = args.p or 0
    if not subject_id or not page:
        return ajax.jsonp_fail(request, message=u'参数错误')
    nowt = int(time.time())
    if nowt < PHASE_1_START_TIME:
        return ajax.jsonp_fail(request, message=u'活动未开启')
    elif nowt < PHASE_1_END_TIME:
        phase = 1
    elif nowt < PHASE_2_START_TIME:
        phase = 3
    elif nowt < PHASE_2_END_TIME:
        phase = 2
    else:
        phase = 4
    if phase in (3, 4):
        return ajax.jsonp_fail(request, message=u'活动未开启')
    user = request.user
    data = common.get_debris_message(user, subject_id, phase, page)
    return ajax.jsonp_ok(request, data)


@ajax_try({})
@need_login
def get_unit_student(request):
    """
          @api {post} /huodong/summer_activity/sapp/get_unit_student [暑假活动]赠送和索取获取班级下所有学生
          @apiGroup summer2018
          @apiParamExample {json} 请求示例
             {
             }
          @apiSuccessExample {json} 成功返回
             {
              "message": "",
              "next": "",
              "data": [
                    {"user_id" : 1234564, "portrait": "很长很长的Url", "real_name": "张三"}，
                    {"user_id" : 1234564, "portrait": "很长很长的Url", "real_name": "张三"}，
                    {"user_id" : 1234564, "portrait": "很长很长的Url", "real_name": "张三"}，
              ]
              "response": "ok",
              "error": ""
              }
          @apiSuccessExample {json} 失败返回
             {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
      """

    """
   赠送和索取获取班级下所有学生
    """
    nowt = int(time.time())
    if nowt < PHASE_1_START_TIME:
        return ajax.jsonp_fail(request, message=u'活动未开启')
    elif nowt < PHASE_1_END_TIME:
        phase = 1
    elif nowt < PHASE_2_START_TIME:
        phase = 3
    elif nowt < PHASE_2_END_TIME:
        phase = 2
    else:
        phase = 4
    if phase in (3, 4):
        return ajax.jsonp_fail(request, message=u'活动未开启')
    user = request.user
    data = common.get_unit_student(user)
    return ajax.jsonp_ok(request, data)


@ajax_try({})
@need_login
def give_debris(request):
    """
          @api {post} /huodong/summer_activity/sapp/give_debris [暑假活动]赠送碎片
          @apiGroup summer2018
          @apiParamExample {json} 请求示例
             {
                "give_user_id" : 123456 //赠与的用户id
                "subject_id" : 2 5 9
                "debris" : "hat"            // "shoe"  "background"    "pants"    "cloth"
             }
          @apiSuccessExample {json} 成功返回
             {
              "message": "",
              "next": "",
              "data": // 如果失败了会返回fail message会带信息， 如果成功啥也不反回
              "response": "ok",
              "error": ""
              }
          @apiSuccessExample {json} 失败返回
             {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
      """

    """
   赠送碎片
    """
    args = request.QUERY.casts(give_user_id=int, subject_id=int, debris=str)
    subject_id = args.subject_id or 0
    give_user_id = args.give_user_id or 0
    debris = args.debris or ''
    if not give_user_id or not subject_id or not debris:
        return ajax.jsonp_fail(request, message=u'参数错误')
    nowt = int(time.time())
    if nowt < PHASE_1_START_TIME:
        return ajax.jsonp_fail(request, message=u'活动未开启')
    elif nowt < PHASE_1_END_TIME:
        phase = 1
    elif nowt < PHASE_2_START_TIME:
        phase = 3
    elif nowt < PHASE_2_END_TIME:
        phase = 2
    else:
        phase = 4
    if phase in (3, 4):
        return ajax.jsonp_fail(request, message=u'活动未开启')
    user = request.user
    data = common.give_debris(user, give_user_id, phase, subject_id, debris)
    if data:
        return ajax.jsonp_fail(request, message=data)
    return ajax.jsonp_ok(request, data)



@ajax_try({})
@need_login
def ask_for_debris(request):
    """
          @api {post} /huodong/summer_activity/sapp/ask_for_debris [暑假活动]索取碎片
          @apiGroup summer2018
          @apiParamExample {json} 请求示例
             {
                "ask_for_id" : 123456 //   索取的用户id
                "subject_id" : 2 5 9
                "debris" : "hat"            // "shoe"  "background"    "pants"    "cloth"
             }
          @apiSuccessExample {json} 成功返回
             {
              "message": "",
              "next": "",
              "data": [
                    {"user_id" : 1234564, "portrait": "很长很长的Url", "real_name": "张三"}，
                    {"user_id" : 1234564, "portrait": "很长很长的Url", "real_name": "张三"}，
                    {"user_id" : 1234564, "portrait": "很长很长的Url", "real_name": "张三"}，
              ]
              "response": "ok",
              "error": ""
              }
          @apiSuccessExample {json} 失败返回
             {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
      """

    """
   索取碎片
    """
    args = request.QUERY.casts(ask_for_id=int, subject_id=int, debris=str)
    subject_id = args.subject_id or 0
    ask_for_id = args.ask_for_id or 0
    debris = args.debris or ''
    if not ask_for_id or not subject_id or not debris:
        return ajax.jsonp_fail(request, message=u'参数错误')
    nowt = int(time.time())
    if nowt < PHASE_1_START_TIME:
        return ajax.jsonp_fail(request, message=u'活动未开启')
    elif nowt < PHASE_1_END_TIME:
        phase = 1
    elif nowt < PHASE_2_START_TIME:
        phase = 3
    elif nowt < PHASE_2_END_TIME:
        phase = 2
    else:
        phase = 4
    if phase in (3, 4):
        return ajax.jsonp_fail(request, message=u'活动未开启')
    user = request.user
    data = common.ask_for_debris(user, ask_for_id, phase, subject_id, debris)
    return ajax.jsonp_ok(request, data)


@ajax_try({})
@need_login
def open_box(request):
    """
          @api {post} /huodong/summer_activity/sapp/open_box [暑假活动]开宝箱
          @apiGroup summer2018
          @apiParamExample {json} 请求示例
             {
                "box" : "copper",      // copper 铜宝箱 sliver 银宝箱 gold 金宝箱
                "subject_id" : 2 5 9
             }
          @apiSuccessExample {json} 成功返回
             {
              "message": "",
              "next": "",
              "data":  //如果失败了会返回fail message会带信息， 如果成功啥也不反回
              "response": "ok",
              "error": ""
              }
          @apiSuccessExample {json} 失败返回
             {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
      """

    """
   开宝箱
    """
    args = request.QUERY.casts(subject_id=int, box=str)
    subject_id = args.subject_id or 0
    box = args.box or ''
    if not box or not subject_id:
        return ajax.jsonp_fail(request, message=u'参数错误')
    nowt = int(time.time())
    if nowt < PHASE_1_START_TIME:
        return ajax.jsonp_fail(request, message=u'活动未开启')
    elif nowt < PHASE_1_END_TIME:
        phase = 1
    elif nowt < PHASE_2_START_TIME:
        phase = 3
    elif nowt < PHASE_2_END_TIME:
        phase = 2
    else:
        phase = 4
    if phase in (3, 4):
        return ajax.jsonp_fail(request, message=u'活动未开启')
    user = request.user
    data = common.open_my_box(user, box, phase, subject_id)
    if data:
        return ajax.jsonp_fail(request, message=data)
    return ajax.jsonp_ok(request, data)


@ajax_try({})
@need_login
def get_rank(request):
    """
          @api {post} /huodong/summer_activity/sapp/get_rank [暑假活动]排行榜
          @apiGroup summer2018
          @apiParamExample {json} 请求示例
             {
                "p" : 1,      // 分页 从1开始
                "subject_id" : 2 5 9
             }
          @apiSuccessExample {json} 成功返回
             {
              "message": "",
              "next": "",
              "data":  {
                "person_rank" : "500+"   // 用户个人排名  str形式
                "open_num" : 100     //用户个人开启次数
                "rank" : [
                        {"user_id"： 123456， "open_num": 10, "real_name": "张三", "school_name":"北大附小"}
                ]
              }
              "response": "ok",
              "error": ""
              }
          @apiSuccessExample {json} 失败返回
             {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
      """

    """
   排行榜
    """
    args = request.QUERY.casts(p=int, subject_id=int)
    subject_id = args.subject_id or 0
    page = args.p or 0
    if not page or not subject_id:
        return ajax.jsonp_fail(request, message=u'参数错误')
    nowt = int(time.time())
    if nowt < PHASE_1_START_TIME:
        return ajax.jsonp_fail(request, message=u'活动未开启')
    elif nowt < PHASE_1_END_TIME:
        phase = 1
    elif nowt < PHASE_2_START_TIME:
        phase = 3
    elif nowt < PHASE_2_END_TIME:
        phase = 2
    else:
        phase = 4
    if phase in (3, 4):
        return ajax.jsonp_fail(request, message=u'活动未开启')
    user = request.user
    data = common.get_rank(user.id, page, subject_id, user.unit.unit_class_id)
    return ajax.jsonp_ok(request, data)
