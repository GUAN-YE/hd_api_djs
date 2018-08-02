# coding:utf8
import json
import re

from apps.full_class.math_com import replace_symbol
from libs.utils import db, Struct, join
from libs.utils import db, Struct, dedupe, time, join, tbktapi, get_absurl, num_to_ch


def user_grade(user_id):
    """
    查询用户设置教材的年级
    :return:
    """
    grade_id = db.tbkt_active.full_score_book_set.get(user_id=user_id)
    if not grade_id:
        return 1
    return grade_id.grade_id


def test_info(user_id, week_id, grade_id):
    """
    知识训练场用户是否完成训练
    :param user_id:
    :param week_id:
    :param grade_id:
    :return:
    """
    test = db.tbkt_active.full_score_test.select("text").get(
        user_id=user_id, week_id=week_id, grade_id=grade_id, type=2, status=1)
    return 1 if test else 0


def get_source(week_id, grade_id):
    """
    获取知识点信息
    :param week_id: 
    :param grade_id: 
    :return: 
    """
    source = db.tbkt_active.full_score_week_detail.select("knowledge_id", "week_id") \
        .get(week_id=week_id, grade_id=grade_id)
    if not source:
        return []
    kids = set(source.knowledge_id.split(","))
    hub = tbktapi.Hub()
    url = "/sx/knowledges"
    r = hub.sx.post(url, {"kid": join(list(kids))})
    if not r or r.response != "ok":
        return []
    return map(Struct, r.data)


def get_knowledge_list(user_id, week_id):
    """
    获取知识训练场列表数据
    :param user_id: 
    :param week_id: 
    :return: 
    """
    grade_id = user_grade(user_id)   # 获取用户设置教材id
    out = Struct()
    out.info = []                                               # 视频信息列表
    out.test_status = test_info(user_id, week_id, grade_id)     # 测试完成状态
    out.finish_status = 0                   # 视频完成状态
    out.q_num = 0
    source = get_source(week_id, grade_id)  # 获取课程资源
    if not source:
        return out

    test = db.tbkt_active.full_score_test.select("text").get(
        user_id=user_id, week_id=week_id, grade_id=grade_id, type=1)
    out.finish_status = 1 if test else 0

    for i, v in enumerate(source):
        if not test:
            if i == 0:
                status = 0
            else:
                status = -1
        else:
            text = test.text.split(",")
            if i == 0:
                if str(v.id) in text:
                    status = 1
                else:
                    status = 0
            else:
                if str(source[i - 1].id) in text:
                    status = 0
                    if str(source[i].id) in text:
                        status = 1
                else:
                    status = -1
        v.status = status
    out.info = source
    out.q_num = len(out.info)
    return out


def video_submit(user_id, knowledge_id, week_id, city):
    """
    保存用户提交看视频的记录
    :param user_id:
    :param knowledge_id: 用户观看知识点视频的knowledge_id
    :param week_id: 知识训练场的week_id
    :param city: 保存用户地市
    :return:
    """
    grade_id = user_grade(user_id)  # 获取用户设置教材id
    nowt = int(time.time())
    # 查看用户查看视频记录
    info = db.tbkt_active.full_score_test.get(user_id=user_id, week_id=week_id, grade_id=grade_id, type=1)
    if info and info.status == 1:
        return

    source = get_source(week_id, grade_id)
    if not source:
        return
    num = len(source)
    with db.tbkt_active as active:
        if not info:
            status = 1 if num == 1 else 0
            active.full_score_test.create(grade_id=grade_id,
                                          week_id=week_id,
                                          status=status,
                                          add_time=nowt,
                                          user_id=user_id,
                                          type=1,
                                          city=city,
                                          text=knowledge_id),
            return

        added = info.text.split(",")
        if str(knowledge_id) in added:
            return
        status = 1 if num - len(added) == 1 else 0
        added.append(knowledge_id)
        active.full_score_test.filter(id=info.id).update(text=join(added), status=status)


def get_knowledge_question(week_id, grade_id):
    """
    获取知识点题目信息
    :param week_id: 课程id
    :param grade_id:  用户教材id
    :return: 
    """
    source = db.tbkt_active.full_score_week_detail.select("knowledge_id") \
        .get(week_id=week_id, grade_id=grade_id)
    if not source:
        return []
    kids = map(int, source.knowledge_id.split(","))
    info = db.ziyuan.sx_knowledge_question.select("knowledge_id", "id", "content", "display_type", "options",
                                                  "answer").filter(knowledge_id__in=kids, status=1)[:]
    for i, v in enumerate(info):
        v.q_index = i + 1
        v.content = replace_symbol(v.content)
        if v.display_type == 2:
            v.answer = v.answer.split(',')
        else:
            v.answer = json.loads(replace_symbol(v.answer))
            v.options = json.loads(replace_symbol(v.options))
            v.options = sorted(v.options, key=lambda key: key["option"])
    return info


