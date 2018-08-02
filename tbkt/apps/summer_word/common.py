#coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: common.py
@time: 2017/8/2 18:14
"""

from libs.utils import db
from libs.utils.common import Struct


def get_unit_yyteacher(unit_id):
    """
    功能说明：                获取班级的英语教师
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-8-2
    """
    teachers = db.ketang_slave.mobile_order_region.filter(unit_class_id=unit_id)[:]  # 该班级所有教师
    tids = [t.user_id for t in teachers]  # 该班级所有教师的id
    tea_dict = {}
    for t in teachers:
        tea_dict[t.user_id] = t

    yy_teacher = db.tbkt_user_slave.auth_user.filter(id__in=tids, type=3, sid=9)[0]
    if not yy_teacher:
        return 0
    yy_tea = tea_dict.get(yy_teacher.id)
    yy_tea.update(yy_teacher)
    return yy_tea

def get_users_name(user_ids, type):
    """
    功能说明：                获取多个用户的名字信息
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-8-2
    """
    if not user_ids:
        return {}
    users = db.tbkt_user_slave.auth_user.select('real_name', 'id').filter(id__in=user_ids, type=type)[:]
    user_dict = {}
    ids = []
    for obj in users:
        ids.append(obj.id)
        user_dict[int(obj.id)] = obj.real_name
    return user_dict, ids