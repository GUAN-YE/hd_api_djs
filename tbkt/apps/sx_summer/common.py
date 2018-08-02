# coding:utf-8
import datetime
import logging
import re
from collections import OrderedDict
from contextlib import contextmanager
from functools import wraps
import requests
import simplejson as json
import time
from django.conf import settings
from apps.sx_summer.active_cofing import *
from com import com_user
from com.com_cache import cache
from libs.utils import db, Struct, get_videourl


def ctime(func):
    @wraps(func)
    def wapper(*args, **kwargs):
        begin = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        if settings.DEBUG == True:
            print (func.__name__, end - begin)
        return result

    return wapper


@contextmanager
def timeblock(label):
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print('{} : {}'.format(label, end - start))


# ############################## 作业相关   ####################
def get_questions(qids):
    """使用缓存获取题目, 返回值同get_questions_direct"""
    # 读缓存
    cached = cache.sx_question.get_many(qids)  # 缓存过的题目 {qid: question}
    # 读出来是字典, 整理成Struct
    for q in cached.itervalues():
        question_restruct(q)
    direct_qids = [qid for qid in qids if qid not in cached]  # 未缓存的qids
    directs = get_questions_direct(direct_qids)
    qmap = {q.id: q for q in directs}
    questions = []
    tocache = {}  # 待缓存的题目
    for qid in qids:
        q = cached.get(qid) or qmap.get(qid)
        if q:
            questions.append(q)
            if qid not in cached:
                tocache[qid] = q
    # 写缓存
    if tocache:
        cache.sx_question.set_many(tocache)
    # 刷新题号
    for i, q in enumerate(questions):
        q.number = i + 1
        for j, a in enumerate(q.asks):
            a.number = j + 1
            a.title = "%s(%s)" % (q.number, a.number) if len(q.asks) > 1 else "%s" % q.number
    return questions


def get_right_option(options):
    """获得正确选项"""
    for op in options:
        if op.get('is_right') == 1:
            return op.get('option') or ''


def get_questions_direct(qids):
    """
    获取试题综合数据
    -------------------------------
    王晨光     2016-11-18
    -------------------------------
    :param qids: 大题ID列表
    :returns: [question]
        [{
            id: 大题ID,
            number: 1  # 大题号
            subject: 大题干
            type: 题型,
            display: 1选择题 3解答题
            video_url: 大题视频
            asks: [{
                id: 小问ID,
                number: 1  # 小题号
                subject: 小题干,
                parse: 解题步骤,
                video_url: 小问视频
                options: [{id:选项ID, content:内容, image:{'url':图片地址, 'align':''}, 'option':'A', 'is_right':1或0}] 选择题选项
            }]
        }]
    """
    questions = pure_questions(qids)
    if not questions:
        return []

    asks = pure_asks(qids)
    aids = [a.id for a in asks]
    options = pure_options(aids)
    akids = pure_kids(aids)
    # 把question, ask, option组合起来
    for i, q in enumerate(questions):
        q.asks = [a for a in asks if a.question_id == q.id]
        q.number = i + 1  # 给一个默认题号
        for j, a in enumerate(q.asks):
            a.options = [o for o in options if o.ask_id == a.id] if q.display == 1 else create_subjective_options(a.id)
            # 判断题补充选项内容
            if q.type == 2 and len(a.options) >= 2:
                a.options[0]['content'] = u'正确'
                a.options[1]['content'] = u'错误'
            a.right_option = get_right_option(a.options)
            a.number = j + 1
            # 小问相关知识点
            a.knowledge = [k for k in akids if k.ask_id == a.id]

    return questions


def question_restruct(question):
    "把dict转成struct"
    try:
        question.asks = map(Struct, question.asks)
    except:
        logging.error(question.asks)
        raise
    for a in question.asks:
        a.options = map(Struct, a.options)
    return question


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


def parse_subject(subject):
    """解析题干

    :returns: {'content':内容, 'image':{'url':图片地址, 'align':''}}
    """
    if not subject:
        return {"content": "", "image": {"url": ""}}
    obj = json.loads(subject)
    obj["content"] = replace_symbol(obj["content"])
    images = obj.get("images", [])
    if images:
        image = images[0]
        image['url'] = format_url(image['url'])
    else:
        image = {}
    obj["image"] = image
    return obj


def parse_parse(parse):
    """文字解析

    :returns: [{'content':内容, 'image':{'url':图片地址, 'align':''}}]
    """
    if not parse:
        return [{"content": "", "image": {"url": ""}}]
    object_list = json.loads(parse) if parse else []
    new_object_list = []
    for obj in object_list:
        obj["content"] = replace_symbol(obj.get("content", ''))
        images = obj.get('images', [])
        if images:
            image = images[0]
            image['url'] = format_url(image['url'])
        else:
            image = {}
        obj['image'] = image
        obj = Struct(obj)
        new_object_list.append(obj)
    return new_object_list


