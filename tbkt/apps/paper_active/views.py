# coding: utf-8
import logging

from com.com_user import need_login
from libs.utils import ajax, db


@need_login
def r_stu_list(request):
    """
    学生端奖品列表
    :param request: 
    :return: 
    """
    args = request.QUERY.casts(p=int)
    p = args.p or 1
    user = request.user
    app_id = 28 if user.city != '411200' else 30
    data = base_award_list(request, app_id, p)
    return ajax.jsonp_ok(request, data)


@need_login
def r_tea_list(request):
    """
    教师端奖品列表
    :param request: 
    :return: 
    """
    args = request.QUERY.casts(p=int)
    p = args.p or 1
    user = request.user
    app_id = 29 if user.city == '411200' else 27
    data = base_award_list(request, app_id, p)
    return ajax.jsonp_ok(request, data)


def base_award_list(request, app_id, p):
    """
    活动结束列表(公用)
    :param request:
    :param app_id: 
    :param p: 
    :return: 
    """
    sql = """
    select distinct a.user_id, a.award_name, a.user_name from 
    active_award a where a.award_name != '谢谢参与' and active_id = %s
    order by a.award_type asc limit %s,50
    """ % (app_id, (p - 1)*50)
    rows = db.tbkt_web_slave.fetchall_dict(sql)
    user_ids = [i.user_id for i in rows]
    info = db.ketang_slave.mobile_order_region.filter(user_id__in=user_ids).select('user_id', 'school_name')[:]
    info_map = {i.user_id: i.school_name for i in info}
    for r in rows:
        r.school_name = info_map.get(r.user_id, "")
    return rows

