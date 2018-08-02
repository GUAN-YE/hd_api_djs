# coding:utf-8
"""
@author: lvyang
@time: 2017/12/14
"""
import random
import time
from apps.com_post.common import today_temp
from com.com_user import get_open_status
from libs.utils import db, pinyin_abb, tbktapi, Struct
from libs.utils.auth import create_token
from .config import *


def active_status():
    """判断活动状态，结束返回0"""
    active_info = db.tbkt_active.active.get(id=ACTIVE_ID)
    begin_time = active_info.begin_time
    end_time = active_info.end_time
    if begin_time > int(time.time()) or end_time < int(time.time()):
        return False
    return True


def any_open_status(user_id):
    """三科 任一开通，返回1"""
    open_data = get_open_status(user_id, [2, 5, 9])
    status = any([o['status'] for o in open_data])
    return status


def open_prop(user):
    """开通用户首次登录奖励"""
    if not active_status():
        return u''
    if not any_open_status(user.id):
        return u''
    if db.tbkt_active.active_score_user_detail.filter(
            user_id=user.id, active_id=ACTIVE_ID, item_no='open_prop').exists():
        return u''
    remark = u'开通获得'
    db.tbkt_active.active_score_user_detail.create(
        user_id=user.id, active_id=ACTIVE_ID, item_no='open_prop', add_username=user.id, score=1,
        remark=remark, add_date=int(time.time())
    )
    user_prop = db.tbkt_active.active_user_props.get(user_id=user.id, item_no='shoe', active_id=ACTIVE_ID)
    if user_prop:
        db.tbkt_active.active_user_props.filter(user_id=user.id, active_id=ACTIVE_ID, item_no='shoe').update(
            num=user_prop.num + 1)
    else:
        db.tbkt_active.active_user_props.create(
            active_id=ACTIVE_ID, user_id=user.id, item_no='shoe', name=PROPS_REMARK.get('shoe', u''), num=1)
    return remark + u'圣诞鞋'


def get_user_props(user_id):
    """返回用户道具数量"""
    user_props = db.tbkt_active.active_user_props.filter(active_id=ACTIVE_ID, user_id=user_id).select('item_no', 'name',
                                                                                                      'num')[:]
    user_props_map = {i.item_no: i for i in user_props}

    prop_rank = {'hat': 1, 'clothes': 2, 'shoe': 3, 'glove': 4, 'bag': 5}
    props = user_props_map.values()
    for k in PROPS_REMARK.keys():
        if k not in user_props_map:
            o = Struct()
            o.item_no = k
            o.name = PROPS_REMARK[k]
            o.num = 0
            props.append(o)
    props.sort(key=lambda x: prop_rank.get(x.item_no))
    return props


def user_props_detail(user_id):
    """返回用户获得道具详情,获奖详情"""
    award_detail = db.tbkt_active_slave.active_award.filter(
        user_id=user_id, active_id=ACTIVE_ID).select('add_time', 'award_name as prop_name')[:]
    for d in award_detail:
        d.date = time.strftime("%m月%d日", time.localtime(d.add_time))
        d.remark = u'开宝箱获得'
        d.status = 1
        d.item_no = 'gift'

    detail = db.tbkt_active_slave.active_score_user_detail.filter(
        user_id=user_id, active_id=ACTIVE_ID).select('item_no', 'add_date', 'remark', 'score').order_by('-id')[:]
    for d in detail:
        d.date = time.strftime("%m月%d日", time.localtime(d.add_date))
        d.prop_name = PROPS_REMARK.get(d.item_no, u'')
        d.status = -1 if d.score == -1 else 1
        if str(d.item_no) == 'open_prop':
            d.prop_name = u'圣诞鞋'
        award_detail.append(d)
    return award_detail


def user_props_news(user_id):
    """用户索要奖品记录表"""
    news = db.tbkt_active_slave.active_user_props_news.filter(
        active_id=ACTIVE_ID, user_id=user_id).select('msg', 'user_id', 'add_user', 'add_time', 'item_no', 'id',
                                                     'status').order_by('-id')[:]
    for n in news:
        n.date = time.strftime("%m月%d日", time.localtime(n.add_time))
        n.name = PROPS_REMARK.get(n.item_no, '')
    return news


