# coding=utf-8
# test task 公共方法

from django.conf import settings
import simplejson as json
from libs.utils import db, get_absurl
import random
from libs.utils.common import Struct
import time
import re
from datetime import datetime, date
from . import com_yy
from com.com_cache import cache

FILE_ROOT = settings.FILE_WEB_URLROOT + "/upload_media/"
TTS_ROOT = settings.FILE_WEB_URLROOT + "/upload_media/tts/"


def format_media_url(url):
    """文件url 添加前缀"""
    if not url:
        return ''
    if url.startswith("http"):
        return url
    if url.endswith("mp3"):
        return "%s/upload_media/tts/%s" % (settings.FILE_WEB_URLROOT, url)
    return "%s/upload_media/%s" % (settings.FILE_WEB_URLROOT, url)

def format_ziyuan_url(url):
    """
    文件url 添加前缀2天之内的用江西的前缀，否则河南的前缀
    zsn
    """
    return get_absurl(url)
    # if not url:
    #     return url
    # if url.startswith("http"):
    #     return url
    # date_ziyuan = re.findall(r'/(\d+)/(\d+)/(\d+)/', url)
    # today = date.today()
    # ziyuan_source = ''
    # if date_ziyuan and len(date_ziyuan[0]) == 3:
    #     date_ziyuan = map(int, [d for d in date_ziyuan[0]])
    #     ziyuan_date = date(date_ziyuan[0], date_ziyuan[1], date_ziyuan[2])
    #     ctime = (today - ziyuan_date).days
    #     if ctime <= 2:
    #         ziyuan_source = settings.FILE_TBKT_UPLOAD_URLROOT
    #     else:
    #         ziyuan_source = settings.FILE_WEB_URLROOT
    # else:
    #     ziyuan_source = settings.FILE_WEB_URLROOT
    # if url.endswith("mp3"):
    #     return "%s/upload_media/tts/%s" % (ziyuan_source, url)
    # return "%s/upload_media/%s" % (ziyuan_source, url)

def add_word_options(n, words):
    """打氣球 单词添加随机选项"""
    if not words:
        return
    rows = cache.yy_balloon_option.get('word')
    if not rows:
        sql = """SELECT t1.id,t1.word FROM `yy_word` AS t1 JOIN (
    SELECT ROUND(RAND() * (SELECT MAX(id) FROM `yy_word`)) AS id) AS t2
    WHERE t1.id >= t2.id ORDER BY t1.id ASC LIMIT 2000 """
        rows = db.ziyuan_slave.fetchall_dict(sql)
        cache.yy_balloon_option.set('word', rows)

    for word in words:
        options = []
        _op = random.sample(rows, n + 1)
        for w in _op:
            if w.id != word.id and len(options) < n:
                options.append(w.word)
        options.insert(0, word.word)
        word.options = json.dumps(options)


def get_aid_dict(qids):
    "返回多道大题的小问, {qid:[ask_id]...}"
    if not qids:
        return {}
    sql = """
    select question_id, id from yy_question_ask
    where question_id in (%s)
    order by id
    """ % (','.join(str(i) for i in qids))
    rows = db.ziyuan_slave.fetchall(sql)
    aid_dict = {}
    for qid, aid in rows:
        row = aid_dict.get(qid, [])
        row.append(aid)
        aid_dict[qid] = row
    return aid_dict


def get_test_question_number_sheet(test_id):
    """获取未完成test的question列表  和 答题卡详情{ask_id:{qid:1,answer:用户答案}},"""

    sql = """select id,test_id,question_id,ask_id,result,answer,option_id from yy_test_detail where test_id=%s """ % test_id
    details = db.tbkt_yingyu.fetchall_dict(sql)

    numbers = [Struct({'qid': d.question_id, 'aid': d.ask_id}) for d in details]
    qids = [n.qid for n in numbers]
    if not qids:
        return 0, 0

    """优化"""
    # sql = """select id from yy_question where id in (%s) ORDER BY type""" % ','.join(str(q) for q in qids)
    # questions = db.ziyuan_slave.fetchall(sql)
    # qa_dict = get_aid_dict([q[0] for q in questions])
    # que_list = []
    # for q in questions:
    #     que_list += qa_dict.get(list(q)[0])
    que_list = [d.ask_id for d in details]

    sheet = {}
    for d in details:
        sheet[d.ask_id] = d
    new_sheet = [sheet.get(d) for d in que_list if sheet.get(d)]

    new_list = []
    for sheet in new_sheet:
        new_list += [n for n in numbers if n.aid == sheet.ask_id]
    ask_no = 1
    for q in new_list:
        q.ask_no = ask_no
        ask_no += 1
    # new_list.sort(key=lambda x: x.qid)
    # new_sheet.sort(key=lambda x: x.question_id)
    return new_list, new_sheet


