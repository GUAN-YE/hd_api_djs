# coding:utf-8
import json
import random

import time

from collections import defaultdict

from libs.utils import db, Struct, join
from libs.utils.tbktapi import Hub

WRONG_TYPE = 4


def get_wrong_source(week_id, grade_id):
    data = db.tbkt_active.full_score_week_detail.get(week_id=week_id, grade_id=grade_id)
    return json.loads(data.wrong_qid) if data and data.wrong_qid else []


def get_wrong_question(user_id, week_id, grade_id):
    """
    获取高频试题资源
    :param week_id: 
    :param grade_id:
    :param user_id: 
    :return: 
    """
    # 获取题目信息
    data = get_wrong_source(week_id, grade_id)
    if not data:
        return []
    test = db.tbkt_active.full_score_test.select('text').get(user_id=user_id,
                                                             week_id=week_id,
                                                             grade_id=grade_id, type=WRONG_TYPE)

    if test and test.status == 1:
        # 用户已完成当前练习
        return []
    text = json.loads(test.text) if test and test.text else []
    text_map = defaultdict(dict)
    for i in text:
        temp = Struct(i)
        text_map[str(temp.qid)].update({temp.aid: (temp.option, temp.result)})

    qids = [str(i.get("qid")).strip() for i in text]
    qid_map = {str(i.get("qid")).strip(): (i.get("count"), i.get("ratio", "75%")) for i in data if i.get("qid")}
    source_qids = [str(i.get("qid")).strip() for i in data]
    r = Hub().sx.get("/sx/questions", dict(qid=join(source_qids)))
    if not r or r.response != "ok":
        return []
    questions = map(Struct, r.data)
    questions = [i for i in questions if i not in qids]
    print [i.id for i in questions]
    out = []
    for i in questions:
        q = text_map.get(str(i.id))
        asks = map(Struct, i.asks)
        if q and len(asks) == len(q):
            continue
        if not qid_map.get(str(i.id)):
            continue
        i.count, i.ratio = qid_map.get(str(i.id))
        temp = int(i.ratio.replace("%", ""))

        i.ratio = "%s%%" % (temp + 20) if temp <= 55 else i.ratio
        i.count = random.randint(217, 500) + i.count
        for ask in asks:
            option, result = q.get(ask.id, ("", "")) if q else ("", "")
            ask.user_answer = option
            ask.user_result = result
        i.asks = asks
        out.append(i)
    return out


def get_question_ask(grade_id, week_id):
    """
    获取小题id
    :param grade_id:
    :param week_id:
    :return:
    """
    data = get_wrong_source(grade_id, week_id)
    if not data:
        return []
    qids = [i.get("qid") for i in data if i.get("qid")]
    return db.ziyuan.sx_question_ask.select('id').filter(question_id__in=qids).flat("id")[:]


def wrong_submit(user_id, week_id, grade_id, data, user_city):
    """
    高频错题提交
    :param user_id:
    :param data:
    :param week_id:
    :param grade_id:
    :param user_city:
    :return:
    """
    test = db.tbkt_active.full_score_test.select('id', 'text', "status") \
        .get(user_id=user_id, week_id=week_id, grade_id=grade_id, type=WRONG_TYPE)
    if test and test.status == 1:
        return test.id

    with db.tbkt_active as active:
        ask_ids = get_question_ask(week_id, grade_id)
        if not test:
            status = 1 if len(data) == len(ask_ids) else 0

            test_id = active.full_score_test.create(
                user_id=user_id,
                week_id=week_id,
                grade_id=grade_id,
                status=status,
                text=json.dumps(data),
                type=WRONG_TYPE,
                city=user_city,
                add_time=int(time.time())
            )
            return test_id
        text = json.loads(test.text) if test and test.text else []

        added = {i.get("aid"): i for i in text}

        for i in data:
            ask_id = i.get("aid")
            temp = added.get(ask_id)
            if temp:
                for txt in text:
                    if txt.get("aid") == ask_id:
                        txt.update(i)
            else:
                text.append(i)
        status = 1 if len(text) == len(ask_ids) else 0
        db.tbkt_active.full_score_test.filter(id=test.id).update(status=status, text=json.dumps(text))
        return test.id


def wrong_result(user_id, week_id, grade_id):
    """
    高频错题结果页
    :param user_id:
    :param week_id:
    :param grade_id:
    :return:
    """
    data = get_wrong_source(week_id, grade_id)
    if not data:
        return []
    test = db.tbkt_active.full_score_test.select('text').get(user_id=user_id,
                                                             week_id=week_id,
                                                             grade_id=grade_id,
                                                             type=WRONG_TYPE)
    if not test or not test.text:
        return []

    text = map(Struct, json.loads(test.text)) if test and test.text else []
    result_map = {}
    for i in text:
        result_map[i.aid] = (i.option, i.result)

    qids = [i.get("qid") for i in data]
    r = Hub().sx.get("/sx/questions", dict(qid=join(qids)))
    if not r or r.response != "ok":
        return []
    questions = map(Struct, r.data)
    for i in questions:
        for a in i["asks"]:
            option, result = result_map.get(a['id'], ("", ""))
            a["user_answer"] = option
            a["user_result"] = result
    # 对结果页进行排序 与题目返回数据顺序一致
    # questions = sorted(questions,key=lambda x:(-i for i,v in enumerate(questions)))
    return questions
