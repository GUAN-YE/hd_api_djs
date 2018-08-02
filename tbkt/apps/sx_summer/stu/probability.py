# coding:utf-8
import random
import datetime
from libs.utils import db

"""                6月19-6月30日 发奖概率

奖品	                  全省每天发放数量	      发放规则	                               三门峡	  发放规则
ipad                   0                                                                                      0
宝视达护眼灯	   1	                                  每天18点发	                           0
卡通水笔           20（暂时一共）	     	  6点 -23 点,1516点不发          5            12：30 13：30 19:30 20:30 21:30各一个
语文免费体验	  300                                 隔5中一         	                       100	      隔5中一（抽中的不再抽中）
---------------------------------------------------------------------------------------------------------------------------------------

                   7月1-7月10日 发奖概率

奖品	                  全省每天发放数量	      发放规则	                               三门峡	  发放规则
ipad                   0                                                                                      0
宝视达护眼灯	   1	                                  每天18点发	                           三天一个
卡通水笔           30（暂时一共）	     	  6点 -23 点,                              15
语文免费体验	  300                                 隔5中一         	                       100	      隔5中一（抽中的不再抽中）
---------------------------------------------------------------------------------------------------------------------------------------

                   7月11-7月20日 发奖概率

同 1-10日
---------------------------------------------------------------------------------------------------------------------------------------
                   7月21-7月30日 发奖概率

奖品	                  总量                    	                                  三门峡	  发放规则
ipad                   1                                                              0               0
宝视达护眼灯	   20	                               	                           5
卡通水笔           600（暂时一共）	                                  200                                                                     (均未发完)
语文免费体验	  4000                                	                      350	      隔5中一（抽中的不再抽中）
---------------------------------------------------------------------------------------------------------------------------------------


                   7月31-8月6日 发奖概率

奖品	                  总量                    	                                  三门峡	  发放规则
ipad                   1                                                              1               0
宝视达护眼灯	   12	                               	                           5
卡通水笔           180（暂时一共）	                                  200

---------------------------------------------------------------------------------------------------------------------------------------

"""

smx_pro_3 = {
    6: 3, 8: 4, 9: 6, 11: 8, 12: 15, 13: 19, 14: 20, 17: 24, 18: 26, 19: 29, 20: 35, 21: 39, 22: 40
}
hn_pro_3 = {
    6: 2, 7: 4, 8: 6, 9: 8, 10: 10, 11: 12, 12: 18, 13: 24, 14: 26, 15: 28, 16: 30, 17: 32, 18: 36, 19: 42, 20: 50,
    21: 58, 22: 60
}


def get_user_award_type(user_id, app_id=35):
    """6月19-6月30日全省抽奖概率 返回获奖 奖项"""
    # 每日 最大发放量
    total_num = {1: 0, 2: 2, 3: 40, 4: 0}
    total_award = {1: 0, 2: 80, 3: 2000, 4: 0}

    now = datetime.datetime.now()
    choice_unm = random.randint(1, 1000)
    award_type = 0
    if choice_unm == 1:
        award_type = 0
    elif 1 < choice_unm <= 5 and now.hour >= 18:
        award_type = 2
    elif 10 < choice_unm <= 30 and 22 > now.hour >= 6:
        award_type = 3
    elif 200 < choice_unm <= 600:
        award_type = 0

    if award_type == 0:
        return 0
    # 不能重复
    exist = db.tbkt_web.active_award.filter(user_id=user_id, active_id=app_id, award_type=award_type).exists()
    award_num = get_daily_award_num(app_id, award_type)
    if exist or award_num >= total_num.get(award_type, 0):
        return 0
    if award_type == 3:
        # 已经抽到的奖品数量
        num = get_now_award_num(app_id, award_type, now)
        if num >= hn_pro_3.get(now.hour, 0):
            return 0
    all_award_num = db.tbkt_web.active_award.filter(active_id=app_id, award_type=award_type).exclude(
        city=411200).count()
    if total_award.get(award_type, 0) <= all_award_num:
        return 0
    return award_type


def get_smx_user_award_type(user_id, app_id=35):
    """6月19-6月30日三门峡抽奖概率 返回获奖 奖项"""
    total_num = {1: 0, 2: 2, 3: 19, 4: 0}
    total_award = {1: 0, 2: 30, 3: 999, 4: 0}
    now = datetime.datetime.now()
    choice_unm = random.randint(0, 1000)
    award_type = 0
    if choice_unm in [1, 2, 3]:
        award_type = 0
    elif 5 < choice_unm <= 55 and int(now.day) % 2 == 0:
        award_type = 2
    elif 100 < choice_unm <= 700:
        award_type = 3
    elif 700 < choice_unm <= 1000:
        award_type = 0
    exist = db.tbkt_web.active_award.filter(user_id=user_id, active_id=app_id, award_type=award_type).exists()
    award_num = get_daily_award_num(app_id, award_type, is_smx=1)

    if exist or award_num >= total_num.get(award_type, 0):
        return 0
    if award_type == 3:
        # 已经抽到的奖品数量
        num = get_now_award_num(app_id, award_type, now, is_smx=1)
        if num >= smx_pro_3.get(now.hour, 0):
            return 0
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


def get_yw_status(user):
    # 返回用户语文科目开通状态
    if db.ketang_slave.mobile_subject.filter(user_id=user.id, subject_id=5):
        return 1
    return 0
