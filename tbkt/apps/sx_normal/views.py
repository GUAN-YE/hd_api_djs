# coding:utf-8
from com import com_award
from com.com_user import need_login
from libs.utils import ajax, ajax_json, ajax_try, Struct, db
from . import common
STU_LOTTERY_COST = 1000
TEA_LOTTERY_COST = 2000

STU_ACTIVE_ID = 8
TEA_ACTIVE_ID = 9


def base(request):
    user = request.user
    active_id = STU_ACTIVE_ID
    if user.is_teacher:
        active_id = TEA_ACTIVE_ID
    return user, active_id


@ajax_try({})
@need_login
def r_info(request):
    """
    @api /huodong/sx/normal/com/info [数学常态活动]积分信息 
    @apiGroup math_normal
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "score": 0,   # 用户积分
            "num": 0,
            "top": 0
        },
        "response": "ok",
        "error": ""
    }
    """
    user, active_id = base(request)
    out = Struct()
    out.open_add = -1
    if user.type == 1:
        out.open_add = common.stu_open_add_score(user)

    info = common.get_user_score(user, active_id)
    out.score = info.score
    cost = TEA_LOTTERY_COST if user.is_teacher else STU_LOTTERY_COST
    out.num = info.score/cost
    out.top = info.rank_no
    out.user_id=user.id
    out.is_teacher = user.is_teacher
    return ajax_json.jsonp_ok(request, out)


@ajax_try({})
@need_login
def r_score_detail(request):
    """
    @api /huodong/sx/normal/com/score/detail [数学常态活动]积分详情
    @apiGroup math_normal
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
    user, active_id = base(request)
    args = request.QUERY.casts(p=int)
    page = args.p or 1
    data = common.user_score_detail(user, active_id, page)
    return ajax.jsonp_ok(request, data)


@ajax_try({})
@need_login
def r_award_info(request):
    """
    @api /huodong/sx/normal/com/award/display [数学常态活动]奖品信息
    @apiGroup math_normal
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": [
            {
                "num": 3,  # 奖品数量
                "sequence": 1,  # 几等奖
                "end_num": 0,     
                "active_type": 1, # 奖品类型 1抽奖奖品 2排名奖品
                "start_num": 0,   
                "active_id": 1,  # 活动id
                "img_url": "http://file.tbkt.cn/upload_media/knowledge/img/2015/09/21/20150921113843806676.png",
                "active_name": "ipad"   # 奖品名字
            }
        ],
        "response": "ok",
        "error": ""
    }
    """
    user, active_id = base(request)
    data = com_award.show_award(active_id)
    return ajax.jsonp_ok(request, data)


@ajax_try({})
@need_login
def r_score_rank(request):
    """
    @api /huodong/sx/normal/score/ranks [数学常态活动]河南积分排名
    @apiGroup math_normal
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": [
            {
                "city": "411700",
                "score": 1082111,
                "user_id": 405269,
                "portrait": "portrait/2017/09/09/2017090915481764690.png",
                "school_name": "创恒中学",
                "real_name": "呃呃呃呃"
            }
        ],
        "response": "ok",
        "error": ""
    }
    
    * 显示登录身份的排名
    """
    args = request.QUERY.casts(p=int)
    page_no = args.p or 1
    user = request.user
    active_id = 1
    if user.is_teacher:
        active_id = 2
    data = common.score_rank(active_id, page_no)
    return ajax.jsonp_ok(request, data)


@ajax_try({})
@need_login
def r_award_winner(request):
    """
    @api /huodong/sx/normal/award/winner [数学常态活动] 河南抽奖排名
    @apiGroup math_normal
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": [
            {
                "award_name": "ipad",
                "user_id": 591113,
                "city": "410400",
                "portrait": "portrait/2017/09/09/2017090918151214417.png",
                "school_name": "平顶山市卫东区矿工路小学",
                "real_name": "啊啊啊"
            }
        ],
        "response": "ok",
        "error": ""
    }

    * 显示登录身份的排名
    """
    args = request.QUERY.casts(p=int)
    page_no = args.p or 1

    user = request.user
    active_id = 1
    if user.is_teacher:
        active_id = 2

    data = common.award_winner(active_id, page_no)
    return ajax.jsonp_ok(request, data)


@ajax_try({})
@need_login
def r_class_rank(request):
    """
    @api /huodong/sx/normal/class/ranks [数学常态活动]班级排名
    @apiGroup math_normal
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": [
            {
                "phone": "13900000000",
                "score": 280,
                "is_open": 1,
                "portrait": "https://file.m.tbkt.cn/upload_media/portrait/2015/05/26/20150526191718620086.png",
                "user_name": "赵勇铮",
                "id": 383892
            }
        ],
        "response": "ok",
        "error": ""
    }
    """
    user = request.user
    args = request.QUERY.casts(unit_id=int)
    unit_id = args.unit_id
    if not unit_id:
        unit_id = user.units[0].id
    data = common.class_stu_rank(user, unit_id, STU_ACTIVE_ID)
    return ajax.jsonp_ok(request, data)
