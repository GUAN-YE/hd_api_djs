# coding=utf-8
"""
提取公共部分 便于加缓存
"""

import re
import math
import time
from django.conf import settings
from libs.utils import db, get_absurl
from collections import OrderedDict, defaultdict
from libs.utils.common import Struct
import random
import simplejson as json
from com.com_cache import cache
from datetime import datetime, date


def score_to_en(score):
    """
    功能说明：对应的分数转换为相应的积分 A：100-80，B：80-70，C：70-60，D：60以下
    """
    if not score:
        return "D"
    score = int(score)
    if score >= 80:
        return 'A'
    elif 70 <= score < 80:
        return 'B'
    elif 60 <= score < 70:
        return 'C'
    else:
        return 'D'


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

def pick_int(name):
    "从字符串中提取第一个数字"
    m = re.search(r'(\d+)', name)
    if not m:
        return 1
    num = re.search(r'(\d+)', name).group()
    num = int(num)
    return num


def format_date(date, format="%Y-%m-%d %H:%M:%S"):
    """时间格式化, 支持整数时间戳
    ~ 用法：{{xxx|date('%Y-%m-%d %H:%M:%S')}}
    """
    if not date:
        return u''
    if isinstance(date, (int, long)):
        t = time.localtime(date)
        date = datetime(*t[:6])
    s = date.strftime(format.encode('utf-8'))
    return s.decode('utf-8')


################################  资源  ##################################

def get_catalogs(book_id):
    """
    教材大章目录
    """
    if not book_id:
        return
    # 读缓存
    catalogs = cache.yy_book_catalogs.get(book_id)
    if not catalogs:
        sql = """SELECT id, name,level,type,parent_id,is_node,path,is_main  FROM yy_catalog
    WHERE book_id = %s and `status` = 1 and `level` = 1 ORDER BY(sequence);""" % book_id
        catalogs = db.ziyuan_slave.fetchall_dict(sql)
        cache.yy_book_catalogs.set(book_id, catalogs)
    return catalogs


def get_all_chapter(book_id):
    """
    获取教材所有章节
    """
    if not book_id:
        return
    # 读缓存
    catalogs = cache.yy_book_chapter.get(book_id)
    if not catalogs:
        sql = """select id,name,level ,type,parent_id,is_node,path  from yy_catalog
    where book_id=%s and status=1 ORDER BY sequence""" % book_id
        catalogs = db.ziyuan_slave.fetchall_dict(sql)
        cache.yy_book_chapter.set(book_id, catalogs)
    return catalogs


def get_chapter_data(cid):
    if not cid:
        return
    # 读缓存
    chapter = cache.yy_chapter_data.get(cid)
    if not chapter:
        sql = """select id,name,level,book_id,is_main,type,sequence from yy_catalog where id=%s and  status=1""" % cid
        chapter = db.ziyuan_slave.fetchone_dict(sql)
        cache.yy_chapter_data.set(cid, chapter)
    return chapter


def get_chapter_words(cid, word_cid=0):
    """
    获取某章节单词数据,
    if  word_cid ==True   cid为目录章节type=4
    """
    if not word_cid:
        sql = """select id from yy_catalog where path like "|%s|%%%%" and is_node=1 and type=4 and  status=1""" % cid
        chapter = db.ziyuan_slave.fetchone_dict(sql)
        if not chapter:
            return []
        cid = chapter.id
    # 读缓存
    words = cache.yy_chapter_words.get(cid)
    if not words:
        sql = """select id, translation, male_audio,female_audio,image,example,example_translation,
    lesson,lesson_translation,phonetic,word,duration from yy_word where catalog_id = %s and tts=1 and status<>-1 ORDER BY sequence""" % cid
        words = db.ziyuan_slave.fetchall_dict(sql)
        for word in words:
            word.female_audio = format_ziyuan_url(word.female_audio)
            word.male_audio = format_ziyuan_url(word.male_audio)
            word.audio = word.female_audio or word.male_audio
            word.image = format_ziyuan_url(word.image)
            del word.female_audio
            del word.female_audio
        cache.yy_chapter_words.set(cid, words)
    return words


