#coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: com_paper.py
@time: 2017/4/7 15:29
"""

import time

from libs.utils import db, json
from libs.utils.common import Struct
from . import com_user
from . import com_method


#试卷id对应的试卷名字
PAPER = {
    101: '提分试卷-卷(一)',
    102: '提分试卷-卷(二)',
    103: '提分试卷-卷(三)',
    104: '提分试卷-卷(四)',
    105: '提分试卷-卷(五)',
    106: '提分试卷-卷(一)',
    107: '提分试卷-卷(二)',
    108: '提分试卷-卷(三)',
    109: '提分试卷-卷(四)',
    110: '提分试卷-卷(五)',
    111: '提分试卷-卷(一)',
    112: '提分试卷-卷(二)',
    113: '提分试卷-卷(三)',
    114: '提分试卷-卷(四)',
    115: '提分试卷-卷(五)',
    116: '提分试卷-卷(一)',
    117: '提分试卷-卷(二)',
    118: '提分试卷-卷(三)',
    119: '提分试卷-卷(四)',
    120: '提分试卷-卷(五)',
    121: '提分试卷-卷(一)',
    122: '提分试卷-卷(二)',
    123: '提分试卷-卷(三)',
    124: '提分试卷-卷(四)',
    125: '提分试卷-卷(五)',
    126: '提分试卷-卷(一)',
    127: '提分试卷-卷(二)',
    128: '提分试卷-卷(三)',
    129: '提分试卷-卷(四)',
    130: '提分试卷-卷(五)',
    131: '提分试卷-卷(一)',
    132: '提分试卷-卷(二)',
    133: '提分试卷-卷(三)',
    134: '提分试卷-卷(四)',
    135: '提分试卷-卷(五)',
    136: '提分试卷-卷(一)',
    137: '提分试卷-卷(二)',
    138: '提分试卷-卷(三)',
    139: '提分试卷-卷(四)',
    140: '提分试卷-卷(五)',
    141: '提分试卷-卷(一)',
    142: '提分试卷-卷(二)',
    143: '提分试卷-卷(三)',
    144: '提分试卷-卷(四)',
    145: '提分试卷-卷(五)',
    146: '提分试卷-卷(一)',
    147: '提分试卷-卷(二)',
    148: '提分试卷-卷(三)',
    149: '提分试卷-卷(四)',
    150: '提分试卷-卷(五)',
    151: '提分试卷-卷(一)',
    152: '提分试卷-卷(二)',
    153: '提分试卷-卷(三)',
    154: '提分试卷-卷(四)',
    155: '提分试卷-卷(五)',
    156: '提分试卷-卷(一)',
    157: '提分试卷-卷(二)',
    158: '提分试卷-卷(三)',
    159: '提分试卷-卷(四)',
    160: '提分试卷-卷(五)',

    161: '提分试卷-卷(一)',
    162: '提分试卷-卷(二)',
    163: '提分试卷-卷(三)',
    164: '提分试卷-卷(四)',
    165: '提分试卷-卷(五)',
    166: '提分试卷-卷(一)',
    167: '提分试卷-卷(二)',
    168: '提分试卷-卷(三)',
    169: '提分试卷-卷(四)',
    170: '提分试卷-卷(五)',
    171: '提分试卷-卷(一)',
    172: '提分试卷-卷(二)',
    173: '提分试卷-卷(三)',
    174: '提分试卷-卷(四)',
    175: '提分试卷-卷(五)',
    176: '提分试卷-卷(一)',
    177: '提分试卷-卷(二)',
    178: '提分试卷-卷(三)',
    179: '提分试卷-卷(四)',
    180: '提分试卷-卷(五)'
}

def get_class_stu_paper_progress(task_id, class_id):
    students = com_user.get_class_students_all(class_id)
    students = [s for s in students if s.bind_id]
    students.sort(lambda x, y: cmp(x.first_name, y.first_name))  # 按照姓名进行排序
    stu_ids = set([int(s.id) for s in students])                             # 所有学生的id

    stu_ids = ','.join(str(u) for u in stu_ids)
    if not stu_ids:
        return [], [], 0

    sql = "SELECT id, user_id from yy_task_progress WHERE task_id= %s " \
          " and `status` = 1 and user_id in (%s);" % (task_id, stu_ids)

    task_finish_list = db.tbkt_yingyu.fetchall_dict(sql)

    finish_stu_ids = [task.user_id for task in task_finish_list]  # 完成作业的学生user_id 集合
    no_finish_students = []  # 未完成作业的学生信息
    finish_students = []       # 完成作业的学生信息
    for stu in students:
        if stu.id not in finish_stu_ids:
            no_finish_students.append(stu)
    for stu in students:
        if stu.id in finish_stu_ids:
            finish_students.append(stu)
    task_finish = get_task_finish_count(task_id, no_finish_students)
    return finish_students, no_finish_students, task_finish

def get_task_finish_count(task_id, no_finish_students):
    """获取班级做作业的小项数"""
    no_finish_students = ','.join(str(u.id) for u in no_finish_students if u.id)
    if not no_finish_students:
        return 0
    sql = "select id from yy_test where user_id in(%s) and object_id = %s AND status = 1;" % (no_finish_students, task_id)
    task_finished = db.tbkt_yingyu.fetchall_dict(sql)
    if task_finished:
        return 1
    else:
        return 0

# def get_stu_paper(task_id, stu_id):
#     """
#     功能说明：               得到学生试卷作业的完成情况
#     -----------------------------------------------
#     修改人                    修改时间
#     -----------------------------------------------
#     张帅男                    2017-4-6
#     """
#     sql = "SELECT DISTINCT(catalog_id) AS paper_id FROM yy_task_detail " \
#           "WHERE task_id = %s ORDER BY id;" % task_id
#     task_datas = db.tbkt_yingyu.fetchall_dict(sql)
#     paper_ids = set([int(task.paper_id) for task in task_datas])  # 作业包含的试卷id
#     paper_ids_t = tuple(paper_ids)
#     if len(paper_ids_t) == 1:
#         paper_ids_t = (paper_ids_t[0], 0)
#     sql = "SELECT catalog_id, `status`, id FROM yy_test" \
#           " WHERE object_id = %s AND catalog_id in %s AND user_id = %s;" % (task_id, paper_ids_t, stu_id)
#     paper_status = db.tbkt_yingyu.fetchall_dict(sql)
#     paper_dicts = {}
#     for obj in paper_status:
#         paper_dicts[obj.catalog_id] = obj
#     data = []
#     for pid in paper_ids:
#         row = Struct()
#         row.title = PAPER[pid]
#         row.pid = pid
#         if pid in paper_dicts.keys():
#             row.status = paper_dicts[pid].status
#             row.test_id = paper_dicts[pid].id
#         else:
#             row.status = 0
#             row.test_id = 0
#         data.append(row)
#     # data.sort(key=lambda x: x.pid)
#     return data

