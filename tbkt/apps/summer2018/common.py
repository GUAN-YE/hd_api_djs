# coding=utf-8
import json

from django.conf import settings

from libs.utils import db, Struct, num_to_ch, format_url


def get_question_by_type(object_id, paper_id, scan_type):
    """
    根据试卷题目类型 返回题目信息
    :param scan_type: 扫描类型 1:整张试卷 2:题目类型 3：题目ID
    :param object_id: 1：paper_id, 2:paper_type_id（试卷类型ID）, 3:question_id（题目ID）
    :param paper_id: 试卷ID
    :return:
    """
    sql = """
    select a.id ask_id, a.question_id, d.paper_type_id from
    sx2_paper_question_number n inner join sx2_paper_detail d on n.paper_id = %s
    and n.paper_id = d.paper_id and n.type = 2 and n.object_id = d.question_id
    inner join sx2_question_ask a on a.question_id = d.question_id
    """ % paper_id
    rows = db.ziyuan_slave.fetchall_dict(sql)

    if not rows:
        return

    # 试卷题目类型去重
    paper_type = db.ziyuan_slave.sx2_paper_question_number.select("object_id").filter(paper_id=paper_id,
                                                                                      type=1).flat("object_id")[:]
    if scan_type == 2:
        # 按试卷题目类型查询
        ask_ids = [i for i in rows if i.paper_type_id == object_id]
    elif scan_type == 3:
        # 按照题目ID查询
        ask_ids = [i for i in rows if i.question_id == object_id]
    else:
        ask_ids = [i for i in rows]
    print ask_ids
    # 获取举一反三试题详情
    out = Struct()
    out.title = get_paper_title(paper_id)
    out.paper_id = paper_id
    out.list = []

    paper_number = get_paper_number(paper_id)

    n = 0  # 初始化小题号
    for k, p in enumerate(paper_type):
        ask_info = Struct()
        ask_info.q_num = num_to_ch(k + 1)
        ask_info.paper_type_id = p
        asks = []
        for a in ask_ids:
            if a.paper_type_id == p:
                n += 1
                info = Struct()
                # 题号 (1)
                info.num = paper_number.get(a.ask_id, Struct()).a_num or ""
                # 题目ID
                info.aid = a.ask_id
                asks.append(info)
            else:
                # 重新赋值 避免返回整张试卷问题
                n = 0
        ask_info.asks = asks
        out.list.append(ask_info)
    out.list = [i for i in out.list if i.asks]
    return out


def get_paper_title(paper_id):
    """
    返回试卷标题
    :param paper_id: 试卷ID
    :return:
    """
    sql = """
    select if(p.name!='',p.name,(select c.name from sx2_work_book_catalog c
    where c.id = p.work_book_catalog_id)) name from sx2_paper p
    where p.id = %s
    """ % paper_id
    r = db.ziyuan_slave.fetchone_dict(sql)
    return r.name if r else ''


def get_ask_explain(ask_id, paper_id):
    """
    :param ask_id: 
    :param paper_id: 
    :return: 
    """
    sql = """
    select a.subject a_subject, a.content a_content, a.image_url a_image_url, 
    q.subject q_subject, q.content q_content, q.image_url q_image_url
    from sx2_question_ask a, sx2_question q
    where a.id = %s and a.question_id = q.id
    """ % ask_id
    row = db.ziyuan_slave.fetchone_dict(sql)
    if not row:
        return []
    paper_number = get_paper_number(paper_id)
    out = Struct()
    num = paper_number.get(ask_id) if paper_number else ""
    out.q_num = num.q_num if num else ''
    out.a_num = num.a_num if num else ''
    out.big_subject = parse_subject(row.q_subject) if row.q_subject else parse_new_subject(row.q_content, row.q_image)
    out.small_subject = parse_subject(row.a_subject) if row.a_subject else parse_new_subject(row.a_content, row.a_image)
    out.ask_id = ask_id
    return out


def parse_subject(subject):
    """
    解析题干
    :returns: {'content':内容, 'image':{'url':图片地址, 'align':''}}
    """
    if not subject:
        return {"content": "", "image": ""}
    obj = json.loads(subject)
    obj["content"] = replace_symbol(obj["content"])
    images = obj.get("images", [])
    if images:
        image = images[0]
        image = format_url(image['url'])
    else:
        image = ""
    obj["image"] = image
    return obj


def parse_new_subject(content, image):
    if not content and not image:
        return {"content": "", "image": ""}
    _image = format_url(image)
    content = replace_symbol(content)
    return {"content": content, "image": _image}


def replace_symbol(content=""):
    """
    替换特殊符号
    """
    content = u"%s" % content
    replace_content = content.replace('#y#',
                                      '<img src="%s/upload_media/math_img/round.png" /><span class="round"></span>' % settings.FILE_VIEW2_URLROOT) \
        .replace('#s#',
                 '<img src="%s/upload_media/math_img/delta.png" /><span class="delta"></span>' % settings.FILE_VIEW2_URLROOT) \
        .replace('#p#',
                 '<img src="%s/upload_media/math_img/rhomb.png" /><span class="rhomb"></span>' % settings.FILE_VIEW2_URLROOT) \
        .replace('#px#',
                 '<img src="%s/upload_media/math_img/rhomb_lit.png" /><span class="rhomb_lit"></span>' % settings.FILE_VIEW2_URLROOT) \
        .replace('#f#', '<img src="%s/upload_media/math_img/tupian.png" />' % settings.FILE_VIEW2_URLROOT) \
        .replace('#word#', '<input class="underline_input" type="text">') \
        .replace('#df#', '<img src="%s/upload_media/math_img/squares_big.png" />' % settings.FILE_VIEW2_URLROOT) \
        .replace('#ds#',
                 '<img src="%s/upload_media/math_img/delta_big.png" /><span class="delta"></span>' % settings.FILE_VIEW2_URLROOT) \
        .replace('#dy#',
                 '<img src="%s/upload_media/math_img/round_big.png" /><span class="round"></span>' % settings.FILE_VIEW2_URLROOT) \
        .replace(u'\\therefore', u'∴') \
        .replace(u'\\because', u'∵')
    return replace_content


def get_paper_number(paper_id):
    """
    根据试卷ID返回 题目标题
    :param paper_id: 试卷ID
    :return: {ask_id:{'q_num': 大题号, 'a_num': 小题号}}
    """
    paper_type = db.ziyuan_slave.sx2_paper_question_number.select("object_id").filter(paper_id=paper_id,
                                                                                      type=1).flat("object_id")[:]

    sql = """
    select a.id ask_id, a.question_id, d.paper_type_id from
    sx2_paper_question_number n inner join sx2_paper_detail d on n.paper_id = %s
    and n.paper_id = d.paper_id and n.type = 2 and n.object_id = d.question_id
    inner join sx2_question_ask a on a.question_id = d.question_id
    """ % paper_id
    papers = db.ziyuan_slave.fetchall_dict(sql)

    if not papers:
        return {}

    out = {}
    n = 0  # 初始化小题号
    for k, p in enumerate(paper_type):
        q_num = num_to_ch(k + 1)
        for a in papers:
            if a.paper_type_id == p:
                r = len([i for i in papers if i.paper_type_id == p])
                n += 1
                # 题号 (1)
                a_num = u"(%s)" % n # if r > 1 else ''
                out[int(a.ask_id)] = Struct(q_num=q_num, a_num=a_num)
                # 题目ID
            else:
                # 重新赋值 避免返回整张试卷问题
                n = 0
    return out
