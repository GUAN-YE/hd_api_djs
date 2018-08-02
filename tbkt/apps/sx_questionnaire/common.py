# coding:utf-8
import json

import time

from libs.utils import db
from apps.sx_summer.common import add_score
from apps.sx_summer.active_cofing import APP_ID_TEA


def submit(user, data):
    if not data or not user:
        return False, 'no_user'
    exist = db.tbkt_web.active_questionnaire.get(user_id=user.id)
    if exist:
        return False, u'请勿重复提交'

    # 统计
    count_num(data)
    # 保存用户记录：
    save_detail(user, data)

    # 加分
    unit = user.unit.id if user.unit else 0
    add_score(APP_ID_TEA, user.id, 3000, 'questionnaire', u'添加问卷调查加分', user.city or 0, unit)
    return True, ''


def count_num(data):
    """统计调查问卷详情"""
    qids = [d['qid'] for d in data]
    sql = """select qid,`option` from active_questionnaire_detail where qid in (%s)""" % ','.join(str(q) for q in qids)
    rows = db.tbkt_web.fetchall_dict(sql)
    rows_list = [(q.qid, q.option) for q in rows]

    update_detail = []
    insert_detail = []
    for d in data:
        qid = d['qid']
        option = d['option'].split(',')
        for op in option:
            if op.strip():
                if (qid, op) in rows_list:
                    d = (qid, op)
                    update_detail.append(d)
                else:
                    d = dict(qid=qid, option=op, num=1)
                    insert_detail.append(d)
    if insert_detail:
        db.tbkt_web.active_questionnaire_detail.bulk_create(insert_detail)
    if update_detail:
        sql = """update active_questionnaire_detail set num=num+1 where qid =%s and `option` =%s """
        db.tbkt_web.execute_many(sql, update_detail)


def save_detail(user, data):
    """保存调查问卷记录"""
    text = json.dumps(data)
    now = int(time.time())
    db.tbkt_web.active_questionnaire.create(user_id=user.id, text=text, add_time=now)
    return


def user_detail(user_id):
    """用户调查问卷"""
    if not user_id:
        return
    detail = db.tbkt_web.active_questionnaire.get(user_id=user_id)
    if not detail:
        return []
    text = json.loads(detail.text)
    return text
