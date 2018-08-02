# coding: utf-8
import time
from collections import defaultdict

from apps.terminal2018.subject.chinese import yw_paper_list
from libs.utils import db, num_to_ch, thread_pool, join
from libs.utils.common import Struct
from com.com_cache import cache
from ..terminal2018.subject import english


def get_gradelist(subject_id, type, grade_id, book_id=0):
    """
    选年级教材列表
    :param subject_id: 学科ID
    :param type: 1教材 2教辅
    :param grade_id: 年级ID
    :param book_id: 设置教材要对应年级
    :return: [{id:BOOKID, name:书名, press_name:出版社, version:版本, volume:上下册}]
    """
    if type == 1:
        order_by = "order by press_name,p.id, volume"
    else:
        order_by = "order by name,press_name, volume"
    book_related = ''
    if type == 2 and subject_id in (21, 22) and book_id:
        book_related = 'and b.book_id =%s and b.volume = 2 ' % book_id
    if subject_id == 21:
        version_str = 'and p.id in (2,8,4) and b.volume = 2 '
    elif subject_id == 91:
        if grade_id < 3:
            return
        version_str = 'and p.id in (2,23,35) and v.id in (63,73,79) and b.volume = 2 '
    else:
        version_str = ' and b.volume = 2 '
    # and p.id in (2,29,4,8,15) 代表教材属于人教 北师大 苏教  苏教新版   人教灵通
    sql = """
    select b.id, b.name, b.subject_id, b.grade_id, p.name press_name, p.id press_id, 
        v.name version_name, b.volume, b.book_type
    from zy_book b
    inner join zy_press p on p.id=b.press_id
    inner join zy_press_version v on v.id=b.version_id
    where b.subject_id=%s  and b.book_type=%s and b.is_active=1 %s %s
    %s
    """ % (subject_id,  type, book_related, version_str, order_by)
    books = db.ziyuan_slave.fetchall_dict(sql)
    for b in books:
        b.volume_name = {1: u'上册', 2: u'下册', 3: u'全册'}.get(b.volume, u'')
        b.grade_name = num_to_ch(b.grade_id) + u'年级'
        if b.book_type == 1:
            b.name = b.grade_name + b.volume_name
    return books


def set_subject_info(user_id, subject_id):
    """
    用户未设置活动教材之前的教材信息
    :return:
    """
    _book = db.default.user_book.select('book_id').get(user_id=user_id, is_work_book=0, subject_id=subject_id)
    if not _book:
        return
    if subject_id == 21:
        sql = """
        select p.id
        from zy_book b left join zy_press p on b.press_id = p.id
        where b.id = %s;
        """ % _book.book_id
        result = db.ziyuan_slave.fetchone_dict(sql)
        if result and result["id"]:
            # 期末活动教材设置--人教版 苏教版 北师大版的教材id
            if result["id"] in(2, 4, 8):
                return result
    if subject_id == 91:
        sql = """
        select p.id
        from zy_book b left join zy_press p on b.press_id = p.id
        where b.id = %s and b.grade_id > 2;
        """ % _book.book_id
        result = db.ziyuan_slave.fetchone_dict(sql)
        if result and result["id"]:
            if result["id"] in(2, 23, 35):
                return result
    return


def p_user_book(user_id, subject_id):
    """
    用户的教材信息
    :param user_id:
    :param subject_id:
    :return:
    """
    # 返回用户教材信息  没有设置教材
    book = db.tbkt_active.mid_term_user_book.select('book_id').get(user_id=user_id, is_work_book=0,
                                                                   subject_id=subject_id)
    if book:
        book_id = book.book_id
    if not book:
        # 如果用户未设置教材
        _book = db.default.user_book.select('book_id').get(user_id=user_id, is_work_book=0, subject_id=subject_id)
        result = set_subject_info(user_id, subject_id)
        if result:
            db.tbkt_active.mid_term_user_book.create(
                book_id=_book.book_id,
                subject_id=subject_id,
                user_id=user_id,
                add_time=int(time.time()),
                is_work_book=0
            )
            book_id = _book.book_id
        else:
            return
    sql = '''
    select b.id,b.name, p.name name1, b.grade_id
    from zy_book b left join zy_press p on b.press_id = p.id
    where b.id = %s;
    ''' % book_id
    result = db.ziyuan_slave.fetchone_dict(sql)
    data = Struct()
    name = result.name.encode('utf-8') + '(' + result.name1.encode('utf-8') + ')'
    data.name = name
    data.id = result.id
    data.grade_id = result.grade_id
    return data


