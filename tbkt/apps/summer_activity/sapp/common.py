# coding=utf-8
import json
import random
import time

from django.conf import settings

from libs.utils import db, Struct, num_to_ch, format_url, get_absurl

PHASE_2_START_TIME = 0


def get_debris(phase, subject_id, user_id, nowt, method='GET', debris_species='', remark=''):
    '''
    @param user_id:
    @param nowt:
    @param method:  方法种类
    @param debris_species:   增加/减少碎片类型
    @return:
    '''
    if method == 'GET':
        # 获取用户当前道具数量
        user_species = db.tbkt_active.summer2018_stu_debris.select('debris').get(user_id=user_id, subject_id=subject_id, phase=phase)
        if not user_species:
            user_species = {"hat":0, "shoe":0, "background":0, "pants":0, "cloth":0}
            db.tbkt_active.summer2018_stu_debris.create(
                user_id=user_id,
                debris=json.dumps(user_species),
                add_time=nowt,
                subject_id=subject_id,
                phase=phase,
            )
        else:
            user_species = json.loads(user_species.debris)
        return user_species
    elif method == 'ADD':
        # 增加道具
        if not debris_species or debris_species not in ['hat', 'shoe', 'background', 'pants', 'cloth']:
            raise AttributeError('add debris_species is not right')
        if not remark:
            raise AttributeError('can not add debris without remark')
        else:
            user_debris = db.tbkt_active.summer2018_stu_debris.select('debris').get(user_id=user_id, subject_id=subject_id, phase=phase)
            if not user_debris:
                user_debris = {"hat": 0, "shoe": 0, "background": 0, "pants": 0, "cloth": 0}
                if debris_species in user_debris.keys():
                    user_debris[debris_species] += 1
                else:
                    raise AttributeError('Add debris_species raise a error, debris_species is %s' % debris_species)
                db.tbkt_active.summer2018_stu_debris.create(
                    user_id=user_id,
                    debris=json.dumps(user_debris),
                    add_time=nowt,
                    subject_id=subject_id,
                    phase=phase
                )
                db.tbkt_active.summer2018_stu_debris_detail.create(
                    user_id=user_id,
                    subject_id=subject_id,
                    debris=debris_species,
                    debris_method=u'open',
                    add_time=nowt,
                    remark=remark,
                    phase=phase,
                )
            else:
                user_debris = json.loads(user_debris.debris)
                if debris_species in user_debris.keys():
                    user_debris[debris_species] += 1
                    db.tbkt_active.summer2018_stu_debris.filter(user_id=user_id, subject_id=subject_id).update(
                        debris=json.dumps(user_debris)
                    )
                    db.tbkt_active.summer2018_stu_debris_detail.create(
                        user_id=user_id,
                        subject_id=subject_id,
                        debris=debris_species,
                        debris_method=u'open',
                        add_time=nowt,
                        remark=remark,
                        phase=phase
                    )
                else:
                    raise AttributeError('Add debris_species raise a error, debris_species is %s' % debris_species)
            return user_debris
    elif method == 'USE':
        # 消耗道具
        if not debris_species or debris_species not in ['hat', 'shoe', 'background', 'pants', 'cloth']:
            raise AttributeError('use debris_species is not right')
        pass
    elif method == 'GIVE':
        if not debris_species or debris_species not in ['hat', 'shoe', 'background', 'pants', 'cloth']:
            raise AttributeError('add debris_species is not right')
        if not remark:
            raise AttributeError('can not GIVE debris without remark')
        else:
            user_debris = db.tbkt_active.summer2018_stu_debris.select('debris').get(user_id=user_id,
                                                                                    subject_id=subject_id, phase=phase)
            if not user_debris:
                raise AttributeError('This user has not debris info, raise a error')
            else:
                user_debris = json.loads(user_debris.debris)

                if debris_species in user_debris.keys():
                    if user_debris[debris_species] < 1:
                        return u'您的道具不足'
                    user_debris[debris_species] -= 1
                    db.tbkt_active.summer2018_stu_debris.filter(user_id=user_id, subject_id=subject_id).update(
                        debris=json.dumps(user_debris)
                    )
                    db.tbkt_active.summer2018_stu_debris_detail.create(
                        user_id=user_id,
                        subject_id=subject_id,
                        debris=debris_species,
                        debris_method=u'give',
                        add_time=nowt,
                        remark=remark,
                        phase=phase
                    )
                else:
                    raise AttributeError('Give debris_species raise a error, debris_species is %s' % debris_species)
            return None
    elif method == 'RECEIVE':
        if not debris_species or debris_species not in ['hat', 'shoe', 'background', 'pants', 'cloth']:
            raise AttributeError('add debris_species is not right')
        if not remark:
            raise AttributeError('can not RECEIVE debris without remark')
        else:
            user_debris = db.tbkt_active.summer2018_stu_debris.select('debris').get(user_id=user_id,
                                                                                    subject_id=subject_id, phase=phase)
            if not user_debris:
                user_debris = {"hat": 0, "shoe": 0, "background": 0, "pants": 0, "cloth": 0}
                if debris_species in user_debris.keys():
                    user_debris[debris_species] += 1
                else:
                    raise AttributeError('Add debris_species raise a error, debris_species is %s' % debris_species)
                db.tbkt_active.summer2018_stu_debris.create(
                    user_id=user_id,
                    debris=json.dumps(user_debris),
                    add_time=nowt,
                    subject_id=subject_id,
                    phase=phase
                )
                db.tbkt_active.summer2018_stu_debris_detail.create(
                    user_id=user_id,
                    subject_id=subject_id,
                    debris=debris_species,
                    debris_method=u'receive',
                    add_time=nowt,
                    remark=remark,
                    phase=phase
                )
            else:
                user_debris = json.loads(user_debris.debris)
                if debris_species in user_debris.keys():
                    user_debris[debris_species] += 1
                    db.tbkt_active.summer2018_stu_debris.filter(user_id=user_id, subject_id=subject_id).update(
                        debris=json.dumps(user_debris)
                    )
                    db.tbkt_active.summer2018_stu_debris_detail.create(
                        user_id=user_id,
                        subject_id=subject_id,
                        debris=debris_species,
                        debris_method=u'receive',
                        add_time=nowt,
                        remark=remark,
                        phase=phase
                    )
                else:
                    raise AttributeError('Add debris_species raise a error, debris_species is %s' % debris_species)
            return None


