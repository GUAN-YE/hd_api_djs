# coding:utf8
import json
import datetime
from collections import defaultdict
from com.com_cache import cache
from libs.utils import db, Struct, time, join, get_absurl, num_to_ch, ajax
from . import math_com


def time_stamp():
    """
    获取下周六 下周一的零点时间
    """
    saturday = (datetime.datetime.today() - datetime.timedelta(days=time.localtime().tm_wday - 5)).strftime("%Y-%m-%d")
    sa_time = int(time.mktime(time.strptime(saturday, "%Y-%m-%d")))
    sunday = (datetime.datetime.today() - datetime.timedelta(days=time.localtime().tm_wday - 7)).strftime("%Y-%m-%d")
    sd_time = int(time.mktime(time.strptime(sunday, "%Y-%m-%d")))
    return sa_time, sd_time


def week_pk_status(user_id, week_id, grade_id):
    """
    首页竞技机会返回状态值
    :return:
    """
    pk_chance = db.tbkt_active.full_score_test.filter(user_id=user_id, type=3, week_id=week_id, grade_id=grade_id)[:]
    if pk_chance and len(pk_chance) >= 2:
        return 0
    return 1


def user_index(user_id):
    """
    正式第一周 rc测试
    """
    # c = config()  # 读取测试环境配置信息， rc环境替换为程序配置
    grade_id = user_grade(user_id)
    out = Struct()
    out.know_status = -1     # 知识训练场
    out.wrong_status = -1    # 高频错题
    out.pk_status = -1       # 每周竞技
    out.month_status = -1    # 每月竞技
    out.is_open = 0          # 是否在开放日期里
    out.once_open = 1        # 往期回顾是否开放
    out.once_week = []
    out.id = 0
    week_day = datetime.date.today().weekday()
    week_info = db.tbkt_active.full_score_week_list.select("id", "name", "begin_time", "end_time").order_by(
        "begin_time")
    b_time, e_time = time_stamp()
    for i in week_info:
        if b_time <= i.begin_time < e_time:
            # 如果开始在本周之内，则算是本周课程
            out.name = i.name
            out.id = i.id
            i.open_time = i.begin_time + 9 * 3600
            out.open_time = time.strftime("%m月%d日 %H点", time.localtime(i.open_time))
            out.chance_over = pk_num(user_id, i.id).have_chance
            if week_day in (5, 6):
                # 在开课天里，返回状态关闭往期回顾
                out.once_open = 1
            if int(time.time()) >= i.open_time:
                # 达到开课时间点
                out.is_open = 1
                out.once_open = 0
                out.know_status, out.wrong_status, out.pk_status = user_knowledge_info(user_id, i.id, grade_id)
                if out.pk_status == 1 and out.chance_over > 0:
                    out.pk_status = 0
        if i.begin_time < b_time:
            # 如果开始时间小于本周开始时间，则算是往期课程
            out.once_week.append(
                dict(
                    id=i.id,
                    name=i.name
                )
            )
        out.once_week = sorted(out.once_week, key=lambda x: (-x["id"]))
    return out


def once_week_wrong(user_id, week_id):
    """
    往期回顾用户错题记录完成状态
    :return:
    """
    test = db.tbkt_active.full_score_test.get(user_id=user_id, week_id=week_id, type=4, status=1,
                                              grade_id=user_grade(user_id))
    if test:
        return 0
    return 1


def user_knowledge_info(user_id, week_id, grade_id):
    """
    周六周日根据用户做题状态 判断任务开放状态
    :param user_id:
    :param week_id:
    :param grade_id:用户设置教材年级
    :return:
    """
    know_status = 0  # 知识训练场
    _wrong_status = -1  # 高频错题
    pk_status = -1  # 每周竞技
    test_type = db.tbkt_active.full_score_test.select("type").filter(
        week_id=week_id, user_id=user_id, status=1, grade_id=grade_id).group_by("type").flat("type")[:]

    if not test_type:
        # 如果用户未做过，则返回默认值
        return know_status, _wrong_status, pk_status

    # (1,2) (1,2,4) (1,2,3,4)
    status = tuple(test_type)

    temp = {
        (1, 2): (1, 0, -1),
        (1, 2, 4): (1, 1, 0),
        (1, 2, 3, 4): (1, 1, 1),
        (1, 2, 3): (1, 0, -1)
    }
    # 根据三种情况 获取开启状态
    return temp.get(status, (0, -1, -1))


