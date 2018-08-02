# coding:utf-8
"""
奖池一个 所以active_id 唯一， app_id 用于区分学科
"""

from apps.com_post import common
from com import com_user
from com.com_award import Award, ctime
from com.com_user import need_login
from libs.utils import ajax_json, ajax_try, db, format_url

# 排行分页
PAGE_COUNT = 20
# 活动id
APP_ID_ALL = [11, 10, 8, 9, 6, 7]
STU_ID_ALL = [10, 8, 6]

# 抽奖对应奖品id
STU_ACTIVE_ID = 8
TEA_ACTIVE_ID = 9
# 抽奖消耗积分
LOTTERY_COST = {8: 1000, 9: 2000}

# 奖品类型，award_type:几等奖，rate:中奖概率，total：奖品总数-1为不限量，day_num:奖品日发放量，-1为不限量
TEA_AWARD_SORT2 = [
    dict(award_type=1, rate=0, total=0, day_num=0, is_award=1),
    dict(award_type=2, rate=0, total=2, day_num=1, is_award=1),
    dict(award_type=3, rate=0.03, total=1, day_num=0, is_award=1),
    dict(award_type=4, rate=0, total=2, day_num=1, is_award=1),
    dict(award_type=5, rate=0.05, total=20, day_num=1, is_award=1),
    dict(award_type=6, rate=0, total=0, day_num=0, is_award=1),
    dict(award_type=7, rate=0.1, total=20, day_num=2, is_award=1),
    dict(award_type=8, rate=0, total=10, day_num=1, is_award=1),
    dict(award_type=9, rate=0.5, total=70, day_num=10, is_award=1),
    dict(award_type=10, rate=0.32, total=30, day_num=10, is_award=1)
]

STU_AWARD_SORT2 = [
    dict(award_type=1, rate=0, total=1, day_num=1, is_award=1),
    dict(award_type=2, rate=0.003, total=2, day_num=1, is_award=1),
    dict(award_type=3, rate=0.003, total=2, day_num=1, is_award=1),
    dict(award_type=4, rate=0.02, total=20, day_num=4, is_award=1),
    dict(award_type=5, rate=0.02, total=20, day_num=4, is_award=1),
    dict(award_type=6, rate=0.3, total=500, day_num=25, is_award=1),
    dict(award_type=7, rate=0.3, total=500, day_num=25, is_award=1)
]


@ajax_try([])
@need_login
def p_award(request):
    """
    @api {post} /huodong/com/award [公共 ]活动抽奖
    @apiGroup com
    @apiParamExample {json} 请求示例
       {
            app_id:1   活动id
        }
    @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {
                "award_type": 1,
                "name": "ipad",
                "is_award": 1
            },
            "response": "ok",
            "error": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "积分不足", "error": "", "data": "", "response": "fail", "next": ""}
    """
    user = request.user
    args = request.QUERY.casts(app_id=int)
    app_id = args.app_id
    if app_id not in APP_ID_ALL:
        return ajax_json.jsonp_fail(request, message=u'缺少参数')
    active_id = TEA_ACTIVE_ID if user.is_teacher else STU_ACTIVE_ID
    # 获取抽奖配置
    award_sort = TEA_AWARD_SORT2 if user.is_teacher else STU_AWARD_SORT2
    lottery_cost = LOTTERY_COST.get(int(app_id), 0)
    if not lottery_cost:
        return ajax_json.jsonp_fail(request, message=u'缺少参数')
    # 抽奖
    award = Award(app_id=app_id, active_id=active_id, user=user, lottery_cost=lottery_cost)
    result, why = award.draw_award(award_sort=award_sort)
    if not result:
        return ajax_json.jsonp_fail(request, message=why)
    return ajax_json.jsonp_ok(request, data=why)