def demand_props(user, stu_id, item_no):
    """索要道具"""
    msg = u"%s向你索要" % user.name
    db.tbkt_active.active_user_props_news.create(
        active_id=ACTIVE_ID, msg=msg, user_id=stu_id, item_no=item_no, add_user=user.id, add_time=int(time.time()))


def give_props(user, stu_id, item_no, new_id):
    """赠送道具"""
    if item_no not in PROPS_REMARK.keys():
        return False, u'标识错误'
    stu = db.tbkt_user_slave.auth_user.filter(id=stu_id).select('real_name').first()
    if not stu:
        return False, u'未找到该用户！'
    with db.tbkt_active as active:
        sql = """select num from active_user_props where user_id=%s and item_no='%s' and active_id=%s for update""" \
              % (user.id, item_no, ACTIVE_ID)
        user_prop = active.fetchone_dict(sql)
        if not user_prop or user_prop.num < 1:
            return False, u'道具数量不够，无法赠送！'
        # 减去一个
        active.active_user_props.filter(user_id=user.id, item_no=item_no, active_id=ACTIVE_ID).update(
            num=user_prop.num - 1)
        active.active_score_user_detail.create(user_id=user.id, item_no=item_no, remark=u'赠送%s' % stu.real_name,
                                               score=-1, add_date=int(time.time()), active_id=ACTIVE_ID,
                                               add_username=user.id)

        # 加上一个
        active.active_score_user_detail.create(user_id=stu_id, item_no=item_no, remark=u'%s赠送你' % user.name, score=1,
                                               add_date=int(time.time()), active_id=ACTIVE_ID, add_username=user.id)
        stu_prop = active.active_user_props.get(active_id=ACTIVE_ID, user_id=stu_id, item_no=item_no)
        if stu_prop:
            active.active_user_props.filter(active_id=ACTIVE_ID, user_id=stu_id, item_no=item_no).update(
                num=stu_prop.num + 1)
        else:
            active.active_user_props.create(
                active_id=ACTIVE_ID, user_id=stu_id, item_no=item_no, name=PROPS_REMARK.get(item_no, u''), num=1)
        # 如果通过索要记录赠送，则更新消息表
        if new_id:
            active.active_user_props_news.filter(id=new_id).update(status=1)
        return True, u''


def open_box(user):
    """打开宝箱，获得奖品"""
    active_info = db.tbkt_active.active.get(id=ACTIVE_ID)
    begin_time = active_info.begin_time
    end_time = active_info.end_time
    if begin_time > int(time.time()):
        return u'', u'活动未开始'
    if end_time < int(time.time()):
        return u'', u'活动已结束'

    props_item = PROPS_REMARK.keys()
    item_no = ','.join("'%s'" % str(i) for i in props_item)
    with db.tbkt_active as active:
        sql = """
            select count(id) total from active_user_props where active_id=%s and  user_id=%s and item_no in(%s) and num>0
        """ % (ACTIVE_ID, user.id, item_no)
        user_props = active.fetchone_dict(sql)
        if not user_props or user_props.total < len(props_item):
            return u'', u'道具不够，不能打开宝箱！'
        sql = """update active_user_props set num=num-1 where user_id =%s and item_no in (%s) and active_id=%s""" % (
            user.id, item_no, ACTIVE_ID)
        active.execute(sql)
        award_name = u'小怪兽文具礼盒 '
        active.active_award.create(
            user_id=user.id, user_name=user.name, award_type=1, active_id=ACTIVE_ID,
            award_name=award_name, city=user.city, remark=1, add_time=int(time.time()))
        return award_name, u''


