#coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: com_yy.py
@time: 2017/12/21 9:11
"""

import re
import random
import json
import time
from collections import OrderedDict

from com.com_cache import cache
from libs.utils.common import Struct, get_absurl, get_videourl
from libs.utils import db

def get_aid_dict(qids):
    """
    返回多道大题的小问, {qid:[ask_id]...}
    """
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

def get_active_paper_question_number_sheet(user_id, active_id, paper_id):
    details = db.tbkt_active_slave.active_paper_detail.select('text')\
        .filter(user_id=user_id, active_id=active_id, paper_id=paper_id).last()
    if not details:
        return [], []

    numbers = []
    ask_no = 1
    text = details.text
    text = json.loads(text)
    text = [Struct(t) for t in text]
    text.sort(lambda x, y: cmp(x['qid'], y['qid']))
    for d in text:
        number = Struct()
        number.ask_no = ask_no
        number.qid = d.qid
        number.aid = d.aid
        numbers.append(number)
        ask_no += 1
    qids = [q.qid for q in numbers]
    if not qids:
        return [], []
    ask_list = [d.aid for d in text]

    sheet = {}
    for d in text:
        detail = {}
        detail['question_id'] = d.qid
        detail['ask_id'] = d.aid
        detail['option_id'] = d.oid
        detail['answer'] = d.answer
        detail['result'] = d.result
        sheet[d.aid] = detail
    sheets = [sheet[d] for d in ask_list if sheet.get(d)]
    return numbers, sheets

def get_question_data(qid, ask_no=1):
    """
    功能说明：                问题详情
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-12-21
    """
    question = db.ziyuan_slave.yy_question.select('id', 'subject', 'classify', 'type', 'video_url', 'video_image').get(id=qid)
    if not question:
        return []
    question.ask = get_question_ask(question)

    #  补充一些特殊题型的格式
    special_handle_question(question)
    question.ask_no = ask_no
    for ask in question['ask']:
        ask['no'] = ask_no
        ask_no += 1
    return question

def get_questions_data(qid_list):
    """返回多道习题的数据"""
    if not qid_list:
        return
    questions = db.ziyuan_slave.yy_question.filter(id__in=qid_list) \
        .select('id', 'subject', 'classify', 'type', 'video_url', 'video_image')
    questions = [Struct(q) for q in questions if q]
    if not questions:
        return
    qid_list = [q.id for q in questions]
    asks = db.ziyuan_slave.yy_question_ask.filter(question_id__in=qid_list) \
        .select('id', 'subject', 'parse', 'video_url', 'video_image', 'listen_audio', 'listen_text', 'question_id',
                'duration')
    asks = [Struct(a) for a in asks if a]
    ask_ids = [a.id for a in asks]
    options = db.ziyuan_slave.yy_ask_options.filter(ask_id__in=ask_ids) \
        .select('id', 'ask_id', 'content', 'image', '`option`', 'is_right', 'link_id')
    options = [Struct(o) for o in options if o]
    for o in options:
        o.image = get_absurl(o.image)

    for ask in asks:
        ask.subject = json.loads(ask.subject)
        ask.parse = json.loads(ask.parse)
        ask.video_url = get_videourl(ask.video_url)
        ask.video_image = get_absurl(ask.video_image)
        ask.listen_audio = get_absurl(ask.listen_audio)

        ask.options = [o for o in options if o.ask_id == ask.id]
        right_options = [o for o in ask.options if o.is_right]
        ask.right_option = right_options[0] if right_options else None
        ask.subject = Struct(ask.subject)
        _ask_images = []
        if ask.subject["images"]:
            for img in ask.subject["images"]:
                _ask_images.append(get_absurl(img))
            ask.subject["images"] = _ask_images

        if ask.right_option and ask.right_option.get("image"):
            ask.right_option["image"] = get_absurl(ask.right_option["image"])
        _options = []
        for _option in ask.options:
            if _option.get("image"):
                _option["image"] = get_absurl(_option["image"])
            _options.append(_option)
        ask.options = _options

    asks_dict = OrderedDict()
    for a in asks:
        asks_dict[a.question_id] = asks_dict.get(a.question_id, []) + [a]

    for question in questions:
        question.asks = asks_dict.get(question.id)
        for ask in question.asks:
            #  补充一些特殊题型的格式
            if question.type == 9:  # 填空题: 把<span></span>里的东西挖出来, 用____替换
                words = re.findall(r'<span .*?>(.*?)</span>', ask.subject.content)
                ask.answer = words
                ask.subject.content = re.sub(r'<span .*?>(.*?)</span>', '<input>', ask.subject.content)
            elif question.type == 10:  # 连词成句: 打乱分词顺序
                words = re.split(r'<.*?>', ask.subject.content)
                words = [w.strip() for w in words]
                words = [w for w in words if w]
                answer = words[:]
                random.shuffle(words)

                ask.subject.content = ",".join(w for w in words)
                ask.words = words
                ask.answer = answer
            elif question.type == 11:  # 连句成段: 打乱句子顺序
                sentences = re.split(r'<.*?>', ask.subject.content)
                sentences = [s.strip() for s in sentences]
                sentences = [s for s in sentences if s]
                _sentences = []
                for s in sentences:
                    if s and s.startswith("("):
                        s = re.sub(r"\(.*?\)", "", s)
                    _sentences.append(s)
                sentences = _sentences
                answer = sentences[:]
                random.shuffle(sentences)
                ask.sentences = sentences
                ask.subject.content = ",".join(s for s in sentences)
                ask.answer = answer
                ask.answer_orders = {i: s for i, s in enumerate(answer)}
            else:  # 其他当成选择题
                ask.answer = ''
                for op in ask.options:
                    if op.is_right:
                        ask.answer = op.option
                        break

            if question.type == 4:  # 判断正误题选项内容: A正确 B错误
                for op in ask.options:
                    if op.option == u'A':
                        op.content = u'正确'
                    elif op.option == u'B':
                        op.content = u'错误'

        # 补充一些特殊题型的格式
        special_handle_question(question)
    return questions

def get_question_ask(question):
    """
    功能说明：                获取问题的小问
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-12-21
    """
    asks = db.ziyuan_slave.yy_question_ask.\
        select('id', 'subject', 'parse', 'video_url', 'video_image', 'listen_audio', 'listen_text', 'duration').\
        filter(question_id=question.id)[:]
    ask_ids = [a.id for a in asks]

    options = db.ziyuan_slave.yy_ask_options.\
        select('id', 'ask_id', 'content', 'image', '`option`', 'is_right', 'link_id').\
        filter(ask_id__in=ask_ids).order_by('id')[:]

    for o in options:
        o.image = get_absurl(o.image)

    for ask in asks:
        ask.subject = json.loads(ask.subject)
        ask.parse = json.loads(ask.parse)
        ask.video_url = get_videourl(ask.video_url)
        ask.video_image = get_absurl(ask.video_image)
        ask.listen_audio = get_absurl(ask.listen_audio)
        ask.options = [o for o in options if o.ask_id == ask.id]
        right_options = [o for o in ask.options if o.is_right]
        ask.right_option = right_options[0] if right_options else None
        ask.subject = Struct(ask.subject)
        _ask_images = []
        if ask.subject["images"]:
            for img in ask.subject["images"]:
                _ask_images.append(get_absurl(img))
            ask.subject["images"] = _ask_images
        if ask.right_option and ask.right_option.get("image"):
            ask.right_option["image"] = get_absurl(ask.right_option["image"])
        _options = []
        for _option in ask.options:
            if _option.get("image"):
                _option["image"] = get_absurl(_option["image"])
            _options.append(_option)
        ask.options = _options

        #  补充一些特殊题型的格式
        if question.type == 9:  # 填空题: 把<span></span>里的东西挖出来, 用____替换
            words = re.findall(r'<span .*?>(.*?)</span>', ask.subject.content)
            ask.answer = words
            ask.subject.content = re.sub(r'<span .*?>(.*?)</span>', u'<input placeholder="点击填写">', ask.subject.content)
        elif question.type == 10:  # 连词成句: 打乱分词顺序
            words = re.split(r'<.*?>', ask.subject.content)
            words = [w.strip() for w in words]
            words = [w for w in words if w]
            answer = words[:]
            random.shuffle(words)

            ask.subject.content = ",".join(w for w in words)
            ask.words = words
            ask.answer = answer
            ask.answer_orders = {w: i for i, w in enumerate(answer)}

        elif question.type == 11:  # 连句成段: 打乱句子顺序
            sentences = re.split(r'<.*?>', ask.subject.content)
            sentences = [s.strip() for s in sentences]
            sentences = [s for s in sentences if s]
            _sentences = []
            for s in sentences:
                if s and s.startswith("("):
                    s = re.sub(r"\(.*?\)", "", s)
                _sentences.append(s)
            sentences = _sentences
            answer = sentences[:]
            random.shuffle(sentences)
            ask.sentences = sentences
            ask.subject.content = ",".join(s for s in sentences)
            ask.answer = answer
            ask.answer_orders = {i: s for i, s in enumerate(answer)}
        elif question.type == 2:  # 连线题
            options = [op for op in ask.options if op.link_id >= 0]
            answer = []
            for obj in options:
                a = str(obj['id']) + '-' + str(obj['link_id'])
                answer.append(a)
            answer = '|'.join(answer)
            ask.answer = answer
        else:  # 其他当成选择题
            ask.answer = ''
            for op in ask.options:
                if op.is_right:
                    ask.answer = op.option
                    break

        if question.type == 4:  # 判断正误题选项内容: A正确 B错误
            for op in ask.options:
                if op.option == u'A':
                    op.content = u'正确'
                elif op.option == u'B':
                    op.content = u'错误'


    return asks

def special_handle_question(question):
    #  改为json格式，文件url添加前缀
    question.subject = json.loads(question.subject)
    question.subject = Struct(question.subject)
    if question.subject.get("images"):
        _images = []
        for a in question.subject["images"]:
            _images.append(get_absurl(a))
        question.subject["images"] = _images

    question.video_url = get_videourl(question.video_url)
    question.video_image = get_absurl(question.video_image)

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

def paper_submit(user_id, active_id, paper_id, status, data):
    """ 提交试卷做题记录 """
    nowt = int(time.time())
    rows = [Struct(row) for row in data if row]
    for row in rows:
        row.question_id = int(row.question_id)
        row.ask_id = int(row.ask_id)
        row.option_id = int(row.option_id or 0)
        row.result = int(row.result) if row.result else 0
    rows = {(r.question_id, r.ask_id): r for r in rows}

    cache_args = []

    text_ed = db.tbkt_active_slave.active_paper_detail.select('text').get(user_id=user_id, active_id=active_id,
                                                                          paper_id=paper_id)
    text_ed = [Struct(t) for t in json.loads(text_ed.text)]  # 全部问题
    text = []
    for row in text_ed:
        tmp = rows.get((row.qid, row.aid)) or ''
        if tmp:
            row.oid = tmp.option_id
            row.result = tmp.result
            row.answer = tmp.answer
        text.append(row)
        c_arg = (int(row.result), row.answer, int(row.oid), int(row.aid), int(row.qid))
        cache_args.append(c_arg)

    with db.tbkt_active as ac:
        ac.active_paper_detail.filter(user_id=user_id, active_id=active_id, paper_id=paper_id).update(
            text=json.dumps(text),
            add_time=nowt
        )
        n = len(cache_args)
        nright = sum(1 for r in cache_args if r[0] == 1)
        score = int(100 * nright / n) if n > 0 else 0
        ac.active_paper.filter(user_id=user_id, active_id=active_id, paper_id=paper_id).update(
            score=score,
            status=status,
            test_time=nowt
        )

    if int(status) == 1:
        fields = ["result", "answer", "oid", "aid", "qid"]
        details = [Struct(zip(fields, row)) for row in cache_args]
        cache_data = Struct()
        cache_data.details = details
        cache.hd_paper_result.set((user_id, active_id, paper_id), cache_data)

def get_paper_result(user_id, active_id, paper_id):
    """试卷结果"""
    details = get_paper_detail(user_id, active_id, paper_id)
    for d in details:
        d.result = int(d.get('result', 0))

    number = len(details)
    wrong_number = sum(1 for d in details if d.result != 1)

    data = {
        'number': number,
        'wrong_number': wrong_number,
    }
    return data

def get_paper_result_detail(user_id, active_id, paper_id, type_id):
    """试卷结果详细，1 全部， 2 错误 """
    details = get_paper_detail(user_id, active_id, paper_id)
    questions, sheet = get_paper_question_detail(details)
    questions = get_special_user_answer(questions)
    questions.sort(lambda x, y: cmp(x['id'], y['id']))
    ask_no = 1
    for q in questions:
        for a in q.asks:
            a.no = ask_no
            ask_no += 1
    _question = []
    if type_id == 2:
        for q in questions:
            if len(q.asks) > 1:
                n = 0
                asks = []
                for a in q.asks:
                    if not a.user_result:
                        n += 1
                    if int(a.user_result) == 1:
                        continue
                    asks.append(a)
                q.asks = asks
                if n:
                    _question.append(q)
            else:
                if not q.asks[0].user_result:
                    _question.append(q)
    else:
        _question = questions
    _numbers = [Struct({'qid': d.qid, 'aid': d.aid, "result": sheet.get(d.aid).result}) for d in details]
    numbers = []
    new_sheet = []
    _question.sort(lambda x, y: cmp(x['id'], y['id']))  # zsn排序
    for q in _question:
        for a in q.asks:
            numbers += [n for n in _numbers if n.aid == a.id]
            sheet.get(a.id)
            if sheet.get(a.id):
                sheet.get(a.id).no = a.no
                new_sheet += [sheet.get(a.id)]
    data = {
        "question": _question,
        "sheet": new_sheet,
        "numbers": numbers,
    }
    return data

def get_paper_detail(user_id, active_id, paper_id):
    """获取试卷结果qid,aid,oid,result,answer"""
    cache_data = cache.hd_paper_result.get((user_id, active_id, paper_id))
    if cache_data:
        details = [Struct(d) for d in cache_data["details"]]
    else:
        details = db.tbkt_active_slave.active_paper_detail.select('text').filter(user_id=user_id, active_id=active_id,
                                                                                 paper_id=paper_id).last()
        details = json.loads(details.text)
        details = [Struct(t) for t in details]
    return details

def get_paper_question_detail(details):
    """获取试卷问题详情，和答题卡"""
    qid_list = [d.qid for d in details if d]
    questions = get_questions_data(qid_list)
    detail_dict = {d.aid: d for d in details}
    ask_no = 1
    for q in questions:
        for a in q.asks:
            a.no = ask_no
            ask_no += 1

            # 结果页不显示"点击选择"
        if q.type == 7:
            q.subject.content = q.subject.content.replace(u'点击选择', u'')
        for a in q.asks:
            d = detail_dict.get(a.id)
            a.user_result = d.result if d else -1
            a.user_answer = d.answer if d else ''

            if q.type == 9:  # 填空题
                user_answer = a.user_answer.split('|')
                user_answer = [s for s in user_answer if s]
                a.user_answer = user_answer
            elif q.type in (10, 11):  # 连词连句
                indexs = a.user_answer.split('|')
                user_answer = []
                for n, i in enumerate(indexs):
                    if i.isdigit():
                        i = int(i)
                        ans = a.answer[i]
                        if i != n:
                            ans = "<em style='color:red'>%s</em>" % ans
                        else:
                            ans = "<em>%s</em>" % ans
                        user_answer.append(ans)
                a.user_answer = user_answer

            a.user_option_id = d.option_id if d else 0
            user_options = [o for o in a.options if o.id == a.user_option_id]
            a.user_option = user_options[0] if user_options else None

            if q.type == 7:  # 完形
                # 避免重复格式化浪费时间
                if not q.answer:
                    q.answer = [a.right_option.option + ':' + a.right_option.content for a in q.asks if a]
                    q.user_answer = [a.user_answer or '' for a in q.asks]

    ask_dict = {}
    for q in questions:
        for a in q.asks:
            a.qtype = q.type
            ask_dict[a.id] = a
    sheet = Struct()
    for d in details:
        d.right_answer = ''
        # 补充连线题原题答案
        ask = ask_dict.get(d.aid)
        if ask:
            d.right_answer = ask.answer
        if ask and ask.qtype == 2:
            rows = ['%s-%s' % (o.id, o.link_id) for o in ask.options if o.link_id >= 0]
            d.right_answer = '|'.join(rows)

        sheet[d.aid] = d
    return questions, sheet

def get_special_user_answer(questions):
    """给问题补充上用户答案"""
    def repl_9(m):
        s = m.group()
        ask = a.answer[a.i] if a.i < len(a.answer) else None
        user_answer = a.user_answer[a.i] if a.i < len(a.user_answer) else None
        if not user_answer:
            return
        user_words = user_answer
        user_words = [re.sub(r'[^A-Za-z]', '', user_words)]  # 剔除非字母字符
        user_words = '|'.join(u for u in user_words)

        answer = [re.sub(r'[^A-Za-z]', '', ask)]  # 剔除非字母字符
        answer = '|'.join(a for a in answer)
        result = int(answer.lower() == user_words.lower())
        style = 'green' if result else 'red'

        if ask and user_answer:
            s = u'<u style="color:%s">%s</u>' % (style, user_answer)
        return s

    def repl_f(m):
        s = m.group()
        ask = question.asks[question.i] if question.i < len(question.asks) else None
        if ask:
            if question.asks[question.i].user_option:
                style = 'green' if int(question.asks[question.i].user_result) != 0 else 'red'
                s = u'<span >%s</span>:<em style="color:%s">  %s   %s </em>' % (
                    question.asks[question.i].no, style,
                    question.asks[question.i].user_option.option,
                    question.asks[question.i].user_option.content)  # 结果页不让显示点击选择
                question.i += 1
                question._no += 1
        return s

    for question in questions:
        question.i = 0

        if question.type == 9:
            for a in question.asks:
                a.i = 0
                a.subject.content = re.sub(r"<input>", repl_9,
                                           a.subject.content)  # '<u style="color:green">'+a.answer[0]+'</u>'

        # 完形填空补充用户答案
        if question.type == 7:
            question.i = 0
            question._no = question.ask_no or 1
            question.subject.content = re.sub(r'<span.*?</span>:<em>.*?</em>', repl_f, question.subject.content)
    return questions