def user_grade(user_id):
    """
    查询用户设置教材年级
    :return:
    """
    book = db.tbkt_active.full_score_book_set.get(user_id=user_id)
    if not book:
        # 如果用户没有设置年级，则默认保存为一年级
        region = db.ketang.mobile_order_region.select("unit_class_id").get(user_id=user_id)
        grade_id = 1
        if region:
            unit = db.default.school_unit_class.get(id=region.unit_class_id)
            grade_id = unit.grade_id if unit.grade_id > 0 else 1
        set_user_book(user_id, grade_id)
        return grade_id
    return book.grade_id


def pk_submit(user_id, week_id, info, score, user_city):
    """
    每周竞技提交
    :param user_id: 用户id
    :param week_id: 课程id
    :param info:    提交数据
    :param score:   成绩
    :param user_city: 用户城市id
    :return:
    """
    grade_id = user_grade(user_id)
    have_chance = pk_num(user_id, week_id).have_chance
    if have_chance <= 0:
        return {}
    score = score if score > 0 else 0
    nowt = int(time.time())
    pk_info = db.tbkt_active.full_score_test.get(type=3, user_id=user_id, week_id=week_id, grade_id=grade_id,status=1)
    out = Struct()
    out.pk_status = 1 if score else 0
    out.score = score
    if pk_info and pk_info.score >= score:
        out.max_score = pk_info.score
        out.pk_status = 0
    else:
        out.max_score = score

    with db.tbkt_active as active:
        active.full_score_test.create(
            user_id=user_id,
            grade_id=user_grade(user_id),
            week_id=week_id,
            type=3,
            city=user_city,
            text=json.dumps(info),
            status=1,
            score=score,
            add_time=nowt
        )
    out.rank = pk_result(user_id, week_id, user_city)   # 结果页数据返回排行
    out.num = pk_num(user_id, week_id).have_chance      # 用户剩余pk次数
    return out


def user_pk_index(user_id, week_id, grade_id, user_city):
    """
    获取用户分数下标 取前后排名用户
    :param user_id:
    :param week_id:
    :param user_city:
    :param grade_id:
    :return:
    """
    data = Struct()
    data.score = 0
    # 获取用户周竞技提交分数 判断所有分数是否在同一地市
    submit_score = db.tbkt_active.full_score_test.select("user_id", "city").filter(
        week_id=week_id, type=3, status=1, user_id=user_id, grade_id=grade_id)[:]

    if not submit_score:
        return []
    for i in submit_score:
        if i.city != user_city:
            db.tbkt_active.full_score_test.filter(
                user_id=user_id, week_id=week_id, grade_id=grade_id, type=3).update(city=user_city)

    score = db.tbkt_active.full_score_test.select("user_id", "score", "city").filter(
        week_id=week_id, type=3, status=1, grade_id=grade_id, city=user_city).order_by('-score', "id")[:]
    temp = []
    user_rank = []
    for s in score:
        if s.user_id in temp:
            continue
        else:
            user_rank.append(s)
            temp.append(s.user_id)
    for i, k in enumerate(user_rank):
        if k.user_id == user_id:
            user_index_info = i
            user_info = k
            return user_index_info, user_info


def pk_result(user_id, week_id, user_city):
    """
    获取用户前后排名信息
    :param user_id:
    :param week_id:
    :param user_city:
    :return:
    """
    grade_id = user_grade(user_id)
    index = user_pk_index(user_id, week_id, grade_id, user_city)
    # return index[0]
    pk_index = []
    if index:
        self_index = index[0]
        if self_index == 0:
            pk_index = [self_index, self_index + 1]
        if self_index > 0:
            pk_index = [self_index - 1, self_index, self_index +1]

    if not pk_index:
        return []
    submit_score = db.tbkt_active.full_score_test.select("user_id", "score").filter(
        week_id=week_id, type=3, status=1, city=user_city, grade_id=grade_id).order_by('-score', 'id')

    temp = []
    user_rank = []
    for i in submit_score:
        if i.user_id in temp:
            continue
        else:
            user_rank.append(i)
            temp.append(i.user_id)
    rank_map = {}
    for i, k in enumerate(user_rank):
        if i in pk_index:
            k.index = i
            k.rank = i + 1
            k.is_self = 0
            if k.user_id == user_id:
                k.is_self = 1
            rank_map[i] = k

    ranks = []
    for i in pk_index:
        rank_info = rank_map.get(i, {})
        if not rank_info:
            continue
        ranks.append(rank_info)
    if not ranks:
        return []
    user_ids = [i.user_id for i in ranks]
    user = users_info(user_ids)
    user_map = {i["user_id"]: i for i in user}

    for r in ranks:
        if not r:
            continue
        info = user_map.get(r["user_id"])
        if not info:
            continue
        r.portrait = info["portrait"]
        r.border_url = info["border_url"]
        r.real_name = info["real_name"]
    return ranks


