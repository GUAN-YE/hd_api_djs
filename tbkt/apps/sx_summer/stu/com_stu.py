# coding:utf-8
import random
from collections import OrderedDict
import simplejson as json
import time
from apps.sx_summer import common
from apps.sx_summer.common import dedupe
from apps.sx_summer.active_cofing import *
from libs.utils import db, Struct


def get_paper_list(gread_id, user_id):
    """返回 年级 试卷列表"""

    grade = {1: u'一年级', 2: u'二年级', 3: u'三年级', 4: u'四年级', 5: u'五年级', 6: u'六年级'}
    # sql = """
    #
    # SELECT c.*,p.id paper_id,p.name paper_name,IFNULL(t.status,-1)status,IFNULL(t.id,0)test_id FROM (
    #     SELECT c1.id,c1.name,c2.name v_name  FROM tbkt_a_active_catalog c1
    #     JOIN tbkt_a_active_catalog c2 ON c2.id=c1.parent_id
    #     WHERE c1.active_id=45 AND c1.name='{0}' AND c2.`name`<>'青岛版')c
    # JOIN sx_paper_relate r ON r.object_id= c.id AND status=1
    # JOIN sx_paper p ON p.id=r.paper_id
    # LEFT JOIN tbkt_web.active_test t ON t.object_id=p.id AND t.active_id={2} AND t.user_id={1}
    # ORDER BY p.id
    # """.format(grade[gread_id].encode('utf-8'), user_id, APP_ID_STU)


    sql = """
    SELECT c.*,p.id paper_id,p.name paper_name FROM (
        SELECT c1.id,c1.name,c2.name v_name  FROM tbkt_a_active_catalog c1
        JOIN tbkt_a_active_catalog c2 ON c2.id=c1.parent_id
        WHERE c1.active_id=45 AND c1.name='%s' AND c2.`name`<>'青岛版')c
    JOIN sx_paper_relate r ON r.object_id= c.id AND status=1
    JOIN sx_paper p ON p.id=r.paper_id
    ORDER BY p.id"""%grade[gread_id].encode('utf-8')
    paper = db.ziyuan_slave.fetchall_dict(sql)

    sql = """SELECT t.object_id paper_id, t.status ,t.id  test_id FROM tbkt_web.active_test t where  t.active_id=%s AND t.user_id=%s"""%(APP_ID_STU,user_id)
    test = db.tbkt_web.fetchall_dict(sql)
    test_dict = {t.paper_id:t for t in test}
    for p in paper:
        t = test_dict.get(p.paper_id, {'paper_id':p.paper_id,'status':-1,'test_id':0})
        p.update(t)

    paper_dict = OrderedDict()
    for p in paper:
        paper_dict[p.v_name] = paper_dict.get(p.v_name, []) + [p]
    return paper_dict


def get_paper_detail(paper_id):
    """返回 试卷习题列表"""
    if not paper_id:
        return {}
    sql = """
    select a.id ask_id,a.question_id from sx_paper_question_number n
    inner join sx_paper_detail d on n.paper_id = %s and n.paper_id = d.paper_id and n.type = 2 and n.object_id = d.question_id
    inner join sx_question_ask a on a.question_id = d.question_id
    """ % paper_id
    # 按照试卷题目顺序 返回试卷题目信息
    paper = db.ziyuan_slave.fetchall_dict(sql)
    return paper


def get_or_creat_test(user_id, paper_Id):
    """创建测试记录"""
    test = db.tbkt_web.active_test.get(active_id=ACTIVE_ID, object_Id=paper_Id, user_id=user_id)
    if test:
        return test
    paper = db.ziyuan.sx_paper.get(id=paper_Id)
    test_id = db.tbkt_web.active_test.create(
        active_id=ACTIVE_ID,
        object_Id=paper_Id,
        user_id=user_id,
        title=paper.name,
        status=-1,
        add_time=int(time.time())
    )
    test = Struct()
    test.id = test_id
    test.status = 0
    test.title = paper.name
    return test


