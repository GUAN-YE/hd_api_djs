# coding: utf-8

from libs.utils import db, num_to_ch


def paper_list(user_id, subject_id):
    """
    活动试卷列表
    :param user_id: 年级_id
    :param subject_id: 二位学科id
    :return:
    """
    if subject_id != 21:
        return

    # 用户已设置教材信息
    book = db.default.user_book.get(user_id=user_id, is_work_book=0, subject_id=subject_id)
    if not book:
        return

    book_id = book.book_id
    book = db.ziyuan_slave.zy_book.get(id=book_id)
    if book.volume != 1:
        return
    grade_name = get_grade_cn(book.grade_id)
    press_id = get_press(book.press_id)

    active_id = 48

    sql = """
    select t.id from
    (select p.id, p.name, c.name grade_name,
    (select c1.id from tbkt_a_active_catalog c1 where c1.id= c.parent_id) press_id
    from sx_paper p, sx_paper_relate r, tbkt_a_active_catalog c
    where p.id = r.paper_id and c.id = r.object_id and c.active_id = %s and r.status = 1) t
    where t.grade_name like '%s' and press_id like '%s'
    """ % (active_id, grade_name, press_id)
    print sql
    rows = db.ziyuan_slave.fetchall_dict(sql)
    if not rows:

        return

    # 获取试卷id集合
    object_ids = [i.id for i in rows]

    # 查询已发试卷
    task = db.tbkt_shuxue.sx_task.filter(add_user=user_id, type=101, status__gt=0, object_id__in=object_ids)

    # {试卷id：1}
    task_map = {i.object_id: 1 for i in task}
    for i, v in enumerate(rows):
        v.status = task_map.get(v.id, 0)
        v.name = "期末提分试卷（%s）" % (num_to_ch(i+1))
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
    press_map = {2: 280, 4: 283, 8: 294, 38: 301}
    return press_map.get(press_id)