def users_info(user_ids):
    """
    获取用户姓名头像边框
    :param user_ids:批量获取用户信息id
    :return:
    """
    sql = """ 
        select a.id, a.real_name, p.portrait from auth_user a, auth_profile p
        where a.id = p.user_id and user_id in (%s)
        """ % join(user_ids)
    user_info = db.tbkt_user.fetchall_dict(sql)
    user_map = {i.id: i for i in user_info}
    user_ids = [i.id for i in user_info]
    school_info = db.ketang.mobile_order_region.select(
        'school_name', 'user_id', 'unit_class_id unit_id').filter(user_id__in=user_ids).group_by('user_id')[:]
    school_map = {i.user_id: i for i in school_info}
    unit_ids = [i.unit_id for i in school_info]
    unit_names = db.default.school_unit_class.filter(id__in=unit_ids).select("unit_name", "id")[:]
    unit_map = {i.id: i.unit_name for i in unit_names}
    user_borders = db.default.user_border_detail.filter(user_id__in=user_ids, status=1)[:]
    border_map = {i.user_id: i.border_id for i in user_borders}
    users = []
    for i in user_info:
        user = user_map.get(i.id)
        region = school_map.get(i.id, Struct())
        border_id = border_map.get(i.id, 0)
        border_url = ""
        if border_id != 0:
            border_info = db.default.border.get(id=border_id)
            if border_info:
                border_url = border_info.border_url
        if not region:
            continue
        users.append(dict(
            user_id=i["id"],
            real_name=user.real_name,
            portrait=math_com.get_portrait(user.portrait, 1),
            school_name=region.school_name,
            unit_name=unit_map.get(region.unit_id),
            border_url=get_absurl(border_url)
        ))
    return users


def users_info_temp(user_ids):
    """
    获取用户姓名头像边框
    :param user_ids:批量获取用户信息id
    :return:
    """
    sql = """ 
        select a.id, a.real_name, p.portrait from auth_user a, auth_profile p
        where a.id = p.user_id and user_id in (%s)
        """ % join(user_ids)
    user_info = db.tbkt_user.fetchall_dict(sql)
    user_map = {i.id: i for i in user_info}
    user_ids = [i.id for i in user_info]
    school_info = db.ketang.mobile_order_region.select(
        'school_name', 'user_id', 'unit_class_id unit_id').filter(user_id__in=user_ids).group_by('user_id')[:]
    school_map = {i.user_id: i for i in school_info}
    unit_ids = [i.unit_id for i in school_info]
    unit_names = db.default.school_unit_class.filter(id__in=unit_ids).select("unit_name", "id")[:]
    unit_map = {i.id: i.unit_name for i in unit_names}
    user_borders = db.default.user_border_detail.filter(user_id__in=user_ids, status=1)[:]
    border_map = {i.user_id: i.border_id for i in user_borders}
    users = []
    for i in user_info:
        user = user_map.get(i.id)
        region = school_map.get(i.id, Struct())
        border_id = border_map.get(i.id, 0)
        border_url = ""
        if border_id != 0:
            border_info = db.default.border.get(id=border_id)
            if border_info:
                border_url = border_info.border_url
        if not region:
            continue
        users.append(dict(
            user_id=i["id"],
            real_name=user.real_name,
            portrait=math_com.get_portrait(user.portrait, 1),
            school_name=region.school_name,
            unit_name=unit_map.get(region.unit_id),
            border_url=get_absurl(border_url)
        ))
    out = {i["user_id"]: i for i in users}
    return out