def get_test_question(user_id, qids, object_id):
    """
    返回作业题目信息
    :param object_id: paper_id
    :param user_id:   用户ID
    :param qids:      题目ID
    :return:
    """
    test = db.tbkt_web.active_test.filter(active_id=ACTIVE_ID, user_id=user_id, object_id=object_id).select("id").last()
    question = common.get_questions(qids)
    answer = []

    for q in question:
        for a in q.asks:
            a.user_answer = ""  # 用户答案
            a.user_result = ""  # 是否正确 1/0
    if test:
        detail = db.tbkt_web.active_test_detail.filter(test_id=test.id).select("question_id", "ask_id", "result",
                                                                               "answer")
        # 读取已做试题用户答案
        for q in question:
            for a in q.asks:
                for d in detail:
                    if a.id == d.ask_id:
                        a.user_answer = d.answer
                        a.user_result = d.result

        # 返回顺序题号 页面答题卡展示
        done = []
        answer = []
        done_qids = [i.question_id for i in detail]
        for d in done_qids:
            if d not in done:
                done.append(d)

        # 返回用户已做的结果
        for q in done:
            ask_list = []
            for d in detail:
                if q == d.question_id:
                    ask_list.append({"ask_id": d.ask_id, "option": d.answer, 'result': d.result})
                    db_result = {"ask_list": ask_list, "question_id": q}
                    if db_result not in answer:
                        answer.append({"ask_list": ask_list, "question_id": q})

        for i, qid in enumerate(done):
            for q in question:
                if q.id == qid:
                    q.number = i + 1

    return question, answer


submit_locks = {}


def test_submit(user, paper_id, status, data, test_type):
    global submit_locks

    key = (user.id, test_type, paper_id)
    if status == 1:
        if key in submit_locks:  # locking
            test = db.tbkt_web.active_test.get(active_id=ACTIVE_ID, user_id=user.old_user_id, object_id=paper_id)
            return {"test_id": test.id} if test else {"test_id": 0}
        submit_locks[key] = 1  # add lock
    try:
        return _test_submit(user, paper_id, status, data)
    finally:
        submit_locks.pop(key, None)  # release lock


def check_user_grade(user_id, paper_id):
    """检查用户提交的试卷是否为所选年级下的试卷"""
    grade = {1: u'一年级', 2: u'二年级', 3: u'三年级', 4: u'四年级', 5: u'五年级', 6: u'六年级'}
    user_grade = db.tbkt_web.active_user_book.get(active_id=APP_ID_STU, user_id=user_id)
    if not user_grade:
        return False
    grade_id = user_grade.book_id
    sql = """
            SELECT 1 FROM tbkt_a_active_catalog c
            JOIN sx_paper_relate r ON r.object_id= c.id AND r.status=1
            WHERE active_id=45 AND name='%s' AND paper_id=%s
            """ % (grade[grade_id], paper_id)
    paper = db.ziyuan_slave.fetchall_dict(sql)
    if paper:
        return True
    return False


def _test_submit(user, paper_id, status, data):
    """
    测试提交
    :param user_id:
    :param paper_id:试卷ID
    :param status:试卷ID
    :param data: 做题数据
    :return: 返回错题信息
    """

    # check = check_user_grade(user.old_user_id, paper_id)
    # if not check:
    #     return
    test = db.tbkt_web.active_test.get(active_id=ACTIVE_ID, user_id=user.old_user_id, object_id=paper_id)
    if not test or test.status == 1:
        return
    if test.status == 1:
        return {"test_id": test.id}
    if int(test.status) != 1:
        field = []  # 批量更新
        wrong_ask_ids = []  # 错题
        wrong_num = 0  # 错题数
        nask = 0  # 全部小题数
        all_ask_ids = []

        for d in data:
            has_wrong = False
            for a in d["ask_list"]:
                ask_id = int(a["ask_id"])
                question = int(d["question_id"])
                result = int(a["result"])
                option = a["option"]
                field.append([ACTIVE_ID, test.id, question, ask_id, option, result])
                all_ask_ids.append(ask_id)
                if result == 0:
                    has_wrong = True
                    if ask_id not in wrong_ask_ids:
                        wrong_ask_ids.append(ask_id)
                nask += 1
            if has_wrong:
                wrong_num += 1

        if field:
            # 删除保存的记录
            sql = """DELETE FROM active_test_detail WHERE test_id = %s and ask_id in (%s)""" % (
                test.id, ','.join(str(i) for i in all_ask_ids))
            db.tbkt_web.execute(sql)

            # 更新用户做题信息
            sql = """
            insert into  active_test_detail
            (active_id, test_id , question_id , ask_id , answer , result )
            VALUES (%s,%s,%s,%s,%s,%s)
            """
            db.tbkt_web.execute_many(sql, field)
            # 保存未掌握知识点
            save_knowledge_id(wrong_ask_ids, test.id, user.old_user_id)
        score = 0
        if status == 1:
            # 算分
            nwrong = len(wrong_ask_ids)
            score = int(100.0 * (nask - nwrong) / nask) if nask > 0 else 0

            _score = score * 2 if user.openstatus(2) else score
            unit = user.unit.id if user.unit else 0
            common.add_score(APP_ID_STU, user.id, _score, 'test', u'完成试卷获得%s' % _score, user.city or 0,unit)

        # 做完更新 状态 成绩
        sql = """
        update active_test set
        status = %s, score= %s, test_time = %s
        where active_id = %s and user_id = %s and object_id = %s
        """ % (status, score, int(time.time()), ACTIVE_ID, user.old_user_id, paper_id)
        db.tbkt_web.execute(sql)
    return {"test_id": test.id}


