# coding:utf-8
import random
import datetime
from libs.utils import db

"""
"""


def get_user_award_type(user_id, app_id=36):
    """6月19-6月30日全省抽奖概率 返回获奖 奖项"""
    total_num = {1: 0, 2: 0, 3: 14, 4: 5000}
    total_award = {1: 2, 2: 10, 3: 100, 4: 5000}
    now = datetime.datetime.now()
    choice_unm = random.randint(1, 500)
    award_type = 4
    if choice_unm in range(50) and now.day in (15, 21):
        award_type = 0
    elif 110 < choice_unm <= 100:
        award_type = 2
    elif 110 < choice_unm <= 200 and 23 > now.hour >= 6:
        award_type = 3
    elif choice_unm:
        award_type = 4

    # if award_type == 0:
    #     return 0
    # 不能重复
    exist = 0
    if award_type != 4:
        exist = db.tbkt_web.active_award.filter(user_id=user_id, active_id=app_id, award_type=award_type).exists()
    award_num = get_daily_award_num(app_id, award_type)
    if exist or award_num >= total_num.get(award_type, 0):
        return 0
    if award_type == 3:
        # 已经抽到的奖品数量
        num = get_now_award_num(app_id, award_type, now)
        if num > 3:
            return 4
    all_award_num = db.tbkt_web.active_award.filter(active_id=app_id, award_type=award_type).exclude(
        city=411200).count()
    if total_award.get(award_type, 0) <= all_award_num:
        return 0
    return award_type


def get_smx_user_award_type(user_id, app_id=36):
    """6月19-6月30日三门峡抽奖概率 返回获奖 奖项"""
    total_num = {1: 0, 2: 1, 3: 14, 4: 70}
    total_award = {1: 0, 2: 5, 3: 100, 4: 500}
    now = datetime.datetime.now()
    choice_unm = random.randint(0, 500)
    award_type = 3
    if choice_unm in [1, 2, 3, 4, 5]:
        award_type = 0
    elif 5 < choice_unm <= 30:
        award_type = 2
    elif 100 < choice_unm <= 300:
        award_type = 3
    elif 300 < choice_unm <= 500:
        award_type = 4
    if award_type != 4:
        exist = db.tbkt_web.active_award.filter(user_id=user_id, active_id=app_id, award_type=award_type).exists()
        award_num = get_daily_award_num(app_id, award_type, is_smx=1)

        if exist or award_num >= total_num.get(award_type, 0):
            return 4
    if award_type == 3:
        # 已经抽到的奖品数量
        num = get_now_award_num(app_id, award_type, now, is_smx=1)
        if num >= 3:
            return 4
    all_award_num = db.tbkt_web.active_award.filter(active_id=app_id, award_type=award_type, city=411200).count()
    if total_award.get(award_type, 0) <= all_award_num:
        return 0
    return award_type


def get_daily_award_num(active_id, award_type, is_smx=0):
    smx = 'city=411200' if is_smx else 'city<>411200'
    if award_type == 0:
        return 0
    sql = """SELECT count(id) num FROM active_award WHERE active_id=%s AND award_type=%s
AND %s  AND DATE(FROM_UNIXTIME(add_time))='%s' """ % (
        active_id, award_type, smx, datetime.date.today())

    num = db.tbkt_web.fetchone_dict(sql).num
    return num


def get_now_award_num(active_id, award_type, now, is_smx=0):
    smx = 'city=411200' if is_smx else 'city<>411200'
    if award_type == 0:
        return 0
    sql = """SELECT count(id) num FROM active_award WHERE active_id=%s AND award_type=%s
AND %s  AND DATE(FROM_UNIXTIME(add_time))='%s'  AND HOUR(FROM_UNIXTIME(add_time))<='%s' """ % (
        active_id, award_type, smx, datetime.date.today(), now.hour)

    num = db.tbkt_web.fetchone_dict(sql).num
    return num
