# coding:utf-8
from apps.active.common import get_user_rank, get_active_rank, update_score
from com.com_user import users_info, get_unit_students
from libs.utils import db, Struct, dedupe, time, join


def get_users_info(user_ids, display_unit=False):
    """
    根据user_id 获取用户信息
    ——————————————————————
    王世成    2017.9.12
    ——————————————————————
    :param user_ids:  用户id集合
    :param display_unit:  是否显示班级信息
    :return: 
    """
    if not isinstance(user_ids, (list, tuple)):
        return []
    # TODO 加入缓存
    # 获取正常用户真实姓名
    names = db.tbkt_user_slave.auth_user.select('real_name', 'id').filter(id__in=user_ids, status__ne=2)[:]
    names_map = {i.id: i.real_name for i in names}
    # 获取对应信息
    info = db.ketang_slave.mobile_order_region.select(
        'city', 'school_name', 'user_id', 'unit_class_id unit_id').filter(user_id__in=user_ids).group_by('user_id')[:]
    info_map = {i.user_id: i for i in info}

    unit_map = {}
    if display_unit:
        # 获取班级信息
        unit_ids = dedupe([i.unit_id for i in info])
        units = db.slave.school_unit_class.select('id', 'unit_name').filter(id__in=unit_ids)
        unit_map = {unit.id: unit.unit_name for unit in units}
    out = []
    for user_id, real_name in names_map.iteritems():
        mor = info_map.get(user_id, None)
        if not mor:
            continue
        mor.real_name = real_name
        if display_unit:
            mor.unit_name = unit_map.get(user_id, '')
        out.append(mor)
    return out


def get_user_score(user, active_id):
    """
    获取用户积分
    ——————————————————
    王世成  2017.9.12
    ——————————————————
    :param user:  用户对象
    :param active_id:  对应活动id
    :return: 
    """
    rank = Struct(get_user_rank(active_id, user.id))
    return rank


def user_score_detail(user, active_id, page):
    """
    获取用户积分详情
    ——————————————————
    王世成  2017.9.12
    ——————————————————
    :param user: 
    :param active_id:
    :param page: 
    :return: 
    """
    sql = """
    select  distinct i.item_name, d.score, d.add_date
    from active_score_user_detail d
    inner join active_score_item i on i.item_no = d.item_no and i.active_id=d.active_id
     and d.user_id = %s and d.active_id = %s
    order by d.add_date desc limit %s, %s
    """ % (user.id, active_id, (page-1)*50, 50)
    data = db.tbkt_active_slave.fetchall_dict(sql)
    for i in data:
        i.add_date = format_date(i.add_date)
    return data


def get_tips_award(active_id):
    """
    获取最新抽奖信息(滚动数据)
    暂无使用
    ———————————————————
    王世成    2017.9.12
    ———————————————————
    :param active_id: 
    :return: 
    """
    tips = db.tbkt_active_slave.active_award.select('user_name', 'award_name')\
        .filter(active_id=active_id, award_type__in=(1, 2, 3, 4)).order_by('add_time desc')[:10]
    return tips


def score_rank(active_id, page):
    """
    积分排名
    :return: 
    """
    size = 50
    ranks = get_active_rank(active_id, page, size)
    uids = [int(i.get('user_id')) for i in ranks]
    info_map = users_info(uids)
    for i in ranks:
        d = info_map.get(i.get('user_id'))
        if d:
            i.update(d)
    if active_id == 2:
        return ranks[:7]
    return ranks


def award_winner(active_id, page):
    """
    获奖排名
    :return: 
    """
    size = 50
    res = page * size
    page = (page - 1) * size

    if int(active_id) == 1:
        user_award = db.tbkt_active_slave.active_award.select('user_id', 'award_name') \
            .filter(remark=active_id, award_type__ne=8).order_by('award_type, add_time')[page: res]
    else:
        user_award = db.tbkt_active_slave.active_award.select('user_id', 'award_name') \
                         .filter(remark=active_id, award_type__ne=11).order_by('award_type, add_time')[page: res]
    uids = [i.user_id for i in user_award]
    info_map = users_info(uids)
    for i in user_award:
        d = info_map.get(i.get('user_id'))
        if d:
            i.update(d)
    return user_award


def class_stu_rank(user, unit_id, stu_active_id):
    """
    获取班级学生信息
    ———————————————————
    王世成    2017.9.12
    ———————————————————
    :param unit_id: 
    :param request:
    :param stu_active_id: 
    :param user
    :return: 
    """
    stu_ids = user.get_mobile_order_region().select("user_id") \
                  .filter(unit_class_id=unit_id, user_type=1).flat('user_id')[:]
    if not stu_ids:
        return []

    sql = """
    select a.id, a.real_name,a.id from auth_user a, auth_profile p
    where a.id = p.user_id and user_id in (%s)
    """ % join(stu_ids)
    rows = db.tbkt_user_slave.fetchall_dict(sql)
    
    stu_ids = [i.id for i in rows]
    stu_score = db.tbkt_active_slave.active_score_user.select('user_id', 'score')\
        .filter(user_id__in=stu_ids, active_id=stu_active_id).order_by('score desc')[:]
    score_map = {i.user_id: i.score for i in stu_score}

    for i in rows:
        i.score = score_map.get(i.id, 0)
    rows.sort(key=lambda x: (-x.score,x.id))
    return rows


def format_date(temp):
    # 时间格式化
    if not temp:
        return ''
    return time.strftime("%m月%d日 %H:%M:%S", time.localtime(temp))

STU_ACTIVE_ID = 8
OPEN_ITEM = 'stu_open'


def stu_open_add_score(user):
    # 学生开通加分
    if int(user.city) != 411200:
        return
    is_open = user.openstatus(2)
    if is_open:
        if db.tbkt_active.active_score_user_detail.get(user_id=user.id, active_id=STU_ACTIVE_ID, item_no='stu_open'):
            return 0
        else:
            update_score(user.id, STU_ACTIVE_ID, OPEN_ITEM, user.id, user.city, user.unit.id)
            return 1
