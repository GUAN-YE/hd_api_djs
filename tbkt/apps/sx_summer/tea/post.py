# coding:utf-8
from apps.sx_summer import common
from apps.sx_summer.active_cofing import *
from apps.sx_summer.tea import probability
from com.com_user import need_teacher
# from libs.apps.user.common import open_subject
from libs.utils import ajax_json, db, ajax_try, tbktapi


@ajax_try([])
@need_teacher
def p_rank(request):
    """
    @api {post} /huodong/sx_summer/t/rank [暑假活动 教师]排行
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
       {
            p:1,
            is_smx:0   1:是三门峡
        }
    @apiSuccessExample {json} 成功返回
        {
          "message": "",
          "error": "",
          "data": [
          "rank":
            {
              "user_id": "1185342",
              "num": 1,
              "user_name": "郭小帅",
              "score": "370",
              "school_name": "睢县河堤乡姜庄小学"
            },
            {
              "user_id": "2180866",
              "num": 2,
              "user_name": "杨铮",
              "score": "110",
              "school_name": "商丘市八一路小学"
            }...
          ],
          "response": "ok",
          "next": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "no_app_id", "data": "", "response": "fail", "next": ""}
    """

    args = request.QUERY.casts(p=int, is_smx=int)
    page = args.p
    user = request.user
    is_smx = 1 if user.city and int(user.city) == 411200  else 0
    rank, total = common.get_rank(APP_ID_TEA, page or 1, is_smx)
    return ajax_json.jsonp_ok(request, {'rank': rank, 'total': total})



@ajax_try([])
@need_teacher
def p_unit_rank(request):
    """
    @api {post} /huodong/sx_summer/t/unit_rank [暑假活动 教师]排行
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
       {
            p:1,
        }
    @apiSuccessExample {json} 成功返回
        {
          "message": "",
          "error": "",
          "data": [
          "rank":
            {
              "user_id": "1185342",
              "num": 1,
              "user_name": "郭小帅",
              "score": "370",
              "school_name": "睢县河堤乡姜庄小学"
            },
            {
              "user_id": "2180866",
              "num": 2,
              "user_name": "杨铮",
              "score": "110",
              "school_name": "睢县河堤乡姜庄小学"
            }...
          ],
          "response": "ok",
          "next": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "no_app_id", "data": "", "response": "fail", "next": ""}
    """

    args = request.QUERY.casts(p=int)
    page = args.p
    user = request.user
    units = user.units
    if not units:
        return ajax_json.jsonp_ok(request, {'rank': [], 'total': 0})
    unit_ids = [u.id for u in units]
    rank, total = common.get_unit_rank(unit_ids, page or 1)
    return ajax_json.jsonp_ok(request, {'rank': rank, 'total': total})