def p_yw_user_book(user_id):
    """
    获取语文教材信息
    :param user_id:  
    :return: 
    """
    # 获取用户设置的期末活动教材
    book = db.tbkt_active.mid_term_user_book.select('book_id').get(user_id=user_id, is_work_book=0,
                                                                   subject_id=51)
    if book:
        book_id = book.book_id
    else:
        # 获取用户设置教材
        _book = db.default.user_book.select('book_id').get(user_id=user_id, is_work_book=0, subject_id=51)
        if not _book:
            return {}
        data = db.tbkt_yw.yw_chinesetextbooks.select("ct_ID").filter(
            ct_VersionNum__in=("JC001001", "JC001008"), ct_status=0, enable_flag=0).flat("ct_ID")[:]
        if _book.book_id in data:
            # 说明用户设置的是人教版 则直接进行保存
            db.tbkt_active.mid_term_user_book.create(
                book_id=_book.book_id,
                subject_id=51,
                user_id=user_id,
                add_time=int(time.time()),
                is_work_book=0
            )
            book_id = _book.book_id
        else:
            return {}
    sql = """
    SELECT b.dict_Name name,a.ct_SeesawVolumes volumes,a.ct_Grade grade  from yw_chinesetextbooks a 
    INNER JOIN yw_dictionary b ON  b.dict_Code = a.ct_VersionNum
    where a.ct_ID = %s AND a.ct_Status = 0 AND a.enable_flag = 0;
    """ % book_id
    info = db.tbkt_yw_slave.fetchone_dict(sql)
    if not info:
        return {}

    out = Struct()
    out.id = book_id
    grade = num_to_ch(info.grade.replace("NJ00100", "")) + u'年级'
    volume = {1: u'上册', 2: u'下册', 3: u'全册'}.get(info.volumes, u'')
    out.name = u"人教版" + grade + volume
    out.grade_id = info.grade[-1]
    return out


def p_booklist(subject_id, type, grade_id, book_id=0):
    """
    :param subject_id: 学科
    :param type:1教材 2教辅
    :param grade_id:年级ID
    :param book_id:设置教材要对应年级
    :return:[{id:BOOKID, name:书名, press_name:出版社, version:版本, volume:上下册}]
    """
    # 数学英语列表返回
    if subject_id in (21, 91):
        book_all = get_gradelist(subject_id, type, grade_id, book_id)
        books = []
        for b in book_all:
            if str(b.grade_id) in grade_id:
                books.append(b)
        return books
    # 资源不统一 语文单独查询
    if subject_id == 51:
        sql = """
        select b.dict_Name,a.ct_SeesawVolumes,a.ct_ID,a.ct_Grade,b.dict_ID  from yw_chinesetextbooks a 
        inner join yw_dictionary b ON  b.dict_Code = a.ct_VersionNum where b.dict_ID = 2 
        and a.ct_SeesawVolumes = 2
        and a.ct_Status = 0 AND a.enable_flag = 0 or a.ct_ID = 65;
        """
        # 查询本次活动指定教材信息
        book_info = db.tbkt_yw_slave.fetchall_dict(sql)
        books = []
        for b in book_info:
            if b.ct_Grade[-1] in grade_id:
                books.append(b)
        if not books:
            return
        for i in books:
            i.press_id = i.dict_ID  # 出版社id
            i.volume_name = {1: u'上册', 2: u'下册', 3: u'全册'}.get(i.ct_SeesawVolumes, u'') # 上下册
            i.press_name = u"人教版"  # 出版社名称
            i.subject_id = 51
            i.grade_id = int(i.ct_Grade[-1])
            i.grade_name = num_to_ch(i.grade_id) + u"年级"
            i.name = i.grade_name + i.volume_name
            i.id = i.ct_ID
            i.book_type = 1
            del i.dict_Name
            del i.ct_SeesawVolumes
            del i.ct_ID
            del i.ct_Grade
            del i.dict_ID
        return books