def parse_video(video_url):
    """解析视频绝对地址"""
    return get_videourl(video_url)


def pure_questions(qids):
    """
    获得试题原始数据

    :param qids: [题ID]
    :return: [{id:ID, subject:题干, type:题型, display: 1选择题 3解答题, video_url:大题视频}]
    """
    if not qids:
        return []

    qids_s = ','.join(str(i) for i in qids)
    sql = """
    select id, subject, display, type, video_url from sx_question
    where id in (%s)
    """ % qids_s
    questions = db.ziyuan_slave.fetchall_dict(sql)
    # 格式化题干
    for q in questions:
        q.subject = parse_subject(q.subject)
        q.video_url = parse_video(q.video_url)
    # 数据库读出来的顺序会乱, 这里按输入的qids顺序重新排序
    qmap = {q.id: q for q in questions}
    return [qmap[qid] for qid in qids if qid in qmap]


def pure_asks(qids):
    """
    获得小问原始数据

    :qids: [题ID]
    :return: [{id:小问ID, question_id:题ID, subject:题干, parse:解题步骤}]
    """
    if not qids:
        return []

    qids_s = ','.join(str(i) for i in qids)
    # 小题顺序按ID从小到大
    sql = """
    select id, question_id, subject, parse, video_url from sx_question_ask
    where question_id in (%s)
    order by id
    """ % qids_s
    asks = db.ziyuan_slave.fetchall_dict(sql)
    # 格式化题干和解题步骤
    for a in asks:
        a.subject = parse_subject(a.subject)
        a.parse = parse_parse(a.parse)
        a.video_url = parse_video(a.video_url)
    return asks


def parse_option(op_content):
    """解析选项内容

    :returns: {'content':内容, 'image':{'url':图片地址, 'align':''}, 'option':'A', 'is_right':1或0}
    """
    if not op_content:
        return {}
    option = json.loads(op_content) or {}
    option = Struct(option)
    option["content"] = replace_symbol(option.get("content", ""))
    images = option.pop("images", [])
    if images:
        image = images[0]
        image['url'] = format_url(image['url'])
    else:
        image = {}
    option['image'] = image
    option['is_right'] = int(option.get('is_right') or 0)
    return option


def pure_options(aids):
    """
    获得选项原始数据

    :param aids: [小问ID]
    :return: [{id:选项ID, ask_id:小问ID, content:内容, image:{'url':图片地址, 'align':''}, 'option':'A', 'is_right':1或0}]
    """
    if not aids:
        return []

    aids_s = ','.join(str(i) for i in aids)
    # 选项顺序按ID从小到大
    sql = """
    select id, ask_id, content from sx_ask_options
    where ask_id in (%s)
    """ % aids_s
    options = db.ziyuan_slave.fetchall_dict(sql)
    # 格式化选项数据
    for o in options:
        d = parse_option(o.content)
        del o.content
        o.update(d)
    return options


def format_url(data_url, tts=None):
    """根据日期判断 资源所用服务器"""
    if not data_url:
        return ''

    tts_root = '/upload_media/tts/' if tts else '/upload_media/'
    _url = settings.FILE_VIEW2_URLROOT + tts_root + data_url
    try:
        date = re.findall(r'/(\d+)\.', data_url)
        today = datetime.date.today()
        if date and len(date[-1]) >= 8:
            date_num = date[-1]
            video_date = datetime.date(year=int(date_num[:4]), month=int(date_num[4:6]), day=int(date_num[6:8]))
            ctime = (today - video_date).days
            if ctime <= 2:
                _url = settings.FILE_VIEW_URLROOT + tts_root + data_url
    except:
        return _url
    return _url


def create_subjective_options(ask_id):
    """
    构造主观题选项
    [{id:0, content:'', image:{}, 'option':'A', 'is_right':1或0}]
    """
    return [
        Struct({'ask_id': ask_id, 'id': 0, 'content': u'我答对了', 'image': {}, 'option': u'A', 'is_right': 1}),
        Struct({'ask_id': ask_id, 'id': 0, 'content': u'我答错了', 'image': {}, 'option': u'B', 'is_right': 0}),
    ]


