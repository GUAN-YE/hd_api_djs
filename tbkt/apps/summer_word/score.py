#coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: score.py
@time: 2017/8/2 15:58
"""

import datetime
import time

from libs.utils import db
from libs.utils.ajax import jsonp_ok

ITEM_NO_MATK = {1: '学生情景对话',
                # 'task': '学生单词、[作业]气球打地鼠、做练习',
                2: '学生同步练习',
                3: '学生课文跟读、背诵',
                4: '气球打地鼠游戏',
                }

ITEM = {
            1: 'dialog',
            # 'task': '学生单词、[作业]气球打地鼠、做练习',
            2: 'test',
            3: 'text',
            4: 'word',
}

APP_ID = 32      # 积分主档   tbkt.score_app
MAX_SCORE_OPENED = 600
MAX_SCORE_NOOPEN = 300

def add_score(request):
    """
    功能说明：                英语学生做练习加分
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-8-2
    """
    args = request.loads() or request.QUERY.casts(item_no=int)
    item_no = args.item_no or 0
    if not item_no:
        return jsonp_ok(request)

    user = request.user
    score = 0
    if item_no in (1, 2, 3):        # 课文习题 20分
        score += 20
    else:                           # 单词游戏 10分
        score += 10
    update_score(user, item_no, score)

    return jsonp_ok(request)

def update_score(user, item_no, add_score):
    """
    功能说明：                更新积分
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-8-2
    """
    if int(user.type) == 3:
        return 
    open_status = user.openstatus(9)        # 英语开通状态
    user_id = user.id
    school_id = int(user.unit.school_id) if user.unit else 0
    city_id = int(user.city) if user.city != '' else 0

    # 检查用户当天积分是否超过上限。排除开通学科加的1000分情况,排除给老师积分情况,排除抽奖扣分,
    # 排除分享积分（590分时分享不加分还是加到690导致规则漏洞 产品已修正规则

    cut_time = time.time()
    ling_time = cut_time - cut_time % 86400

    sql = """ SELECT sum(score) FROM score_user_detail
                      WHERE user_id = %s and item_no <> 'open_yy' and item_no <> 'login_add_tea_score' AND item_no <> 'lottery'
                      and item_no<>'share' and app_id=%s AND add_date > '%s';""" \
          % (user_id, APP_ID, ling_time)
    rs = db.slave.fetchone_dict(sql)

    day_score = rs['sum(score)'] if rs['sum(score)'] else 0     # 当天积分
    if (open_status == 1 and day_score >= MAX_SCORE_OPENED) or (open_status == 0 and day_score >= MAX_SCORE_NOOPEN):
        # print '超过当日积分上限'
        return True

    # 查询总积分表
    sql = """ select id, score from score_user
              where user_id=%s and app_id=%s """ \
          % (user_id, APP_ID)
    rs = db.default.fetchone_dict(sql)

    score = rs['score'] if rs else 0  # 原始总分
    if not rs:
        # 第一次积分
        sql = """ insert into score_user (user_id,score,app_id,city,unit_id) values (%s,%s,%s,%s,%s)""" \
                % (user_id, score, APP_ID, city_id, school_id)
        db.default.execute(sql)

    # 写明细表
    sql_1 = """ INSERT INTO score_user_detail (user_id, item_no, score, remark, add_date, app_id)
              VALUES (%s, '%s', %s, '%s', '%s', %s); """ \
                % (user_id, ITEM[item_no], add_score, ITEM_NO_MATK[item_no], cut_time, APP_ID)
    # db.default.execute(sql)

    sql_2 = """ UPDATE score_user SET score = score+%s, city=%s, unit_id=%s WHERE app_id = %s AND user_id = %s;""" \
          % (add_score, city_id, school_id, APP_ID, user_id)
    # db.default.execute(sql)

    try:
        with db.default as c:
            c.execute(sql_1)
            c.execute(sql_2)
    except Exception, e:
        print e, sql_1, sql_2
        return False
    return True