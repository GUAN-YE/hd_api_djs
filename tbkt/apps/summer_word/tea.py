#coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: tea.py
@time: 2017/8/3 9:27
"""

import datetime, time
import random

from libs.utils import db
from libs.utils import ajax_json, ajax_try
from com.com_user import need_teacher
from libs.utils import tbktapi
from apps.summer_word import common
from com import com_post

ITEM_NO_MATK = {        # 积分方式标识 说明
                # 'dialog': '学生情景对话',
                # 'task': '学生单词、[作业]气球打地鼠、做练习',
                # 'test': '学生同步练习',
                # 'text': '学生课文跟读、背诵',
                # 'word': '学生气球打地鼠游戏',
                'share': '学生分享活动',
                'lottery': '抽奖扣除积分',
                'send_sms': '教师发活动短信',
                'send_open': '教师发开通短信',
                'update_city': '+0',     #【废弃】更新city
                }

# config
ACTIVE_ID_STU = 35      # 前端入口控制、后端没做判断 各科一样用数学的  活动主档学生  tbkt_web.active
ACTIVE_ID_TEA = 36      # 活动主档教师  tbkt_web.active
APP_ID_STU = 32      # 【教师】积分主档   tbkt.score_app
APP_ID_TEA = 34      # 【教师】积分主档   tbkt.score_app


PAGE_COUNT = 10
LOTTERY_COST_TEA = 1000    # 教师抽奖每次消耗积分
TOTAL_SCORE_AWARD = {   # 总积分前十名的奖项
    1: "美的遥控塔扇",        # 1个
    2: "志高熨烫机",         # 5个
    3: "精美天堂太阳伞"       # 30个
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
    user_id = user.id
    school_id = int(user.unit.school_id) if user.unit else 0
    city_id = int(user.city) if user.city != '' else 0

    # 教师积分无上限

    # 查询总积分表
    sql = """ select id, score from score_user
              where user_id=%s and app_id=%s """ \
          % (user_id, app_id)
    rs = db.slave.fetchone_dict(sql)

    score = rs['score'] if rs else 0    # 原始总分

    if not rs:
        sql = """ insert into score_user (user_id,score,app_id,city,unit_id) values (%s,%s,%s,%s,%s)""" \
                % (user_id, score, APP_ID_TEA, city_id, school_id)
        db.default.execute(sql)

    # 写明细表
    sql = """ INSERT INTO score_user_detail (user_id, item_no, score, remark, add_date, app_id)
              VALUES (%s, '%s', %s, '%s', '%s', %s); """ \
                % (user_id, item_no, add_score, ITEM_NO_MATK[item_no], time.time(), app_id)

    num = db.default.execute(sql)

    # 更新总积分表
    new_score = score + add_score
    sql = """ UPDATE score_user SET score = %s, city=%s, unit_id=%s WHERE app_id = %s AND user_id = %s;""" \
          % (new_score, city_id, school_id, app_id, user_id)
    db.default.execute(sql)

    return True

@ajax_try({})
@need_teacher
def send_sms(request):
    """
    @api {post} /huodong/summer_word/t/send_sms [暑假活动-教师] 发短信给班级下学生
    @apiGroup summer_word
    @apiParamExample {json} 请求示例
       {'content':'家长您好....',type:1 开通短信 0 普通短息}
    @apiSuccessExample {json} 成功返回
       {"message": "积分成功", "error": "", "data": ', "response": "ok" , "next": ""}
    @apiSuccessExample {json} 失败返回
       {"message": "发送短信，每天只能加分一次", "error": "", "data": "null", "response": "fail", "next": ""}
    """
    # 普通短信
    item_no = 'send_sms'
    add_score = 50

    user = request.user
    user_id = user.id
    args = request.QUERY.casts(content=unicode, type=int)

    if not args.content.strip():
        return ajax_json.jsonp_fail(request, message='内容不能为空')
    # 开通短信
    if args.type == 1:
        item_no = 'send_open'
        add_score = 100

    # 群发短信
    unit_class_id = [u.id for u in user.units]           # user.units 教师所在年级的班级
    unit_ids = ','.join(str(t) for t in unit_class_id)
    hub = tbktapi.Hub(request)
    hub.sms.post('/sms/send', {'platform_id': user.platform_id, 'unit_id': unit_ids, 'content': args.content})

    # 积分明细查当天发送短信次数
    cut_time = time.time()
    ling_time = cut_time - cut_time % 86400
    sql = """ SELECT count(id) FROM score_user_detail
                  WHERE user_id = %s AND item_no = '%s' AND app_id=%s AND add_date > '%s';""" \
          % (user_id, item_no, APP_ID_TEA, ling_time)
    rs = db.slave.fetchone_dict(sql)

    # 是否更新积分主表
    if rs and rs['count(id)'] > 0:
        return ajax_json.jsonp_ok(request, message='发送短信，每天只能加分一次')
    else:
        # 写积分明细表、主表
        update_score(user, APP_ID_TEA, item_no, add_score=add_score)
    return ajax_json.jsonp_ok(request, message='积分成功')

@ajax_try({})
@need_teacher
def send_open(request):
    """
    @api {post} /huodong/summer_word/t/send_open [暑假活动-教师] 开通班级下学生学科
    @apiGroup summer_word
    @apiParamExample {json} 请求示例
       {}
    @apiSuccessExample {json} 成功返回
       {"message": "", "error": "", "data": ', "response": "ok", "next": ""}
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    user = request.user
    # 发开通短信
    unit_class_id = [u.id for u in user.units]
    hub = tbktapi.Hub(request)
    student = []
    for i in unit_class_id:
        r = hub.com.post('/class/students', {"unit_id": i})
        if r and r.response == 'ok':
            data = r.data
            student += (data.get('students', []))
    phones = ','.join(str(s['phone_number']) for s in student if s.get('status',0) not in [2,9])
    platform_id = int(user.platform_id) if user and user.platform_id else 1
    r = hub.bank.post('/cmcc/open', {'phone_number': phones, 'subject_id': 9, "platform_id": platform_id})
    if not r:
        return ajax_json.jsonp_fail(request, message='服务器开小差了')
    if r.response == 'fail':
        return ajax_json.jsonp_fail(request, message=r.message)
    return ajax_json.jsonp_ok(request, message='已发送开通短信')

@ajax_try({})
@need_teacher
def my_rank(request):
    """
    @api {post} /huodong/summer_word/t/my_rank [暑假活动-教师]我的积分、排名
    @apiGroup summer_word
    @apiParamExample {json} 请求示例
       {}
    @apiSuccessExample {json} 成功返回
       {"message": "", "error": "",
       "data": {'rank_no':122, 'score': 1000 }, "response": "ok", "next": ""}
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    data = {}

    user = request.user
    user_id = user.id
    user_city = int(user.city) if user.city != '' else 0
    school_id = int(user.unit.school_id) if user.unit else 0

    # 更换地市触发次更新以免积分主档中的city没变查找时被过滤
    sql = """ select city from score_user where app_id=%s and user_id=%s """ % (APP_ID_TEA, user_id)
    rs = db.slave.fetchone_dict(sql)
    if rs:
        if int(rs['city']) != user_city:
            sql = """ UPDATE score_user SET city=%s, unit_id=%s WHERE app_id = %s AND user_id = %s;""" \
                  % (user_city, school_id, APP_ID_TEA, user_id)
            db.default.execute(sql)

    # 排名
    smx = 'city = 411200' if user.city == '411200' else 'city<>411200'  # 三门峡
    sql = """ select rank_no,score,city from
                (select S.user_id,S.score, @rownNum:=@rownNum+1 as rank_no, city from
                    (select user_id, score, app_id, city, unit_id from score_user
                    where app_id=%s and %s and user_id<>0
                    order by score desc) S, (select @rownNum:=0) R
                ) A
                where user_id=%s;""" \
          % (APP_ID_TEA, smx, user_id)

    rs = db.slave.fetchone_dict(sql)
    rank_no = rs['rank_no'] if rs else 0
    score = rs['score'] if rs else 0

    data['rank_no'] = int(rank_no)
    data['score'] = score

    return ajax_json.jsonp_ok(request, data)

@ajax_try({})
@need_teacher
def user_rank(request):
    """
    @api {post} /huodong/summer_word/t/user_rank [暑假活动-教师] 所有教师排名
    @apiGroup summer_word
    @apiParamExample {json} 请求示例
       {}
    @apiSuccessExample {json} 成功返回
          {
           "message": "",
           "next": "",
            "data": {
                "page_num": 20,     # 总页数
                "page_no": 1,       # 当前页
               "rank_info": [
                       {
                           "user_name": "13600000000xs",
                           "score": 30,
                           "school_name": "创恒中学"
                       },{},...
                   ]
           },
           "response": "ok",
           "error": ""
           }
    @apiSuccessExample {json} 失败返回
       {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    user = request.user
    data = {'rank_info': []}

    page_no = request.QUERY.get('page_no')
    if not page_no:
        return ajax_json.ajax_fail(error='缺少page_no参数')
    else:
        page_no = int(page_no)

    smx = 'city = 411200' if user.city == '411200' else 'city<>411200'  # 三门峡
    # 那一页的教师id和分数
    sql = """ select user_id, score, city, unit_id as school_id from score_user
              where app_id=%s and user_id > 0 and %s
              order by score desc limit %s,%s  """ \
          % (APP_ID_TEA, smx, (page_no - 1) * PAGE_COUNT, PAGE_COUNT)  # limit 10,5  检索第11-16
    rs = db.slave.fetchall_dict(sql)

    if not rs:
        return ajax_json.jsonp_ok(request, {"rank_info": []})

    # 获取名字,教师身份
    user_name_dict, tea_ids = common.get_users_name([int(r.user_id) for r in rs if r.user_id], 3)
    for r in rs:
        r.user_name = user_name_dict.get(int(r.user_id), '')

    # 学生id查学校名和姓名
    rank_user_id_list = [str(r['user_id']) for r in rs]

    sql2 = """
        select user_id, school_id, school_name from mobile_order_region
        where unit_class_id >0 and is_update = 0 and user_id > 0 and user_id in({});
    """.format(','.join(str(r) for r in rank_user_id_list))

    rs2 = db.ketang_slave.fetchall_dict(sql2)

    for n, r in enumerate(rs):
        school_name = ''  # 没有加入班级的学校名空
        for r2 in rs2:
            if r['user_id'] == r2['user_id']:
                school_name = r2['school_name']
                continue
        data['rank_info'].append(dict(user_name=r['user_name'], score=r['score'], school_name=school_name))

    # 总页数
    sql3 = """ select count(id) from score_user where app_id=%s and user_id<>0 and %s """\
            % (APP_ID_TEA, smx)
    rs3 = db.slave.fetchone_dict(sql3)
    data['page_num'] = int((int(rs3['count(id)'])-1)/PAGE_COUNT)+1
    data['page_no'] = page_no
    return ajax_json.jsonp_ok(request, data)

@ajax_try({})
@need_teacher
def my_stu_rank(request):
    """
        @api {post} /huodong/summer_word/t/my_stu_rank [暑假活动-教师]排名 所有班级学生积分排名
        @apiGroup summer_word
        @apiParamExample {json} 请求示例
           {page_no=1}
        @apiSuccessExample {json} 成功返回
           {
            "message": "",
            "next": "",
            "data": {
                "page_num": 5,      # 总业数
                "page_no": 1,       # 当前页
                "rank_info": [      # (1)请求的那一页为空 (2)教师班级下无学生，"rank_info":[]
                    {"user_name": "杨铮",
                    "score": 2000
                    "rank_no": 1
                    "school_name":"创新中学"
                    },{},{}, ...
                ]
            },
            "response": "ok",
            "error": ""
            }
        @apiSuccessExample {json} 失败返回 注意，此信息由中间件返回
           {"message": "请先加入一个班级", "error": "no_class", "data": null, "response": "fail", "next": ""}
    """
    page_no = int(request.QUERY.get('page_no', '1'))
    data = {'rank_info':[]}
    user = request.user

    all_units = user.units
    unit_ids = [str(unit['id']) for unit in all_units]

    # 教师下所有班级学生 有些学生user_id=0已过滤
    sql = """
            select user_id, school_id, school_name from mobile_order_region
            where unit_class_id >0 and is_update = 0 and user_id > 0
            and user_type <> 3 and unit_class_id in ({}) ;
        """.format(','.join(unit_ids))
    rs = db.ketang_slave.fetchall_dict(sql)
    if not rs:
        return ajax_json.jsonp_ok(request, data=data)

    # 用户对应的学校
    stu_school_name = {}
    for r in rs:
        stu_school_name[r.user_id] = r.school_name

    # 所有学生中参加活动的，按积分排名
    stu_user_ids = [str(r['user_id']) for r in rs]
    stu_name_dict, stu_ids = common.get_users_name(stu_user_ids, 1)

    sql2 = """ SELECT user_id, score, city, unit_id AS school_id FROM score_user
                  WHERE app_id=%s AND  user_id IN (%s)
                  ORDER BY score DESC limit %s,%s  """ \
           % (APP_ID_STU, ','.join(stu_user_ids), (page_no - 1) * PAGE_COUNT, PAGE_COUNT)
    rs2 = db.slave.fetchall_dict(sql2)

    if not rs2:
        return ajax_json.jsonp_ok(request, data=data)

    for r in rs2:
        r.real_name = stu_name_dict.get(r.user_id, '')
    page_num = int(len(rs2)/PAGE_COUNT) + 1

    for n, r2 in enumerate(rs2):
        school_name = stu_school_name.get(r2.user_id, '')  # 没有加入班级的学校名空
        data['rank_info'].append(dict(user_name=r2['real_name'], score=r2['score'],
                                      rank_no=(page_no-1)*PAGE_COUNT+n+1, school_name=school_name))
    data['page_num'] = page_num
    data['page_no'] = page_no
    return ajax_json.jsonp_ok(request, data)

@ajax_try({})
@need_teacher
def award_my_score(request):
    """
        @api {post} /huodong/summer_word/t/award/my_score [暑假活动-教师]抽奖 教师用户自己总积分和可用抽奖次数
        @apiGroup summer_word
        @apiParamExample {json} 请求示例
           {}
        @apiSuccessExample {json} 成功返回
           {
            "message": "",
            "next": "",
            "data": {
                "score": 8140,           # 总积分  没有积分0
                "times": 4            # 可以抽奖的次数    没有次数0
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
        % (APP_ID_TEA, user_id)
    rs = db.slave.fetchone_dict(sql)
    if rs:
        score = rs['score']
        times = int(score / LOTTERY_COST_TEA)
    else:
        pass

    data['score'] = score
    data['times'] = times
    return ajax_json.jsonp_ok(request, data)

@ajax_try({})
@need_teacher
def award_my_award(request):
    """
        @api {post} /huodong/summer_word/t/award/my_award [暑假活动-教师]抽奖 我的奖品列表
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
                        "award_type": 4            # 1 ipad    2志高挂烫机  3精美天堂太阳伞   4金豆2个   5谢谢参与
                        "award_name": "语文学科体验一个月"
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
    user_id = request.user.id

    sql = """ SELECT user_id,user_name, award_type, award_name, add_time FROM active_award
              where user_id=%s and active_id=%s and award_type<> %s
              order by add_time desc""" \
              % (user_id, ACTIVE_ID_TEA, 5)     # app_id公用奖池 表中active_id实存app_id 排除type5谢谢参与
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
@need_teacher
def award_won_list(request):
    """
        @api {post} /huodong/summer_word/t/award/won_list [暑假活动-教师] 轮播已获奖名单
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

    smx = 'city = 411200' if user.city == '411200' else 'city<>411200'  # 三门峡411200
    sql = """ select user_name, award_name from active_award
              where award_type <> 5 and active_id=%s and remark='%s' and %s
              order by add_time desc limit 0,10 ;""" % (ACTIVE_ID_TEA, APP_ID_TEA, smx)
    rs = db.tbkt_web_slave.fetchall_dict(sql)
    if not rs:
        return ajax_json.jsonp_ok(request,data={'won_list':[]})

    for r in rs:
        won_list.append(dict(user_name=r['user_name'], award_name=r['award_name']))
    data['won_list'] = won_list
    return ajax_json.jsonp_ok(request,data)

@ajax_try({})
@need_teacher
def total_score_rank(request):
    """
        @api {post} /huodong/summer_word/t/result/total_score_rank [暑假活动-教师]结束页 总积分获奖名单
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
                    {
                        "award_name": "小米平衡车",
                        "score": 100000,
                        "award_type": 1,
                        "school_name": "创恒中学",
                        "user_name": "铮教师"
                    },{},{}, ...
                ]
            },
            "response": "ok",
            "error": ""
            }
        @apiSuccessExample {json} 失败返回
           {"message": "", "error": "", "data": "", "response": "fail", "next": ""}
    """
    data = {'rank_info': []}
    user = request.user
    page_no = int(request.QUERY.get('page_no', '1'))

    smx = 'city = 411200' if user.city == '411200' else 'city<>411200'  # 三门峡411200
    # 那一页
    sql = """ select user_id, score, city, unit_id as school_id from score_user
                  where app_id=%s and %s
                  order by score desc limit %s,%s  """ \
          % (APP_ID_TEA, smx,  (page_no - 1) * PAGE_COUNT, PAGE_COUNT)  # limit 10,5  检索第11-16
    rs = db.slave.fetchall_dict(sql)
    if not rs:
        return ajax_json.jsonp_ok(request, data)

    user_name_dict, tea_ids = common.get_users_name([int(r.user_id) for r in rs], 3)
    for r in rs:
        r.real_name = user_name_dict.get(int(r.user_id), '')

    # 补上排名
    for n,r in enumerate(rs):
        r['rank_no'] = (page_no-1)*PAGE_COUNT + n+1
    if len(rs) > 36:
        return ajax_json.jsonp_ok(request, data)

    # userid查学校名
    rank_user_id_list = [int(r['user_id']) for r in rs if rs]
    sql2 = """
        select user_id, school_id, school_name from mobile_order_region
        where unit_class_id >0 and is_update = 0 and user_id > 0 and user_id in({});
    """.format(','.join(str(obj) for obj in rank_user_id_list))
    rs2 = db.ketang_slave.fetchall_dict(sql2)

    for n, r in enumerate(rs):
        if r['rank_no'] == 1:
            award_type = 1
        elif 2 <= r['rank_no'] <= 6:
            award_type = 2
        elif 7 <= r['rank_no'] <= 36:
            award_type = 3
        else:
            continue

        award_name = TOTAL_SCORE_AWARD.get(award_type, '')
        school_name = ''  # 没有加入班级的学校名空
        for r2 in rs2:
            if r['user_id'] == r2['user_id']:
                school_name = r2['school_name']
                continue
        data['rank_info'].append(dict(user_name=r['real_name'], score=r['score'], award_name=award_name,
                                      award_type=award_type, school_name=school_name))
    return ajax_json.jsonp_ok(request, data)

@ajax_try({})
@need_teacher
def draw_lottery_rank(request):
    """
        @api {post} /huodong/summer_word/t/result/draw_lottery_rank [暑假活动-教师]结束页 抽奖获奖名单
        @apiGroup summer_word
        @apiParamExample {json} 请求示例
           {}
        @apiSuccessExample {json} 成功返回
           {
            "message": "",
            "next": "",
            "data": {
                "rank_info": [      # 请求的那一页为空的话，"rank_info":[]
                    {"user_name": "杨铮",
                    "award_type": 2
                    "award_name": "宝视达护眼"     # 奖品名称
                    "school_name":"创新中学"
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

    # 那一页的用户。 按一等奖、二等奖排序 。过滤谢谢参与
    smx = 'city = 411200' if user.city == '411200' else 'city<>411200'  # 三门峡411200
    sql = """ SELECT user_id,user_name,award_name,award_type,city  FROM active_award
              where active_id=%s and remark=%s and award_type<>5 and %s
              order by award_type limit %s, %s; """\
          % (ACTIVE_ID_TEA, APP_ID_TEA, smx, (page_no - 1) * PAGE_COUNT, PAGE_COUNT )
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