def pure_kids(aids):
    """
    小问相关知识点ID

    :param aids: [小问ID]
    :return: [(小问ID, 知识点ID)]
    """
    if not aids:
        return []

    aids_s = ','.join(str(i) for i in aids)
    sql = """
    SELECT distinct r.ask_id, k.id,k.name,k.video_url FROM sx_ask_relate_knowledge r
    inner join sx_knowledge k on k.id=r.knowledge_id and k.status=1
    where r.ask_id in (%s)
    """ % aids_s
    rows = db.ziyuan_slave.fetchall_dict(sql)
    for i in rows:
        i.video_url = parse_video(i.video_url)
    return rows


def dedupe(items):
    """
    去重
    :param items: list集合
    :return:
    """
    seen = set()
    for i in items:
        if i not in seen:
            yield i
            seen.add(i)


def get_ask_kids(ask_ids):
    """
    获取小问知识点
    :param ask_ids: [小问ID]
    :return: [知识点ID]
    """
    if not ask_ids:
        return []
    ask_ids_s = ','.join(str(i) for i in ask_ids)
    sql = """
    select distinct knowledge_id from sx_ask_relate_knowledge
    where ask_id in (%s)
    """ % ask_ids_s
    rows = db.ziyuan_slave.fetchall(sql)
    return [r[0] for r in rows]


# ####################################### 积分抽奖 ########################
def get_rank(app_id, page=1, is_smx=False, num=10):
    # 判断是否为三门峡
    if page < 0: page = 1
    smx = 's.city <> 411200' if not is_smx else 's.city=411200'
    sql = """SELECT (@rowNum:=@rowNum+1) AS num,z.* from(
                        select s.user_id,s.score FROM score_user s
                        WHERE app_id=%s AND score<>0 AND %s
                        ORDER BY score DESC,s.user_id   limit %s, %s
                    )z,(SELECT (@rowNum :=%s)) n
                """ % (app_id, smx, (page - 1) * num, num, (page - 1) * num)
    rank = db.slave.fetchall_dict(sql)
    rank_dict = {r.user_id: r for r in rank}
    user_info = com_user.users_info(rank_dict.keys())

    for user_id in rank_dict.keys():
        info = user_info.get(user_id, {})
        rank_dict[user_id].update(info)

    rank = rank_dict.values()
    rank = sorted(rank, key=lambda x: int(x.num))
    sql = """SELECT count(1) num FROM score_user s WHERE app_id = %s  AND  score  <> 0 AND %s
                ORDER BY score DESC,user_id """ % (app_id, smx)
    row = db.slave.fetchone_dict(sql)
    total = row.num if row else 0

    return rank, total


def get_unit_rank(units, page=1, num=10):
    """返回教师所有班级 学生排行"""
    if not units:
        return
    unit_ids = ','.join(str(i) for i in units)
    sql = """select user_id from mobile_order_region where unit_class_id in (%s) and user_type<>3 GROUP BY user_id""" % unit_ids
    stu = db.ketang_slave.fetchall_dict(sql)
    if not stu:
        return
    sql = """SELECT (@rowNum:=@rowNum+1) AS num, s.user_id,s.score from (select user_id, if(score,score,0) score from score_user
            where user_id in (%s)   and app_id=%s
            ORDER BY score DESC
            ) s ,(SELECT (@rowNum :=%s)) z
            """ % (','.join(str(s.user_id) for s in stu), APP_ID_STU, (page - 1) * num)
    rank = db.default.fetchall_dict(sql)
    rank_dict = {r.user_id: r for r in rank}
    stu_detail = {}
    for s in stu:
        _detail = rank_dict.get(s.user_id, {'num': -1, 'user_id': s.user_id, 'score': 0})
        stu_detail.update({s.user_id: _detail})
    user_info = com_user.users_info(stu_detail.keys())
    for new in stu_detail.keys():
        info = user_info.get(new, {})
        stu_detail[new].update(info)
    rank = stu_detail.values()
    rank = sorted(rank, key=lambda x: x['num'] if x['num'] > 0 else 10000)
    # 重新添加名次
    rank = rank[(page - 1) * num:page * num]
    for k, v in enumerate(rank):
        v['num'] = (page - 1) * num + 1 + k

    total = len(stu)
    return rank, total


def get_user_rank(app_id, user_id, score=0, city=0):
    is_smx = 0 if city and int(city) != 411200 else 1
    smx = 'city <> 411200' if not is_smx else 'city=411200'
    if not (app_id and user_id and score):
        return 0
    rank = cache.sx_summer_rank.get([1, app_id, user_id, is_smx])
    if not rank:
        db.default.score_user.filter(app_id=app_id, user_id=user_id).update(city=str(city))
        sql = """
            SELECT user_id,num from(
              SELECT score,user_id,(@rowNum:=@rowNum+1) AS num  FROM score_user ,(SELECT (@rowNum :=0)) r
              WHERE app_id = %s  and  score >= %s AND  %s
              ORDER BY score DESC,user_id)t
            WHERE user_id=%s;""" % (app_id, score, smx, user_id)
        score_user = db.default.fetchone_dict(sql)
        rank = int(score_user.num) if score_user else 0
        cache.sx_summer_rank.set([1, app_id, user_id, is_smx], rank)
    return rank


