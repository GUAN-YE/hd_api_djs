# coding: utf-8
import random
import re
from collections import defaultdict, Counter

import logging

from libs.utils import db, get_absurl, Struct, join, num_to_ch


# 语文试题说明
# category 1 一题一问 2 一题多问
# type 1.选择题 2.填空题 3.判断 4.连线题  5.连词成句 6.断句 7.解答题 8.解答题
# status 1.启用 0.禁用 -1.删除


def get_question(question_ids):
    # todo 加入缓存(需要保证数据正确)
    return _get_question(question_ids)


def get_article(article):
    re_str = re.match(r'.*<p align="center"><span>(.+?)<span></span></span></p>.+', article, re.S)
    if re_str:
        return re_str.group(1)
    return ""


def format_content(content):
    """
    替换参数中 p br span 标签
    :param content: 
    :return: 
    """
    if content in ("<p><br></p>", "<p><br/></p>"):
        # 资源后台 富文本编辑框 如果为空 默认会追加<p><br></p>
        return ""
    content = content.replace("<p>", "").replace("</p>", "").replace("</span>", "") \
        .replace('<br>', "").replace("<span>", "").replace(" ", "").replace("imgsrc", "img src")
    return content


def format_parse(parse):
    """
    格式化 解析
    :param parse: 
    :return: 
    """
    if parse in ("<p><br></p>", "<p><br/></p>"):
        return ""
    return format_content(parse)


def format_question_title(question_title):
    """
    格式化 小题标题
    :param question_title: 
    :return: 
    """
    if question_title in ("<p><br></p>", "<p><br/></p>"):
        return ""
    if not question_title or question_title in ("null", ):
        return ""
    return format_content(question_title)


def _get_question(question_ids):
    """
    get question
    :param question_ids: 
    :return: 
    """
    if not isinstance(question_ids, (list, tuple)):
        return []
    questions = db.tbkt_yw.yw_question.select(
        "content", "video", "image", "type", "show_parse", "category", "id", "article_text").filter(
        id__in=question_ids)[:]
    if not questions:
        return []
    out = []
    ask_map = get_ask(question_ids)
    for k, i in enumerate(questions):
        d = Struct()
        d.article_title = ""
        d.article_text = ""
        d.content = ""
        if i.type == 8:
            # 阅读理解
            d.article_title = format_content(i.content)
            d.article_text = i.article_text
        else:
            # 不是阅读理解
            d.content = i.content
        d.video = get_absurl(i.video).replace("//", "/")
        d.image = get_absurl(i.image).replace("//", "/")
        d.type = i.type
        d.category = i.category
        d.no = num_to_ch(k + 1)
        d.num = k + 1
        d.asks = ask_map.get(i.id, [])
        d.id = i.id
        out.append(d)
    return out


def get_ask(question_ids):
    """
    Under the big question ask info 
    :param question_ids
    :return: {}
    """
    if not isinstance(question_ids, (list, tuple)):
        return {}
    sql = """
    select a.id, a.question_id, a.content, a.video, a.image, a.parse,
    if(a.type, a.type, q.type) type, a.question_title, q.category,
    q.show_parse from yw_question q, yw_question_ask a 
    where q.id = a.question_id and q.id in (%s) order by a.question_number
    """ % (join(question_ids))
    asks = db.tbkt_yw.fetchall_dict(sql)
    if not asks:
        return {}

    ask_id = [i.id for i in asks]
    options = db.tbkt_yw.yw_question_options.filter(question_id__in=ask_id)[:]
    options_map = defaultdict(list)
    for i in options:
        options_map[i.question_id].append(i)
    out = defaultdict(list)
    for i in asks:
        i.image = get_absurl(i.image).replace("//", "/")
        i.video = get_absurl(i.video).replace("//", "/")
        i.content = i.content if i.content not in ("<p><br></p>", "<p><br/></p>") else ""
        i.question_title = format_question_title(i.question_title)
        i.parse = format_parse(i.parse)
        if not i.show_parse:
            i.parse = ""
        del i.show_parse
        del i.sequence
        del i.question_number
        out[i.question_id].append(i)

    for qid, asks in out.iteritems():
        ask_len = len(asks)
        for i, a in enumerate(asks):
            a.no = "(%s)" % (i + 1) if ask_len > 1 else ""
            op = options_map.get(a.id)
            get_options(a, op)
            del a.category
    return out