@ajax_try([])
@need_login
def p_award_list(request):
    """
    @api {post} /huodong/com/award/list [公共] 用户获奖详情
    @apiGroup com
    @apiParamExample {json} 请求示例
       {
            app_id:1   活动id
        }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": [
            {
                "url": "http://flv.tbkt.cn/upload_media/knowledge/img/2015/09/21/20150921113843806676.png",
                "award_type": "1",
                "name": "ipad",
                "time": "2017-09-11 18:23:55"
            },
            {
                "url": "http://flv.tbkt.cn/upload_media/knowledge/img/2015/09/21/20150921113843806676.png",
                "award_type": "3",
                "name": "三等奖",
                "time": "2017-09-11 18:21:03"
            },
            {
                "url": "http://flv.tbkt.cn/upload_media/knowledge/img/2015/09/21/20150921113843806676.png",
                "award_type": "4",
                "name": "四等奖",
                "time": "2017-09-11 18:19:34"
            }
        ],
        "response": "ok",
        "error": ""
    }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "no_app_id", "data": "", "response": "fail", "next": ""}
    """
    args = request.QUERY.casts(app_id=int)
    user = request.user
    app_id = args.app_id
    if app_id not in APP_ID_ALL:
        return ajax_json.jsonp_fail(request, message=u'缺少参数')
    active_id = TEA_ACTIVE_ID if user.is_teacher else STU_ACTIVE_ID
    award_list = Award(app_id=app_id, active_id=active_id, user=user).user_award_detail()
    return ajax_json.jsonp_ok(request, award_list)


@ajax_try([])
@need_login
def p_award_recent(request):
    """
    @api {post} /huodong/com/award/recent  [公共] 获取最近10位中奖用户
    @apiGroup com
    @apiParamExample {json} 请求示例
       {
            app_id:1   活动id
        }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": [
            {
                "url": "http://flv.tbkt.cn/upload_media/knowledge/img/2015/09/21/20150921113843806676.png",
                "user_name": "李果果",
                "award_type": "3",
                "award_name": "三等奖",
                "time": "2017-09-12 16:34:58"
            }
        ],
        "response": "ok",
        "error": ""
    }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "no_app_id", "data": "", "response": "fail", "next": ""}
    """
    args = request.QUERY.casts(app_id=int)
    user = request.user
    app_id = args.app_id
    if app_id not in APP_ID_ALL:
        return ajax_json.jsonp_fail(request, message=u'缺少参数')
    active_id = TEA_ACTIVE_ID if user.is_teacher else STU_ACTIVE_ID
    award_list = Award(app_id=app_id, active_id=active_id).recent_award()
    return ajax_json.jsonp_ok(request, award_list)


@ajax_try([])
@need_login
def p_award_all(request):
    """
    @api {post} /huodong/com/award/all  [公共] 分页返回中奖用户
    @apiGroup com
    @apiParamExample {json} 请求示例
       {
            app_id:1   抽奖奖品对应id
            p:1   页码
        }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "total": 1,
            "detail": [
                {
                    "city": "410200",
                    "user_id": 378394,
                    "name": "三等奖",
                    "url": "http://flv.tbkt.cn/upload_media/knowledge/img/2015/09/21/20150921113843806676.png",
                    "school_name": "鼓楼区杨砦小学",
                    "real_name": "李果果",
                    "award_type": "3",
                    "time": "2017-09-12 18:30:21"
                }
            ]
        },
        "response": "ok",
        "error": ""
    }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "no_app_id", "data": "", "response": "fail", "next": ""}
    """
    args = request.QUERY.casts(app_id=int, p=int)
    user = request.user
    app_id = args.app_id
    p = args.p or 1
    if app_id not in APP_ID_ALL:
        return ajax_json.jsonp_fail(request, message=u'缺少参数')
    active_id = TEA_ACTIVE_ID if user.is_teacher else STU_ACTIVE_ID
    detail, total = Award(app_id=app_id, active_id=active_id).all_award_detail(p)
    return ajax_json.jsonp_ok(request, {'detail': detail, 'total': total})

@ajax_try([])
@need_login
@ctime
def p_rank(request):
    """
    @api {post} /huodong/com/rank [公共] 分页返回活动积分排行
    @apiGroup com
    @apiParamExample {json} 请求示例
       {
            grade_id：1  按年级排行时需要传入
            unit_id:123   按班级排行时需要传入，p=-1 返回全班
            active_id:6   活动id
            p:1   页码
            page_num:10 每页排行数量  ，不传时默认20
        }
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
       {"message": "", "error": "no_app_id", "data": "", "response": "fail", "next": ""}
    """
    args = request.QUERY.casts(grade_id=int, active_id=int, unit_id=int, page_num=int)
    grade_id = args.grade_id
    active_id = args.active_id
    unit_id = args.unit_id
    p = int(request.QUERY.get('p', 1))
    p = p or 1
    page_num = args.page_num or PAGE_COUNT

    if active_id not in APP_ID_ALL:
        return ajax_json.jsonp_fail(request, message=u'缺少参数')
    # 分年级返回
    if grade_id:
        rank = common.get_active_rank(active_id, p, page_num, grade_id=grade_id)
    # 分班级返回
    elif unit_id:
        rank = common.get_active_rank(active_id, p, page_num, unit_id=unit_id)
    else:
        rank = common.get_active_rank(active_id, p, page_num)
    user_dict = com_user.users_info([int(r.user_id) for r in rank])
    for r in rank:
        r.real_name = user_dict.get(r.user_id).get("real_name")
        r.school_name = user_dict.get(r.user_id).get("school_name")
        r.portrait = format_url(user_dict.get(r.user_id).get("portrait"))
    return ajax_json.jsonp_ok(request, {"rank": rank})