def test_submit(test_id, status, data):
    """"提交答案"""
    sql = """select count(id) from u_yy_test_detail where test_id =%s""" % test_id
    details_len = db.tbkt_web.fetchone(sql)[0]
    if len(data) == details_len:
        status = 1
    rows = [Struct(row) for row in data if row]
    for row in rows:
        row.question_id = int(row.question_id)
        row.ask_id = int(row.ask_id)
        row.option_id = int(row.option_id or 0)

    nowt = int(time.time())

    sql = """select  question_id from  u_yy_test_detail where test_id=%s""" % test_id
    question_ids = db.tbkt_web.fetchall(sql)
    question_ids = [q[0] for q in question_ids]
    questions = com_yy.get_task_questions_data(question_ids)
    q_dict = {q.id: q for q in questions}
    a_dict = {}

    for q in questions:
        for a in q.asks:
            a_dict[a.id] = a

    sql_args = []
    # 遍历:判断对错
    cache_args = []
    for row in rows:
        q = q_dict.get(row.question_id)
        a = a_dict.get(row.ask_id)
        if status != 1 and not row.answer:
            result = -1
        else:
            result = check_user_answer(q, a, row.answer, row.option_id)
        # arg = (result, row.answer, row.option_id, test_id, row.ask_id)

        db.tbkt_web.u_yy_test_detail.filter(test_id=test_id, ask_id=row.ask_id).update(
            result=result,
            answer=row.answer,
            option_id=row.option_id
        )

        c_arg = (result, row.answer, row.option_id, test_id, row.ask_id, row.question_id)
        # sql_args.append(arg)
        cache_args.append(c_arg)

    # sql = """
    # UPDATE u_yy_test_detail SET result=%s, answer=%s, option_id=%s
    # WHERE test_id=%s AND ask_id=%s
    # """
    # db.tbkt_web.execute_many(sql, sql_args)

    n = len(sql_args)
    nright = sum(1 for r in sql_args if r[0] == 1)
    score = int(100 * nright / n) if n > 0 else 0

    # 保存主记录
    sql = """update u_yy_test set score=%s, status=%s,test_time=%s where id =%s""" % (score, status, nowt, test_id)
    if int(status) == 1:
        fields = ["result", "answer", "option_id", "test_id", "ask_id", "question_id"]
        details = [Struct(zip(fields, row)) for row in cache_args]
        test = {"id": test_id, "status": status}
        cache_data = Struct()
        cache_data.details = details
        cache_data.test = test
        # cache.yy_test_result.set(test_id, cache_data)
    db.tbkt_web.execute(sql)

def test_submit_now(test_id, status, data):
    """提交答案"""
    sql = """select count(id) from u_yy_test_detail where test_id =%s""" % test_id
    details_len = db.tbkt_web.fetchone(sql)[0]
    if len(data) == details_len:
        status = 1
    rows = [Struct(row) for row in data if row]
    for row in rows:
        row.question_id = int(row.question_id)
        row.ask_id = int(row.ask_id)
        row.option_id = int(row.option_id or 0)
        row.result = int(row.result)

    cache_args = []
    for row in rows:
        c_arg = (row.result, row.answer, row.option_id, test_id, row.ask_id, row.question_id)
        cache_args.append(c_arg)

    sql = "update u_yy_test_detail set result=%s, answer=%s, option_id=%s where test_id=%s and ask_id=%s and question_id=%s"
    db.tbkt_web.execute_many(sql, cache_args)

    nowt = int(time.time())

    n = len(cache_args)
    nright = sum(1 for r in cache_args if r[0] == 1)
    score = int(100 * nright / n) if n > 0 else 0


    # 保存主记录
    sql = """update u_yy_test set score=%s, status=%s,test_time=%s where id =%s""" % (score, status, nowt, test_id)
    if int(status) == 1:
        fields = ["result", "answer", "option_id", "test_id", "ask_id", "question_id"]
        details = [Struct(zip(fields, row)) for row in cache_args]
        test = {"id": test_id, "status": status}
        cache_data = Struct()
        cache_data.details = details
        cache_data.test = test
        cache.yy_test_result.set(test_id, cache_data)
    db.tbkt_web.execute(sql)

