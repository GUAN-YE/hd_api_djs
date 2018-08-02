# coding:utf-8
from com.com_user import need_login
from libs.utils import ajax_json, db, ajax_try
from . import com_stu, probability
from apps.sx_summer import common
from apps.sx_summer.active_cofing import *


@ajax_try({})
@need_login
def p_get_grade(request):
    """
    @api {post} /huodong/sx_summer/s/get_grade [暑假活动 学生]获取所选年级
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
       {}
    @apiSuccessExample {json} 成功返回
        {"message": "", "error": "", "data": {"grade_id": "1"}, "response": "ok", "next": ""}
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    user = request.user

    grade = db.tbkt_web.active_user_book.get(active_id=ACTIVE_ID, user_id=user.old_user_id)
    grade_id = 0
    if grade:
        grade_id = grade.book_id
    return ajax_json.jsonp_ok(request, {'grade_id': grade_id})


@ajax_try({})
@need_login
def p_set_grade(request):
    """
    @api {post} /huodong/sx_summer/s/set_grade [暑假活动 学生]设置年级
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
       {'grade_id':1}
    @apiSuccessExample {json} 成功返回
        {"message": "", "error": "", "data": [], "response": "ok", "next": ""}
    @apiSuccessExample {json} 失败返回
        {
          "message": "已设置过班级，不能重复设置",
          "error": "",
          "data": "",
          "response": "fail",
          "next": ""
        }
    """
    user = request.user
    args = request.QUERY.casts(grade_id=int)
    if not args.grade_id:
        return ajax_json.jsonp_fail(request, error=u'no_grade_Id')
    if args.grade_id not in range(1, 7):
        return ajax_json.jsonp_fail(request, error='wrong_grade_id')
    grade = db.tbkt_web.active_user_book.get(active_id=com_stu.ACTIVE_ID, user_id=user.old_user_id)
    if grade:
        return ajax_json.jsonp_fail(request, message=u'已设置过班级，不能重复设置')
    db.tbkt_web.active_user_book.create(active_id=com_stu.ACTIVE_ID, user_id=user.old_user_id, book_id=args.grade_id)
    return ajax_json.jsonp_ok(request)


@ajax_try({})
@need_login
def add_tea_score(request):
    """
    @api {post} /huodong/sx_summer/s/add_tea_score [暑假活动 学生]学生登录教师加积分
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
       {}
    @apiSuccessExample {json} 成功返回
        {
          "message": "",
          "error": "",
          "data": {}
          "response": "ok",
          "next": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "no_app_id", "data": "", "response": "fail", "next": ""}
    """
    user = request.user
    if user.is_teacher:
        return ajax_json.jsonp_fail(request, message=u"学生用户才能登录")
    tea = com_stu.get_user_tea(user.unit.id) if user.unit else 0
    if not tea:
        return ajax_json.jsonp_ok(request)
    score = STU_LOGIN_SCORE if not user.openstatus(2) else STU_LOGIN_SCORE * 2
    for t in tea:
        num = common.get_score_add_num(APP_ID_TEA, t.id, 'stu_login_%s' % user.id)
        if num:
            return ajax_json.jsonp_ok(request)
        common.add_score(APP_ID_TEA, t.id, score, 'stu_login_%s' % user.id, u'学生%s登录活动,加%s积分' % (user.name, score),
                         t.city or 0)
    return ajax_json.jsonp_ok(request)


user_info_locks = {}


@ajax_try({})
@need_login
def add_open_score(request):
    """
    @api {post} /huodong/sx_summer/s/add_open_score [暑假活动 学生]学生开通加积分
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
       {}
    @apiSuccessExample {json} 成功返回
        {
          "message": "",
          "error": "",
          "data": {
            "add_score":0     # 1 加1000 积分   0 未开通不加积分
          }
          "response": "ok",
          "next": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """

    global user_info_locks
    user = request.user
    if user.is_teacher:
        return ajax_json.jsonp_fail(request, message=u"学生用户才能加分")
    add_score = 0
    if user.id in user_info_locks:
        return ajax_json.jsonp_ok(request, {'add_score': add_score})
    else:
        user_info_locks[user.id] = 1
        try:
            if user.openstatus(2):
                if not db.default.score_user_detail.filter(app_id=APP_ID_STU, user_id=user.id, item_no='open').exists():
                    add_score = 1
                    unit = user.unit.id if user.unit else 0
                    common.add_score(APP_ID_STU, user.id, OPEN_USER_ADD_SCORE, 'open',
                                     u'开通学科获得%s积分' % OPEN_USER_ADD_SCORE,
                                     user.city or 0, unit)
        finally:
            user_info_locks.pop(user.id, None)
    return ajax_json.jsonp_ok(request, {'add_score': add_score})


@ajax_try({})
@need_login
def get_user_info(request):
    """
    @api {post} /huodong/sx_summer/s/user_rank [暑假活动 学生]获取学生 分数和排行
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
       {'grade_id':1}
    @apiSuccessExample {json} 成功返回
        {"message": "", "error": "", "data": {"score": 100, "rank": 2}, "response": "ok", "next": ""}
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    user = request.user
    score, rank = _get_user_rank(user.id, user.city or 0)
    score = 0 if score < 0 else score
    return ajax_json.jsonp_ok(request, {'score': score, 'rank': rank})


def _get_user_rank(user_id, city):
    score_user = db.default.score_user.get(app_id=APP_ID_STU, user_id=user_id)
    rank = 0
    score = 0 if not score_user else score_user.score
    if score_user:
        rank = common.get_user_rank(APP_ID_STU, user_id, score, city)
    return score, rank


@ajax_try({})
@need_login
def user_share(request):
    """
    @api {post} /huodong/sx_summer/s/share [暑假活动 学生]分享
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
       {}
    @apiSuccessExample {json} 成功返回
        {
          "message": "分享成功，加10分",
          "error": "",
          "data": "",
          "response": "ok",
          "next": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "每天只能分享一次", "error": "", "data": "", "response": "fail", "next": ""}
    """
    user = request.user
    if user.is_teacher:
        return ajax_json.jsonp_fail(request, message=u"学生用户才能加分")
    share_num = common.get_score_add_num(APP_ID_STU, user.id, 'share')
    score = SHARE_SCORE
    if share_num < SHARE_NUM:
        unit = user.unit.id if user.unit else 0
        common.add_score(APP_ID_STU, user.id, score, 'share', u'分享', user.city or 0, unit or 0)
        return ajax_json.jsonp_ok(request, message=u'分享成功，加%s分' % score)
    return ajax_json.jsonp_fail(request, message=u"每天只能分享一次")


@ajax_try({})
@need_login
def p_rank(request):
    """
    @api {post} /huodong/sx_summer/s/rank [暑假活动 学生]排行
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
       {
            p:1,
            is_smx: 1       1:是三门峡排行
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
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    args = request.QUERY.casts(p=int, is_smx=int)
    page = args.p
    user = request.user
    is_smx = 1 if user.city and int(user.city) == 411200  else 0
    rank, total = common.get_rank(APP_ID_STU, page or 1, is_smx)
    return ajax_json.jsonp_ok(request, {'rank': rank, 'total': total})


stu_lottery_locks = {}


@ajax_try({})
@need_login
def p_award(request):
    """
    @api {post} /huodong/sx_summer/s/award [暑假活动 抽奖]抽奖
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
       {app_id:35}   35：数学学生     43：语文学生    ,  32：英语学生
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
    if user.is_teacher:
        return ajax_json.jsonp_fail(request, message=u"学生用户才能使用")

    is_smx = 0 if user.city and int(user.city) != 411200 else 1
    args = request.QUERY.casts(app_id=int)
    app_id = args.app_id
    if not app_id or app_id not in ALL_APP_ID:
        return ajax_json.jsonp_fail(request, error='no_app_id')

    if not common.get_active_status(app_id):
        return ajax_json.jsonp_fail(request, message=u'活动已经结束')

    # 判断 是教师还是学生活动 区分范围
    lottery_cost = TEA_LOTTERY_COST
    if app_id in STU_APP_IDS:
        lottery_cost = STU_LOTTERY_COST

    # 判断用户是否有抽奖资格
    # 语文
    if app_id in [YW_APP_ID_TEA, YW_APP_ID_STU]:
        lottery_able = common.get_yuwen_lottery_able(request, app_id, user, lottery_cost)
    else:
        lottery_able = db.default.score_user.filter(app_id=app_id, user_id=user.id,
                                                    score__gte=lottery_cost).exists()

    if not lottery_able:
        return ajax_json.jsonp_ok(request, data={'award': 6}, message=u'您的积分已不足，快去赚积分吧！')
    # 抽奖
    global stu_lottery_locks
    if (user.id, app_id) in stu_lottery_locks:
        return ajax_json.jsonp_fail(request, message=u'手速太快了，请稍后尝试')
    else:
        stu_lottery_locks[(user.id, app_id)] = 1

        try:
            # 获取获奖奖项
            if is_smx:
                award_type = probability.get_smx_user_award_type(user.old_user_id)
            else:
                award_type = probability.get_user_award_type(user.old_user_id)

            # 判断是否开通语文
            if award_type == 4:
                award_type = 0 if probability.get_yw_status(user) else award_type

            # 语文
            if app_id in [YW_APP_ID_STU, YW_APP_ID_TEA]:
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
        finally:
            stu_lottery_locks.pop((user.id, app_id), None)
    if not (award and award_name):
        return ajax_json.jsonp_ok(request, data={'award': 5}, message=u'很遗憾，您本次未抽中任何奖品！')
    return ajax_json.jsonp_ok(request, data={'award': award}, message=u'恭喜获奖，获得%s！' % award_name)


@ajax_try({})
@need_login
def user_award(request):
    """
    @api {post} /huodong/sx_summer/s/award/detail  [暑假活动 抽奖]抽奖详情
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
       {app_id:45}    # 36：教师，  35：学生，
    @apiSuccessExample {json} 成功返回
        {
          "message": "",
          "error": "",
          "data": {
                my_award:['2017年6月23日 22：35',  '精美雨伞一个'...],
                all_award:['张晓燕在抽奖活动中获得精美天堂太阳伞1个'...]
                is_smx: 1    1:表示三门峡获奖情况
                }
          "response": "ok",
          "next": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "no_app_id", "data": "", "response": "fail", "next": ""}
    """
    user = request.user
    is_smx = 0 if user.city and int(user.city) != 411200 else 1
    args = request.QUERY.casts(app_id=int)
    app_id = args.app_id
    if not app_id or app_id not in ALL_APP_ID:
        return ajax_json.jsonp_fail(request, error='no_app_id')
    _app_id = APP_ID_STU
    if app_id in TEA_APP_IDS:
        _app_id = APP_ID_TEA
    my_award = common.get_user_award(_app_id, user.old_user_id, is_smx)
    all_award = common.get_award_detail(_app_id, is_smx)
    data = {
        'my_award': my_award,
        'all_award': all_award,
        'is_smx': is_smx
    }
    return ajax_json.jsonp_ok(request, data)


@ajax_try({})
@need_login
def p_award_result(request):
    """
    @api {post} /huodong/sx_summer/s/award/result [暑假活动 学生]滚动显示 抽奖结果
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
       {
            p:1,
            app_id:35,   #35 学生   36 教师
        }
    @apiSuccessExample {json} 成功返回
        {
          "message": "",
          "error": "",
          "data": {}
          "response": "ok",
          "next": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "no_app_id", "data": "", "response": "fail", "next": ""}
    """
    args = request.QUERY.casts(p=int, app_id=int, is_smx=int)
    page = args.p or 1
    user = request.user
    is_smx = 0 if user.city and int(user.city) != 411200 else 1
    app_id = args.app_id
    if not app_id or app_id not in ALL_APP_ID:
        return ajax_json.jsonp_fail(request, error='no_app_id')
    app_id = args.app_id or APP_ID_STU
    award = common.get_award_detail(app_id, is_smx, page)
    return ajax_json.jsonp_ok(request, award)


def p_award_all(request):
    """
    @api {post} /huodong/sx_summer/s/award/all [暑假活动 学生]活动结果页 抽奖结果
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
       {
            p:1,
            app_id:35,   #35 学生   36 教师
        }
    @apiSuccessExample {json} 成功返回
        {
          "message": "",
          "error": "",
          "data": {}
          "response": "ok",
          "next": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "no_app_id", "data": "", "response": "fail", "next": ""}
    """
    args = request.QUERY.casts(p=int, app_id=int)
    page = args.p or 1
    user = request.user
    is_smx = 0 if user.city and int(user.city) != 411200 else 1
    app_id = args.app_id
    if not app_id or app_id not in ALL_APP_ID:
        return ajax_json.jsonp_fail(request, error='no_app_id')
    app_id = args.app_id or APP_ID_STU
    award,total = common.get_all_award_detail(app_id, is_smx, page)
    return ajax_json.jsonp_ok(request, {'award':award,'total':total})


@ajax_try({})
@need_login
def p_rank_result(request):
    """
    @api {post} /huodong/sx_summer/s/rank/result [暑假活动 学生]活动结果页 排行结果
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
       {
            p:1,
            app_id:35,    35：学生   36：教师
        }
    @apiSuccessExample {json} 成功返回
        {
          "message": "",
          "error": "",
          "data": {}
          "response": "ok",
          "next": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "no_app_id", "data": "", "response": "fail", "next": ""}
    """
    args = request.QUERY.casts(p=int, app_id=int, is_smx=int)
    page = args.p or 1
    user = request.user
    is_smx = 0 if user.city and int(user.city) != 411200 else 1
    app_id = args.app_id
    if not app_id or app_id not in [APP_ID_TEA, APP_ID_STU]:
        return ajax_json.jsonp_fail(request, error='no_app_id')
    rank, _ = common.get_rank(app_id, page or 1, is_smx)
    rank, total = common.add_rank_award(app_id, is_smx, rank)
    if _ < total:
        total = _
    data = {'rank': rank, 'total': total}
    return ajax_json.jsonp_ok(request, data)


@ajax_try({})
@need_login
def p_active_info(request):
    """
    @api {post} /huodong/sx_summer/s/rank/result [暑假活动 学生]活动结果页 排行结果
    @apiGroup sx_summer
    @apiParamExample {json} 请求示例
       {
            p:1,
            app_id:35,    35：学生   36：教师
        }
    @apiSuccessExample {json} 成功返回
        {
          "message": "",
          "error": "",
          "data": {status:True } # True 未结束，False :结束
          "response": "ok",
          "next": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "no_app_id", "data": "", "response": "fail", "next": ""}
    """
    args = request.QUERY.casts(app_id=int)
    app_id = args.app_id
    if not app_id or app_id not in [APP_ID_STU, APP_ID_TEA]:
        return ajax_json.jsonp_fail(request, error='no_app_id')
    status  = common.get_active_status(app_id)
    return ajax_json.jsonp_ok(request, {'status': status})


@ajax_try({})
@need_login
def questionnaire(request):
    """
    :param request:
    :return:  status 1 需要显示
    """
    user = request.user
    question = db.tbkt_web.active_questionnaire.get(user_id=user.id)
    status = 0
    if question:
        if not question.status:
            status = 1
            db.tbkt_web.active_questionnaire.filter(user_id=user.id).update(status=1)
    return ajax_json.jsonp_ok(request, {'status': status})


def test(request):
    num = db.default.score_gift.get(id=688).num
    if num > 0:
        with db.default as c:
            row = c.fetchone_dict("select num from score_gift  where id=688 for update")
            # 判断是否发完
            if row.num == 0:
                return ajax_json.jsonp_ok(request)
            c.execute("update score_gift set num=%s where id=688" % (row.num - 1))
        db.tbkt_web.execute('INSERT INTO `active_award`(user_name,award_type,user_id,active_id)VALUES(1,1,1,66)')
        print num
    return ajax_json.jsonp_ok(request)