def open_box(phase, user_id, box_species, subject_id):
    '''
    @param user_id:
    @param open_num:
    @return:
    '''
    if not box_species:
        raise AttributeError('box_species can not null')
    nowt = int(time.time())
    open_status = db.tbkt_active.summer2018_stu_open_box.select('open_num').get(user_id=user_id)
    if open_status:
        update_num = open_status.open_num + 1
        # 更新开启次数
        db.tbkt_active.summer2018_stu_open_box.filter(user_id=user_id).update(open_num=update_num, add_time=nowt)
        # 获取用户当前碎片数目
        user_debris = get_debris(phase, subject_id, user_id, nowt, 'GET')
        # 抽奖
        get_debris_species = prize_draw(user_debris)
        # 更新用户碎片数目,更新开启记录
        get_debris(phase, subject_id, user_id, nowt, 'ADD', get_debris_species, box_species)
        return get_debris_species
    else:
        raise AttributeError("You can not open box without into index")


def get_user_rank(user_id, subject_id, unit_id, phase):
    # 用户开启次数   修改一下，然后牺牲空间换取时间效率
    nowt = int(time.time())
    open_num = db.tbkt_active.summer2018_stu_open_box.select('open_num').get(user_id=user_id, subject_id=subject_id)
    if open_num:
        if phase == 2:
            phase_2_join = db.tbkt_active.summer2018_stu_open_box.select('open_num').get(user_id=user_id, subject_id=subject_id, add_time__gt=PHASE_2_START_TIME)
            if not phase_2_join:
                db.tbkt_active.summer2018_stu_open_box.filter(user_id=user_id, subject_id=subject_id).update(add_time=nowt)
        open_num = open_num.open_num
    else:
        #  头一次进入活动，
        #  注册活动
        db.tbkt_active.summer2018_stu_open_box.create(
            user_id=user_id,
            open_num=0,
            add_time=nowt,
            subject_id=subject_id,
            unit_id=unit_id
        )
        open_num = 0

    # 用户排名
    # 排名还需要加缓存
    sql = '''
    select user_id
    from summer2018_stu_open_box
    where subject_id = %s
    order by open_num desc, add_time desc 
    limit 500
    ''' % (subject_id)
    data = db.tbkt_active.fetchall_dict(sql)
    print data
    rank = 0
    for i in data:
        rank += 1
        if i.user_id == user_id:
            break
    else:
        rank = '500+'
    if isinstance(rank, int):
       rank = str(rank)
    return open_num, rank