def award_props(user, work_type):
    """完成作业获得道具"""
    if work_type not in [1, 2, 3, 4]:
        return u'', u'type值错误'
    work_props = WORK_PROPS.get(work_type)

    active_info = db.tbkt_active.active.get(id=ACTIVE_ID)
    begin_time = active_info.begin_time
    end_time = active_info.end_time
    if begin_time > int(time.time()):
        return u'', u'活动未开始'
    if end_time < int(time.time()):
        return u'', u'活动已结束'

    day_temp = today_temp()
    detail = db.tbkt_active.active_score_user_detail.filter(
        user_id=user.id, active_id=ACTIVE_ID, item_no__in=PROPS_WORD.keys(), add_date__gte=day_temp).select('remark')[:]
    if detail:
        for d in detail:
            if u'赠送' not in d.remark:
                return u'', u'今天已经发过奖品了'

    props_sort = PROPS_WORD.values()
    # 根据获奖概率,具体规则见config.py
    dice = random.random()
    begin = 0
    award_item = {}
    for s in props_sort:
        if begin < dice <= begin + s['rate']:
            award_item = s
            break
        else:
            begin += s['rate']
    if not award_item:
        item = choice_free_props()
        award_item = PROPS_WORD.get(item)
    # 未开通用户不能获得背包
    if award_item['item_no'] == 'bag' and not any_open_status(user.id):
        item = choice_free_props()
        award_item = PROPS_WORD.get(item)
    # 每天限量发，按比例发，具体规则见config.py
    if award_item['day_num'] != -1:
        # 获取奖品总数
        props_info = db.tbkt_active_slave.active_score_gift.get(
            active_id=ACTIVE_ID, active_type=1,
            name=award_item['item_no'],
            sequence=work_type)

        #  活动开始天数
        able_day = (((int(time.time() - begin_time)) / (24 * 60 * 60)) + 1)
        # 按比例的每日发放量
        day_num = award_item['day_num'] * work_props[award_item['item_no']] / award_item['total']
        able_num = able_day * day_num
        # 剩余数量小于 （总数减去 开始天数*day_num ）时 不能再发
        if not props_info or props_info.num <= 0 or props_info.num <= work_props[award_item['item_no']] - able_num:
            item = choice_free_props()
            award_item = PROPS_WORD.get(item)
    remark = u'完成%s获得' % work_props['name']
    is_free = True if award_item['day_num'] == -1 else False
    name = add_props(user.id, award_item['item_no'], remark, work_type, is_free)
    return u'获得' + name, u''


def add_props(user_id, item, remark, work_type, free=False):
    with db.tbkt_active as active:
        if not free:
            sql = """
            select num from active_score_gift where active_id =%s and active_type=1 and sequence=%s and name='%s'
            """ % (ACTIVE_ID, work_type, item)
            user_prop = active.fetchone_dict(sql)
            if not user_prop or user_prop.num < 1:
                item = choice_free_props()
            else:
                sql = """update active_score_gift set num=num-1
                where active_id=%s and active_type=1 and sequence=%s  and name='%s' """ % (ACTIVE_ID, work_type, item)
                active.execute(sql)
        user_prop = active.active_user_props.get(user_id=user_id, item_no=item, active_id=ACTIVE_ID)
        if user_prop:
            active.active_user_props.filter(user_id=user_id, item_no=item, active_id=ACTIVE_ID).update(
                num=user_prop.num + 1)
        else:
            active.active_user_props.create(user_id=user_id, item_no=item, active_id=ACTIVE_ID, name=PROPS_REMARK[item],
                                            num=1)
        active.active_score_user_detail.create(
            user_id=user_id, active_id=ACTIVE_ID, item_no=item, add_username=user_id, score=1,
            remark=remark, add_date=int(time.time()))
        return PROPS_REMARK[item]


def get_unit_stu(user):
    """获取班级下学生"""
    unit_id = user.unit.id if user.unit else 0
    if not unit_id:
        return []
    stu_ids = get_unit_stu_ids(unit_id)
    if user.id in stu_ids:
        stu_ids.remove(user.id)
    if not stu_ids:
        return []
    sql = """
            select a.id, a.real_name name,a.id from auth_user a, auth_profile p
            where a.id = p.user_id and user_id in (%s)
            """ % ','.join(str(i) for i in stu_ids)
    rows = db.tbkt_user_slave.fetchall_dict(sql)
    for i in rows:
        i.pinyin = pinyin_abb(i.name)
        i.initial = i.pinyin[0] if i.pinyin else ''
    rows.sort(key=lambda x: x.initial)
    return rows