def test_special(user_id, special_id, status, data):
    """
    保存个性化学习记录
    王世成
    special_id: 个性化学习主记录

    status: 1/0 是否做完
    data: 具体做题数据
    :return:
    """
    # 更新个性化学习主记录状态
    special = db.tbkt_web.active_special.get(id=special_id)
    if status == 1:
        sql = """
        update active_special set status = %s where id = %s
        """ % (status, special_id)
        db.tbkt_web.execute(sql)
    detail_args = []
    correct_ask = []
    for q in data:
        for a in q["ask_list"]:
            ask_id = a["ask_id"]
            result = a["result"]
            option = a["option"]
            option_id = 0
            option_list = db.ziyuan_slave.sx_ask_options.filter(ask_id=ask_id)
            for op in option_list:
                content = json.loads(op.content) if op.content else {}
                if content.get("option") == option:
                    option_id = op.id
                    if content.get("is_right") == "1":
                        result == 1
                        correct_ask.append(a["ask_id"])
                        break
            detail_args.append((option, result, option_id, special_id, q["question_id"], ask_id))
    detail_update = """
                    update active_special_detail set answer=%s, result=%s, option_id=%s
                    where test_id = %s and question_id = %s and ask_id = %s
                    """
    db.tbkt_web.execute_many(detail_update, detail_args)
    kids = common.get_ask_kids(correct_ask)

    # 如果有答对的知识点 修正状态
    if special:
        db.tbkt_web.active_weak_knowledge.filter(user_id=special.user_id,
                                                 knowledge_id__in=kids,
                                                 object_id=special.object_id).update(status=1)
    return special_id


def save_knowledge_id(ask_ids, test_id, user_id):
    """
    保存未掌握知识点
    :param ask_ids: 错题id
    :param test_id: 测试主记录ID active_test
    :param user_id:
    :return:
    """
    # 关联知识点
    kids = common.get_ask_kids(ask_ids)
    weak = db.tbkt_web.active_weak_knowledge.filter(active_id=ACTIVE_ID,
                                                    object_id=test_id,
                                                    knowledge_id__in=kids).flat("knowledge_id")
    # 是否已保存
    kids = [i for i in kids if i not in weak]

    if kids:
        field = []
        for k in kids:
            r = dict(active_id=ACTIVE_ID,
                     user_id=user_id,
                     book_id=0,
                     catalog_id=0,
                     knowledge_id=k,
                     object_id=test_id,
                     status=0,
                     add_time=int(time.time()))
            field.append(r)
        # 批量生成
        db.tbkt_web.active_weak_knowledge.bulk_create(field)


def test_evaluate(test_id):
    """
    练习结果页
    :param test_id: 测试记录ID
    :return:
    """
    if not test_id:
        return {}
    # 读取缓存
    test = db.tbkt_web.active_test.get(id=test_id, active_id=ACTIVE_ID)

    question_list = []
    wrong_question = []
    paper_detail = get_paper_detail(test.object_id)
    question_ids = list(dedupe([i.question_id for i in paper_detail]))
    details = db.tbkt_web.active_test_detail.filter(test_id=test_id, question_id__in=[i for i in question_ids])
    for qid in question_ids:
        result = 1
        for d in details:
            if d.question_id == qid and d.result == 0:
                result = 0
                break
        d = Struct()
        d.result = result
        d.qid = qid
        if result == 0:
            wrong_question.append(qid)
        question_list.append(d)

    sql = """
    select distinct k.id,if(k.name!='',k.name,r.name) name from sx_knowledge k
    inner join (select distinct knowledge_id from sx_ask_relate_knowledge r where r.question_id in (%s))a
    on a.knowledge_id = k.id inner join sx_text_book_catalog_relate_knowledge r on r.knowledge_id = k.id
    """ % (','.join(str(i) for i in wrong_question) or 0)
    knowledge_list = db.ziyuan_slave.fetchall_dict(sql)

    new_knowledge_list = []
    for obj in knowledge_list:
        d = Struct()
        d.knowledge_id = obj.id
        d.name = obj.name
        new_knowledge_list.append(d)

    data = Struct()
    data.test_id = test_id  # 测试记录ID
    data.test_name = test.title if test else ""  # 标题名称
    data.knowledge_count = len(new_knowledge_list)  # 未掌握知识点
    data.knowledge_list = new_knowledge_list  # 知识点信息
    data.wrong_qid = list(dedupe(wrong_question))
    data.all_qid = list(dedupe([d.qid for d in question_list]))
    return data


