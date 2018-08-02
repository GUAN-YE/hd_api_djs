#coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: stu.py
@time: 2017/8/2 17:31
"""

import datetime, time
import random

from libs.utils import db
from libs.utils import ajax_json, ajax_try
from com.com_user import need_login
from apps.summer_word.common import get_unit_yyteacher
from apps.summer_word import common
from com import com_post

ITEM_NO_MATK = {
                # 'dialog': '学生情景对话',
                # 'task': '学生单词、[作业]气球打地鼠、做练习',
                # 'test': '学生同步练习',
                # 'text': '学生课文跟读、背诵',
                # 'word': '学生气球打地鼠游戏',
                'share': '学生分享活动',
                'login_add_tea_score': '学生登录加教师积分',
                'lottery': '抽奖扣除积分',
                'open_yy': '开通用户+1000',
                'update_city': '+0',     #【废弃】更新city
                }

# config
ACTIVE_ID_STU = 35      # 暑假数学活动主档 三科公共 英语也用这个，用于活动时间判断，抽奖active_id
ACTIVE_ID_TEA = 36      # 暑假数学活动教师主档 三科公共  ，用于活动时间判断，抽奖active_id
APP_ID_STU = 32      # 【学生】积分主档   score_app
APP_ID_TEA = 34      # 【教师】积分主档   score_app
MAX_SCORE_OPENED = 600      # 已开通英语单日积分上限
MAX_SCORE_NOOPEN = 300      # 未开通英语单日积分上限

PAGE_COUNT = 10
LOTTERY_COST = 500    # 抽奖每次消耗积分
TOTAL_SCORE_AWARD = {   # 总积分前十名的奖项
    1: "小米平衡车",
    2: "乐高城市警察系列",
    3: "乐高城市警察系列",
    4: "乐高城市警察系列",
    5: "尤克里里",
    6: "尤克里里",
    7: "尤克里里",
    8: "尤克里里",
    9: "尤克里里",
    10: "尤克里里"
}

def active_auth():
    """
    活动时间6.19--8.31
    :return:
    """
    now = time.time()
    if now >= 1497801600 and now <= 1504195199:             # 在活动时间内
        return True
    return False

def update_score(user, app_id, item_no, add_score):
    """
    更新积分
    :param user:
    :param app_id:
    :param item_no:
    :return:
    """
    if not active_auth():
        return False

    # 用户信息
    open_status = user.openstatus(9)
    user_id = user.id
    school_id = int(user.unit.school_id) if user.unit else 0
    city_id = int(user.city) if user.city != '' else 0

    # 检查用户当天积分是否超过上限。排除开通学科加的1000分情况,排除给老师积分情况,排除抽奖扣分,
    # 排除分享积分（590分时分享不加分还是加到690导致规则漏洞 产品已修正规则）。
    cut_time = time.time()
    ling_time = cut_time - cut_time % 86400
    sql = """ SELECT sum(score) FROM score_user_detail
              WHERE user_id = %s and item_no <> 'open_yy' and item_no <> 'login_add_tea_score' AND item_no <> 'lottery'
              and item_no<>'share' and app_id=%s AND add_date > '%s';""" \
          % (user_id, app_id, ling_time)
    rs = db.slave.fetchone_dict(sql)
    day_score = rs['sum(score)'] if rs['sum(score)'] else 0

    if (open_status==1 and day_score >= MAX_SCORE_OPENED) or (open_status==0 and day_score >= MAX_SCORE_NOOPEN):
        # print '超过当日积分上限'
        return True

    # 查询总积分表
    sql = """ select id, score from score_user
              where user_id=%s and app_id=%s """ \
          % (user_id, app_id)
    rs = db.slave.fetchone_dict(sql)

    score = rs['score'] if rs else 0    # 原始总分
    try:
        if not rs:
            # 第一次积分
            # print '第一次积分 建立主记录'
            sql = """ insert into score_user (user_id,score,app_id,city,unit_id) values (%s,%s,%s,%s,%s)""" \
                    % (user_id, score, app_id, city_id, school_id)
            db.default.execute(sql)

        # 写明细表
        sql = """ INSERT INTO score_user_detail (user_id, item_no, score, remark, add_date, app_id)
                  VALUES (%s, '%s', %s, '%s', '%s', %s); """ \
                    % (user_id, item_no, add_score, ITEM_NO_MATK[item_no], cut_time, app_id)
        # print sql
        num = db.default.execute(sql)

        # 更新总积分表
        new_score = score + add_score
        sql = """ UPDATE score_user SET score = %s, city=%s, unit_id=%s WHERE app_id = %s AND user_id = %s;""" \
              % (new_score, city_id, school_id, app_id, user_id)
        db.default.execute(sql)
    except Exception as e:
        print e, sql

    return True

@ajax_try({})
@need_login
def share(request):
    """
    @api {post} /huodong/summer_word/s/share [暑假活动-学生]分享活动
    @apiGroup summer_word
    @apiParamExample {json} 请求示例
       {}
    @apiSuccessExample {json} 成功返回
       {    "message": "",
        "next": "",
        "data": "分享成功",  or   "今天已经分享一次了"
        "response": "ok",
        "error": ""}
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    # 分享每次100分
    add_score = 100
    item_no = 'share'

    user = request.user
    user_id = user.id
    app_id = APP_ID_STU

    cut_time = time.time()
    ling_time = cut_time - cut_time % 86400
    sql = """ SELECT id FROM score_user_detail
              WHERE user_id = %s AND item_no = '%s' AND app_id=%s AND add_date > '%s';""" \
          % (user_id, item_no, app_id, ling_time)
    # print 'share', sql
    rs = db.slave.fetchone_dict(sql)

    if rs:
        # print '今天已经分享一次了'
        return ajax_json.jsonp_ok(request, u'今天已经分享一次了')

    update_score(user=user, app_id=app_id, item_no=item_no, add_score=add_score)
    return ajax_json.jsonp_ok(request, u'分享成功')