def get_options(ask, options):
    """
    Formatting ask or questions
    :param ask: {ask_id: type} 
    :param options: 小题选项
    :return: 
    """
    ask.options = []  # 选项
    ask.choice_answer = []  # 选择题正确答案
    ask.right_answer = []   # 其他类型正确答案
    ask.refer = ""          # 解答题正确答案
    ask.point = ""          # 断句题文字展示
    func_map = {
        1: choice,
        2: completion,
        3: judge,
        4: matching,
        5: connect_sentence,
        6: breakpoint,
        7: explain
    }
    func = func_map.get(ask.type)
    if not func:
        return
    func(ask, options)


def base_option(options):
    """
    选项基础数据
    :param options:
    :return: 
    """
    if not options:
        return []
    option = []
    for i in options:
        d = Struct()
        d.id = i.id
        d.content = i.content
        d.image = get_absurl(i.image)
        d.is_right = i.is_right
        d.option = i.option
        d.ask_id = i.question_id
        d.link_id = i.link_id
        option.append(d)
    return option


def choice(ask, options):
    """
    选择题
    :param options: 
    :param ask: 
    :return: 
    """
    option = base_option(options)
    ask.choice_answer = []
    for i in option:
        if not i.is_right:
            continue
        ask.choice_answer.append(i)
    ask.options = option


def completion(ask, options):
    """
    格式化填空题
    :param options:
    :param ask: 
    :return: 
    """
    answer = re.findall(r'<span style="color:[\s]*red[;]*">(.*?)</span>', ask.content)
    content = re.sub(r'<span style="color:[\s]*red[;]*">(.*?)</span>', u'<input placeholder="点击填写">', ask.content)
    ask.content = content
    temp = []
    for i in answer:
        if u'\u0261' in i:
            i = i.replace(u'\u0261', u'g')
        temp.append(i)
    ask.right_answer = temp


def matching(ask, options):
    """
    格式化连线题
    :param options:
    :param ask:
    :return: 
    """
    option = base_option(options)
    left_option = []
    right_option = dict()
    answer = []
    for i, k in enumerate(option):
        if k.link_id == "-2":
            continue

        if k.link_id == "-1":
            left_option.append(k.id)
        else:
            right = map(int, k.link_id.split(","))
            for r in right:
                right_option[r] = k.id
    for i, r in right_option.iteritems():
        if i >= len(left_option):
            continue
        answer.append(str(left_option[i]) + "-" + str(r))
    ask.options = option
    ask.right_answer = ["|".join(answer)]


def connect_sentence(ask, options):
    """
    连词成句
    :param options: 
    :param ask:
    :return: 
    """
    words = format_content(ask.content).split("|")
    ask.right_answer = words[:]
    random.shuffle(words)
    ask.words = words
    ask.content = ""


def breakpoint(ask, options):
    """
    断句
    :param options: 
    :param ask:
    :return: 
    """
    ask.point = ask.content.replace(" ", "")
    content = ask.content.replace("<p>", "@").replace("</p>", "#").replace(" ", "")
    temp = ""
    for i in content.replace("|", ""):
        temp += (u'%s<span class="point"></span>' % i) if i not in ("@", "#") else i
    right_answer = []
    answer = content.replace("@", "").replace("#", "").split("|")
    for i, k in enumerate(answer):
        num = len("".join(answer[:i + 1]))
        if i + 1 >= len(answer):
            continue
        right_answer.append(num)
    ask.content = temp.replace("@", "<p>").replace("#", "</p>")
    ask.right_answer = right_answer


def explain(ask, options):
    """
    解答题
    :param options:
    :param ask:     
    :return: 
    """
    ask.refer = options[0].content


def judge(options, ask):
    """
    判断题
    :param options: 
    :param ask:
    :return: 
    """
    pass