def get_reading_pages(book_id, pages):
    """
    功能说明：            获取课本点读页
    """
    reading = cache.yy_reading.get((book_id, pages))

    if reading:
        reading = Struct(reading)
        reading.details = [Struct(r) for r in reading.details]
    else:
        page_names = 'P%s' % pages
        sql = """select r.* from yy_reading r join yy_catalog c on c.id=r.catalog_id
    where c.book_id=%s and c.name = '%s' and c.status>=0 ORDER BY c.sequence""" % (
            book_id, page_names)
        reading = db.ziyuan_slave.fetchone_dict(sql)
        if not reading:
            return
        sql = """select id,reading_id,audio_text,translation,audio_url,area,duration  from yy_reading_detail where reading_id=%s""" % reading.id
        details = db.ziyuan_slave.fetchall_dict(sql)
        # 去除翻译中的换行
        for d in details:
            d.translation = d.translation.replace('\n', '')
        reading.details = details
        cache.yy_reading.set((book_id, pages), reading)
    return reading


def get_all_pageno(book_id):
    """
    功能说明：            返回教材下所有页码
    """
    sql = """SELECT DISTINCT c.`name` FROM yy_catalog c
join yy_reading r on r.catalog_id=c.id
join yy_reading_detail d on d.reading_id=r.id and d.tts>0
WHERE book_id = %s and type = 5 and `status` >= 0 ORDER BY(sequence);""" % book_id
    names = db.ziyuan_slave.fetchall_dict(sql)
    names = [n.name for n in names]
    pages = []
    for s in names:
        num = pick_int(s)
        pages.append(num)
    return pages


def get_capters_pageno(catalogs):
    """每個章节添加当前页码"""
    if not catalogs:
        return
    # 填充章节页码
    sql = """select DISTINCT c.parent_id,c.name from yy_catalog c
join yy_reading r on r.catalog_id=c.id
join yy_reading_detail d on d.reading_id=r.id and d.tts>0
where c.parent_id in (%s) and c.type=5 and c.status>=0 ORDER BY c.sequence""" % ",".join(
        str(c.id) for c in catalogs)
    rows = db.ziyuan_slave.fetchall_dict(sql)
    names_dict = defaultdict(list)
    for row in rows:
        names_dict[row.parent_id].append(row.name)
    for c in catalogs:
        names = names_dict.get(c.id, [])
        pages = []
        for s in names:
            num = pick_int(s)
            pages.append(num)
        c.pages = pages
    return catalogs


def get_user_book(user_id, subject_id):
    """
    获得用户教材
    """
    if (subject_id not in [91, 92]) or (not user_id):
        return
    # 读缓存
    book_id = cache.userbook.get((user_id, subject_id, 1))
    if not book_id:

        sql = "SELECT book_id FROM user_book WHERE user_id = %s AND subject_id = %s AND is_work_book = 0;" % (
            user_id, subject_id)
        ubook = db.slave.fetchone_dict(sql)
        if not ubook:
            return
        book_id = int(ubook.book_id)
        if not book_id:
            return
            # 存入缓存
            # cache.userbook.set((user_id, subject_id, 1), book_id)
    # 读缓存
    user_book = cache.book.get(book_id)
    if not user_book:
        sql = """
            select b.id, b.name, b.subject_id, b.grade_id, p.name press_name, v.name version_name, b.volume
            from zy_book b
            inner join zy_press p on p.id=b.press_id
            inner join zy_press_version v on v.id=b.version_id
            where b.id=%s
            """ % book_id
        user_book = db.ziyuan_slave.fetchone_dict(sql)
        # 存入缓存
        # cache.book.set(book_id, user_book)
    return user_book


