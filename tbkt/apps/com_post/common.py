# coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: common.py
@time: 2017/9/5 11:50
"""
import time

import datetime

from libs.utils import db, Struct, get_ling_time, join, tbktapi
from com.com_cache import cache
import logging


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
            extra_info = ""
            if grade_id:
                extra_info += ",grade_id=%s" % grade_id
            if unit_id:
                extra_info += ",unit_id=%s" % unit_id
            sql = """ UPDATE active_score_user SET score = score+%s ,city=%s  %s WHERE active_id = %s AND user_id=%s;""" % (
                score, city, extra_info, active_id, user_id)
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
    """
    active_config = db.tbkt_active_slave.active_config.select('begin_time', 'end_time', 'grade_id', 'city_id',
                                                              'county_id').get(active_id=active_id)
    nowt = int(time.time())
    # 判断时间是否符合
    if active_config.begin_time > nowt or active_config.end_time < nowt:
        return
    # 年级是否符合
    if active_config.grade_id and grade_id:
        grade_ids = map(int, active_config.grade_id.split(','))
        if int(grade_id) not in grade_ids:
            return
    # city是否符合
    if (active_config.city_id or active_config.county_id) and city:
        if not (int(city) == int(active_config.city_id) or int(city) == int(active_config.county_id)):
            return

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

    start = (page_no - 1) * pnums
    end = start + pnums
    if start >= 300:
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
                     WHERE  su.active_id = %s
                """ % active_id

            if conf_name == "unit_id":
                conf += " AND unit_id in (%s) " % conf_value
            elif conf_name == "grade_id":
                conf += "AND grade_id=%s" % conf_value
            order = " ORDER BY su.score DESC, su.id limit 300"
            sql += conf + order
            rank = db.tbkt_active_slave.fetchall_dict(sql)
        if not rank:
            return []
        cache.hd_user_rank.set((active_id, conf_name, conf_value), rank)
    if page_no == -1 and kw.get('unit_id'):
        return rank
    return rank[start: end]


def get_user_rank(active_id, user_id, grade_id=None, unit_id=None):
    """
    张帅男      用户在当前活动中的排名和积分  返回值{"rank_no": 1, "score":100}
    :param active_id:   活动id
    :param user_id:     用户id
    :return:
    """
    data = cache.hd_user_score_rank.get((active_id, user_id))  # 读取整个活动的缓存
    if not data:
        my_score_dict = db.tbkt_active_slave.active_score_user.select("score", "id").filter(user_id=user_id,
                                                                                            active_id=active_id).first()
        if my_score_dict:
            my_score = my_score_dict.score
            my_id = my_score_dict.id
            conf = ""
            if grade_id:
                conf += """and grade_id=%s """ % grade_id
            if unit_id:
                conf += """and unit_id=%s """ % unit_id
            sql = """
                select count(score) num from active_score_user
                                where active_id=%s and score > %s   %s
                    """ % (active_id, my_score, conf)

            rank = db.tbkt_active_slave.fetchone_dict(sql)
            count = rank.num if rank else 0
            sql = """select count(*) num from active_score_user where active_id=%s and score=%s %s  and  id<%s""" % (
                active_id, my_score, conf, my_id)
            row = db.tbkt_active_slave.fetchone_dict(sql)
            num = row.num if row else 0
            my_rank = int(count) + 1 + num
        else:
            my_rank = 0
            my_score = 0
        data = {}
        data['rank_no'] = my_rank if my_rank else 0
        data['score'] = my_score if my_score else 0
        cache.hd_user_score_rank.set((active_id, user_id), data)

    return data


def get_user_item_today(user_id, active_id, item_no):
    day_temp = today_temp()
    d = db.tbkt_active.active_score_user_detail.get(
        user_id=user_id, active_id=active_id, item_no=item_no, add_date__gte=day_temp)
    if d:
        return True
    return False


def today_temp():
    to_day = datetime.datetime.now()
    d = datetime.datetime(to_day.year, to_day.month, to_day.day, 0, 0, 0)
    return int(time.mktime(d.timetuple()))


def unit_stu_rank(user, stu_active_id, unit_id):
    """
    获取班级学生信息, 分班返回
    """
    stu_ids = user.get_mobile_order_region().select("user_id") \
                  .filter(unit_class_id=unit_id, user_type=1).flat('user_id')[:]
    if not stu_ids:
        return []

    sql = """
        select a.id, a.real_name,a.id from auth_user a, auth_profile p
        where a.id = p.user_id and user_id in (%s)
        """ % join(stu_ids)
    rows = db.tbkt_user_slave.fetchall_dict(sql)

    stu_ids = [i.id for i in rows]
    stu_score = db.tbkt_active_slave.active_score_user.select('user_id', 'score', 'id') \
                    .filter(user_id__in=stu_ids, active_id=stu_active_id)[:]
    score_map = {i.user_id: i.score for i in stu_score}
    # 积分相同时按用户参加活动顺序排序
    score_id_map = {i.user_id: i.id for i in stu_score}
    for i in rows:
        i.score = score_map.get(i.id, 0)
        i.score_id = score_id_map.get(i.id, 0)
    rows.sort(key=lambda x: (-x.score, x.score_id))
    return rows


def user_score_detail(user, active_id, page):
    """
    获取用户积分详情
    ——————————————————
    王世成  2017.9.12
    ——————————————————
    :param user:
    :param active_id:
    :param page:
    :return:
    """
    sql = """
    select  distinct i.item_name, d.score, d.add_date
    from active_score_user_detail d inner join active_score_item i
    on i.item_no = d.item_no and i.active_id=d.active_id and d.user_id = %s and d.active_id = %s
    order by d.id desc limit %s, %s
    """ % (user.id, active_id, (page - 1) * 50, 50)
    data = db.tbkt_active_slave.fetchall_dict(sql)
    for i in data:
        i.add_date = time.strftime("%m月%d日 %H:%M:%S", time.localtime(i.add_date))
    return data


def send_sms(request, user, content):
    # 群发短信
    unit_class_id = [u.id for u in user.units]  # user.units 教师所在年级的班级
    unit_ids = ','.join(str(t) for t in unit_class_id)
    hub = tbktapi.Hub(request)
    hub.sms.post('/sms/send', {'platform_id': user.platform_id, 'unit_id': unit_ids, 'content': content})