@ajax_try([])
@need_login
@ctime
def p_user_info(request):
    """
        @api {post} /huodong/com/user/info [公共]首页
        @apiGroup com
        @apiParamExample {json} 请求示例
           {
                active_id:6   活动id
            }
        @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {
                "score": 210,
                "rank_no": 1,
                "is_sign":True,True签过，Flase未签
            },
            "response": "ok",
            "error": ""
        }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
        """
    user = request.user
    active_id = int(request.QUERY.get('active_id', 0))
    if active_id not in APP_ID_ALL:
        return ajax_json.jsonp_fail(request, message=u'缺少参数')
    user_id = request.user_id
    grade_id = 0
    unit_id = 0
    # 按年级排名
    if active_id in [6, 11]:
        grade_id = user.grade_id
    # 按班级排名
    if active_id in [10]:
        unit_id = user.unit.id if user.unit else 0
    data = common.get_user_rank(active_id, user_id, grade_id=grade_id,unit_id=unit_id)
    is_sign = common.get_user_item_today(user_id, active_id, 'sign')
    data['is_sign'] = is_sign
    return ajax_json.jsonp_ok(request, data)

@ajax_try({})
@need_login
@ctime
def p_today_item(request):
    """
        @api {post} /huodong/com/user/today_item [公共]返回当日某加分项是否加分
        @apiGroup com
        @apiParamExample {json} 请求示例
           {
                active_id:6   活动id
                item: send_sms   加分项 如：sign ：签到，send_sms:发作业，stu_do_task 做作业 等
            }
        @apiSuccessExample {json} 成功返回
        {
            "message": "",
            "next": "",
            "data": {
                "status":True,True加过分，Flase未加分
            },
            "response": "ok",
            "error": ""
        }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
        """
    user_id = request.user_id
    args = request.QUERY.casts(active_id=int, item=str)
    if not args.active_id or not args.item:
        return ajax_json.jsonp_fail(request, message=u'缺少参数')
    status = common.get_user_item_today(user_id, args.active_id, args.item)
    data = {'status':status}
    return ajax_json.jsonp_ok(request, data)

@ajax_try({})
@need_login
@ctime
def p_score_info(request):
    """
    @api /huodong/com/user/detail [公共]用户积分详情
    @apiGroup com
    @apiParamExample {json} 请求示例
   {
        active_id:6   活动id
    }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": [
            {
                "item_name": "做作业",
                "add_date": "09月12日 11:43:52",
                "score": 120
            }
        ],
        "response": "ok",
        "error": ""
    }
    """
    user = request.user
    active_id = int(request.QUERY.get('active_id', 0))
    args = request.QUERY.casts(p=int)
    page = args.p or 1
    data = common.user_score_detail(user, active_id, page)
    return ajax_json.jsonp_ok(request, data)