def get_dialog(cid):
    '情景对话'
    if not cid:
        return
    data = cache.yy_chapter_dialog.get(cid)
    if data:
        data = Struct(data)
        data.roles = [Struct(r) for r in data.roles if r]
        sentences = []
        for r in data.sentences:
            r = Struct(r)
            r.role = Struct(r.role) if r.role else None
            sentences.append(r)
        data.sentences = sentences

    else:
        sql = """select id,title from yy_standard_pool where status<>-1 and catalog_id=%s and type in (1,3) and tts=1""" % cid
        lesson = db.ziyuan_slave.fetchone_dict(sql)
        if not lesson:
            return

        sql = """select id,pool_id,text,audio_text,translation,male_audio,female_audio,is_key,role_id,sequence,line,duration from yy_standard_pool_detail s
    where s.pool_id=%s and s.status<>-1 ORDER BY s.sequence """ % lesson.id
        sentences = db.ziyuan_slave.fetchall_dict(sql)

        role_dict = {}
        roles_list = [i.role_id for i in sentences if i.role_id]
        if roles_list:
            sql = """select r.id ,r.name_en,r.name_zh,r.code,r.image_id,r.sequence,i.portrait, i.gif_1, i.gif_2 from yy_role r
            LEFT JOIN yy_role_image i on i.id=r.image_id
            where r.id in (%s)""" % ','.join(str(i) for i in roles_list)
            rows = db.ziyuan_slave.fetchall_dict(sql)
            role_dict = {r.id: r for r in rows}

        for s in sentences:
            s.role = role_dict.get(s.role_id)

            path = s.female_audio or s.male_audio
            if path:
                s.audio = format_ziyuan_url(path)

        roles = OrderedDict()
        for s in sentences:
            if s.role and s.role.id not in roles:
                roles[s.role.id] = s.role
                if s.role.gif_1:
                    s.role.gif_1 = format_ziyuan_url(s.role.gif_1)
                if s.role.gif_2:
                    s.role.gif_2 = format_ziyuan_url(s.role.gif_2)
                s.role.portrait = format_ziyuan_url(s.role.portrait)

        rename_role(sentences)

        data = Struct()
        data.title = lesson.title
        data.roles = []
        for role in roles.values():
            row = Struct()
            row.id = role.id
            row.name_en = role.name_en
            row.portrait = role.portrait
            row.gif_1 = role.gif_1
            row.gif_2 = role.gif_2
            data.roles.append(row)
        data.sentences = []
        for s in sentences:
            row = Struct()
            row.id = s.id
            row.role_id = s.role.id if s.role else None
            row.name_en = 'A'
            if s.role and s.role.name_en:
                row.name_en = s.role.name_en
            row.audio = s.audio
            row.audio_text = s.audio_text
            row.text = s.text
            row.translation = s.translation
            row.duration = math.ceil(s.duration)
            data.sentences.append(row)
        cache.yy_chapter_dialog.set(cid, data)
    return data


def get_lesson(chapter):
    """获得课文数据"""

    lesson = cache.yy_chapter_lesson.get(chapter.id)
    if lesson:
        lesson = Struct(lesson)
        lesson.chapter = Struct(lesson.chapter) if lesson.chapter else None
        sentences = []
        for r in lesson.sentences:
            r = Struct(r)
            r.role = Struct(r.role) if r.role else None
            sentences.append(r)
        lesson.sentences = sentences
    else:
        sql = """select id,title from yy_standard_pool where status<>-1 and catalog_id=%s and type in (1,3) and tts=1""" % chapter.id
        lesson = db.ziyuan_slave.fetchone_dict(sql)
        if not lesson:
            return

        sql = """select id, pool_id,text,audio_text,translation,male_audio,female_audio,is_key,role_id,duration from yy_standard_pool_detail s
    where s.pool_id=%s and s.status<>-1 ORDER BY s.sequence """ % lesson.id
        sentences = db.ziyuan_slave.fetchall_dict(sql)
        role_dict = {}
        roles_list = [i.role_id for i in sentences if i.role_id]
        if roles_list:
            sql = """select r.id ,r.name_en,r.name_zh,r.image_id,i.portrait from yy_role r
            LEFT JOIN yy_role_image i on i.id=r.image_id
            where r.id in (%s)""" % ",".join(str(i) for i in roles_list)
            rows = db.ziyuan_slave.fetchall_dict(sql)
            role_dict = {r.id: r for r in rows}
        for s in sentences:
            s.role = role_dict.get(s.role_id)

            path = s.female_audio or s.male_audio
            if path:
                s.audio = format_ziyuan_url(path)
            del s.female_audio
            del s.male_audio

        roles = OrderedDict()
        for s in sentences:

            if s.role and s.role.id not in roles:
                roles[s.role.id] = s.role
                s.role.portrait = format_ziyuan_url(s.role.portrait)
                s.name_en = s.role.name_en
        rename_role(sentences)
        for s in sentences:
            if not s.name_en:
                s.name_en = "A"

        lesson.sentences = sentences
        lesson.nrole = get_role_count(chapter, sentences)
        lesson.has_translation = False
        if sentences:
            lesson.has_translation = bool(sentences[0].translation)
        lesson.chapter = chapter
        cache.yy_chapter_lesson.set(chapter.id, lesson)
    return lesson


