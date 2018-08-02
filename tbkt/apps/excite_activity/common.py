# coding=utf-8

"""
@varsion: ??
@author: 张嘉麒
@file: urls.py
@time: 2017/12/12 17:30
"""
import calendar
import time
import random
from collections import Counter

from libs.utils import db, tbktapi, get_absurl


def get_year(nowt):
    # 获取当前年份 int
    return time.localtime(nowt).tm_year


def get_month(nowt):
    # 获取当前月份 int
    return time.localtime(nowt).tm_mon


def get_first_day_in_month(nowt_year, nowt_month):
    # 利用当前年份和月份获取本月第一天00:00分的时间戳
    a = "%s-%s-1" % (nowt_year, nowt_month)
    timeArray = time.strptime(a, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


def process_phone_num(phone_num):
    # 将手机号 13333333333   --->    133****3333
    phone_num = str(phone_num)
    phone_num = phone_num[:3] + '****' + phone_num[7:]
    return str(phone_num)


def get_month_date(nowt):
    # 获得当前月份和日期
    time_local = time.localtime(nowt)
    month = time.strftime("%m", time_local)
    date = time.strftime("%d", time_local)

    return month, date


def get_year(nowt):
    time_local = time.localtime(nowt)
    year = time.strftime("%Y", time_local)
    return year


def get_last_month_range(nowt):
    """获取给定时间 的上个月时间范围"""
    month = time.localtime(nowt).tm_mon
    year = time.localtime(nowt).tm_year
    if month == 1:
        month = 12
        year -= 1
    else:
        month -= 1
    _, last_day = calendar.monthrange(year, month)
    first_day = time.mktime((year, month, 1, 0, 0, 0, 0, 0, 0))
    last_day = time.mktime((year, month, last_day, 23, 59, 59, 0, 0, 0))
    return int(first_day), int(last_day)


def get_user_tickets(user_id):
    """
    功能说明：                获取当前用户在这个月份的抽奖券的数量
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张嘉麒                    2017-12-12
    """
    nowt = time.time()
    nowt_month = get_month(nowt)
    user_tickets = db.tbkt_active.excita_lottery.select('num', 'add_time').get(user_id=user_id, month=nowt_month)
    if not user_tickets:
        return nowt_month, 0
    ticket_num = user_tickets.num
    return nowt_month, ticket_num


def coin_join_actitvity(user_id, excite_activity_id):
    """
    功能说明：                用户通过金币参与活动
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张嘉麒                    2017-12-12
    """
    if not user_id or not excite_activity_id:
        return u'没有user_id, 参数错误'
    nowt = int(time.time())

    # 查询本次活动的信息
    need_coin = db.tbkt_active.excita_config.select('sign_gold', 'end_time', 'name').get(
        id=excite_activity_id, type__ne=1, status=1)
    if need_coin:
        if need_coin.sign_gold:
            need_coin_num = need_coin.sign_gold
        else:
            return u'找不到活动的金币信息'
    else:
        return u'找不到活动相关信息'
    activity_name = need_coin.name

    # 只报名未参与抽奖的用户batch_id暂为0
    batch_id = 0

    # 查询用户金币信息
    user_coin = db.default.score_user.get(user_id=user_id, app_id=7)
    if user_coin:
        user_coin_num = user_coin.score
    else:
        return u'金币不足'
    if user_coin_num >= need_coin_num:
        user_coin_num -= need_coin_num
    else:
        return u'金币不足'


    with db.default as com:
        com.score_user.filter(user_id=user_id, app_id=7).update(score=user_coin_num)
        com.score_user_detail.create(
            user_id=user_id,
            score=need_coin_num,
            app_id=7,
            item_no=u'tea_voucher',
            remark=u'"%s"活动扣除' % activity_name,
            add_date=nowt,
            cycle_num=0
        )
    db.tbkt_active.excita_sign_up.create(
        user_id=user_id,
        excita_id=excite_activity_id,
        batch_id=batch_id,
        type=1,
        add_time=nowt
    )
    return ''


def ticket_join_actitvity(user_id, excite_activity_id):
    """
    功能说明：                用户通过奖券参与活动
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张嘉麒                    2017-12-12
    """
    if not user_id or not excite_activity_id:
        return u'没有user_id, 参数错误'

    nowt = int(time.time())

    # 查询本次活动的信息
    need_ticket_and_capped = db.tbkt_active.excita_config.select(
        'lottery_join_num', 'lottery_up', 'end_time', 'name').get(id=excite_activity_id, status=1)
    if not need_ticket_and_capped:
        return u'没有找到这次活动的参与信息'
    else:
        need_ticket = need_ticket_and_capped.lottery_join_num
        capped_num = need_ticket_and_capped.lottery_up
        activity_name = need_ticket_and_capped.name

    # 只报名未参与抽奖的用户batch_id暂为0
    batch_id = 0

    # 查询用户抽奖券信息
    had_join_ticket = db.tbkt_active.excita_sign_up.filter(excita_id=excite_activity_id, type=2, batch_id=batch_id)
    if had_join_ticket:
        had_join_ticket = had_join_ticket.count()
    else:
        had_join_ticket = 0
    if had_join_ticket >= capped_num:
        return u'使用奖券参加的人数已达上限'

    nowt_month, ticket_num = get_user_tickets(user_id)
    if ticket_num < need_ticket:
        return u'您的抽奖券数量不足'
    ticket_num -= need_ticket

    db.tbkt_active.excita_lottery.filter(month=nowt_month, user_id=user_id).update(num=ticket_num)

    db.tbkt_active.excita_sign_up.create(
        user_id=user_id,
        excita_id=excite_activity_id,
        batch_id=batch_id,
        type=2,
        add_time=nowt
    )
    db.tbkt_active.excita_lottery_detail.create(
        user_id=user_id,
        type=0,
        num=need_ticket,
        add_time=nowt,
        remark=u'"%s"扣除' % activity_name
    )

    return ''


def get_winning_list(excite_activity_id):
    """
     功能说明：                获取获奖名单
     -----------------------------------------------
     修改人                    修改时间
     -----------------------------------------------
     张嘉麒                    2017-12-13
     """
    winning_list = db.tbkt_active.excita_draw.select('real_name', 'school_name',
                                                     'phone').filter(excita_id=excite_activity_id)
    winner_list = []
    for winner in winning_list:
        winner['phone'] = process_phone_num(winner['phone'])
        winner_list.append(winner)
    return winner_list


def get_activity_entrance():
    """
     功能说明：                获取入口需要资源
     -----------------------------------------------
     修改人                    修改时间
     -----------------------------------------------
     张嘉麒                    2017-12-12
     """
    activity_array = db.tbkt_active.excita_config.select('id').filter(status=1).order_by('-start_time', '-end_time',
                                                                                         "id")
    if activity_array:
        actitity_len = activity_array.count()
        return actitity_len
    else:
        actitity_len = 0
        return actitity_len


def get_activity(excite_activity_id, user_id):
    """
     功能说明：                获取活动信息
     -----------------------------------------------
     修改人                    修改时间
     -----------------------------------------------
     张嘉麒                    2017-12-12
     """
    activity_info = db.tbkt_active.excita_config.select('open_person', 'lottery_up', 'type').get(id=excite_activity_id)

    # 已参与人数
    had_join = db.tbkt_active.excita_sign_up.select('id').filter(excita_id=excite_activity_id, batch_id=0)
    if had_join:
        had_join = had_join.count()
    else:
        had_join = 0
    activity_info["had_join"] = had_join

    # 已开奖次数
    had_lottery = db.tbkt_active.excita_batch.select('id').filter(excita_id=excite_activity_id, status=1)
    if had_lottery:
        had_lottery = had_lottery.count()
    else:
        had_lottery = 0
    activity_info["had_lottery"] = had_lottery

    # 目前活动参与人数，转换成中奖率
    join_num = db.tbkt_active.excita_sign_up.select('id').filter(excita_id=excite_activity_id,
                                                                 user_id=user_id, batch_id=0)
    if join_num:
        join_num = join_num.count()
    else:
        join_num = 0
    if join_num == 0:
        lottery_rate = '0%'
    else:
        lottery_rate = '%.2f %%' % (100 * float(join_num) / float(activity_info.open_person))
    activity_info["lottery_rate"] = lottery_rate

    # 批次信息
    batch_id = 0

    # 已经用奖券参与的人数
    had_use_ticket_join = db.tbkt_active.excita_sign_up.select('id').filter(type=2, excita_id=excite_activity_id,
                                                                            batch_id=batch_id)
    if had_use_ticket_join:
        had_use_ticket_join = had_use_ticket_join.count()
    else:
        had_use_ticket_join = 0
    if had_use_ticket_join > activity_info.lottery_up:
        had_use_ticket_join = activity_info.lottery_up
    activity_info["had_use_ticket_join"] = had_use_ticket_join

    # 该用户是否中奖
    is_winner = db.tbkt_active.excita_draw.filter(excita_id=excite_activity_id, user_id=user_id).exists()
    activity_info['is_winner'] = is_winner

    return activity_info


def send_sms(phone_num, user_id, request, user):
    nowt = int(time.time())

    # 获取当月第一天的时间戳
    nowt_month = get_month(nowt)
    nowt_year = get_year(nowt)
    nowt_month_first_day = get_first_day_in_month(nowt_year, nowt_month)

    send_homework_status = db.slave.message.select('id').get(type__in=(2, 7, 8, 9), add_time__gt=nowt_month_first_day,
                                                             add_user=user_id)
    if not send_homework_status:
        return u'不满足条件'

    invited_people = db.tbkt_user.auth_user.select('id').filter(phone=str(phone_num), type=3).order_by('-last_login')[:]
    if not invited_people:
        return u'无效号码'
    else:
        invited_people = invited_people[0].id

    print invited_people, user_id
    if invited_people == user_id:
        return u'不能邀请自己'

    # 获取发送者姓名
    teacher_name = db.tbkt_user.auth_user.select('real_name').get(id=user_id)
    teacher_name = teacher_name.real_name

    region = db.ketang_slave.mobile_order_region.get(user_id=user_id)
    if region and region.city == "411200":
        return u"三门峡用户暂无法邀请"

    invited_status = db.tbkt_active.excita_invite_tea.select('id').get(invite_phone=phone_num,
                                                                       add_time__gt=nowt_month_first_day, )
    if invited_status:
        return u'已被邀请'
    else:
        content = u'''我在参加同步课堂抽奖活动，有机会抽到空气净化器，华为手机等礼品，你也一起来参加吧！去发作业还有抽奖券可以领呢，下载地址m.tbkt.cn【%s老师】''' % teacher_name
        hub = tbktapi.Hub(request)
        r = hub.sms.post("/sms/send", {"platform_id": user.platform_id, "phone": phone_num, "content": content})
        print r
        if r:
            if r.response == "ok":
                db.tbkt_active.excita_invite_tea.create(
                    invite_phone=phone_num,
                    invite_user_id=invited_people,
                    user_id=user_id,
                    add_time=nowt
                )
            else:
                return r.message
    return ''


def create_stu_invite_data_to_mysql(stu_id, user_id):
    try:
        stu_id = stu_id.split(',')
    except:
        return u'传过来的stu_id有误，请查证'

    # 获取当前月第一天和下个月第一天的时间戳
    nowt = time.time()
    nowt_month = get_month(nowt)
    nowt_year = get_year(nowt)
    next_month = nowt_month + 1
    if next_month == 13:
        next_month = 1
        next_year = nowt_year + 1
    else:
        next_year = nowt_year
    nowt_month_first_day = get_first_day_in_month(nowt_year, nowt_month)
    next_month_first_day = get_first_day_in_month(next_year, next_month)

    # 对当月没有出现在excita_invite_open表中的邀请数据进行插入
    had_inserted_stu_invite_info = db.tbkt_active.excita_invite_open.select('stu_user_id').filter(
        user_id=user_id, stu_user_id__in=stu_id, add_time__range=(nowt_month_first_day, next_month_first_day))
    had_inserted_stu_id = [str(x.stu_user_id) for x in had_inserted_stu_invite_info]
    args = []
    for id in stu_id:
        if id not in had_inserted_stu_id:
            d = dict(
                user_id=user_id,
                stu_user_id=id,
                add_time=nowt,
                is_open=0
            )
            args.append(d)
    if args:
        db.tbkt_active.excita_invite_open.bulk_create(args)
    return ''


def change_batch_id(request, excite_activity_id):
    """
   功能说明：                判断参与抽奖人数是否够300人
   -----------------------------------------------
   修改人                    修改时间
   -----------------------------------------------
   张嘉麒                    2017-12-12
   """
    # 获取300个人的Id,不够直接返回
    nowt = int(time.time())
    join_nums = db.tbkt_active.excita_sign_up.select('id', 'user_id').filter(excita_id=excite_activity_id, batch_id=0)
    open_person = db.tbkt_active.excita_config.select('open_person').get(id=excite_activity_id)
    open_person = open_person.open_person
    if not join_nums:
        return ''
    if join_nums.count() < open_person:
        return ''
    join_ids = [int(join_num.id) for join_num in join_nums]
    join_ids = join_ids[:open_person]
    user_ids = [int(join_num.user_id) for join_num in join_nums]
    user_ids = user_ids[:open_person]

    # 创建批次信息,获取批次id
    db.tbkt_active.excita_batch.create(
        excita_id=excite_activity_id,
        open_time=0,
        status=0,
        add_time=nowt,
    )
    batch_id = db.tbkt_active.excita_batch.select('id').get(excita_id=excite_activity_id, open_time=0, add_time=nowt)
    batch_id = batch_id.id
    # 更新300个人的批次信息
    db.tbkt_active.excita_sign_up.filter(id__in=join_ids, batch_id=0).update(batch_id=batch_id)

    # 调用抽奖函数
    luck_boy = find_a_luck_boy(user_ids, batch_id, excite_activity_id, open_person)
    # 发短信
    # content = u'您在同步课堂众筹活动中奖，请在同步课堂客户端活动页面填写中奖信息。'
    # hub = tbktapi.Hub(request)
    # hub.sms.post('/sms/send', {'platform_id': 1, 'user_id': luck_boy, 'content': content})
    # return 'yes'


def find_a_luck_boy(user_ids, batch_id, excite_activity_id, open_person):
    """
   功能说明：                抽奖
   -----------------------------------------------
   修改人                    修改时间
   -----------------------------------------------
   张嘉麒                    2018-4-12
   """
    # 抽一个人
    # 一个长度为open_person的用户id的数组
    # random_num = random.randint(0, open_person - 1)
    # luck_boy = int(user_ids[random_num])
    user_ids = Counter(user_ids)
    a_array = user_ids.most_common()
    big_frequency = 0
    big_user_ids = []
    for a in a_array:
        if a[1] >= big_frequency:
            big_user_ids.append(a[0])
            big_frequency = a[1]
        if a[1] < big_frequency:
            break
    print big_user_ids
    random_num = random.randint(0, len(big_user_ids) - 1)
    luck_boy = int(big_user_ids[random_num])

    # 更新活动批次表中开奖状态
    print batch_id
    db.tbkt_active.excita_batch.filter(id=batch_id).update(status=1)

    print luck_boy
    # 获取获奖者信息
    user_info = db.tbkt_user.auth_user.select('real_name', 'phone').get(id=luck_boy)
    school_name = db.ketang.mobile_order_region.select('school_name').get(user_id=luck_boy)

    # 更新获奖者名单
    nowt = time.time()
    db.tbkt_active.excita_draw.create(
        excita_id=excite_activity_id,
        batch_id=batch_id,
        user_id=luck_boy,
        school_name=school_name.school_name,
        phone=user_info.phone,
        add_time=nowt,
        real_name=user_info.real_name,
        address='',
        addressee='',
        addressee_phone=''
    )
    return luck_boy


def get_activeity_list():

    activity_info = db.tbkt_active.excita_config.select('id', 'url', 'open_person', 'start_time', 'lottery_join_num',
                                                        'end_time', 'sign_gold', 'name', 'original_price',
                                                        'type').filter(status=1).order_by('-start_time', '-end_time')[:]

    active_ids = [a.id for a in activity_info]
    # 参与人数
    tea_num = {}
    if active_ids:
        sql = """
          select count(1) num,excita_id from excita_sign_up where excita_id in (%s) and batch_id=0 group by excita_id
        """ % ','.join(str(i) for i in active_ids)
        rows = db.tbkt_active_slave.fetchall_dict(sql)
        tea_num = {i.excita_id: i.num for i in rows}

    for activity in activity_info:
        activity["strat_time_month"], activity["start_time_date"] = get_month_date(activity.start_time)
        activity["end_time_month"], activity["end_time_date"] = get_month_date(activity.end_time)
        activity.url = get_absurl(activity.url)
        activity["strat_time_year"] = get_year(activity.start_time)
        activity["end_time_year"] = get_year(activity.end_time)
        activity['tea_num'] = tea_num.get(activity['id'], 0)
    return activity_info


def last_month_winning():
    """返回上个月获奖信息"""
    time_range = get_last_month_range(time.time())
    active_info = db.tbkt_active.excita_config.filter(end_time__range=time_range
                                                      ).select('id', 'url').order_by('end_time')[:]
    if not active_info:
        return []

    winning_list = db.tbkt_active.excita_draw.select('excita_id', 'real_name', 'school_name',
                                                     'phone').filter(excita_id__in=[a.id for a in active_info])[:]

    active_winner = {}
    for winner in winning_list:
        winner.phone = process_phone_num(winner['phone'])
        winner.real_name = winner['real_name'][0] + u'教师'
        active_winner.setdefault(winner.excita_id, []).append(winner)

    for a in active_info:
        a.url = get_absurl(a.url)
        a.winner = active_winner.get(a.id, [])
        a.winner.sort(key=lambda x: x.add_time)

    return active_info


def submit_winner_info(user_id, excita_id, address, addressee, phone):
    """提交中奖信息"""
    is_winner = db.tbkt_active.excita_draw.filter(excita_id=excita_id, user_id=user_id).exists()
    if not is_winner:
        return u'未获得奖品，请核实'
    db.tbkt_active.excita_draw.filter(excita_id=excita_id, user_id=user_id).update(
        address=address, addressee=addressee, addressee_phone=phone)