def check_user_answer(question, ask, user_answer, user_option_id):
    """
    功能说明：            判断用户答案是否正确
    返回1/0
    填空题: 把所有的填的词用|连起来
    连词成句: 把排好的词的序号用|连起来
    连句成段: 把排好的句子的序号用|连起来
    连线题: 按把右侧从上到下 option_id-link_id用|连起来, 例如: 123-1|234-0|231-2|456-3
    其他：都按选择题处理
    """
    if question.type == 9:  # 填空
        user_words = user_answer.split('|')
        user_words = [w.strip() for w in user_words]
        user_words = [w for w in user_words if w]
        user_words = [re.sub(r'[^A-Za-z]', '', w) for w in user_words]  # 剔除非字母字符
        user_answer = '|'.join(user_words)
        words = [w.strip() for w in ask.answer]
        words = [w for w in words if w]
        words = [re.sub(r'[^A-Za-z]', '', w) for w in words]  # 剔除非字母字符
        answer = '|'.join(words)
    elif question.type == 10:  # 连词成句
        answer = '|'.join(str(i) for i in xrange(len(ask.answer)))
    elif question.type == 11:  # 连句成段
        answer = '|'.join(str(i) for i in xrange(len(ask.answer)))
    elif question.type == 2:  # 连线题
        user_options = {}
        if user_answer:
            rows = [r.split('-') for r in user_answer.split('|')]
            user_options = {int(r[0] or 0): int(r[1] or -1) for r in rows if len(r) > 1}

        options = [op for op in ask.options if op.link_id >= 0]
        for o in options:
            user_link_id = user_options.get(o.id)
            if user_link_id != o.link_id:
                return 0
        else:
            return 1
    elif question.type == 12:  # 书面表达
        if int(user_answer) == 1:
            return 1
        else:
            return 0
    else:
        for op in ask.options:
            if op.is_right and op.id == user_option_id:
                return 1
        else:
            return 0
    return int(answer.lower() == user_answer.lower())


def special_handle_question(question):
    #  改为json格式，文件url添加前缀
    question.subject = json.loads(question.subject)
    question.subject = Struct(question.subject)
    if question.subject.get("images"):
        _images = []
        for a in question.subject["images"]:
            _images.append(format_ziyuan_url(a))
        question.subject["images"] = _images

    question.video_url = format_ziyuan_url(question.video_url)
    question.video_image = format_ziyuan_url(question.video_image)

    # 完形填空: 把题干里的<span class="xxx">____</span>替换为<span>(题号)</span><em class="JS-space" ask_id="123"></em>
    if question.type == 7:
        question.i = 0
        question._no = question.ask_no or 1

        def repl_f(m):
            s = m.group()
            ask = question.asks[question.i] if question.i < len(question.asks) else None
            if ask:
                s = u'<span>(%s)</span>:<em>点击选择</em>' % question._no
                question.i += 1
                question._no += 1
            return s

        question.subject = Struct(question.subject)
        question.subject.content = re.sub(r'<span.*?</span>', repl_f, question.subject.content)
        question.subject.title = u"完形填空"
        if question.subject.content.startswith(u"完形填空"):
            question.subject.content = question.subject.content.replace(u'完形填空。', '')


def get_user_book(user_id):
    user_book = com_yy.get_user_book(user_id, subject_id=91)
    if user_book:
        user_book.original_name = user_book.name
        if user_book.name.startswith(u'小学英语'):
            user_book.name = user_book.name[4:]
        user_book.name = user_book.name + "(" + user_book.press_name + ")"
        return user_book
    return