def get_unit_stu_ids(unit_id):
    if not unit_id:
        return []
    stu_ids = db.ketang_slave.mobile_order_region.select(
        "user_id").filter(unit_class_id=unit_id, user_type=1).flat('user_id')[:]
    return stu_ids


def verify_user(user_id, phone, name):
    """确认邀请用户"""
    if len(phone) != 11 or not phone.isdigit():
        return u'', u'请输入正确手机号！'
    stus = db.tbkt_user_slave.auth_user.filter(
        username__startswith=phone, type=1).select('id', 'real_name')[:]
    if not stus:
        return u'', u'您不是同步课堂用户，请登录http://user.jxtbkt.cn/注册'
    stu = None
    for s in stus:
        if s.real_name == name:
            stu = s
            break
    if not stu:
        return u'', u'手机号或用户名错误!'
    open_info = get_open_status(stu.id, [2, 5, 9])
    token = create_token(stu.id)
    data = dict(open_info=open_info, token=token)
    return data, None


def invite_open(request, user, subject_id, sn_code, invite_user_id):
    """邀请开通"""
    sid = subject_id.split(',')
    hub = tbktapi.Hub(request)
    open_status = 0
    error = None

    open_info = get_open_status(user.id, sid)
    for o in open_info:
        if o['status'] == 1:
            sid.remove(o['subject_id'])
    if not sid:
        return False, u'该学科已开通！'
    for s in sid:
        r = hub.bank.post('/cmcc/open', {'phone_number': user.phone, 'subject_id': s, 'sn_code': sn_code})
        if r.response == 'ok':
            open_status = 1
        else:
            error = r.message
    if open_status != 1:
        return False, error

    is_invite = db.tbkt_active.active_user_invite.filter(user_id=invite_user_id, stu_id=user.id,
                                                         active_id=ACTIVE_ID).first()
    if is_invite:
        sid = list(set(is_invite.subject_id.split(',') + sid))
        _sid = ','.join(str(i) for i in sid)
        db.tbkt_active.active_user_invite.filter(
            active_id=ACTIVE_ID, user_id=invite_user_id, stu_id=user.id).update(subject_id=_sid)
    else:
        _sid = ','.join(str(i) for i in sid)
        db.tbkt_active.active_user_invite.create(user_id=invite_user_id, stu_id=user.id, subject_id=_sid, status=0,
                                                 active_id=ACTIVE_ID, update_time=int(time.time()))

    return True, None


def check_invite(user):
    """检擦是否开通"""
    if not active_status():
        return {}
    # 产品规则，邀请自己开通不做统计
    invite_info = db.tbkt_active_slave.active_user_invite.filter(
        active_id=ACTIVE_ID, user_id=user.id, stu_id__ne=user.id, status=0).select('stu_id', 'subject_id')[:]
    if not invite_info:
        return {}
    name_map = {}
    for i in invite_info:
        stu_id = i.stu_id
        sids = i.subject_id.split(',')
        open_info = get_open_status(stu_id, sids)
        is_open = 0
        for o in open_info:
            if o['status'] == 1:
                is_open = 1
                break
        if is_open:
            db.tbkt_active.active_user_invite.filter(user_id=user.id, active_id=ACTIVE_ID, stu_id=i.stu_id).update(
                status=1)
            # 发奖品
            item_no = 'shoe'
            work_type = 5
            if any_open_status(user.id):
                item_no = 'bag'
            remark = u'通过邀请开通获得'
            name = add_props(user.id, item_no, remark, work_type, free=False)
            name_map[name] = name_map.get(name, 0) + 1
    return name_map


def choice_free_props():
    """随机返回一个免费的道具标识"""
    free_props = []
    for k in PROPS_REMARK.keys():
        if PROPS_WORD[k]['total'] == -1:
            free_props.append(k)
    return random.choice(free_props)