def add_score(app_id, user_id, score, item_no, remark, city, unit_id=0):
    '''修改积分'''
    if not get_active_status(app_id):
        return False
    if not city:
        city = 0
    is_smx = 0 if city and int(city) != 411200 else 1
    sql_1 = """INSERT INTO score_user_detail (app_id, user_id, item_no, remark, score, add_date)
                        VALUES (%s,%s,'%s','%s',%s,'%s');
                  """ % (app_id, user_id, item_no, remark.encode('utf-8'), score, str(int(time.time())))

    score_user = db.default.score_user.get(app_id=app_id, user_id=user_id, )
    if score_user:
        sql_2 = """ UPDATE score_user SET score = score+%s ,city=%s,unit_id=%s WHERE app_id = %s AND user_id=%s;""" % (
            score, str(city), unit_id, app_id, user_id)
    else:
        sql_2 = """INSERT INTO score_user (app_id, user_id, score,city,unit_id) VALUES (%s,%s,%s,%s,%s);""" % (
            app_id, user_id, score, str(city), unit_id)
    try:
        with db.default as c:
            c.execute(sql_1)
            c.execute(sql_2)
    except Exception, e:
        print e, sql_1, sql_2
        return False
    # db.default.execute(sql)
    # 删除缓存
    cache.sx_summer_rank.delete([1, app_id, user_id, is_smx])
    return True


def get_score_add_num(app_id, user_id, item_no):
    assert (app_id and user_id and item_no), 'get_score_add_num:lack parameter'
    sql = """SELECT count(id) num FROM score_user_detail
WHERE app_id=%s AND user_id=%s AND item_no='%s'  AND DATE(FROM_UNIXTIME(add_date))='%s' """ % (
        app_id, user_id, item_no, datetime.date.today())
    num = db.default.fetchone_dict(sql).num
    return num


def get_score_detail(app_id, user_id, page=1):
    """获取积分详情"""
    assert (app_id and user_id), 'get_score_detail:lack parameter'
    sql = """SELECT sum(score), remark FROM score_user_detail
                    WHERE app_id=%s AND user_id=%s  GROUP BY DATE(FROM_UNIXTIME(add_date)),item_no
              """ % (app_id, user_id)
    detail = db.default.fetchall_dict(sql)
    day_detail = OrderedDict()
    for d in detail:
        day_detail[d] = day_detail.get(d, []) + [d]
    return day_detail


def get_user_award(app_id, user_id, is_smx):
    """返回用户获奖情况"""
    award_type = 5
    if is_smx:
        if app_id in TEA_APP_IDS:
            award_type = 6
    detail = db.tbkt_web_slave.active_award.filter(active_id=app_id, user_id=user_id,
                                                   award_type__lt=award_type).order_by(
        '-add_time')[:]
    if not detail:
        return []
    award_detail = []
    for d in detail:
        if d.award_name == u'谢谢参与':
            continue
        awd = [time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(d.add_time)).decode('utf-8'), d.award_name]
        award_detail.append(awd)

    return award_detail


def get_award_detail(app_id, is_smx, p=1):
    begin = int((p - 1) * 10)
    end = int(p * 10)
    if is_smx:
        award_type = 5
        if app_id in TEA_APP_IDS:
            award_type = 6
        detail = db.tbkt_web_slave.active_award.filter(active_id=app_id, award_type__lt=award_type,
                                                       city=411200).order_by(
            'award_type',
            '-add_time')[begin:end]
    else:
        detail = db.tbkt_web_slave.active_award.filter(active_id=app_id, award_type__lt=5).exclude(
            city=411200).order_by('-add_time', 'award_type')[begin:end]
    if not detail:
        return []
    award_detail = []
    for d in detail:
        if d.award_name == u'谢谢参与':
            continue
        awd = u'%s通过抽奖获得%s' % (d.user_name, d.award_name)
        award_detail.append(awd)

    return award_detail