def pk_num(user_id, week_id):
    """
    竞技用户第几回合 剩余机会
    :param user_id:
    :param week_id:
    :return:
    """
    data = Struct()
    test_num = db.tbkt_active.full_score_test.select("score", "week_id", "text") \
        .filter(user_id=user_id, week_id=week_id, type=3, status=1, grade_id=user_grade(user_id)).count()
    data.num = test_num + 1
    data.have_chance = 2 - test_num
    if data.have_chance <= 0:
        data.have_chance = 0
    return data


def get_pk_question(user_id, week_id):
    """
    获取周竞技题目信息
    :param user_id:
    :param week_id:
    :return:
    """
    grade_id = user_grade(user_id)
    info = db.tbkt_active.full_score_week_detail.get(week_id=week_id, grade_id=grade_id)
    if not info:
        return
    pk_qid = info.week_qid.split(',')
    data = Struct()
    out = get_question_info(pk_qid)
    data.out = out
    data.num = pk_num(user_id, week_id).num
    pk_score = db.tbkt_active.full_score_test.select("score", "week_id", "text", "use_time") \
        .filter(user_id=user_id, week_id=week_id, type=3, grade_id=grade_id, status=0).last()
    if not pk_score:
        return data
    out_map = map(Struct, json.loads(pk_score.text))
    # data.q_info = out_map
    data.use_time = pk_score.use_time
    if pk_score.use_time == 0:
        data.use_time = 300
    added_aid = [i.aid for i in out_map]
    un_finish = []
    for i in out:
        if i.id in added_aid:
            continue
        un_finish.append(i)
    data.out = un_finish
    return data


def get_question_info(qid):
    """
    获取周竞技题目信息
    :param qid:题目id
    :return:
    """
    qid = map(int, qid)
    questions = db.ziyuan.sx_question.select("id", "subject", "video_url", "type").filter(id__in=qid)[:]
    asks = db.ziyuan.sx_question_ask.select("id", "question_id", "subject").filter(question_id__in=qid)[:]
    ask_ids = [i.id for i in asks]
    options = db.ziyuan.sx_ask_options.select("ask_id", "content").filter(ask_id__in=ask_ids)[:]
    for q in questions:
        q.subject = math_com.parse_subject(q.subject)
        q.video_url = math_com.parse_video(q.video_url)
    question_map = {i.id: i for i in questions}
    options_map = defaultdict(list)
    for o in options:
        options_map[o.ask_id].append(math_com.parse_option(o.content))
    for ask in asks:
        ask.q_subject = question_map.get(ask.question_id)
        ask.subject = math_com.parse_subject(ask.subject)
        ask.option = options_map.get(ask.id)
        try:
            if ask.q_subject.type == 2 and len(ask.option) <= 2:
                ask.option[0]['content'] = u'正确'
                ask.option[1]['content'] = u'错误'
        except:
            pass
    return asks


def rank_user_id(user_id, week_id, user_city):
    """
    获取竞技排名前100的user_id
    :param user_id:
    :param week_id:
    :param user_city:
    :return:
    """
    grade_id = user_grade(user_id)
    city_info = db.tbkt_active.full_score_test.select("city").get(
        user_id=user_id, type=3, status=1, week_id=week_id, grade_id=grade_id)
    if city_info and city_info.city != user_city:
        db.tbkt_active.full_score_test.filter(
            user_id=user_id, type=3, grade_id=grade_id, week_id=week_id).update(city=user_city)

    submit_score = db.tbkt_active.full_score_test.select("user_id", "score").filter(
        week_id=week_id, type=3, status=1, grade_id=grade_id, city=user_city).order_by('-score', "id")[:250]
    temp = []
    user_rank = []

    for i in submit_score:
        if i.user_id in temp:
            continue
        else:
            user_rank.append(i)
            temp.append(i.user_id)
        user_rank = user_rank[:100]
    return user_rank


def pk_week_rank(user_id, week_id, user_city):
    """
    1-5 6-7 排行
    :param user_id:
    :param week_id:
    :param user_city:
    :return:
    """
    # 获取当前时间 周一至周五top 周末实时
    data = Struct()
    data.user_rank = []
    data.my_rank = []
    week_day = datetime.date.today().weekday()
    if week_day in (0, 1, 2, 3, 4):
        data = week_rank(user_id, week_id, user_city)
        return data
    if week_day in (5, 6):
        data = get_rank(user_id, week_id, user_city)
    return data