@ajax_try({})
@need_login
def add_tea_score(request):
    """
    @api {post} /huodong/summer_word/s/add_tea_score [暑假活动-学生] 学生进入活动教师加积分
    @apiGroup summer_word
    @apiParamExample {json} 请求示例
       {}
    @apiSuccessExample {json} 成功返回
       {    "message": "没有对应教师" or "今天已经积过分了" or "积分成功", "next": "", "data": "" , response": "ok", "error": ""}
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    user = request.user
    user_id = user.id
    unit_id = user.unit.id if user.unit else 0
    # config
    add_score = 10 if not user.openstatus(9) else 20
    item_no = 'login_add_tea_score'

    # 学生班级找老师
    tea = get_unit_yyteacher(unit_id)
    if not tea:
        return ajax_json.jsonp_ok(request, message='学生班级没有对应科目教师')

    cut_time = time.time()
    ling_time = cut_time - cut_time % 86400

    # 此生当天是否已为老师积过一次分
    sql = """select id from score_user_detail where app_id=%s  and user_id=%s and item_no='%s' and add_date='%s'""" % (
        APP_ID_STU, user_id, item_no, ling_time)
    row = db.slave.fetchone(sql)
    if row:
        return ajax_json.jsonp_ok(request, message='今天已经通过此方式积过分了')

    # 更新学生积分明细 为了查询当天是否积过分
    sql = """ INSERT INTO score_user_detail (user_id, item_no, score, remark, add_date, app_id)
                  VALUES (%s, '%s', %s, '%s', '%s', %s); """ \
          % (user_id, item_no, add_score, ITEM_NO_MATK[item_no], ling_time, APP_ID_STU)
    db.default.execute(sql)

    # 更新教师积分
    user.id = tea.user_id   # 传tea的用户信息
    user.city = tea.city
    update_score(user, APP_ID_TEA, item_no, add_score)
    return ajax_json.jsonp_ok(request, message='积分成功')

@ajax_try({})
@need_login
def index(request):
    """
    @api {post} /huodong/summer_word/s/index [暑假活动-学生]活动首页
    @apiGroup summer_word
    @apiParamExample {json} 请求示例
       {}
    @apiSuccessExample {json} 成功返回
       {
        "message": "",
        "next": "",
        "data": {
            "score": 30,            # 积分
            "rank_no": 3            # 排名
            "open_status": 1            # 英语学科  1开通 0未开通
        },
        "response": "ok",
        "error": ""
        }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    user = request.user
    user_city = int(user.city) if user.city != '' else 0
    school_id = int(user.unit.school_id) if user.unit else 0

    # 首页触发开通学科判断
    add_score = 1000
    item_no = 'open_yy'
    user = request.user
    user_id = user.id
    open_status = user.openstatus(9)
    data = {}

    # 更换地市触发次更新以免积分主档中的city没变查找时被过滤
    sql = """ select city from score_user where app_id=%s and user_id=%s """ % (APP_ID_STU, user_id)
    rs = db.slave.fetchone_dict(sql)

    if rs:
        if int(rs['city']) != user_city:
            sql = """ UPDATE score_user SET city=%s, unit_id=%s WHERE app_id = %s AND user_id = %s;""" \
                  % (user_city, school_id, APP_ID_STU, user_id)
            rs = db.default.execute(sql)
            # print 'update rs:', rs

    opened = 0
    # 开通学科加一次性积分 新建积分主档
    if not db.default.score_user_detail.filter(app_id=APP_ID_STU, user_id=user.id, item_no=item_no).exists():
        if open_status:
            update_score(user, APP_ID_STU, item_no, add_score)
            opened += 1

    # 排名
    # rank_no = cache.user_score_rank.get([user.id, APP_ID_STU])
    smx = 'city = 411200' if user.city=='411200' else 'city<>411200'    # 三门峡
    sql = """ select rank_no,score,city from
                (select S.user_id,S.score, @rownNum:=@rownNum+1 as rank_no, city from
                    (select user_id, score, app_id, city, unit_id from score_user
                    where app_id=%s and %s and user_id <> 0
                    order by score desc) S, (select @rownNum:=0) R
                ) A
                where user_id=%s;""" \
            % (APP_ID_STU, smx, user_id)
    rs = db.slave.fetchone_dict(sql)
    rank_no = rs['rank_no'] if rs else 0
    score = rs['score'] if rs else 0

    data['rank_no'] = int(rank_no)
    data['score'] = score
    data['open_status'] = open_status
    data['opened'] = opened
    return ajax_json.jsonp_ok(request, data)