def time_stamp():
    """
    获取当天结束时间戳
    :return:
    """
    t = time.localtime(time.time())
    time_begin = int(time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t), '%Y-%m-%d %H:%M:%S')))
    return time_begin


def send_class_info(user_id):
    """
    用户所有班级 并且班级有学生
    :return:
    """
    units = []
    info = db.ketang.mobile_order_region.filter(user_id=user_id)[:]
    for i in info:
        unit = db.ketang.mobile_order_region.filter(unit_class_id=i["unit_class_id"], user_type=1)[:]
        if unit:
            units.append(i["unit_class_id"])
    return len(units)


yy_paper = [(183, 184, 185), (186, 187, 188), (189, 190, 191), (192, 193, 194)]
sx_paper = [
    (20968, 20967, 20966), (21023, 21022, 21021), (21028, 21027, 21026), (21033, 21032, 21031),
    (21038, 21037, 21036), (21085, 21084, 21083),
    (20963, 20962, 20961), (20973, 20972, 20971), (20987, 20986, 20985), (20992, 20991, 20990),
    (20997, 20996, 20995), (21017, 21016, 21015),
    (21058, 21057, 21056), (21110, 21109, 21108), (21100, 21099, 21098), (21090, 21089, 21088),
    (21133, 21132, 21131), (21075, 21074, 21073)
]
yw_paper = [(101, 102, 103), (156, 157, 158), (106, 107, 108), (111, 112, 113), (116, 117, 118), (121, 122, 123)]


def recurrence(source, sent, start=0):
    done = []
    for p in sent:
        for b in source[start]:
            if p == b:
                print p, start
                done.append(p)
        if len(done) >= 3:
            return done
    else:
        start += 1
        if start >= len(source):
            return []
        return recurrence(source, sent, start)


def p_del_pop_up(user_id):
    """
    :param user_id: 
    :return: 
    """
    key = (user_id, time_stamp())
    pop_up = cache.hd_terminal_pop.delete(key)


def p_pop_up(user):
    """
    控制用户教材弹窗
    :return:
    """
    # 获取当天的零点时间 加缓存
    key = (user.id, time_stamp())
    pop_up = cache.hd_terminal_pop.get(key)
    if not pop_up:
        cache.hd_terminal_pop.set(key, 1)
        book_id = db.tbkt_active.mid_term_user_book.select('book_id', 'subject_id').get(user_id=user.id)
        if not book_id:
            return 1
        else:
            if book_id.subject_id == 91:
                sql = """
                select t.object_id, count(distinct c.unit_class_id) num from yy_task t, yy_task_class c
                where t.add_user = %s and t.type = 103 and t.id = c.task_id and c.unit_class_id in (%s) group by t.object_id
                """ % (user.id, ",".join(str(i.id) for i in user.units))
                data = db.tbkt_yingyu.fetchall_dict(sql)
                sent_map = {i.object_id: i.num for i in data}
                done_sent = recurrence(yy_paper, sent_map.keys())
                if not done_sent and len(done_sent) < 3:
                    return 1
                for i in done_sent:
                    sent_num = sent_map.get(i)
                    if not sent_num or sent_num < len(user.units):
                        return 1

            elif book_id.subject_id == 21:
                sql = """
                select t.object_id, count(distinct c.unit_class_id) num from sx_task t, sx_task_class c
                where t.add_user = %s and t.type = 103 and t.id = c.task_id and c.unit_class_id in (%s) group by t.object_id
                """ % (user.id, ",".join(str(i.id) for i in user.units))
                data = db.tbkt_shuxue.fetchall_dict(sql)
                sent_map = {i.object_id: i.num for i in data}
                done_sent = recurrence(sx_paper, sent_map.keys())
                if not done_sent and len(done_sent) < 3:
                    return 1
                for i in done_sent:
                    sent_num = sent_map.get(i)
                    if not sent_num or sent_num < len(user.units):
                        return 1
            elif book_id.subject_id == 51:
                sql = """
                select t.object_id, count(distinct c.unit_class_id) num from yw_task_new t, yw_task_class_new c
                where t.add_user = %s and t.type = 103 and t.id = c.task_id and c.unit_class_id in (%s) group by t.object_id
                """ % (user.id, ",".join(str(i.id) for i in user.units))
                data = db.tbkt_yuwen.fetchall_dict(sql)
                sent_map = {i.object_id: i.num for i in data}
                done_sent = recurrence(yw_paper, sent_map.keys())
                if not done_sent and len(done_sent) < 3:
                    return 1
                for i in done_sent:
                    sent_num = sent_map.get(i)
                    if not sent_num or sent_num < len(user.units):
                        return 1
            return 0
    else:
        return 0