def rename_role(sentences):
    "如果课文角色名只有一个字母, 就按先说的是A, 后说的是B来命名"
    current = 'A'
    tab = {}
    for s in sentences:
        if s.role and len(s.role.name_en) <= 1:
            newname = tab.get(s.role.id)
            if not newname:
                newname = tab[s.role.id] = current
                current = chr(ord(current) + 1)
            s.role.name_en = newname


def get_role_count(chapter, sentences=None):
    "课文角色数量"
    if not (chapter.is_main or chapter.type == 3):
        return 0
    if sentences is None:
        sql = """select id from yy_standard_pool where status<>-1 and catalog_id=%s and type in (1,3) and tts=1""" % chapter.id
        lesson = db.ziyuan_slave.fetchone_dict(sql)
        if not lesson:
            return 0
        sql = """select id,role_id from yy_standard_pool_detail where pool_id=%s and status<>-1""" % lesson.id
        sentences = db.ziyuan_slave.fetchall_dict(sql)
    roles = set()
    for s in sentences:
        if s.role_id:
            roles.add(s.role_id)
    return len(roles)


################################  测试  ##################################


def get_task_details(test_id):
    """返回 完成的 习题答案和 答题卡详情（补充正确答案）"""

    cache_data = cache.yy_test_result.get(int(test_id))
    if cache_data:
        details = [Struct(d) for d in cache_data["details"]]
    else:
        sql = """select id,test_id,question_id,ask_id,result,answer,option_id from yy_test_detail where test_id=%s""" % test_id
        details = db.tbkt_yingyu.fetchall_dict(sql)
    # 大题ID列表
    qid_list = []
    for d in details:
        qid_list.append(d.question_id)
    qid_list = list(set(qid_list))
    questions = get_task_questions_data(qid_list)
    # questions.sort(lambda x, y: cmp((x.classify, x.type), (y.classify, y.type)))

    # 补充用户答案  补充题号
    detail_dict = {d.ask_id: d for d in details}
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
        ask = ask_dict.get(d.ask_id)
        if ask:
            d.right_answer = ask.answer
        if ask and ask.qtype == 2:
            rows = ['%s-%s' % (o.id, o.link_id) for o in ask.options if o.link_id >= 0]
            d.right_answer = '|'.join(rows)

        sheet[d.ask_id] = d
    questions.sort(key=lambda x: x.id)
    return questions, sheet