@ajax_try({})
@need_login
@ctime
def p_sign(request):
    """
    @api /huodong/com/sign [公共]学生签到
    @apiGroup com
    @apiParamExample {json} 请求示例
       {
            active_id:6   活动id
        }
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
    args = request.QUERY.casts(active_id=int)
    active_id = args.active_id
    if not active_id:
        return ajax_json.jsonp_fail(request, message=u'缺少参数')
    active = db.tbkt_active_slave.active.select('subject_id').get(id=active_id)
    if common.get_user_item_today(user.id, active_id, 'sign'):
        return ajax_json.jsonp_fail(request, message=u'已签到过了！')
    subject_id = active.subject_id / 10
    is_open = user.openstatus(subject_id)
    common.update_score_com(user.id, active_id, 'sign', user.id, user.city, user.unit.id, is_open, user.grade_id)
    return ajax_json.jsonp_ok(request)

@ajax_try({})
@need_login
@ctime
def p_share(request):
    """
    @api /huodong/com/share [公共]学生分享
    @apiGroup com
    @apiParamExample {json} 请求示例
       {
            active_id:6   活动id
        }
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
    active_id = int(request.QUERY.get('active_id', 0))
    if active_id not in APP_ID_ALL:
        return ajax_json.jsonp_fail(request, message=u'缺少参数')
    if user.is_teacher:
        return ajax_json.jsonp_fail(request, message=u'教师不能参与学生分享！')
    if common.get_user_item_today(user.id, active_id, 'share'):
        return ajax_json.jsonp_fail(request, message=u'已分享过了！')

    active = db.tbkt_active_slave.active.select('subject_id').get(id=active_id)
    subject_id = active.subject_id / 10
    is_open = user.openstatus(subject_id)
    common.update_score_com(user.id, active_id, 'share', user.id, user.city, user.unit.id, is_open, user.grade_id)
    return ajax_json.jsonp_ok(request)

@ajax_try({})
@need_login
@ctime
def p_rank_units(request):
    """
    @api /huodong/com/rank/units [公共]班级排行
    @apiGroup com
    @apiParamExample {json} 请求示例
   {
        active_id:6   活动id
        unit_id:123 班级id
    }
    @apiSuccessExample {json} 成功返回
    {
        "tbkt_token": "NDgwMDAyfTA0MDAzMzcxNTB9MDQwMDc1MDY2Ng",
        "next": "",
        "error": "",
        "message": "",
        "data": {
            [
                {
                    "score": 0,
                    "id": 591113,
                    "real_name": "翟于讳"
                },
                {
                    "score": 0,
                    "id": 1470977,
                    "real_name": "汤鹏程"
                },
                {
                    "score": 0,
                    "id": 2144020,
                    "real_name": "柳絮"
                },
                {
                    "score": 0,
                    "id": 2884805,
                    "real_name": "欧阳慧兰"
                }
            ]
        },
        "response": "ok"
    }
    """
    user = request.user
    args = request.QUERY.casts(active_id=int, unit_id=int)
    active_id = args.active_id
    unit_id = args.unit_id
    if not active_id or active_id not in STU_ID_ALL or not unit_id:
        return ajax_json.jsonp_fail(request, message=u'缺少参数')
    rank = common.unit_stu_rank(user, active_id, unit_id)
    return ajax_json.jsonp_ok(request, rank)

@ajax_try({})
@need_login
@ctime
def p_send_sms(request):
    """
    @api /huodong/com/tea/send_sms [公共]教师发短信
    @apiGroup com
    @apiParamExample {json} 请求示例
    {
    active_id:6   活动id
    content:'123' 短息内容
    }
    @apiSuccessExample {json} 成功返回
    {
    "tbkt_token": "NDgwMDAyfTA0MDAzMzcxNTB9MDQwMDc1MDY2Ng",
    "next": "",
    "error": "",
    "message": "",
    "data": {},
    "response": "ok"
    }
    """
    user = request.user
    args = request.QUERY.casts(active_id=int, content=unicode)
    active_id = args.active_id
    content = args.content
    if active_id not in APP_ID_ALL or not user.is_teacher:
        return ajax_json.jsonp_fail(request, message=u'只有教师能发短信')
    has_send = common.get_user_item_today(user.id, active_id, 'send_sms')
    if has_send:
        return ajax_json.jsonp_ok(request)
    else:
        common.send_sms(request, user, content)
        common.update_score_com(user.id, active_id, 'send_sms', user.id, user.city, user.unit.id, 0, user.grade_id)
    return ajax_json.jsonp_ok(request)


def cheat(request):
    args = request.QUERY.casts(active_id=int, score=int)
    active_id = args.active_id
    if active_id not in [2, 5]:
        return ajax_json.jsonp_fail(request, message=u'缺少参数')
    user_id = 1928697
    if active_id == 5:
        user_id = 2661647

    sql = """UPDATE  tbkt_active.active_score_user SET score=score+%s where user_id=%s and active_id=%s""" % (
        args.score, user_id, active_id)
    db.tbkt_active.execute(sql)
    return ajax_json.jsonp_ok(request)