def setbook(user, book_id):
    """
    设置用户教材
    :param book_id: 教材/教辅ID
    :param user: 用户对象
    """
    if user.subject_id == 51:
        data = db.tbkt_yw.yw_chinesetextbooks.get(ct_ID=book_id)
        if not data:
            return
        ubook = db.tbkt_active.mid_term_user_book.select('id').get(user_id=user.id, subject_id=51, is_work_book=0)
        if ubook:
            db.tbkt_active.mid_term_user_book.filter(id=ubook.id).update(book_id=book_id)
        else:
            db.tbkt_active.mid_term_user_book.create(
                book_id=book_id,
                subject_id=51,
                user_id=user.id,
                add_time=int(time.time()),
                is_work_book=0,
            )
    else:
        thread_pool.call(_set_book, user.id, book_id)


def _set_book(user_id, book_id):
    """
    用户设置教材
    :param user_id:
    :param book_id: 设置教材id
    :return:
    """
    # 查询教材信息
    book = db.ziyuan_slave.zy_book.select('id', 'book_type', 'subject_id').get(id=book_id)
    if not book:
        return
    is_work_book = 1 if book.book_type == 2 else 0
    # 查询本次活动用户是否已经设置过教材 -- 是否需要新建用户设置活动教材
    ubook = db.tbkt_active.mid_term_user_book.select('id').get(user_id=user_id, subject_id=book.subject_id, is_work_book=0)
    if ubook:
        db.tbkt_active.mid_term_user_book.filter(id=ubook.id).update(book_id=book_id)
    else:
        db.tbkt_active.mid_term_user_book.create(
            book_id=book_id,
            subject_id=book.subject_id,
            user_id=user_id,
            add_time=int(time.time()),
            is_work_book=is_work_book,
        )


def get_grade_cn(grade_id):
    """
    返回年级中文名
    :param grade_id:
    :return:
    """
    g_map = {i: u'%s年级%%%%' % num_to_ch(i) for i in range(1, 10)}
    return g_map.get(grade_id)


def get_press(press_id):
    """
    返回出版中文名
    :param press_id:
    :return:
    """
    press_map = {2: 329, 4: 330, 8: 331}
    return press_map.get(press_id)


def p_paper_list(user, subject_id):
    """
    返回科目的试卷列表
    :param user:
    :param subject_id:
    :return:
    """
    # 资源不统一 需要对三科进行单独判断
    data = Struct
    if subject_id == 21:
        data = sx_paper_list(user, subject_id)
    if subject_id == 91:
        data = yy_paper_list(user, subject_id)
    if subject_id == 51:
        data = yw_paper_list(user, subject_id)
    return data