@ajax_try([])
@need_teacher
def get_user_info(request):
    """
    @api {post} /huodong/sx_summer/t/user_rank [暑假活动 教师]获取教师 分数和排行
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
       {}
    @apiSuccessExample {json} 成功返回
        {"message": "", "error": "", "data": {"score": 100, "rank": 2}, "response": "ok", "next": ""}
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    user = request.user
    score_user = db.default.score_user.get(app_id=APP_ID_TEA, user_id=user.id)
    rank = common.get_user_rank(APP_ID_TEA, user.id, score_user.score, user.city) if score_user else 0
    score = score_user.score if score_user else 0
    score = 0 if score < 0 else score
    return ajax_json.jsonp_ok(request, {'score': score, 'rank': rank})


@ajax_try([])
@need_teacher
def p_score_detail(request):
    user_id = request.user_id
    args = request.QUERY.casts(p=int)
    page = args.p
    detail = common.get_score_detail(APP_ID_TEA, user_id, page or 1)
    return ajax_json.jsonp_ok(request, {'detail': detail})


@ajax_try([])
@need_teacher
def p_send_sms(request):
    """
    @api {post} /huodong/sx_summer/t/send_sms [暑假活动 教师]发送短信
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
       {'content':'家长您好....'}
    @apiSuccessExample {json} 成功返回
        {"message": "", "error": "", "data": ', "response": "ok", "next": ""}
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """

    user = request.user
    args = request.QUERY.casts(content=unicode)
    if not args.content.strip():
        return ajax_json.jsonp_fail(request, message=u'请输入短息内容')
    open_num = common.get_score_add_num(APP_ID_TEA, user.id, 'send_sms')
    if open_num < SEND_SMS_NUM:
        common.add_score(APP_ID_TEA, user.id, SEND_SMS_SCORE, 'send_sms', u'发送通知短信', user.city or 0)
    content = args.content
    unit_class_id = ','.join(str(u.id) for u in user.units)

    hub = tbktapi.Hub(request)
    hub.sms.post('/sms/send', {'unit_id': unit_class_id, 'content': content})
    return ajax_json.jsonp_ok(request)


@ajax_try([])
@need_teacher
def p_send_open(request):
    """
    @api {post} /huodong/sx_summer/t/send_open [暑假活动 教师]发送开通短信
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
       {}
    @apiSuccessExample {json} 成功返回
        {"message": "", "error": "", "data": ', "response": "ok", "next": ""}
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """

    user = request.user
    args = request.QUERY.casts(content=unicode)
    if not args.content.strip():
        return ajax_json.jsonp_fail(request, message=u'请输入短息内容')
    open_num = common.get_score_add_num(APP_ID_TEA, user.id, 'send_open')
    if open_num < SEND_OPEN_NUM:
        common.add_score(APP_ID_TEA, user.id, SEND_OPEN_SCORE, 'send_open', u'发送开通短信', user.city or 0)
    content = args.content
    unit_class_id = [u.id for u in user.units]

    hub = tbktapi.Hub(request)
    student = []
    for i in unit_class_id:
        r = hub.com.post('/class/students', {"unit_id": i})
        if r and r.response == 'ok':
            data = r.data
            student += (data.get('students', []))
    platform_id = int(user.platform_id) if user and user.platform_id else 1
    phones = ','.join(str(s['phone_number']) for s in student if s.get('status',0) not in [2,9])
    r = hub.bank.post('/cmcc/open', {'phone_number': phones, 'subject_id': 2, "platform_id": platform_id})
    # if not r:
    #     return ajax_json.jsonp_fail(request, message='服务器开小差了')
    # if r.response == 'fail':
    #     return ajax_json.jsonp_fail(request, message=r.message)

    hub = tbktapi.Hub(request)
    hub.sms.post('/sms/send', {'phone': phones, 'unit_id': unit_class_id, 'content': content})
    return ajax_json.jsonp_ok(request)



@ajax_try({})
@need_teacher
def p_award(request):
    """
    @api {post} /huodong/sx_summer/t/award [暑假活动 抽奖]教师抽奖
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
       {app_id:35}   36：数学教师     42 ：语文教师   ,  34：英语教师
    @apiSuccessExample {json} 成功返回
        {
          "message": "很遗憾，您本次未抽中任何奖品！",
          "error": "",
          "data": {award:1} 1~4 中奖，5： 谢谢参与，6 积分不足
          "response": "ok",
          "next": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "手速太快了，请稍后尝试", "error": "", "data": "", "response": "fail", "next": ""}
    """

    user = request.user
    is_smx = 0 if user.city and int(user.city) != 411200 else 1
    args = request.QUERY.casts(app_id=int)
    app_id = args.app_id
    if not app_id or app_id not in TEA_APP_IDS:
        return ajax_json.jsonp_fail(request, error='no_app_id')

    lottery_cost = TEA_LOTTERY_COST

    if not common.get_active_status(app_id):
        return ajax_json.jsonp_fail(request, message=u'活动已经结束')

    # 判断用户是否有抽奖资格
    # 语文
    if app_id == YW_APP_ID_TEA:
        lottery_able = common.get_yuwen_lottery_able(request, app_id, user, lottery_cost)
    else:
        lottery_able = db.default.score_user.filter(app_id=app_id, user_id=user.id,
                                                    score__gte=lottery_cost).exists()

    if not lottery_able:
        return ajax_json.jsonp_ok(request, data={'award': 6}, message=u'您的积分已不足，快去赚积分吧！')

    # 抽奖
    # 获取获奖奖项
    if is_smx:
        award_type = probability.get_smx_user_award_type(user.old_user_id)
    else:
        award_type = probability.get_user_award_type(user.old_user_id)

    # 语文
    if app_id == YW_APP_ID_TEA:
        # 抽奖扣分结果
        re_result = common.yw_reduce_score(request, app_id, user, lottery_cost)
        if re_result:
            # 确认抽奖情况，保存获奖记录
            award, award_name = common.get_award_result(app_id, user, award_type, is_smx)
        else:
            award, award_name = 0, 0
    else:
        # 数学英语 抽奖扣分
        unit = user.unit.id if user.unit else 0
        cc = common.add_score(app_id, user.id, -lottery_cost, 'lottery', u'抽奖-%s积分' % lottery_cost, user.city or 0,
                              unit)
        if cc:
            # 确认抽奖情况，保存获奖记录
            award, award_name = common.get_award_result(app_id, user, award_type, is_smx)
        else:
            award, award_name = 0, 0

    if not (award and award_name):
        return ajax_json.jsonp_ok(request, data={'award': 5}, message=u'很遗憾，您本次未抽中任何奖品！')
    return ajax_json.jsonp_ok(request, data={'award': award}, message=u'恭喜获奖，获得%s！' % award_name)