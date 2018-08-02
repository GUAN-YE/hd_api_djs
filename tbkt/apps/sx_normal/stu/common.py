# coding:utf-8
import datetime
import time
from libs.utils import db


def three_date_temp():
    # 返回昨天 前天 大前天 日期 方便做签到判断
    to_day = datetime.date.today()
    out = []
    for i in range(1, 4):
        day = to_day - datetime.timedelta(days=i)
        out.append(int(time.mktime(day.timetuple())))
    return out


def today_temp():
    to_day = datetime.datetime.now()
    d = datetime.datetime(to_day.year, to_day.month, to_day.day, 0, 0, 0)
    return int(time.mktime(d.timetuple()))


def sign_status(user_id, item_no, active_id):
    # 签到状态
    temp = today_temp()
    sign = db.tbkt_active.active_score_user_detail.get(user_id=user_id, item_no=item_no, add_date__gte=temp,
                                                       active_id=active_id)
    return True if sign else False


def stu_sign(user, active_id, item_no):
    """签到"""
    now = int(time.time())
    if sign_status(user.id, item_no, active_id):
        return False, u'已签到'

    yesterday = today_temp() - 60 * 60 * 24
    sql = """select item_no,remark from active_score_user_detail
    where user_id=%s and active_id=%s and item_no ='%s' and add_date BETWEEN %s and %s
    """ % (user.id, active_id, item_no, yesterday, today_temp())
    row = db.tbkt_active.fetchone_dict(sql)
    num = 0
    if row:
        num = abs(int(row.remark.split('_')[-1]))
    score = (num + 1) * 10
    if num >= 5:
        score = 50

    # open_status = user.openstatus(2)
    # score = score * 2 if open_status else score
    _remark = u'签到获取%s积分' % score
    remark = u'签到获取%s积分_%s' % (score, num + 1)
    db.tbkt_active.active_score_user_detail.create(user_id=user.id,
                                                   item_no=item_no,
                                                   score=score,
                                                   remark=remark,
                                                   add_date=now,
                                                   active_id=active_id,
                                                   add_username=user.id,
                                                   affix_info='')
    save_score(user, active_id, score)
    return True, _remark


def _stu_sign(user, active_id, item_no):
    # 签到
    now = int(time.time())
    if sign_status(user.id, item_no, active_id):
        return False, u'已签到'
    three_day = three_date_temp()
    score = 10
    dd = db.tbkt_active
    done_sign = dd.active_score_user_detail.filter(user_id=user.id, item_no=item_no,
                                                   add_date__range=(three_day[1], today_temp()),
                                                   active_id=active_id).order_by('add_date desc').flat('add_date')[:]
    if done_sign:
        if len(done_sign) == 3:
            score = 30
        else:
            yesterday = three_day[0]  # 昨天时间
            anteayer = three_day[1]  # 前天时间

            arry = []
            for i in done_sign:
                new_date = from_unixtime(i).replace(hour=0, minute=0, second=0)
                arry.append(int(int(time.mktime(new_date.timetuple()))))
            if yesterday not in arry:
                # 如果昨天没有签到 说明断签 积分重置
                score = 10
            else:
                if anteayer not in arry:
                    # 如果前天没有签到 说明已签到一天 积分+10
                    score = 20
                else:
                    # 说明连续签到2天
                    score = 30

    open_status = user.openstatus(2)
    score = score * 2 if open_status else score
    remark = u'签到获取%s积分' % score
    db.tbkt_active.active_score_user_detail.create(user_id=user.id,
                                                   item_no=item_no,
                                                   score=score,
                                                   remark=remark,
                                                   add_date=now,
                                                   active_id=active_id,
                                                   add_username=user.id,
                                                   affix_info='')
    save_score(user, active_id, score)
    return True, remark


def save_score(user, active_id, score):
    # 添加总积分
    user_score = db.tbkt_active_slave.active_score_user.get(user_id=user.id, active_id=active_id)
    if user_score:
        sql = """
        update active_score_user set score = %s where id = %s
        """ % (user_score.score + score, user_score.id)
        db.tbkt_active.execute(sql)
    else:
        db.tbkt_active.active_score_user.create(user_id=user.id,
                                                score=score,
                                                active_id=active_id,
                                                city=user.city,
                                                unit_id=user.unit.id)


def get_user_share(user_id, active_id, item_no):
    day_temp = today_temp()
    d = db.tbkt_active.active_score_user_detail.get(
        user_id=user_id, active_id=active_id, item_no=item_no, add_date__gte=day_temp)
    if d:
        return False
    return True


def from_unixtime(stamp):
    """时间戳转Datetime"""
    if not isinstance(stamp, (int, long)):
        return stamp
    st = time.localtime(stamp)
    return datetime.datetime(*st[:6])