def yy_paper_list(user, subject_id):
    """
    英语试卷列表
    :param user:
    :param subject_id:
    :return:
    """
    user_id = user.id
    nowt = int(time.time())
    # 用户是否设置活动教材 当前使用教材是否是指定教材
    mid_book = db.tbkt_active.mid_term_user_book.select('book_id').get(user_id=user_id, subject_id=subject_id)
    if not mid_book:
        book = db.default.user_book.select('book_id').get(user_id=user_id, subject_id=91)
        # 指定教材下的book_id -- 人教版三起点 外研版3起点 湘鲁版三起点
        if book.book_id in (44, 300, 641, 642, 126, 305, 647, 648, 177, 322, 998, 999):
            db.tbkt_active.mid_term_user_book.create(
                user_id=user_id,
                book_id=book.book_id,
                subject_id=91,
                add_time=nowt,
                is_work_book=0,
            )
        else:
            return
    else:
        book = mid_book
    data = {}
    papers = []
    try:
        if book and book.book_id in english.BOOK_PAPER.keys():
            paper_list = english.BOOK_PAPER[book.book_id]
            # 用户是否布置过当前活动试卷
            sql = '''
            select DISTINCT yt.object_id paper_id, ytc.unit_class_id unit_id
            from yy_task yt inner join yy_task_class ytc on yt.id = ytc.task_id
            where ytc.status > 0 and yt.add_user = %s and yt.type = 103 and ytc.unit_class_id in (%s)
            ''' % (user.id,  ",".join(str(i.id) for i in user.units))
            pub_papers = db.tbkt_yingyu.fetchall_dict(sql)
            paper_map = defaultdict(list)
            for i in pub_papers:
                paper_map[i.paper_id].append(i.unit_id)

            units = map(Struct, user.units) if user.units else []

            # 用户使用出版社 查询教材
            for paper in paper_list:
                row = Struct()
                done_unit = len(paper_map.get(paper, []))
                row.id = paper
                row.status = 1 if done_unit >= len(units) else 0
                row.name = english.PAPER[paper]
                papers.append(row)
    except Exception as e:
        print e, 'choice_paper'
    data['papers'] = papers
    return data


def sx_paper_list(user, subject_id):
    """
    数学试卷列表
    :return:
    """
    book_info = p_user_book(user.id, subject_id)
    if not book_info:
        return []
    book_id = book_info.id
    book = db.ziyuan_slave.zy_book.get(id=book_id)
    grade_name = get_grade_cn(book.grade_id)
    press_id = get_press(book.press_id)
    # ziyuan_new 表 中 tbkt_a_active_catalog 活动教材信息
    active_id = 50
    sql = """
    select t.id from
    (select p.id, p.name, c.name grade_name,
    (select c1.id from tbkt_a_active_catalog c1 where c1.id= c.parent_id) press_id
    from sx_paper p, sx_paper_relate r, tbkt_a_active_catalog c
    where p.id = r.paper_id and c.id = r.object_id and c.active_id = %s and r.status = 1) t
    where t.grade_name like '%s' and press_id like '%s'
    """ % (active_id, grade_name, press_id)
    rows = db.ziyuan_slave.fetchall_dict(sql)
    if not rows:
        return []
    # 查询已发试卷
    sql = """
    select yt.object_id paper_id, ytc.unit_class_id unit_id
    from sx_task yt join sx_task_class ytc on yt.id = ytc.task_id
    where ytc.status > 0 and yt.add_user = %s and yt.type = 103 and ytc.unit_class_id in (%s)
    """ % (user.id, ",".join(str(i.id) for i in user.units))
    pub_papers = db.tbkt_shuxue.fetchall_dict(sql)

    paper_map = defaultdict(list)
    for i in pub_papers:
        paper_map[i.paper_id].append(i.unit_id)
    # 查询指定教材下的试卷id
    for i, v in enumerate(rows):
        done_unit = len(paper_map.get(v.id, []))
        v.status = 1 if done_unit >= len(user.units) else 0
        v.name = "期末提分试卷--(%s)" % num_to_ch(i+1)
    return rows


