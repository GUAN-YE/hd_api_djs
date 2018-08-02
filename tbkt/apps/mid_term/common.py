# coding: utf-8
import time

from libs.utils import db, num_to_ch, thread_pool, Struct, logging
from com.com_cache import cache
from libs.utils import db, num_to_ch
from apps.sx_summer.common import get_questions


def paper_list(user_id, subject_id):
    """
    活动试卷列表
    :param user_id: 年级_id
    :param subject_id: 二位学科id
    :return:
    """
    if subject_id != 21:
        return

    # 用户已设置的活动教材信息
    book = db.tbkt_active.mid_term_user_book.select('book_id').get(user_id=user_id, is_work_book=0, subject_id=subject_id)
    if not book:
        _book = db.default.user_book.select('book_id').get(user_id=user_id, is_work_book=0, subject_id=subject_id)
        if _book:
            sql = '''
                select p.id
                from zy_book b left join zy_press p on b.press_id = p.id
                where b.id = %s;
            ''' % _book.book_id
            result = db.ziyuan_slave.fetchone_dict(sql)
            if result['id'] in (2,8,4):
                book = Struct()
                book.book_id = _book.book_id
                db.tbkt_active.mid_term_user_book.create(
                    book_id=_book.book_id,
                    subject_id=subject_id,
                    user_id=user_id,
                    add_time=int(time.time()),
                    is_work_book=0
                )
            else:
                return
        else:
            # 这种状况说明了 用于的教材不为人教版 苏教版 北师大  返回为空 跳转到设置教材页面
            return

    book_id = book.book_id
    book = db.ziyuan_slave.zy_book.get(id=book_id)
    # if book.volume != 2: #  选上下册用的
    #     return
    grade_name = get_grade_cn(book.grade_id)
    press_id = get_press(book.press_id)
    active_id = 49
    # 这个SQL可能要改！！！！！！！！！！！！！！！！！！！！
    # 具体去查  ziyuan_new 表 中 tbkt_a_active_catalog 中的active_id字段
    # ！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
    sql = """
    select t.id from
    (select p.id, p.name, c.name grade_name,
    (select c1.id from tbkt_a_active_catalog c1 where c1.id= c.parent_id) press_id
    from sx_paper p, sx_paper_relate r, tbkt_a_active_catalog c
    where p.id = r.paper_id and c.id = r.object_id and c.active_id = %s and r.status = 1) t
    where t.grade_name like '%s' and press_id like '%s'
    """ % (active_id, grade_name, press_id)
    logging.error("%s" % (sql))
    rows = db.ziyuan_slave.fetchall_dict(sql)
    if not rows:
        return

    # 获取试卷id集合
    object_ids = [i.id for i in rows]
    # 查询已发试卷
    sql = '''
          select DISTINCT yt.object_id
          from sx_task yt left join sx_task_class ytc on yt.id = ytc.task_id
          where ytc.status > 0 and yt.add_user = %s and yt.type = 102
    ''' % user_id
    pub_papers = db.tbkt_shuxue.fetchall_dict(sql)
    pub_papers = [paper.object_id for paper in pub_papers]
    # tasks = db.tbkt_shuxue.sx_task.select('id', 'object_id').filter(add_user=user_id, type=102, status__gt=0, object_id__in=object_ids)
    # task_ids = [task.id for task in tasks]
    # task_maps = {task.id:task.paper for task in tasks}
    # send_tasks = db.tbkt_shuxue.sx_task_class.select('task_id', 'status').filter(task_id__in=task_ids)[:]
    # send_tasks = [i.task_id for i in send_tasks if i.status > 0]
    # send_tasks =
    # print send_tasks , rows
    # {试卷id：1}
    # task_map = {i.object_id: 1 for i in send_tasks}
    for i, v in enumerate(rows):
        v.status = 1 if v.id in pub_papers else 0
        v.name = "期中提分试卷（%s）" % (num_to_ch(i+1))
    return rows


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
    press_map = {2: 308, 4: 315, 8: 322}
    return press_map.get(press_id)


def get_gradelist(subject_id, type, grade_id, book_id=0):
    """
    选年级教材列表
    ---------------------
    王晨光     2017-1-4
    ---------------------
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
    where b.subject_id=%s and b.grade_id=%s and b.book_type=%s and b.is_active=1 %s %s
    %s
    """ % (subject_id, grade_id, type, book_related, version_str, order_by)
    print sql
    books = db.ziyuan_slave.fetchall_dict(sql)
    for b in books:
        b.volume_name = {1: u'上册', 2: u'下册', 3: u'全册'}.get(b.volume, u'')
        b.grade_name = num_to_ch(b.grade_id) + u'年级'
        if b.book_type == 1:
            b.name = b.grade_name + b.volume_name
    return books


def get_sources(book_id):
    """
    教材相关练习册列表
    ----------------------
    王晨光     2017-2-15
    ----------------------
    :param book_id: 教材ID
    :return: [{id:练习册ID, name:书名, press_name:出版社, version:版本, volume:上下册}]
    """
    sql = """
    select b.id, b.name, b.subject_id, b.grade_id, p.name press_name, v.name version_name, b.volume
    from zy_book b 
    inner join zy_press p on p.id=b.press_id
    inner join zy_press_version v on v.id=b.version_id
    where b.book_id=%s and b.is_active=1 and b.book_type=2
    order by b.press_id, b.volume, b.sequence
    """ % (book_id)
    return db.ziyuan_slave.fetchall_dict(sql)


def setbook(user_id, book_id):
    """
    设置用户教材
    ---------------------
    王晨光     2017-1-4
    ---------------------
    :param book_id: 教材/教辅ID
    """
    thread_pool.call(_set_book, user_id, book_id)