def get_task_questions_data(qid_list):
    """
    功能说明：            返回全都大题的数据
    """
    if not qid_list:
        return
    sql = """select id, subject ,classify,type,video_url,video_image   from yy_question where id in(%s)  """ % ','.join(
        str(i) for i in qid_list)
    questions = db.ziyuan_slave.fetchall_dict(sql)
    if not questions:
        return

    sql = """select id,subject,parse,video_url, video_image,listen_audio,listen_text,question_id,duration  from  yy_question_ask
where question_id in(%s)""" % ','.join(str(q.id) for q in questions)
    asks = db.ziyuan_slave.fetchall_dict(sql)

    ask_ids = [a.id for a in asks]
    sql = """select id,ask_id,content,image,`option`,is_right,link_id from yy_ask_options
where ask_id in (%s) ORDER  BY  id""" % ','.join(str(a) for a in ask_ids)

    options = db.ziyuan_slave.fetchall_dict(sql)
    for o in options:
        o.image = format_ziyuan_url(o.image)

    for ask in asks:
        ask.subject = json.loads(ask.subject)
        ask.parse = json.loads(ask.parse)
        ask.video_url = format_ziyuan_url(ask.video_url)
        ask.video_image = format_ziyuan_url(ask.video_image)
        ask.listen_audio = format_ziyuan_url(ask.listen_audio)

        ask.options = [o for o in options if o.ask_id == ask.id]
        right_options = [o for o in ask.options if o.is_right]
        ask.right_option = right_options[0] if right_options else None
        ask.subject = Struct(ask.subject)
        _ask_images = []
        if ask.subject["images"]:
            for img in ask.subject["images"]:
                _ask_images.append(format_ziyuan_url(img))
            ask.subject["images"] = _ask_images

        if ask.right_option and ask.right_option.get("image"):
            ask.right_option["image"] = format_ziyuan_url(ask.right_option["image"])
        _options = []
        for _option in ask.options:
            if _option.get("image"):
                _option["image"] = format_ziyuan_url(_option["image"])
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

def get_test_result_game(test, cache_date=0):
    """
    获取 游戏作业结果
    :param test:
    :return:
    """
    if cache_date:
        details = [Struct(r) for r in cache_date['cache_details']]
    else:
        sql = """select id,word_id,result,score from yy_word_test_detail where test_id =%s""" % test.id
        details = db.tbkt_yingyu.fetchall_dict(sql)

    word_ids = [d.word_id for d in details]
    if not word_ids:
        return
    sql = """select id,word,translation from yy_word where id in(%s)""" % ",".join(str(i) for i in word_ids)
    words = db.ziyuan_slave.fetchall_dict(sql)

    word_dict = {w.id: w for w in words}
    for d in details:
        d.word = word_dict.get(d.word_id)

    context = Struct()
    context.test = test
    context.right_number = sum(1 for d in details if d.result == 1)
    context.score = test.score if test else 0
    context.wrong_words = [d.word for d in details if d.result == 0 and d.word]
    context.words_unmber = len(words)
    return context




def get_read_result(user_id, task_detail):
    """返回单词普通作业结果"""
    cache_data = cache.yy_study_result.get((user_id, task_detail.id))
    if cache_data:
        study = Struct(cache_data["study"])
        details = [Struct(r) for r in cache_data["details"]]
    else:

        sql = """select id,score from yy_study where user_id=%s and object_id=%s """ % (user_id, task_detail.id)
        study = db.tbkt_yingyu.fetchone_dict(sql)
        if not study:
            return
        sql = """select id,study_id,object_id,answer,result, remote_audio,score from yy_study_detail
    where study_id=%s""" % study.id
        details = db.tbkt_yingyu.fetchall_dict(sql)

    data = Struct()
    data.score = study.score
    data.grade = score_to_en(study.score)

    word_ids = [d.object_id for d in details]
    if not word_ids:
        return
    sql = """select id, translation, male_audio,female_audio,phonetic,word from yy_word where id in (%s)""" % ",".join(
        str(i) for i in word_ids)
    words = db.ziyuan_slave.fetchall_dict(sql)
    for word in words:
        word.female_audio = format_ziyuan_url(word.female_audio)
        word.male_audio = format_ziyuan_url(word.male_audio)
        word.audio = word.female_audio or word.male_audio

    word_dict = dict((w.id, w) for w in words)
    rows = []
    for d in details:
        row = Struct()
        word = word_dict[d.object_id]
        row.text = word.word.strip()
        row.phonetic = word.phonetic
        row.translation = word.translation
        row.audio = word.audio
        row.mgrade = score_to_en(d.score)
        if not d.answer:
            d.answer = "<em>%s</em>" % word.phonetic
        row.user_answer = d.answer
        row.user_audio = d.remote_audio.strip() if d.remote_audio else None
        row.result = d.result
        rows.append(row)
    data.words = rows
    return data