def p_task_class(user, grade_id, paper_ids):
    """
    教师发送作业班级信息和发送状态
    :return:
    """
    units = map(Struct, user.units) if user.units else []
    unit_ids = [i.id for i in units]
    status_map = dict()
    if user.subject_id == 21:
        status_map = sx_paper_unit_status(paper_ids, unit_ids, user.id)
    if user.subject_id == 91:
        status_map = yy_paper_unit_status(paper_ids, unit_ids, user.id)
    if user.subject_id == 51:
        status_map = yw_paper_unit_status(paper_ids, unit_ids, user.id)

    unit_info = []
    for i in units:
        unit_info.append(
            dict(
                status=status_map.get(i.id, 0),
                unit_name=i.name,
                unit_class_id=i.id
            )
        )
    data = Struct()
    data.unit_info = unit_info
    data.grade_id = grade_id
    return data


def r_class_num(unit_id):
    """
    查看班级学生人数 如果班级没有人数 不让发送
    :return:
    """
    unit_num = db.ketang.mobile_order_region.select("id").filter(unit_class_id=unit_id, user_type=1)[:]
    if len(unit_num) > 0:
        return 1
    else:
        return 0


def sx_paper_unit_status(paper_ids, unit_ids, user_id):
    """
    :param paper_ids: 
    :param unit_ids: 
    :param user_id: 
    :return: 
    """
    sql = """
    select s.object_id, c.unit_class_id from sx_task s 
    inner join sx_task_class c on s.id=c.task_id 
    where s.add_user=%s and s.type=103 and c.status>-1 and c.unit_class_id in (%s) 
    and s.object_id in (%s) and s.status>-1
    """ % (user_id, join(unit_ids), join(paper_ids))
    rows = db.tbkt_shuxue.fetchall_dict(sql)
    paper_map = defaultdict(list)
    for i in rows:
        paper_map[i.object_id].append(i.unit_class_id)

    out = {}
    for i in paper_ids:
        send_unit = paper_map.get(i, [])
        unsent = set(send_unit) ^ set(unit_ids)
        for u in unit_ids:
            if not send_unit or u in unsent:
                out[u] = 1
            num = r_class_num(u)
            if num == 0:
                out[u] = -1
    return out


def yy_paper_unit_status(paper_ids, unit_ids, user_id):
    """
    
    :param paper_ids: 
    :param unit_ids: 
    :param user_id: 
    :return: 
    """
    sql = """
    select s.object_id, c.unit_class_id from yy_task s 
    inner join yy_task_class c on s.id=c.task_id 
    where s.add_user=%s and s.type=103 and c.status>-1 and c.unit_class_id in (%s) 
    and s.object_id in (%s) and s.status>-1
    """ % (user_id, join(unit_ids), join(paper_ids))
    rows = db.tbkt_yingyu.fetchall_dict(sql)
    paper_map = defaultdict(list)
    for i in rows:
        paper_map[i.object_id].append(i.unit_class_id)

    out = {}
    for i in paper_ids:
        send_unit = paper_map.get(i, [])
        unsent = set(send_unit) ^ set(unit_ids)
        for u in unit_ids:
            if not send_unit or u in unsent:
                out[u] = 1
            num = r_class_num(u)
            if num == 0:
                out[u] = -1
    return out


def yw_paper_unit_status(paper_ids, unit_ids, user_id):
    """
    :param paper_ids: 
    :param unit_ids: 
    :param user_id: 
    :return: 
    """
    sql = """
    select distinct object_id, c.unit_class_id from yw_task_new t, yw_task_class_new c
    where t.type = 103 and t.add_user = %s and t.id = c.task_id and t.object_id in (%s)
    and c.unit_class_id in (%s) and c.status>-1
    """ % (user_id, join(paper_ids), join(unit_ids))
    rows = db.tbkt_yuwen.fetchall_dict(sql)
    paper_map = defaultdict(list)
    for i in rows:
        paper_map[i.object_id].append(i.unit_class_id)

    out = {}
    for i in paper_ids:
        send_unit = paper_map.get(i, [])
        unsent = set(send_unit) ^ set(unit_ids)
        for u in unit_ids:
            if not send_unit or u in unsent:
                out[u] = 1
            num = r_class_num(u)
            if num == 0:
                out[u] = -1
    return out