def my_rank_info(user_id, week_id, user_city):
    """
    用户在本周排名 显示在排名结果页
    """
    user_self = pk_result(user_id, week_id, user_city)
    self_rank = []
    if user_self:
        for i in user_self:
            if i.is_self == 1:
                self_rank.append(i)
    rank_info = users_info(user_id)
    if self_rank:
        rank = self_rank[0]
        my_rank = rank_info[0]
        my_rank["score"] = rank.score
        my_rank["rank"] = rank.rank
    else:
        my_rank = rank_info[0]
        my_rank["score"] = 0
        my_rank["rank"] = ""

    return my_rank


def week_rank(user_id, week_id, user_city):
    """
    周日排行 竞技排行1-5数据库读取
    :param user_id:
    :param week_id:
    :param user_city:
    :return:
    """
    data = Struct()
    data.user_rank = []
    data.my_rank = []
    grade_id = user_grade(user_id)
    ranks = db.tbkt_active.full_score_top.get(city=user_city, week_id=week_id, grade_id=grade_id)
    if not ranks:
        return get_rank(user_id, week_id, user_city)
    user_rank = json.loads(ranks.user_ids)
    user_ids = []
    # python 2.7 字典是无序的  3.+ 版本优化
    ranks = ranks.user_ids.replace('{', '').replace('}', '').split(",")
    for i in ranks:
        temp = i.replace('"', '').split(":")
        user_ids.append(int(temp[0]))
    user_map = users_info_temp(user_ids)
    info = []
    for i, k in enumerate(user_ids):
        user = user_map.get(k)
        if not user:
            i -= 1
            continue
        user["rank"] = i + 1
        user["score"] = user_rank.get(str(k), "")
        info.append(user)
    data.user_rank = info
    data.my_rank = my_rank_info(user_id, week_id, user_city)
    # 获取用户当前周的city 和往期回顾的city 如果city不统一 不显示用户当前地市自己的排名
    once_info = db.tbkt_active.full_score_test.get(week_id=week_id, user_id=user_id, type=1, grade_id=grade_id)
    if not once_info:
        data.my_rank = my_rank_info(user_id, week_id, user_city)
    else:
        once_city = once_info.city
        if once_city == "":
            db.tbkt_active.full_score_test.filter(week_id=week_id, user_id=user_id, type=3).update(city=once_city)
        if int(once_city) != int(user_city):
            db.tbkt_active.full_score_test.filter(week_id=week_id, user_id=user_id, type=3).update(city=once_city)
            rank_info = users_info(user_id)
            my_rank = rank_info[0]
            my_rank["score"] = 0
            my_rank["rank"] = ""
            data.my_rank = my_rank
        else:
            data.my_rank = my_rank_info(user_id, week_id, user_city)
    return data


def get_rank(user_id, week_id, user_city):
    """
    周末排行
    :return:
    """
    data = Struct()
    data.user_rank = []
    data.my_rank = []
    # 取出地市所有用户排名
    user_rank = rank_user_id(user_id, week_id, user_city)
    if not user_rank:
        return data
    for i, v in enumerate(user_rank):
        v.rank = i + 1

    user_ids = [i.user_id for i in user_rank]
    user = users_info(user_ids)
    user_map = {i["user_id"]: i for i in user}
    for i in user_rank:
        info = user_map.get(i.user_id)
        i.portrait = info["portrait"]
        i.school_name = info["school_name"]
        i.unit_name = info["unit_name"]
        i.border_url = info["border_url"]
        i.real_name = info["real_name"]
        if i.user_id == user_id:
            data.my_rank = i
    data.user_rank = user_rank
    if not data.my_rank:
        data.my_rank = my_rank_info(user_id, week_id, user_city)
    return data


def pop_up(user, pop_type, user_city):
    """
    获取是否弹框提示
    每周只弹一次
    :param user:
    :param pop_type:
    :return: 
    """
    info = Struct()
    info.status = 0
    unit = user.unit
    if not unit or unit.grade_id > 6:
        return info
    key = (user.id, pop_type, get_weekend_stamp())
    data = cache.hd_full_pop_up.get(key)
    if not data:
        cache.hd_full_pop_up.set(key, '1')
        if pop_type == "home":
            data = pk_pop(user.id, user_city)
            return data
        if pop_type == "click":
            user_grade(user.id)
        info.status = 1
    if pop_type == "info":
        key = (user.id, "click", get_weekend_stamp())
        data = cache.hd_full_pop_up.get(key)
        if not data:
            info.status = 1
    return info