def get_all_award_detail(app_id, is_smx, p=1):
    """
    全部 获奖详情
    :param app_id:
    :param is_smx:
    :param p:
    :return:
    """
    begin = int((p - 1) * 10)
    award_type = 5
    city = 'a.city<>411200'
    if is_smx:
        city = 'a.city=411200'
        if app_id in TEA_APP_IDS:
            award_type = 6
    sql = """
            select (@rowNum:=@rowNum+1) as num ,a.user_name ,a.award_name, a.user_id from active_award a ,(select (@rowNum :=%s)) z
            where a.active_id=%s and award_type<%s and %s and award_name<>'谢谢参与' order by a.award_type ,add_time DESC limit  %s	 ,%s
    """ % (begin, app_id, award_type, city, begin, 10)
    award_detail = db.tbkt_web.fetchall_dict(sql)
    user_ids = list(set([a.user_id for a in award_detail]))
    user_info = com_user.users_info(user_ids)
    for a in award_detail:
        info = user_info.get(a.user_id)
        if info:
            a.update(info)
    rank = sorted(award_detail, key=lambda x: x.num)
    sql = """select count(1) num from active_award a where active_id=%s and award_type<%s and %s  and award_name<>'谢谢参与'""" % (
        app_id, award_type, city)
    total = db.tbkt_web.fetchone_dict(sql)
    return rank, total.num


def get_yuwen_lottery_able(request, app_id, user, lottery_cost):
    """判断语文能否抽奖"""
    # 0 表示学生1表示教师
    user_type = 0 if user.type == 1 else 1
    host = get_yw_host(request)
    url = '''%sAPI/SummerAct/GetPoint?intUserID=%s&intUserType=%s''' % (host, user.old_user_id, user_type)
    if (user_type == 0 and app_id == YW_APP_ID_STU) or (user_type == 1 and app_id == YW_APP_ID_TEA):
        result = requests.get(url, verify=False)
        score = int(json.loads(result.text).get('point'))
        if score >= lottery_cost:
            return True
    return False


def yw_reduce_score(request, app_id, user, lottery_cost):
    """语文扣分"""
    # 0 表示学生1表示教师
    user_type = 0 if user.type == 1 else 1
    host = get_yw_host(request)
    url = '''%sAPI/SummerAct/DeductPoint?intUserID=%s&intUserType=%s&intPoint=%s''' % (
        host, user.old_user_id, user_type, lottery_cost)
    if (user_type == 0 and app_id == YW_APP_ID_STU) or (user_type == 1 and app_id == YW_APP_ID_TEA):
        result = requests.get(url, verify=False)
        success = str(json.loads(result.text).get('success'))
        if success != 'False':
            return True
    return False


def get_yw_host(request):
    """获取 语文 host"""

    url_root = request.build_absolute_uri()
    domain = ''
    if '-beta' in url_root:
        domain = '-beta'
    elif '-rc' in url_root:
        domain = '-rc'
    url = '''https://ywapihd%s.m.jxtbkt.cn/''' % domain
    return url


def add_rank_award(app_id, is_smx, rank):
    award = RANK_AWARD.get((app_id, is_smx), {})
    if not award:
        return rank, 0
    for r in rank:
        r.award = award.get(r.num, "")
    return rank, len(award.items())


def get_award_result(_app_id, user, award_type, is_smx):
    '''更新后抽奖方法'''

    app_id = APP_ID_STU
    if _app_id in TEA_APP_IDS:
        app_id = APP_ID_TEA

    # 判断奖品数量
    success = 0
    if award_type:
        with db.default as c:
            sql = "select id,num,name,type from score_gift  where type=%s and app_id=%s and category_id=%s for update" % (
                award_type, app_id, is_smx)
            award = c.fetchone_dict(sql)
            if award and award.num > 0:
                c.execute("update score_gift set num=%s where id=%s" % ((award.num - 1), award.id))
                success = 1

        # 中奖
        if success and award_type != 1:
            add_award = db.tbkt_web.active_award.create(
                active_id=app_id,
                user_id=user.old_user_id,
                user_name=user.name,
                award_name=award.name,
                award_type=award.type,
                city=user.city,
                add_time=int(time.time()),
                remark=_app_id
            )
            return award.type, award.name
    # 未中奖
    _name = u'谢谢参与'
    if is_smx and _app_id in TEA_APP_IDS:
        _name = u'300兆流量'
    if not success or not award_type:
        db.tbkt_web.active_award.create(
            active_id=app_id,
            user_id=user.old_user_id,
            user_name=user.name,
            award_name=_name,
            award_type=5,
            city=user.city,
            add_time=int(time.time()),
            remark=_app_id
        )
    return 0, 0


def get_active_status(app_id):
    app_id = APP_ID_STU
    if app_id in STU_APP_IDS:
        app_id = APP_ID_TEA
    active = db.tbkt_web.active.get(id=app_id)
    return time.time() < active.end_time
