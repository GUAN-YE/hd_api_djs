# coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: common.py
@time: 2017/9/5 11:50
"""
import time

import datetime

from libs.utils import db, Struct, get_ling_time
from com.com_cache import cache
import logging

MOBILE_ORDER_REGION = {
    1: "tbkt_ketang.mobile_order_region",
    6: "tbkt_ketang.mobile_order_region_qg"
}


def get_actives(user):
    """
    功能说明：                获取用户在某个时间段能参加能积分的活动id的集合
    user: 用户对象
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-9-11
    """
    nowt = int(time.time())  # 得到现在的时间
    # 查询当前时间内能加积分的活动 is_open 1代表可以加积分, 0表示下线, 2，表示显示活动，但是不加积分
    sql = """
        SELECT a.id, a.name, a.subject_id,  c.platform, c.city_id, c.county_id, a.user_type,
          c.school_id, c.grade_id, if(c.extend,c.extend,"") extend,
          c.begin_time, c.end_time, c.banner_url, c.is_open,
          c.begin_url, c.end_url, a.begin_time as banner_begin, a.end_time as banner_end
          FROM active a INNER JOIN active_config c WHERE a.id = c.active_id
        AND c.is_open !=0 AND a.begin_time <= %s AND a.end_time >= %s;
    """ % (nowt, nowt)
    actives = db.tbkt_active_slave.fetchall_dict(sql)
    out = []
    for a in actives:
        if a.user_type and int(user.type) != int(a.user_type):  # 判断用户身份
            continue
        if int(a.user_type) == 3 and a.subject_id and int(a.subject_id) != int(user.subject_id):
            continue
        if a.platform and int(a.platform) != int(user.platform_id):  # 判断用户省份(平台)
            continue
        if a.city_id and int(a.city_id) != int(user.city):  # 判断用户的地市
            continue
        if a.county_id and int(a.county_id) != int(user.county):  # 判断用户县区
            continue
        if a.school_id and (not user.school_id or int(a.school_id) != int(user.school_id)):  # 判断用户学校
            continue
        if a.grade_id and a.grade_id != '0':
            if int(user.grade_id) not in map(int, a.grade_id.split(',')):  # 判断用户年级
                continue

        a.banner_begin = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(a.banner_begin))
        a.banner_end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(a.banner_end))

        d = dict(
            active_id=a.id,
            name=a.name,
            is_open=a.is_open,  # 1 加分 2 不加分只显示
            extend=a.extend or {},
            banner_begin=a.banner_begin or '',  # 开始时间
            banner_end=a.banner_end or '',  # 结束时间
            banner_url=a.banner_url or '',
            begin_url=a.begin_url or ''
        )
        if d not in out:  # 去重
            out.append(d)
    return out


def get_active_status(user, active_id):
    """
    功能说明：                判断用户参加的这个活动是否属于加分的活动
    """
    nowt = int(time.time())
    # 查询该加分活动的限制条件, is_open 0表示下线, 1 可以加分 ，2，表示显示活动，但是不加积分
    sql = """
            SELECT c.is_open, a.id, a.subject_id, c.platform, c.city_id, c.county_id, a.user_type,
              c.school_id, c.grade_id
              FROM active a INNER JOIN active_config c WHERE a.id = c.active_id AND a.id=%s
            AND c.is_open !=0 AND a.begin_time <= %s AND a.end_time >= %s;
        """ % (active_id, nowt, nowt)
    actives = db.tbkt_active_slave.fetchall_dict(sql)
    is_open = 0  # 该活动是否能加分
    for a in actives:
        if a.user_type and int(user.type) != int(a.user_type):  # 判断用户身份
            continue
        if int(a.user_type) == 3 and a.subject_id and int(a.subject_id) != int(user.subject_id):
            continue
        if a.platform and int(a.platform) != int(user.platform_id):  # 判断用户省份(平台)
            continue
        if a.city_id and int(a.city_id) != int(user.city):  # 判断用户的地市
            continue
        if a.county_id and int(a.county_id) != int(user.county):  # 判断用户县区
            continue
        if a.school_id and (not user.school_id or int(a.school_id) != int(user.school_id)):  # 判断用户学校
            continue
        if a.grade_id and a.grade_id != '0':
            if int(user.grade_id) not in map(int, a.grade_id.split(',')):  # 判断用户年级
                continue
        is_open = a.is_open
    return is_open


def update_score(user_id, active_id, item_no, add_user, city, unit_id, is_open=0, grade_id=0):
    """
    功能说明：                给用户某个活动添加积分
    user: 用户对象
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-9-11
    """
    nowt = int(time.time())
    # 判断该活动是否能加分
    sql = """
            SELECT id FROM active_config WHERE  active_id=%s
            AND is_open =1 AND begin_time <= %s AND end_time >= %s;
        """ % (active_id, nowt, nowt)
    actives = db.tbkt_active_slave.fetchall_dict(sql)
    if not actives:
        return
    score_item = db.tbkt_active_slave.active_score_item \
        .select("score", "type", "cycle_type", "cycle_num", "remark", "item_name", "open_num").filter(
        active_id=active_id, item_no=item_no).first()
    if not score_item:
        print '111111111'
        return
    score = int(score_item.score)  # 积分
    type = int(score_item.type)  # 1、加分+，2、减分-
    cycle_type = int(score_item.cycle_type)  # 3、不限周期，2、一次性，1、每天
    cycle_num = int(score_item.cycle_num)  # 周期次数
    open_num = int(score_item.open_num)  # 开通用户是否翻倍， 1：不翻倍， 2： 翻倍， 3：三倍 类推

    if type == 2:
        score = 0 - score
    if not score or not type:
        print '2222222222'
        return
    if int(is_open) == 1:  # 有开通条件的 区别对待
        score = score * open_num

    if cycle_type == 1:  # 每天
        ling_time = get_ling_time()  # 每天凌晨的时间
        count = db.tbkt_active.active_score_user_detail.filter(user_id=user_id, item_no=item_no, active_id=active_id,
                                                               add_date__gte=ling_time).count()
        if count < cycle_num:  # 没有超过次数
            add_score(user_id, item_no, score, score_item.remark, nowt, active_id, add_user, city, unit_id, grade_id)
    elif cycle_type == 2:  # 一次性加分
        if not db.tbkt_active.active_score_user_detail.filter(user_id=user_id, item_no=item_no,
                                                              active_id=active_id).exists():
            add_score(user_id, item_no, score, score_item.remark, nowt, active_id, add_user, city, unit_id, grade_id)
    elif cycle_type == 3:
        add_score(user_id, item_no, score, score_item.remark, nowt, active_id, add_user, city, unit_id, grade_id)
    return


def add_score(user_id, item_no, score, remark, add_date, active_id, add_user, city, unit_id, grade_id=0):
    """加减分处理"""
    with db.tbkt_active as tbkt_active:
        tbkt_active.active_score_user_detail.create(
            user_id=user_id,
            item_no=item_no,
            remark=remark,
            add_date=add_date,
            active_id=active_id,
            score=score,
            add_username=add_user
        )
        if tbkt_active.active_score_user.filter(user_id=user_id, active_id=active_id).exists():
            up_grade, up_city, up_unit = "", "", ""
            if grade_id:
                up_grade = ",grade_id=%s" % grade_id
            if city:
                up_city = ",city=%s" % city
            if unit_id:
                up_unit = ",unit_id=%s" % unit_id
            sql = """ UPDATE active_score_user SET score = score+%s  %s  %s  %s  WHERE active_id = %s AND user_id=%s;""" % (
                score, up_city, up_unit, up_grade, active_id, user_id)
            tbkt_active.execute(sql)
        else:
            tbkt_active.active_score_user.create(
                user_id=user_id,
                score=score,
                active_id=active_id,
                city=city,
                unit_id=unit_id,
                grade_id=grade_id
            )


def update_score_com(user_id, active_id, item_no, add_user, city, unit_id, is_open=0, grade_id=0):
    """
    功能说明：                给用户某个活动添加积分
    user: 用户对象
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-9-11
    """
    nowt = int(time.time())
    score_item = db.tbkt_active_slave.active_score_item \
        .select("score", "type", "cycle_type", "cycle_num", "remark", "item_name", "open_num").filter(
        active_id=active_id, item_no=item_no).first()
    if not score_item:
        return
    score = int(score_item.score)  # 积分
    type = int(score_item.type)  # 1、加分+，2、减分-
    cycle_type = int(score_item.cycle_type)  # 3、不限周期，2、一次性，1、每天
    cycle_num = int(score_item.cycle_num)  # 周期次数
    open_num = int(score_item.open_num)  # 开通用户是否翻倍， 1：不翻倍， 2： 翻倍， 3：翻三倍 类推

    if type == 2:
        score = 0 - score
    if not score or not type:
        return
    if is_open:  # 有开通条件的 区别对待
        score = score * open_num

    if cycle_type == 1:  # 每天
        ling_time = get_ling_time()  # 每天凌晨的时间
        count = db.tbkt_active.active_score_user_detail.filter(user_id=user_id, item_no=item_no, active_id=active_id,
                                                               add_date__gte=ling_time).count()
        if count < cycle_num:  # 没有超过次数
            add_score(user_id, item_no, score, score_item.remark, nowt, active_id, add_user, city, unit_id, grade_id)
    elif cycle_type == 2:  # 一次性加分
        if not db.tbkt_active.active_score_user_detail.filter(user_id=user_id, item_no=item_no,
                                                              active_id=active_id).exists():
            add_score(user_id, item_no, score, score_item.remark, nowt, active_id, add_user, city, unit_id, grade_id)
    elif cycle_type == 3:
        add_score(user_id, item_no, score, score_item.remark, nowt, active_id, add_user, city, unit_id, grade_id)
    return


def get_active_rank(active_id, page_no=1, pnums=10, **kw):
    """
    张帅男      用户活动排名---- kw中的条件只能是一个, 返回当前页码的排名
    :param active_id:         活动id
    :param page_no:           活动 显示页码 从第一页开始 默认1
    :param pnums:             活动 每页显示多少条数据    默认10
    :param platform_id:       平台id
    :param city_id:           城市id
    :param county_id:         县市id
    :param school_id:         学校id

    :param unit_id:           班级id
    其中active_score_user的city  可以代表 platform_id, city_id, county_id,
    unit_id可以代表 school_id, grade_id, unit_id  加分时传递的参数需注意
    :return:
    """
    rank = []
    platform_id = 1  # 默认是省的
    conf_name = ''  # 排行条件
    conf_value = ''  # 排行条件的值
    if kw:
        for k, v in kw.iteritems():
            if k == "platform_id":  # 省平台
                platform_id = v
            else:
                conf_name = k
                if type(v) == list:
                    conf_value = ','.join(str(c) for c in v)
                else:
                    conf_value = str(v)

    mobile_order_region = MOBILE_ORDER_REGION.get(platform_id, "ketang_slave.mobile_order_region")
    start = (page_no - 1) * pnums
    end = start + pnums
    if start>=300:
        return []
    rank = cache.hd_user_rank.get((active_id, conf_name, conf_value))
    if rank:
        return rank[start: end]
    if not conf_name:  # 全部排名
        rank = db.tbkt_active.active_score_user.select("user_id, score") \
                   .filter(active_id=active_id, user_id__ne=0).order_by("-score", "id")[:300]
        cache.hd_user_rank.set((active_id, conf_name, conf_value), rank)
        return rank[start: end]
    else:
        if not rank:

            conf = ""
            sql = """
                     SELECT su.user_id, su.score FROM tbkt_active.active_score_user su
                          INNER JOIN %s mor ON
                          su.user_id = mor.user_id AND su.active_id = %s AND mor.user_id > 0
                """
            if conf_name == "city_id":  # 按城市排名
                conf += " AND mor.city in (%s) "
            elif conf_name == "county_id":
                conf += " AND mor.county in (%s) "
            elif conf_name == "school_id":
                conf += " AND mor.school_id in (%s) "
            elif conf_name == "unit_id":
                conf += " AND mor.unit_class_id in (%s) "
            elif conf_name == "grade_id":
                conf_name += "and su.grade_id=%s"
            order = " ORDER BY su.score DESC, su.id limit 300"
            sql += conf + order
            if conf:
                sql = sql % (mobile_order_region, active_id, conf_value)
                rank = db.tbkt_active_slave.fetchall_dict(sql)
        if not rank:
            return []
        cache.hd_user_rank.set((active_id, conf_name, conf_value), rank)

    return rank[start: end]


def get_user_rank(active_id, user_id, grade_id=None):
    """
    张帅男      用户在当前活动中的排名和积分  返回值{"rank_no": 1, "score":100}
    :param active_id:   活动id
    :param user_id:     用户id
    :return:
    """
    data = cache.hd_user_score_rank.get((active_id, user_id))  # 读取整个活动的缓存
    if not data:
        my_score_dict = db.tbkt_active_slave.active_score_user.select("score").filter(user_id=user_id,
                                                                                      active_id=active_id).first()
        if my_score_dict:
            my_score = my_score_dict.score
            conf = ""
            if grade_id:
                conf += """and grade_id=%s """ % grade_id

            sql = """
                select count(score) num from active_score_user
                                where active_id=%s and user_id <> 0 and score > %s   %s
                    """ % (active_id, my_score, conf)

            rank = db.tbkt_active_slave.fetchone_dict(sql)
            count = rank.num if rank else 0
            sql = """select user_id from active_score_user where active_id=%s and score=%s order by user_id""" % (
                active_id, my_score)
            rows = db.tbkt_active_slave.fetchall_dict(sql)
            score = [int(r.user_id) for r in rows]
            try:
                score_num = score.index(int(user_id))
            except:
                score_num = 0
            my_rank = int(count) + 1 + score_num
        else:
            my_rank = 0
            my_score = 0
        data = {}
        data['rank_no'] = my_rank if my_rank else 0
        data['score'] = my_score if my_score else 0
        cache.hd_user_score_rank.set((active_id, user_id), data)

    return data


def get_user_share(user_id, active_id, item_no):
    day_temp = today_temp()
    d = db.tbkt_active.active_score_user_detail.get(
        user_id=user_id, active_id=active_id, item_no=item_no, add_date__gte=day_temp)
    if d:
        return False
    return True


def today_temp():
    to_day = datetime.datetime.now()
    d = datetime.datetime(to_day.year, to_day.month, to_day.day, 0, 0, 0)
    return int(time.mktime(d.timetuple()))