def get_paper_title(test_id, stu_name):
    """
    功能说明：               得到学生试卷作业的标题
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-4-6
    """
    title = db.tbkt_yingyu.yy_test.select('catalog_id').get(id=test_id)
    if title:
        return stu_name.encode('utf-8') + PAPER[title.catalog_id]
    return stu_name.encode('utf-8')

# def get_test(user_id, task_id, paper_id):
#     """
#     功能说明：                获得试卷的测试情况， 没有的话，创建记录
#     -----------------------------------------------
#     修改人                    修改时间
#     -----------------------------------------------
#     张帅男                    2017-4-7
#     """
#     sql = """select id, nquestion from yy_test where user_id =%s and object_id=%s AND catalog_id=%s""" % (
#         user_id, task_id, paper_id)
#     test = db.tbkt_yingyu.fetchone_dict(sql)
#     if test:
#         return test
#     # 创建测试记录
#     sql = """select id,question_id from yy_task_detail where task_id = %s and content_type=9 AND catalog_id = %s""" % \
#           (task_id, paper_id)
#
#     details = db.tbkt_yingyu.fetchall_dict(sql)
#     qids = [d.question_id for d in details]
#     # qids.sort()
#     aid_dict = com_method.get_aid_dict(qids)
#     nowt = int(time.time())
#
#     sql = """insert into yy_test  (user_id,object_id,catalog_id,nquestion,score,status,add_time)
#     VALUES (%s,%s,%s,%s,0,0,%s)""" % (user_id, task_id, paper_id, len(qids), nowt)
#     test_id = db.tbkt_yingyu.execute(sql)[1]
#
#     test = Struct({'id': test_id, 'nquestion': len(qids)})
#     # 保存details
#     details = []
#     for qid in qids:
#         ask_ids = aid_dict.get(qid, [])
#         for ask_id in ask_ids:
#             d = dict(
#                 test_id=test['id'],
#                 question_id=qid,
#                 ask_id=ask_id,
#                 result=-1
#             )
#             details.append(d)
#     db.tbkt_yingyu.yy_test_detail.bulk_create(details)
#     return test

# def get_task_details(task_id):
#     "返回作业任务列表"
#     sql = """select id,content_type,catalog_id from yy_task_detail where task_id=%s""" % task_id
#     task_details = db.tbkt_yingyu.fetchall_dict(sql)
#     details = []
#     s = set()
#     for d in task_details:
#         d.task_id = task_id
#         k = (d.content_type, d.catalog_id)
#         if k not in s:
#             details.append(d)
#             s.add(k)
#     return details