def get_write_result(user_id, task_detail):
    """"返回单词测听写作业结果"""
    cache_data = cache.yy_study_result.get((user_id, task_detail.id))
    if cache_data:
        study = Struct(cache_data["study"])
        test_details = [Struct(r) for r in cache_data["details"]]
    else:
        sql = """select id,score from yy_study where user_id=%s and object_id=%s """ % (user_id, task_detail.id)
        study = db.tbkt_yingyu.fetchone_dict(sql)
        if not study:
            return
        sql = """select id,object_id,score,answer,result,remote_audio from yy_study_detail where study_id=%s""" % study.id
        test_details = db.tbkt_yingyu.fetchall_dict(sql)

    word_ids = [d.object_id for d in test_details]
    sql = """select id, translation, male_audio,female_audio,phonetic,word,duration  from yy_word where id in (%s)""" % ",".join(
        str(i) for i in word_ids)
    words = db.ziyuan_slave.fetchall_dict(sql)
    for word in words:
        word.female_audio = format_ziyuan_url(word.female_audio)
        word.male_audio = format_ziyuan_url(word.male_audio)
        word.audio = word.female_audio or word.male_audio

    word_dict = dict((w.id, w) for w in words)

    data = Struct()
    data.grade = score_to_en(study.score)

    rows = []
    for d in test_details:
        row = Struct()
        word = word_dict[d.object_id]
        row.text = word.word.strip()
        row.phonetic = word.phonetic
        row.translation = word.translation
        row.mgrade = score_to_en(d.score)
        row.audio = word.audio
        row.user_answer = d.answer
        row.user_audio = d.remote_audio.strip() if d.remote_audio else None
        row.result = d.result
        rows.append(row)
    data.words = rows
    return data


def get_question_data(qid, ask_no=1):
    """
    功能说明：            返回一道大题的数据
    参数: ask_no 小题题号
    """
    question = cache.yy_question.get(qid)
    if question:
        ask_list = []
        for a in question.asks:
            a = Struct(a)
            a.options = [Struct(r) for r in a.options]
            a.subject = Struct(a.subject)
            a.parse = Struct(a.parse)
            ask_list.append(a)
        question.asks = ask_list
        question.subject = Struct(question.subject)

    if not question:
        sql = """select id,subject,classify,type,video_url,video_image from yy_question where id = %s;""" % qid
        question = db.ziyuan_slave.fetchone_dict(sql)
        if not question:
            return

        question.asks = get_question_ask(question, ask_no)
        #  补充一些特殊题型的格式
        special_handle_question(question)
        cache.yy_question.set(qid, question)

    # 最后补充题号
    question.ask_no = ask_no
    question.num = ask_no + 1
    for ask in question.asks:
        ask["no"] = ask_no
        ask_no += 1
    return question


