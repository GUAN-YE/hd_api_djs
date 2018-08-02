#coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: common.py
@time: 2017/9/12 14:50
"""
import time
from libs.utils import db

def get_actives_status(user, ACTIVE_ID_list):
    """获取所有活动时候在参加可以加分阶段"""
    nowt = int(time.time())
    active_ids = ','.join([str(a) for a in ACTIVE_ID_list])
    # 查询该加分活动的限制条件, is_open 0表示下线, 1 可以加分 ，2，表示显示活动，但是不加积分
    sql = """
            SELECT a.id, a.subject_id, c.platform, c.city_id, c.county_id, a.user_type,
              c.school_id, c.grade_id
              FROM active a INNER JOIN active_config c WHERE a.id = c.active_id AND a.id in (%s)
            AND c.is_open =1 AND a.begin_time <= %s AND a.end_time >= %s AND  a.subject_id=91;
        """ % (active_ids, nowt, nowt)
    actives = db.tbkt_active_slave.fetchall_dict(sql)
    res_active_list = []                                            # 确定可以参加的并可以加分的活动
    for a in actives:
        if a.user_type and int(user.type) != int(a.user_type):       # 判断用户身份
            continue
        if int(a.user_type) == 3 and a.subject_id and int(a.subject_id) != int(user.subject_id):
            continue
        if a.platform and int(a.platform) != int(user.platform_id):  # 判断用户省份(平台)
            continue
        if a.city_id and int(a.city_id) != int(user.city):           # 判断用户的地市
            continue
        if a.county_id and int(a.county_id) != int(user.county):     # 判断用户县区
            continue
        if a.school_id and (not user.school_id or int(a.school_id) != int(user.school_id)):  # 判断用户学校
            continue
        if a.grade_id and a.grade_id != '0':
            if int(user.grade_id) not in map(int, a.grade_id.split(',')):  # 判断用户年级
                continue
        if int(a.id) not in res_active_list:
            res_active_list.append(int(a.id))
    return res_active_list