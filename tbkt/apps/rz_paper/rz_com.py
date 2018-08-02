#coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: rz_com.py
@time: 2017/12/21 9:14
"""

import json
import time

from libs.utils import db
from apps.common import com_yy
from libs.utils.common import Struct


PAPER = {
    3: [9681, 3845, 19263, 18128, 18610, 17470, 17108, 7805, 18136, 18611,
        16267, 14031, 18937, 18903, 17076, 17747, 17725, 5964, 19026, 2690],
    4: [3300, 3104, 17583, 18850, 14323, 10901, 3065, 19448, 17895, 18826,
        15295, 5861, 16058, 6144, 6171, 13700, 6000, 10805, 16158, 20015],
    5: [11755, 13037, 19435, 2949, 19229, 17373, 3102, 13069, 5784, 5764,
        17281, 19876, 5900, 6211, 6185, 16126, 6116, 6052, 1419, 20020],
    6: [2996, 6558, 2992, 10156, 15781, 10160, 3119, 6734, 4752, 5810, 1138,
        19365, 6016, 15799, 6220, 6222, 16107, 942, 6119, 20024]
}


def get_paper_question_number_sheet(user_id, active_id, paper_id):
    """获得试卷中的 未完成的习题id和答题卡， 要是没有测试记录的话，创建测试记录"""
    data = Struct()
    test_flag = create_test(user_id, active_id, paper_id)
    if not test_flag:
        data.numbers = []
        data.sheet = []
        return data

    numbers, sheet = com_yy.get_active_paper_question_number_sheet(user_id, active_id, paper_id)
    data.numbers = numbers
    data.sheet = sheet
    return data

def create_test(user_id, active_id, paper_id):
    """要是没有测试记录的话，创建测试记录"""
    test = db.tbkt_active_slave.active_paper.filter(user_id=user_id, active_id=active_id,
                                                    paper_id=paper_id).select('id')
    if test:
        return True
    qids = PAPER.get(paper_id, [])
    if not qids:
        return False

    aid_dict = com_yy.get_aid_dict(qids)
    nowt = int(time.time())
    with db.tbkt_active as ac:
        ac.active_paper.create(
            active_id=active_id,
            user_id=user_id,
            paper_id=paper_id,
            nquestion=len(qids),
            add_time=nowt,
            status=-1
        )
        details = []
        for qid in qids:
            ask_ids = aid_dict.get(qid, [])
            for ask_id in ask_ids:
                details.append({
                    "qid": qid,
                    "aid": ask_id,
                    "result": -1,
                    "answer": '',
                    "oid": 0,
                })
        ac.active_paper_detail.create(
            user_id=user_id,
            active_id=active_id,
            paper_id=paper_id,
            text=json.dumps(details),
            add_time=nowt
        )
    return True

def paper_submit(user_id, active_id, paper_id, status, data):
    """
    提交试卷做题记录
    """
    com_yy.paper_submit(user_id, active_id, paper_id, status, data)