# def update_progress(user_id, task_id):
#     """更新英语作业总状态"""
#     details = get_task_details(task_id)
#     test_details = [d for d in details if d.content_type == 9]
#     y = 0  # 完成数
#     n = 0  # 未完成数
#     if test_details:
#         sql = """select id, object_id, status, catalog_id from yy_test where user_id=%s and object_id =%s ORDER BY id DESC """ % (
#             user_id, task_id)
#         test = db.tbkt_yingyu.fetchall_dict(sql)
#         test_dict = {}
#         for obj in test:
#             test_dict[(obj.object_id, obj.catalog_id)] = obj
#         for d in test_details:
#             # a = (d.task_id, d.catalog_id)
#             s = test_dict.get((d.task_id, d.catalog_id))
#             if s and s.status == 1:
#                 y += 1
#             else:
#                 n += 1
#     status = 1 if n <= 0 else 2
#
#     nowt = int(time.time())
#     sql = """select id,status from yy_task_progress where user_id =%s and task_id=%s""" % (user_id, task_id)
#     progress = db.tbkt_yingyu.fetchone_dict(sql)
#
#     if progress:
#         sql = """update yy_task_progress set `status`=%s ,update_time=%s  where id=%s""" % (status, nowt, progress.id)
#     else:
#         sql = """insert into yy_task_progress (user_id,task_id,`status`,update_time) VALUES (%s,%s,%s,%s)""" % (
#             user_id, task_id, status, nowt)
#
#     db.tbkt_yingyu.execute(sql)



def get_test(user_id, task_id, paper_id):
    """
    功能说明：                获得试卷的测试情况， 没有的话，创建记录
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-4-7
    """
    sql = """select id, nquestion from yy_test where user_id =%s and object_id=%s """ % (
        user_id, task_id)
    test = db.tbkt_yingyu.fetchone_dict(sql)
    if test:
        return test
    # 创建测试记录
    sql = """select id,text from yy_task_detail where task_id = %s and content_type=10 AND text like '%%%s%%'""" % \
          (task_id, paper_id)

    details = db.tbkt_yingyu.fetchall_dict(sql)
    qids = []
    for d in details:
        text = json.loads(d.text)
        for i in text:
            qids.append(i['qid'])
    print qids
    # qids.sort()
    aid_dict = com_method.get_aid_dict(qids)
    nowt = int(time.time())

    sql = """insert into yy_test  (user_id,object_id,catalog_id,nquestion,score,status,add_time)
    VALUES (%s,%s,%s,%s,0,0,%s)""" % (user_id, task_id, paper_id, len(qids), nowt)
    test_id = db.tbkt_yingyu.execute(sql)[1]

    test = Struct({'id': test_id, 'nquestion': len(qids)})
    # 保存details
    details = []
    for qid in qids:
        ask_ids = aid_dict.get(qid, [])
        for ask_id in ask_ids:
            str = [{"qid":qid,"aid":ask_id}]
            d = dict(
                object_id=test['id'],
                text = json.dumps(str),
                result=-1
            )
            details.append(d)
    db.tbkt_yingyu.yy_test_detail.bulk_create(details)
    return test


def update_progress(user_id, task_id):
    """更新英语作业总状态"""
    details = get_task_details(task_id)
    test_details = [d for d in details if d.content_type == 10]
    y = 0  # 完成数
    n = 0  # 未完成数
    if test_details:
        sql = """select id, object_id, status, catalog_id from yy_test where user_id=%s and object_id =%s ORDER BY id DESC """ % (
            user_id, task_id)
        test = db.tbkt_yingyu.fetchall_dict(sql)
        test_dict = {}
        for obj in test:
            test_dict[(obj.object_id, obj.catalog_id)] = obj
        for d in test_details:
            # a = (d.task_id, d.catalog_id)
            s = test_dict.get((d.task_id, d.catalog_id))
            if s and s.status == 1:
                y += 1
            else:
                n += 1
    status = 1 if n <= 0 else 2

    nowt = int(time.time())
    sql = """select id,status from yy_task_progress where user_id =%s and task_id=%s""" % (user_id, task_id)
    progress = db.tbkt_yingyu.fetchone_dict(sql)

    if progress:
        sql = """update yy_task_progress set `status`=%s ,update_time=%s  where id=%s""" % (status, nowt, progress.id)
    else:
        sql = """insert into yy_task_progress (user_id,task_id,`status`,update_time) VALUES (%s,%s,%s,%s)""" % (
            user_id, task_id, status, nowt)

    db.tbkt_yingyu.execute(sql)


def get_task_details(task_id):
    "返回作业任务列表"
    sql = """select id,content_type,catalog_id from yy_task_detail where task_id=%s""" % task_id
    task_details = db.tbkt_yingyu.fetchall_dict(sql)
    details = []
    s = set()
    for d in task_details:
        d.task_id = task_id
        k = (d.content_type, d.catalog_id)
        if k not in s:
            details.append(d)
            s.add(k)
    return details