def week_pk_border():
    """
    满分课堂周竞技边框 有效期7天 七天过后 批量收回
    """

    week_day = datetime.date.today().weekday()
    return week_day


def pk_pop(user_id, user_city):
    """
    用户pk弹框
    :param user_id:
    :param user_city:
    :return:
    """
    # 本周一的时间戳
    with db.default as dd:
        data = Struct()
        data.status = 0
        data.border_url = ""
        data.border_id = 0
        # 获取上周前100名的用户id
        b_time, _ = time_stamp()
        week = db.tbkt_active.full_score_week_list.select("id").filter(begin_time__lt=b_time)\
                                                                    .order_by("-begin_time").first()
        if not week:
            return data
        rank_id = rank_user_id(user_id, week.id, user_city)
        if not rank_id:
            return data
        user_ids = [i.user_id for i in rank_id]
        if user_id in user_ids:
            # 获取竞技边框信息
            border = dd.border.get(remark="竞技", status=1)
            if not border:
                return data
            # 竞技边框 id
            border_id = border.id
            # 竞技边框url
            border_url = get_absurl(border.border_url)
            # 保存前100名用户获取竞技头像之前的边框
            user_border = dd.user_border_detail.get(user_id=user_id, status=1)
            if user_border:
                # 如果用户用使用中的边框，则更新上次使用状态改为1
                dd.user_border_detail.filter(id=user_border.id).update(once_border_id=1)
            get_pk_border = dd.user_border_detail.get(user_id=user_id, border_id=border_id)
            if get_pk_border:
                return data
            dd.user_border_detail.create(user_id=user_id, border_id=border_id,
                                         add_time=int(time.time()))
            data.border_url = border_url
            data.border_id = border_id
            data.status = 1
        return data


def get_weekend_stamp():
    """
    获取本周结束时间戳 
    周日23:59:59
    :return: 
    """
    interval = 6 - time.localtime().tm_wday
    today = datetime.datetime.today()
    start = datetime.datetime(year=today.year,
                              month=today.month,
                              day=today.day,
                              hour=0, minute=0,
                              second=0)
    start += datetime.timedelta(days=interval, hours=23, minutes=59, seconds=59)
    return int(time.mktime(start.timetuple()))


def get_list():
    """
    获取教材列表
    :return: 
    """
    grade = range(1, 7)
    out = []
    for i in grade:
        d = dict(
            id=i,
            name=u'数学-人教版%s年级下册' % num_to_ch(i)
        )
        out.append(d)
    return out


def set_user_book(user_id, grade_id):
    """
    设置教材
    :param user_id: 
    :param grade_id: 
    :return: 
    """
    with db.tbkt_active as active:
        book = active.full_score_book_set.get(user_id=user_id)
        if not book:
            active.full_score_book_set.create(
                user_id=user_id,
                grade_id=grade_id,
                add_time=int(time.time())
            )
        else:
            active.full_score_book_set.filter(id=book.id).update(grade_id=grade_id)


def wrong_status(user_id, week_id):
    """
    高频错题状态
    :param user_id:
    :param week_id: 
    :return: 
    """
    grade_id = user_grade(user_id)
    test = db.tbkt_active.full_score_test.get(user_id=user_id, grade_id=grade_id, type=4, week_id=week_id, status=1)
    return 1 if test else 0


def need_login(f):
    """
    满分课堂 接口权限验证
    """

    def wrap(request, *args, **kw):
        user = request.user
        if not user:
            return ajax.jsonp_fail(request, error='no_user', message="请您先登录")
        elif user.grade_id > 6:
            return ajax.jsonp_fail(request, error='no authority', message="请使用小学学生账号登录")
        elif user.type != 1:
            return ajax.jsonp_fail(request, error='no authority', message="请使用小学学生账号登录")
        else:
            return f(request, *args, **kw)

    return wrap


def get_user_book_name(user):
    """
    获取用户教材
    :param user: 
    :return: 
    """
    grade_id = user.grade_id
    book = db.tbkt_active.full_score_book_set.get(user_id=user.id)
    if book:
        grade_id = book.grade_id
    if grade_id <= 0:
        grade_id = 1
    return u'数学-人教版%s年级下册' % num_to_ch(grade_id)