def get_question_asks(qids):
    """
    返回qid下的小题id
    :param qids:
    :return:
    """
    if not qids:
        return
    qids = ','.join(str(i) for i in qids)

    sql = """
    select n.question_id, n.id from sx_question q, sx_question_ask n
    where q.id in (%s) and n.question_id = q.id and  n.display_type = 1
    """ % qids
    rows = db.ziyuan_slave.fetchall_dict(sql)
    return set(rows)


def get_weakkids(test):
    """
    获得某次测试的薄弱知识点ID
    :param test: 测试记录active_test
    :return: [知识点ID]
    """
    sql = """
    select distinct knowledge_id from active_weak_knowledge
    where active_id = %s and user_id = %s and object_id = %s and status=0
    """ % (test.active_id, test.user_id, test.id)
    rows = db.tbkt_web_slave.fetchall(sql)
    return [r[0] for r in rows]


def get_allkids(test):
    """
    获得某次测试涉及的全部知识点ID

    :param test: 测试记录active_test
    :return: [知识点ID]
    """
    sql = """
    select distinct k.knowledge_id from active_test_detail d inner join
    ziyuan_new.sx_ask_relate_knowledge_new k where d.test_id = %s and k.ask_id = d.ask_id
    """ % test.id
    rows = db.tbkt_web_slave.fetchall(sql)
    return [r[0] for r in rows]


def get_exclude_qids(test):
    """
    获得某次测试以及专项训练出过的全部试题ID

    :param test: active_test
    :return: [题ID]
    """
    # 原测试做过的题
    sql = """
    select distinct question_id from active_test_detail
    where test_id=%s
    """ % test.id
    rows = db.tbkt_web_slave.fetchall(sql)
    qids1 = [r[0] for r in rows]
    # 专项训练做过的题
    sql = """
    select distinct d.question_id from active_special t
    inner join active_special_detail d on d.test_id=t.id
    where t.test_id=%s
    """ % test.id
    rows = db.tbkt_web_slave.fetchall(sql)
    qids2 = [r[0] for r in rows]
    # 合并&去重
    qids = qids1 + qids2
    qids = list(set(qids))
    return qids


def make_knowledge_qids(kids, exclude_qids=[], limit=10):
    """
    根据知识点出题

    :param kids: 知识点ID
    :param exclude_qids: [已做过的题ID]
    :param limit: 最多出几道题
    :return: [题ID]
    """
    if not kids:
        return []
    # 排除已经做过的题
    exclude_qids_s = list(set(exclude_qids))

    kids_s = ','.join(str(i) for i in kids)
    sql = """
    select distinct question_ids from tbkt_web.active_weak_knowledge
    where knowledge_id in (%s)
    """ % kids_s
    rows = db.tbkt_web_slave.fetchall(sql)
    qids = []
    # 规则：每个知识点取一道大题
    for s, in rows:
        qid_k = map(int, s.split(','))
        qid = [q for q in qid_k if q not in exclude_qids_s]
        if qid:
            qids += random.sample(qid, 1)
    # 去重
    qids = list(set(qids))
    return qids[:limit]


def get_user_tea(unit_id):
    """返回数学教师id"""

    sql = """select r.user_id id, r.city from mobile_order_region r
                    where  r.unit_class_id=%s and r.user_type=3""" % unit_id
    row = db.ketang_slave.fetchall_dict(sql)
    ids = [t.id for t in row]
    if not ids:
        return []
    sql = """select id from auth_user where id in (%s) and sid=2 """%','.join(str(i) for i in ids)
    rows = db.tbkt_user.fetchall_dict(sql)
    sx_tea = [r.id for r in rows]
    tea = []
    for r in row:
        if r.id in sx_tea:
            tea.append(r)
    return tea