@ajax_try({})
@need_login
def open_at_once(request):
    """
        @api {post} /huodong/summer_word/s/index/open_at_once [暑假活动-学生]首页 [公共]立即开通点击统计
        @apiGroup summer_word
        @apiParamExample {json} 请求示例
           {app_id=32 # 英语学生32 数学学生35 语文学生43}
        @apiSuccessExample {json} 成功返回
           {
            "message": "",
            "next": "",
            "data": {
                "status": 1
            },
            "response": "ok",
            "error": ""
            }
        @apiSuccessExample {json} 失败返回
           {"message": "缺少app_id 参数", "error": "", "data": "", "response": "fail", "next": ""}
    """
    # 每请求一次记录一次
    data = {}
    user = request.user
    user_id = user.old_user_id

    city_id = int(user.city) if user.city else 0
    active_id = 35
    app_id = request.QUERY.get('app_id', 0)
    if app_id == 0:
        return ajax_json.jsonp_fail(request,error='缺少app_id 参数')
    sql = """ insert into active_summer_open (user_id,city_id, active_id,app_id,add_time) values(%s,%s,%s,%s,%s)""" \
            % (user_id, city_id, active_id, app_id, time.time())
    num = db.tbkt_web.execute(sql)
    if not num:
        return ajax_json.jsonp_fail(error='插入失败')
    data['status'] = 1
    return ajax_json.jsonp_ok(request, data)