def get_nowt_zero(nowt):
    # 利用当前年份和月份获取当天00:00分的时间戳
    nowt_year = time.localtime(nowt).tm_year
    nowt_month = time.localtime(nowt).tm_mon
    nowt_day = time.localtime(nowt).tm_mday
    a = "%s-%s-%s" % (nowt_year, nowt_month, nowt_day)
    timeArray = time.strptime(a, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


def get_box_status(user_id, subject_id, nowt):
    zero_time = get_nowt_zero(nowt)
    box_status = db.tbkt_active.summer2018_stu_box.select('copper', 'sliver', 'gold').get(user_id=user_id, subject_id=subject_id ,add_time__gt=zero_time)
    if box_status:
        return box_status
    else:
        db.tbkt_active.summer2018_stu_box.create(
            user_id=user_id,
            subject_id=subject_id,
            copper=0,
            sliver=0,
            gold=1,
            add_time=nowt
        )
        return {"copper":0, "sliver":0, "gold":1}


def get_month_day(nowt):
    #获取当前年月日 int
    time_str = '%s月%s日' % (time.localtime(nowt).tm_mon, time.localtime(nowt).tm_mday)
    return time_str


def get_hour_minute_sconed(nowt):
    time_str = '%s:%s:%s' % (time.localtime(nowt).tm_hour, time.localtime(nowt).tm_min, time.localtime(nowt).tm_sec)
    return time_str


def prize_draw(debris):
    # debris = {"hat":1, "shoe":1, "background":1, "pants":1, "cloth":1}
    more_equal_six = []
    less_six = []
    for i in debris.keys():
        if debris[i] >= 6:
            more_equal_six.append(i)
        else:
            less_six.append(i)
    if len(more_equal_six) == 5 or len(more_equal_six) == 0:
        # 等于或超过6片的碎片种类大于5 或 0
        random_int = random.randint(1, 5)
        if random_int == 1:
            return less_six[0]
        elif random_int == 2:
            return less_six[1]
        elif random_int == 3:
            return less_six[2]
        elif random_int == 4:
            return less_six[3]
        else:
            return less_six[4]
    elif len(more_equal_six) == 4:
        # 等于或超过6片的碎片种类大于4
        return less_six[0]
    elif len(more_equal_six) == 3:
        # 等于或超过6片的碎片种类大于3
        random_int = random.randint(1, 200)
        if random_int < 10:
            return more_equal_six[0]
        elif random_int < 20:
            return more_equal_six[1]
        elif random_int < 30:
            return more_equal_six[2]
        elif random_int < 115:
            return less_six[0]
        else:
            return less_six[1]
    elif len(more_equal_six) == 2:
        # 等于或超过6片的碎片种类大于2
        random_int = random.randint(1, 100)
        if random_int < 5:
            return more_equal_six[0]
        elif random_int < 10:
            return more_equal_six[1]
        elif random_int < 40:
            return less_six[0]
        elif random_int < 70:
            return less_six[1]
        else:
            return less_six[2]
    elif len(more_equal_six) == 1:
        # 等于或超过6片的碎片种类大于1
        random_int = random.randint(1, 200)
        if random_int < 20:
            return more_equal_six[0]
        elif random_int < 65:
            return less_six[0]
        elif random_int < 110:
            return less_six[1]
        elif random_int < 155:
            return less_six[2]
        else:
            return less_six[3]


def get_mission(subject_id, phase, grade_id):
    if subject_id == 5:
        # 语文
        mission =  u'yw_reading'
    elif subject_id == 9:
        # 英语
        mission = {0: u'打地鼠', 1: u'同步习题', 2: u'口语流利说', 3: u'情景对话', 4: u'课本点读机', 5: u'单词学习', 6: u'爆破气球'}
        now_week_day = int(time.time()) // 86400 % 7
        mission = mission.get(now_week_day, '')
    else:
        # 数学
        if phase == 1 and grade_id != 6:
            mission = u'sx_test'
        else:
            mission = u'sx_knowledge'
    return mission


def yw_index(user, subject_id, phase):
    nowt = int(time.time())
    user_id = user.id
    unit_id = user.unit.unit_class_id
    grade_id = user.grade_id
    data = {}
    # 注册活动, 获取开启次数和排名状态
    data['open_num'], data['rank'] = get_user_rank(user_id, subject_id, unit_id, phase)
    # 获取宝箱状态
    data['box_status'] = get_box_status(user_id, subject_id, nowt)
    # 获取碎片状态
    data['user_debris'] = get_debris(phase, subject_id, user_id, nowt, 'GET')
    # 获取消息数量
    data['message_num'] = db.tbkt_active.summer2018_stu_ask_info.select('id').filter(user_id=user_id, phase=phase).count()
    # 获取宝箱开启实况
    sql = '''
    select user_id, debris, add_time, debris_method, remark
    from summer2018_stu_debris_detail
    where subject_id=%s and debris_method = 'open'
    order by add_time desc 
    limit 100
    ''' % (subject_id)
    open_live = db.tbkt_active.fetchall_dict(sql)
    # 获取开箱实况的头像 编辑时间
    if not open_live:
        data['open_live'] = []
    else:
        user_ids = [s.user_id for s in open_live]
        user_name_id = db.tbkt_user_slave.auth_user.select('id', 'real_name').filter(user_id__in=user_ids)
        user_name_id = {s.id:s.real_name for s in user_name_id}
        for s in open_live:
            s.add_time = get_hour_minute_sconed(s.add_time)
            s.user_name = user_name_id.get(s.user_id, u'默认')
        data['open_live'] = open_live
    #阶段信息
    data['phase'] = phase
    # 获取任务信息
    data['mission'] = get_mission(subject_id, phase, grade_id)
    return data


def invite(user, subject_id, phase):
    one_day_after_nowt = int(time.time()) - 86400
    subject_id = subject_id
    # 班级里的学生
    all_students = db.ketang_slave.mobile_order_region.select('user_id').filter(user_type=1, unit_class_id=user.unit.unit_class_id)[:]
    all_students = [s.user_id for s in all_students]
    # 已参与学生
    if phase == 1:
        all_join_student = db.tbkt_active.summer2018_stu_open_box.select('user_id').filter(unit_id=user.unit.unit_class_id, subject_id=subject_id)[:]
    else:
        all_join_student = db.tbkt_active.summer2018_stu_open_box.select('user_id').filter(unit_id=user.unit.unit_class_id, add_time__gt=PHASE_2_START_TIME, subject_id=subject_id)[:]
    all_join_student = [s.user_id for s in all_join_student]
    print all_join_student
    # 24小时内已被邀请学生
    had_invited_stu = db.tbkt_active.summer2018_stu_invited.select('invited_user_id').filter(unit_id=user.unit.unit_class_id, add_time__gt=one_day_after_nowt, subject_id=subject_id)[:]
    had_invited_stu = [s.invited_user_id for s in had_invited_stu]
    # 可邀请学生的用户姓名 求差集
    can_invited_stu = list(set(all_students).difference(set(all_join_student + had_invited_stu)))
    user_names = db.tbkt_user_slave.auth_user.select('id', 'real_name').filter(id__in=can_invited_stu)[:]
    user_id_name_dict = {s.id: s.real_name for s in user_names}
    # 可邀请学生的用户头像
    user_portrait = db.tbkt_user_slave.auth_profile.select('user_id', 'portrait').filter(user_id__in=can_invited_stu)[:]
    for s in user_portrait:
        s.real_name = user_id_name_dict.get(s.user_id, '')
        s.portrait = get_absurl(s.portrait) if s.portrait else "http://res-hn.m.jxtbkt.cn/user_media/images/profile/default-student.png"

    return user_portrait


def do_invite(user, subject_id, phase, invite_id, ):
    nowt = int(time.time())
    one_day_after_nowt = nowt - 86400
    zero_time = get_nowt_zero(nowt)
    # 判断是否参与活动
    if phase == 1:
        join_status = db.tbkt_active.summer2018_stu_open_box.select('id').get(user_id=invite_id, subject_id=subject_id)
    else:
        join_status = db.tbkt_active.summer2018_stu_open_box.select('id').get(user_id=invite_id, add_time__gt=PHASE_2_START_TIME, subject_id=subject_id)
    if join_status:
        return u'该学生已经参加活动，不能邀请了'
    # 判断是否已被邀请
    invited_status = db.tbkt_active.summer2018_stu_invited.select('id').get(invited_user_id=invite_id, add_time__gt=one_day_after_nowt, phase=phase, subject_id=subject_id)
    if invited_status:
        return u'该学生已被其他学生邀请，不能邀请了'
    # 创建邀请信息
    db.tbkt_active.summer2018_stu_invited.create(
        user_id=user.id,
        invited_user_id=invite_id,
        subject_id=subject_id,
        phase=phase,
        unit_id=user.unit.unit_class_id,
        add_time=nowt
    )
    # 给与银宝箱的开启权限
    db.tbkt_active.summer2018_stu_box.filter(add_time__gt=zero_time, user_id=user.id).update(sliver=1)
    # 发送短信
    # ？？？？

    return None


def get_ask_message(user, subject_id, phase, page):
    '''
    @param user:
    @param subject_id:  科目id   2sx.5yw.9yy
    @param phase:  阶段id   1/2
    @return:
    '''
    page = (page-1)*20
    # 获取索要消息记录
    sql = '''
    select ask_for_user, ask_thing, add_time
    from summer2018_stu_ask_info
    where user_id=%s and subject_id=%s and phase=%s
    order by add_time desc
    limit %s, 20
    '''  % (user.id, subject_id, phase, page)
    message = db.tbkt_active.fetchall_dict(sql)
    # 获取索要用户姓名
    ask_user = [s.ask_for_user for s in message]
    user_names = db.tbkt_user_slave.auth_user.select('id', 'real_name').filter(id__in=ask_user)[:]
    user_id_name_dict = {s.id: s.real_name for s in user_names}
    # 修改时间显示方式和增加用户姓名
    for s in message:
        s.add_time = get_month_day(s.add_time)
        s.real_name = user_id_name_dict.get(s.ask_for_user, u'默认')

    return message


def get_debris_message(user, subject_id, phase, page):
    '''
    @param user:
    @param subject_id:  科目id   2sx.5yw.9yy
    @param phase:  阶段id   1/2
    @return:
    '''
    page = (page - 1) * 20
    # 获取消息记录
    sql = '''
    select debris, debris_method, remark, add_time 
    from summer2018_stu_debris_detail
    where user_id = %s and subject_id = %s and phase = %s 
    order by add_time desc
    limit %s, 20
    ''' % (user.id, subject_id, phase, page)
    message = db.tbkt_active.fetchall_dict(sql)
    # 编辑一下记录内容，方便前端显示
    content_array = []
    for s in message:
        content_dict = {}
        if s.debris_method == u'open':
            box_name = {u'copper': u'铜宝箱', u'sliver': u'银宝箱', u'gold': u'金宝箱'}
            content_dict['content'] = u'%s开启了%s获得' % (get_month_day(s.add_time), box_name.get(s.remark, u'宝箱'))
            content_dict['debris_num'] = u'+1'
        elif s.debris_method == u'give':
            content_dict['content'] = u'%s赠送了%s' % (get_month_day(s.add_time), s.remark)
            content_dict['debris_num'] = u'-1'
        elif s.debris_method == u'use':
            debris_name = {"hat": u'帽子道具', "shoe": u"鞋子道具", "background": u"背景道具", "pants": u'裤子道具', "cloth":u'上衣道具'}
            content_dict['content'] = u'%s合成了%s' % (get_month_day(s.add_time), debris_name.get(s.debris, '道具'))
            content_dict['debris_num'] = u'-6'
        elif s.debris_method == u'receive':
            content_dict['content'] = u'%s%s向你赠送了' % (get_month_day(s.add_time), s.remark)
            content_dict['debris_num'] = u'+1'
        content_dict['debris'] = s.debris
        content_array.append(content_dict)

    return content_array


def get_unit_student(user):
    # 班级下所有学生
    all_students = db.ketang_slave.mobile_order_region.select('user_id').filter(user_type=1, unit_class_id=user.unit.unit_class_id)[:]
    all_students = [s.user_id for s in all_students]
    # 获取用户真实姓名
    user_names = db.tbkt_user_slave.auth_user.select('id', 'real_name').filter(id__in=all_students)[:]
    user_id_name_dict = {s.id: s.real_name for s in user_names}
    # 获取所有学生的头像
    user_portrait = db.tbkt_user_slave.auth_profile.select('user_id', 'portrait').filter(user_id__in=all_students)[:]

    for s in user_portrait:
        s.real_name = user_id_name_dict.get(s.user_id, '')
        s.portrait = get_absurl(s.portrait) if s.portrait else "http://res-hn.m.jxtbkt.cn/user_media/images/profile/default-student.png"
    return user_portrait


def give_debris(user, give_user_id, phase, subject_id, debris):
    # 获取赠与者和接受者姓名
    nowt = int(time.time())
    giver_name = db.tbkt_user_slave.auth_user.select('id', 'real_name').get(id=user.id)
    receive_name = db.tbkt_user_slave.auth_user.select('id', 'real_name').get(id=give_user_id)
    # 赠与和接受
    message = get_debris(phase, subject_id, user.id, nowt, 'GIVE', debris, giver_name["real_name"])
    if message:
        return message
    message = get_debris(phase, subject_id, give_user_id, nowt, 'RECEIVE', debris, receive_name.real_name)
    if message:
        return message

    return None


def ask_for_debris(user, ask_for_id, phase, subject_id, debris):
    # 建立索要记录
    db.tbkt_active.summer2018_stu_ask_info.create(
        user_id=user.id,
        ask_for_user=ask_for_id,
        ask_thing=debris,
        add_time=int(time.time()),
        phase=phase,
        subject_id=subject_id,
    )
    return None


def open_my_box(user, box, phase, subject_id):
    # 验证是否能开宝箱
    nowt = int(time.time())
    zero_time = get_nowt_zero(nowt)
    box_status = get_box_status(user.id, subject_id, nowt)
    if box_status[box] != 1:
        return u'宝箱无法开启'
    if box == 'gold':
        user_score = db.tbkt_active.homepage_user.select('score').get(user_id=user.id)
        if not user_score or user_score.score < 30:
            return u'用户钻石不足'
        else:
            user_score = user_score.score - 30
            db.tbkt_active.homepage_user.filter(user_id=user.id).update(score=user_score)
            db.tbkt_active.homepage_user_detail.create(
                user_id=user.id,
                score=20,
                type=6,
                remark=u'活动开启金宝箱消耗30钻石',
                add_time=nowt
            )
    # 开宝箱
    open_box(phase, user.id, box, subject_id)
    # 更新宝箱状态
    update_sql = '''
    UPDATE summer2018_stu_box
    SET %s = 2
    WHERE add_time > %s and user_id= %s  and subject_id = %s
    ''' % (box, zero_time, user.id, subject_id)
    print update_sql
    db.tbkt_active.fetchone(update_sql)
    return None


def get_rank(user_id, page, subject_id, unit_id):
    datas = {}
    nowt = int(time.time())
    open_num = db.tbkt_active.summer2018_stu_open_box.select('open_num').get(user_id=user_id, subject_id=subject_id)
    if open_num:
        open_num = open_num.open_num
    else:
        #  头一次进入活动，
        #  注册活动
        db.tbkt_active.summer2018_stu_open_box.create(
            user_id=user_id,
            open_num=0,
            add_time=nowt,
            subject_id=subject_id,
            unit_id=unit_id
        )
        open_num = 0

    # 用户排名
    # 排名还需要加缓存
    sql = '''
       select user_id, open_num
       from summer2018_stu_open_box
       where subject_id = %s
       order by open_num desc, add_time desc 
       limit 500
       ''' % (subject_id)
    data = db.tbkt_active.fetchall_dict(sql)
    rank = 0
    for i in data:
        rank += 1
        if i.user_id == user_id:
            break
    else:
        rank = '500+'
    if isinstance(rank, int):
        rank = str(rank)
    datas['open_num'] = open_num
    datas['person_rank'] = rank
    sql = '''
       select user_id, open_num
       from summer2018_stu_open_box
       where subject_id = %s
       order by open_num desc, add_time desc 
       limit %s, 20
       ''' % (subject_id, (page-1)*20)
    ranks = db.tbkt_active.fetchall_dict(sql)
    user_ids = [s.user_id for s in ranks]
    user_name = db.tbkt_user_slave.auth_user.select('id', 'real_name').filter(id__in=user_ids)[:]
    user_name_dict = {s.id:s.real_name for s in user_name}
    user_school_name = db.ketang_slave.mobile_order_region.select('user_id', 'school_name').filter(user_id__in=user_ids)[:]
    user_school_name_dict = {s.user_id:s.school_name for s in user_school_name}
    for s in ranks:
        s.school_name = user_school_name_dict.get(s.user_id, '')
        s.real_name = user_name_dict.get(s.user_id, '')

    datas['rank'] = ranks

    return datas