def get_question_ask(question, ask_no):
    """返回大题小问"""

    sql = """select id,subject,parse,video_url, video_image,listen_audio,listen_text,duration  from  yy_question_ask
where question_id=%s""" % question.id
    asks = db.ziyuan_slave.fetchall_dict(sql)

    ask_ids = [a.id for a in asks]
    sql = """select id,ask_id,content,image,`option`,is_right,link_id from yy_ask_options where ask_id in (%s) ORDER  BY  id""" % ','.join(
        str(a) for a in ask_ids)

    options = db.ziyuan_slave.fetchall_dict(sql)
    for o in options:
        o.image = format_ziyuan_url(o.image)

    for ask in asks:
        ask.subject = json.loads(ask.subject)
        ask.parse = json.loads(ask.parse)
        ask.video_url = format_ziyuan_url(ask.video_url)
        ask.video_image = format_ziyuan_url(ask.video_image)
        ask.listen_audio = format_ziyuan_url(ask.listen_audio)

        ask.options = [o for o in options if o.ask_id == ask.id]
        right_options = [o for o in ask.options if o.is_right]
        ask.right_option = right_options[0] if right_options else None
        ask.subject = Struct(ask.subject)
        _ask_images = []
        if ask.subject["images"]:
            for img in ask.subject["images"]:
                _ask_images.append(format_ziyuan_url(img))
            ask.subject["images"] = _ask_images

        if ask.right_option and ask.right_option.get("image"):
            ask.right_option["image"] = format_ziyuan_url(ask.right_option["image"])
        _options = []
        for _option in ask.options:
            if _option.get("image"):
                _option["image"] = format_ziyuan_url(_option["image"])
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
        elif question.type == 2:     # 连线题
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


def format_link_answer(options):
    "格式化连线题答案"
    rows = ['%s-%s'%(o.id,o.link_id) for o in options if o.link_id>=0]
    return '|'.join(rows)

def get_answer_sheet_list(test_id , questions = []):
    """
    功能说明：            返回答题卡
    {ask_id:{qid:1,answer:用户答案,right_answer:正确答案}}
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    王晨光                    2016-8-3
    张帅男                    2017-1-7    取消orm， 获得一道题的答案
    """
    ask_dict = {}
    for q in questions:
        for a in q.asks:
            a.qtype = q.type
            ask_dict[a.id] = a
    sheet = []

    cache_data = cache.yy_test_result.get(int(test_id))
    if cache_data:
        details = [Struct(d) for d in cache_data["details"]]
    else:
        sql = "SELECT id, question_id, ask_id, result, answer, option_id from yy_test_detail " \
              "WHERE test_id = %s" % test_id
        details = db.tbkt_yingyu.fetchall_dict(sql)

    details.sort(key=lambda x: x.question_id)
    for d in details:
        if not ask_dict.has_key(d.ask_id):
            continue
        row = Struct()
        row.qid = d.question_id
        row.answer = d.answer
        row.result = d.result
        row.option_id = d.option_id
        row.right_answer = ''
        # 补充连线题原题答案
        ask = ask_dict.get(d.ask_id)
        if ask:
            sql = "SELECT id, `option` as op from yy_ask_options WHERE ask_id = %s and is_right = 1;" % ask.id
            _ask = db.ziyuan_slave.fetchall_dict(sql)
            if _ask:
                _ask = _ask[0]
            row.right_answer = _ask.op if _ask else ''
        if ask and ask.qtype == 2:
            row.right_answer = format_link_answer(ask.options)
        # sheet[d.ask_id] = row
        row.ask_id = d.ask_id
        sheet.append(row)
    # sheet.sort(lambda x, y: (cmp(x.qid, y.qid)))
    return sheet

def get_answer_sheet(questions=[]):
    """
    功能说明：            对正确答案进行格式化
    {ask_id:{qid:1,right_answer:用户答案}}
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2016-11-3
    """
    sheet = []
    for q in questions:
        for ask in q.asks:
            ask = Struct(ask)
            row = Struct()
            row.qid = q.id
            row.aid = ask.id
            row.right_answer = ''
            if ask:
                sql = "SELECT `option` from yy_ask_options WHERE ask_id = %s and is_right = 1;" % ask.id
                _ask = db.ziyuan_slave.fetchall_dict(sql)
                if _ask:
                    _ask = _ask[0]
                row.right_answer = _ask.option if _ask else ''
            if ask and q.type == 2:
                row.right_answer = format_link_answer(ask.options)
            sheet.append(row)
    return sheet

def get_special_user_answer(questions):
    '补充答案'

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
            a.i += 1
            # question.i += 1
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
            a.i = 0
            question._no = question.ask_no or 1
            question.subject.content = re.sub(r'<span.*?</span>:<em>.*?</em>', repl_f, question.subject.content)

    return questions