@ajax_try({})
@need_login
def user_rank(request):
    """
       @api {post} /huodong/summer_word/s/user_rank [暑假活动-学生]所有用户排名
       @apiGroup summer_word
       @apiParamExample {json} 请求示例
          {"page_no": 1}           # 每次请求10条
       @apiSuccessExample {json} 成功返回
          {
           "message": "",
           "next": "",
            "data": {
               "rank_info": [
                       {
                           "user_name": "小明",
                           "score": 30,
                           "school_name": "创恒中学"
                       },{},...
                   ],
               "page_num":20
           },
           "response": "ok",
           "error": ""
           }
       @apiSuccessExample {json} 失败返回
          {"message": "", "error": "", "data": "", "response": "缺少page_no参数", "next": ""}
   """
    user = request.user

    page_no = request.QUERY.get('page_no')
    if not page_no:
        return ajax_json.ajax_fail(error='缺少page_no参数')
    else:
        page_no = int(page_no)

    smx = 'city = 411200' if user.city == '411200' else 'city<>411200'  # 三门峡411200

    # 那一页的学生id和分数
    sql = """ select user_id, score, city, unit_id as school_id from score_user
              where app_id=%s and user_id <> 0 and %s
              order by score desc limit %s,%s  """ \
          % (APP_ID_STU, smx, (page_no - 1) * PAGE_COUNT, PAGE_COUNT)  # limit 10,5  检索第11-16
    rs = db.slave.fetchall_dict(sql)
    if not rs:
        return ajax_json.jsonp_ok(request, {"rank_info":[]})

    # 获取名字,学生身份
    user_name_dict, stu_ids = common.get_users_name([int(r.user_id) for r in rs], 1)
    for r in rs:
        r.real_name = user_name_dict.get(int(r.user_id), '')

    # 学生id查学校名和姓名
    rank_user_id_list = []
    for r in rs:
        rank_user_id_list.append(int(r['user_id']))     # 大量未登陆用户user_id=0,在where in user_id_list中导致慢查询！

    sql2 = """
        select user_id, school_id, school_name from mobile_order_region
        where unit_class_id >0 and is_update = 0 and user_id > 0 and user_id in({});
    """.format(','.join(str(r) for r in rank_user_id_list))
    rs2 = db.ketang_slave.fetchall_dict(sql2)

    data = {'rank_info': []}
    data['page_no'] = page_no
    data['page_num'] = int(len(rs2) / PAGE_COUNT) + 1
    for r in rs:
        flag = 0
        for r2 in rs2:
            if r['user_id'] == r2['user_id']:
                data['rank_info'].append(dict(user_name=r['real_name'], score=r['score'], school_name=r2['school_name']))
                flag = 1
        if flag == 0:   # 没有加入班级的没有学校名
            data['rank_info'].append(dict(user_name=r['real_name'], score=r['score'], school_name=''))

    return ajax_json.jsonp_ok(request, data)