def knowledge_qid_info(user_id, week_id):
    """
    获取知识训练场知识点题目信息
    :param user_id:
    :param week_id: 获取题目的week_id
    :return:
    """
    grade_id = user_grade(user_id)
    out = Struct()
    questions = get_knowledge_question(week_id, grade_id)
    # return questions
    out.q_num = len(questions)
    out.info = questions
    test = db.tbkt_active.full_score_test.get(user_id=user_id, week_id=week_id, grade_id=grade_id, type=2)
    if not test:
        return out

    if test and test.status == 1:
        out.info = []
        return out

    txt = json.loads(test.text) if test.text else []
    qid = [i.get("qid") for i in txt]
    out.info = [i for i in out.info if i.id not in qid]
    return out


def test_submit(user_id, week_id, info, user_city):
    """
    提交知识点测试结果
    :param user_id:
    :param week_id:
    :param info:用户提交题目信息
    :param user_city:
    :return:
    """

    nowt = int(time.time())
    q_info = knowledge_qid_info(user_id, week_id)
    len_info = q_info.q_num
    test = db.tbkt_active.full_score_test.get(week_id=week_id, user_id=user_id, type=2, status=0,grade_id=user_grade(user_id))
    # 查询用户本周未完成记录 如果在原来的基础上添加新的记录 否则新建测试记录
    if test and test.status == 0:
        out = []
        save_info = json.loads(test.text)
        for i in save_info:
            out.append(i)
        for i in info:
            out.append(i)
        if len_info == len(out):
            status = 1
        else:
            status = 0

        db.tbkt_active.full_score_test.filter(user_id=user_id, type=2, week_id=week_id, status=0,grade_id=user_grade(user_id)).update(
            status=status,
            text=json.dumps(out),
        )
        return
    if len_info == len(info):
        status = 1
    else:
        status = 0

    with db.tbkt_active as active:
        active.full_score_test.create(
            user_id=user_id,
            grade_id=user_grade(user_id),
            week_id=week_id,
            type=2,
            text=json.dumps(info),
            status=status,
            add_time=nowt,
            city=user_city
        )
    return


def test_result(user_id, week_id):
    """
    测试结果页
    :param user_id:
    :param week_id:
    :return:
    """
    grade_id = user_grade(user_id)
    question = get_knowledge_question(week_id, grade_id)
    out = Struct()
    out.info = question
    out.wrong_name = []
    # 用户的答题记录 取出用户答案
    test = db.tbkt_active.full_score_test.select("text").get(user_id=user_id, week_id=week_id,
                                                             grade_id=grade_id, status=1, type=2)
    if not test:
        return out

    text = map(Struct, json.loads(test.text))
    wrong_kids = []
    test_map = {}
    for i in text:
        if i.display_type == 2:
            # 填空题类型 将答案格式化成数组
            i.result = i.result.split(',')
        if i.is_right == 0:
            wrong_kids.append(i.kid)
        # {kid: 对应用户答案}
        test_map[i.kid] = i.result
    # 取出知识点视频
    know_info = get_source(week_id, grade_id)
    know_map = {i.id: i for i in know_info}
    wrong_name = []
    for i in out.info:
        k = know_map.get(i.knowledge_id)
        i.video_url = k.video_url
        i.name = k.name
        user_answer = test_map.get(i.knowledge_id)
        if i.display_type == 2:
            i.content = filling(i.content, user_answer, i.answer)
        i.user_answer = user_answer
        if i.knowledge_id in wrong_kids:
            wrong_name.append(i.name)
    out.wrong_name = wrong_name
    return out


def filling(content, user_answer, right_answer):
    """
    用户答案与正确答案匹配
    生成对应class属性的span标签替换题干中的span
    用于填空题结果页
    :param content:      题干 str
    :param user_answer:  用户提交的答案 list
    :param right_answer: 正确答案 list
    :return: 
    """
    it = re.finditer(r'(<span .*?>)(.*?)(</span>)', content)
    for i, k in enumerate(it):
        try:
            ua = user_answer[i]
        except Exception as e:
            print e
            ua = ""
        ra = right_answer[i]
        replace = '<span class="wrong">%s</span>' % ua
        if ua == ra:
            replace = '<span class="right">%s</span>' % ua
        content = content.replace(k.group(), replace)
    return content

