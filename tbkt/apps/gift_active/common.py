#coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: common.py
@time: 2017/10/21 11:40
"""
import time
from libs.utils import db

def join_active(user_id, gift_active_id):
    """
    功能说明：                金豆商城活动， 参加活动
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张嘉麒                    2017-11-07
    """
    if not user_id or not gift_active_id:
        return u'没有user_id, 参数错误'
    if db.tbkt_gift_active.gift_active_user.filter(user_id=user_id, gift_active_id=gift_active_id).exists():
        return u'已经参加活动了'
    need_coin = 5
    user_coin = db.default.score_user.get(user_id=user_id, app_id=7)
    if user_coin:
        user_coin_num = user_coin['score']
    else:
        return u'查不到用户相应金币信息'
    if user_coin >= need_coin:
        user_coin_num -= need_coin
    else:
        return u'金币不足'
    nowt = int(time.time())
    with db.default as com:
        com.score_user.filter(user_id=user_id,app_id=7).update(score=user_coin_num)
        com.score_user_detail.create(
            user_id=user_id,
            score=need_coin,
            app_id=7,
            item_no=u'tea_voucher',
            remark=u'教师礼品商域活动',
            add_date=nowt,
            cycle_num=0
        )
    db.tbkt_gift_active.gift_active_user.create(
        user_id=user_id,
        gift_active_id=gift_active_id,
        add_date=nowt
    )
    return ''

def active_status(user_id, gift_active_id):
    """
    功能说明：                金豆商城活动， 用户时候参加活动， 0 没有， 1参加过
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-10-21
    """
    if not user_id or not gift_active_id:
        return 1
    if db.tbkt_gift_active.gift_active_user.filter(user_id=user_id, gift_active_id=gift_active_id).exists():
        return 1
    return 0


def active_count(gift_active_id):
    """
    功能说明：                获取当前参与此次金豆活动的人数
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张嘉麒                    2017-11-07
    """
    active_count_sql = db.tbkt_gift_active.gift_active_user.filter(gift_active_id=gift_active_id)
    if active_count_sql:
        count = active_count_sql.count()
    else:
        count = 0
    return count