@ajax_try({})
@need_login
def award_my_score(request):
    """
        @api {post} /huodong/summer_word/s/award/my_score [暑假活动-学生]抽奖 用户自己总积分和可用抽奖次数
        @apiGroup summer_word
        @apiParamExample {json} 请求示例
           {}
        @apiSuccessExample {json} 成功返回
           {
            "message": "",
            "next": "",
            "data": {
                "score": 1140,            # 总积分  没有积分0
                "times": 3            # 可以抽奖的次数    没有次数0
            },
            "response": "ok",
            "error": ""
            }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    data = {}
    score = 0
    times = 0

    user = request.user
    user_id = user.id

    sql = """ SELECT user_id,score,app_id,city,unit_id FROM score_user where app_id=%s and user_id=%s;""" \
        % (APP_ID_STU, user_id)
    rs = db.slave.fetchone_dict(sql)
    if rs:
        score = rs['score']
        times = int(score / LOTTERY_COST)
    else:
        pass

    data['score'] = score
    data['times'] = times
    return ajax_json.jsonp_ok(request, data)

@ajax_try({})
@need_login
def award_my_award(request):
    """
        @api {post} /huodong/summer_word/s/award/my_award [暑假活动-学生]抽奖 我的奖品列表
        @apiGroup summer_word
        @apiParamExample {json} 请求示例
           {}
        @apiSuccessExample {json} 成功返回
           {
            "message": "",
            "next": "",
            "data": {
                "user_id": 405365,
                "user_name": "张笑",
                "award_list":[
                    {
                        "award_type": 4            # 1ipad    2卡通文具套盒  3卡通文具袋  4学科免费体验1个月  5谢谢参与
                        "award_type": "语文学科体验一个月"
                        "add_time":"1496668496"        # 获奖时间        时间戳格式
                    },{},{}, ...
                ]
            },
            "response": "ok",
            "error": ""
            }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    data = {}
    user_name = ''
    award_list = []

    user = request.user
    user_id = user.old_user_id          # 老的user_id

    sql = """ SELECT user_id,user_name, award_type, award_name, add_time FROM active_award
              where user_id=%s and active_id=%s and award_type<> %s
              order by add_time desc""" \
              % (user_id, ACTIVE_ID_STU, 5)     # app_id公用奖池 表中active_id实存app_id 排除type5谢谢参与
    rs = db.tbkt_web_slave.fetchall_dict(sql)
    if rs:
        user_name = rs[0]['user_name']
        for r in rs:
            add_time = time.strftime('%m月%d日 %H:%M:%S', time.localtime(r['add_time']))
            award_list.append(dict(award_type=r['award_type'], award_name=r['award_name'], add_time=add_time))
    else:
        pass

    data['user_name'] = user_name
    data['award_list'] = award_list
    return ajax_json.jsonp_ok(request, data)

@ajax_try({})
@need_login
def award_won_list(request):
    """
        @api {post} /huodong/summer_word/s/award/won_list [暑假活动-学生] 轮播已获奖名单 取最近获得的
        @apiGroup summer_word
        @apiParamExample {json} 请求示例
           {}
        @apiSuccessExample {json} 成功返回
           {
            "message": "",
            "next": "",
            "data": {
                "won_list": [
                    {"user_name": "杨铮",
                    "award_name": "文具套装"     # 奖品名称
                    },{},{}, ...
                ]
            },
            "response": "ok",
            "error": ""
            }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    data = {}
    won_list = []
    user = request.user
    user_city = int(user.city) if user.city!='' else 0

    sql = """ select user_name, award_name from active_award
              where award_type <> 5 and city<>411200 and active_id=35 and remark='32'
              order by add_time desc limit 0,10 ;"""
    if user_city == 411200:  # 三门峡
        sql = """ select user_name, award_name from active_award
                      where award_type <> 5 and city=411200 and active_id=35 and remark='32'
                      order by add_time desc limit 0,10 ;"""
    rs = db.tbkt_web_slave.fetchall_dict(sql)
    if not rs:
        return ajax_json.jsonp_ok(request,data={'won_list':[]})

    for r in rs:
        won_list.append(dict(user_name=r['user_name'], award_name=r['award_name']))
    data['won_list'] = won_list
    return ajax_json.jsonp_ok(request,data)

@ajax_try({})
@need_login
def total_score_rank(request):
    """
        @api {post} /huodong/summer_word/s/result/total_score_rank [暑假活动-学生]结束页 积分获奖名单
        @apiGroup summer_word
        @apiParamExample {json} 请求示例
           { page_no=1 }
        @apiSuccessExample {json} 成功返回
           {
            "message": "",
            "next": "",
            "data": {
                "page_no": 1,       # 当前页
                "rank_info": [
                    {"user_name": "杨铮",
                    "award_name": "小米平衡车",
                    "rank_no": 1,
                    "school_name": "创恒中学",
                    },{},{}, ...
                ]
            },
            "response": "ok",
            "error": ""
            }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    # 共一等奖*1 二等奖*3 三等奖*6 前十名获奖
    data = {'rank_info':[]}
    user = request.user

    smx = 'city = 411200' if user.city == '411200' else 'city<>411200'  # 三门峡411200
    # 分数前10
    sql = """ select user_id, score, city, unit_id as school_id from score_user
                  where app_id=%s and %s
                  order by score desc limit %s,%s  """ \
          % (APP_ID_STU, smx, 0, 10)  # limit 10,5  检索第11-16
    rs = db.slave.fetchall_dict(sql)

    # 获取名字,学生身份
    user_name_dict, stu_ids = common.get_users_name([int(r.user_id) for r in rs], 1)
    for r in rs:
        r.real_name = user_name_dict.get(int(r.user_id), '')

    # userid查学校名
    rank_user_id_list = [int(r['user_id']) for r in rs if rs]
    sql2 = """
        select user_id, school_id, school_name from mobile_order_region
        where unit_class_id >0 and is_update = 0 and user_id > 0 and user_id in({});
    """.format(','.join(str(r) for r in rank_user_id_list))
    rs2 = db.ketang_slave.fetchall_dict(sql2)
    for n, r in enumerate(rs):
        award_type = n+1
        award_name = TOTAL_SCORE_AWARD.get((n+1), '')
        school_name = ''  # 没有加入班级的学校名空
        for r2 in rs2:
            if r['user_id'] == r2['user_id']:
                school_name = r2['school_name']
                continue
        data['rank_info'].append(dict(user_name=r['real_name'], score=r['score'], award_name=award_name,
                                      award_type=award_type, school_name=school_name))
    return ajax_json.jsonp_ok(request, data)