def _set_book(user_id, book_id):
    book = db.ziyuan_slave.zy_book.select('id', 'book_type', 'subject_id').get(id=book_id)
    if not book:
        return

    is_work_book = 1 if book.book_type == 2 else 0
    ubook = db.tbkt_active.mid_term_user_book.select('id').get(user_id=user_id, subject_id=book.subject_id, is_work_book=is_work_book)
    if ubook:
        db.tbkt_active.mid_term_user_book.filter(id=ubook.id).update(book_id=book_id)
    else:
        db.tbkt_active.mid_term_user_book.create(
            book_id=book_id,
            subject_id=book.subject_id,
            user_id=user_id,
            add_time=int(time.time()),
            is_work_book=is_work_book
        )
    cache.userbook.set((user_id, book.subject_id, is_work_book), book_id)


def getbook(user_id, subject_id):
    # 用户已设置的活动教材信息
    book = db.tbkt_active.mid_term_user_book.select('book_id').get(user_id=user_id, is_work_book=0,
                                                                   subject_id=subject_id)
    if not book:
        _book = db.default.user_book.select('book_id').get(user_id=user_id, is_work_book=0, subject_id=subject_id)
        if _book:
            if subject_id == 21:
                sql = '''
                       select p.id
                       from zy_book b left join zy_press p on b.press_id = p.id
                       where b.id = %s;
                   ''' % _book.book_id
                result = db.ziyuan_slave.fetchone_dict(sql)
            else:
                sql = '''
                       select p.id
                       from zy_book b left join zy_press p on b.press_id = p.id
                       where b.id = %s and b.grade_id > 2;
                                   ''' % _book.book_id
                result = db.ziyuan_slave.fetchone_dict(sql)
            if not result:
                return
            if result['id'] in (2, 29, 4):
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
        else:
            # 这种状况说明了 用于的教材不为人教版 苏教版 北师大  返回为空 跳转到设置教材页面
            return
    else:
        book_id = book.book_id

    sql = '''
           select b.name, p.name name1
           from zy_book b left join zy_press p on b.press_id = p.id
           where b.id = %s;
       ''' % book_id
    result = db.ziyuan_slave.fetchone_dict(sql)
    name = result.name.encode('utf-8') + '(' + result.name1.encode('utf-8') + ')'

    return name


def get_status(user_id):
    book_id = db.tbkt_active.mid_term_user_book.select('book_id', 'subject_id').get(user_id=user_id)
    if not book_id:
        return 1
    else:
        if book_id.subject_id == 91:
            # 走英语
            result = db.tbkt_yingyu_slave.yy_task.select('id').filter(type=102, add_user=user_id)[:]
            if len(result) >= 3:
                return 0
        elif book_id.subject_id == 21:
            # zou shu xue
            result = db.tbkt_shuxue_slave.sx_task.select('id').filter(type=102, add_user=user_id)[:]
            if len(result) >= 3:
                return 0
    return 1


def get_text_content(content, sendscope, grade_id, tea_name, end_time, subject_id):
    date_string = time.localtime(end_time)
    date_string = time.strftime("%Y-%m-%d", date_string)

    # 只给开通的人发  要更新短信文本
    if subject_id == 21:
        if grade_id == 6:
            content = '''家长您好，孩子面临升学，现阶段对数学方法的归纳和总结尤为重要。我精选了部分题目已发到同步课堂，帮助孩子做好复习，请及时督促孩子完成。【%s老师】（截止时间：%s，网站地址：www.tbkt.cn,APP下载:m.tbkt.cn）''' % (tea_name, date_string)
        else:
            content = '''家长您好，期中考试周就要到了。我精选了部分题目用于孩子期中复习，已经发到同步课堂，请及时督促孩子完成，并进行错题订正，期待孩子考出好成绩！【%s老师】（截止时间：%s，网站地址：www.tbkt.cn,APP下载:m.tbkt.cn）''' % (tea_name, date_string)
    elif subject_id == 91:
        if grade_id == 6:
            content = '''家长您好，孩子面临升学，现阶段对要重视对之前知识的回顾和复习。我精选了部分题目已发到同步课堂，帮助孩子做好复习，请及时督促孩子完成。【%s老师】（截止时间：%s，网站地址：www.tbkt.cn,APP下载:m.tbkt.cn）''' % (tea_name, date_string)
        else:
            content = '''家长您好，期中考试周就要到了。我精选了部分题目用于孩子期中复习，已经发到同步课堂，请及时督促孩子完成，并进行错题订正，期待孩子考出好成绩！【%s老师】（截止时间：%s，网站地址：www.tbkt.cn,APP下载:m.tbkt.cn）''' % (tea_name, date_string)
    return content

def get_month(nowt):
    #获取当前月份 int
    return time.localtime(nowt).tm_mon


def get_ticket(user_id):
    nowt = int(time.time())
    now_month = get_month(nowt)

    lottery_detail = db.tbkt_active.excita_lottery_detail.select('id').filter(type=102, user_id=user_id)[:]
    if len(lottery_detail) > 100:
        return

    lottery_num = db.tbkt_active.excita_lottery.select('num').get(user_id=user_id, month=now_month)
    if not lottery_num:
        db.tbkt_active.excita_lottery.create(
            user_id=user_id,
            month=now_month,
            num=1,
            add_time=nowt
        )
    else:
        lottery_num = lottery_num.num + 1
        db.tbkt_active.excita_lottery.filter(user_id=user_id, month=now_month).update(num=lottery_num)
    db.tbkt_active.excita_lottery_detail.create(
        user_id=user_id,
        type=102,
        num=1,
        remark=u'发放期中试卷奖励1个抽奖券',
        send_task_num=0,
        add_time=nowt
    )