@ajax_try({})
@need_login
def draw_lottery_rank(request):
    """
        @api {post} /huodong/summer_word/s/result/draw_lottery_rank [暑假活动-学生]结束页 抽奖获奖名单
        @apiGroup summer_word
        @apiParamExample {json} 请求示例
           {page_no=1}
        @apiSuccessExample {json} 成功返回
           {
            "message": "",
            "next": "",
            "data": {
                "rank_info": [      # 请求的那一页为空的话，"rank_info":[]
                    {"user_name": "杨铮",
                    "award_type": 2
                    "award_name": "宝视达护眼"     # 奖品名称
                    "school_name":"穿各行中学"
                    },{},{}, ...
                ]
            },
            "response": "ok",
            "error": ""
            }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    page_no = int(request.QUERY.get('page_no', '1'))
    data = {'rank_info': []}
    user = request.user

    # 那一页的用户。 按一等奖、二等奖排序 过滤谢谢参与
    smx = 'city = 411200' if user.city == '411200' else 'city<>411200'  # 三门峡411200
    sql = """ SELECT user_id,user_name,award_name,award_type,city
              FROM active_award where active_id=35 and remark=%s and award_type<>5 and %s
              order by award_type limit %s, %s; """\
          % (APP_ID_STU, smx, (page_no - 1) * PAGE_COUNT, PAGE_COUNT )
    rs = db.tbkt_web_slave.fetchall_dict(sql)
    if not rs:
        return ajax_json.jsonp_ok(request, data={'rank_info': []})

    # userid查学校名
    rank_user_id_list = [int(r['user_id']) for r in rs]         # 老的user_id集合
    # new_user_id_list_dict = com_post.batch_conversion_id(rank_user_id_list)      # 新的user_id的集合
    # new_user_id_list = [int(t) for t in new_user_id_list_dict.keys()]

    sql2 = """
            select user_id, school_id, school_name from mobile_order_region
            where unit_class_id >0 and is_update = 0 and user_id > 0 and user_id in({});
        """.format(','.join(str(obj) for obj in rank_user_id_list))
    rs2 = db.ketang_slave.fetchall_dict(sql2)

    for n, r in enumerate(rs):
        award_name = r['award_name']
        award_type = r['award_type']
        school_name = ''  # 没有加入班级的学校名空
        for r2 in rs2:
            if r['user_id'] == r2['user_id']:
                school_name = r2['school_name']
                continue
        data['rank_info'].append(dict(user_name=r['user_name'], award_name=award_name,
                                      award_type=award_type, school_name=school_name))
    return ajax_json.jsonp_ok(request, data)