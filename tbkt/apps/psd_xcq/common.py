#coding=utf-8
import time

from libs.utils import db, Struct
from libs.utils import ajax_json, ajax_try
from com.com_user import need_login
from com.com_cache import cache

PAGE_COUNT = 10
ITEM_NO_MATK = {11: '分享'}


def update_score(user, app_id, item_no, score, now, school_id):
    """
    更新积分
    :param user_id:
    :param app_id:
    :param item_no:     1: 分享，
    :return:
    :author: 张嘉麒
    """
    user_app = db.default.score_user.select('id', 'score').get(user_id=user.id, app_id=app_id)
    if not user_app:
        # 第一次参见活动
        new_user_app = db.default.score_user.create(user_id=user.id, score=score, app_id=app_id,
                                                    unit_id=school_id)
        new_user_app_detail = db.default.score_user_detail.create(user_id=user.id, item_no=item_no, score=score,
                                                                  app_id=app_id, add_date=now, remark=ITEM_NO_MATK[item_no])
    else:
        # 多次参加活动
        new_score = user_app.score + score
        db.default.score_user.filter(id=user_app.id).update(score=new_score,  unit_id=school_id)
        new_user_app_detail = db.default.score_user_detail.create(user_id=user.id, item_no=item_no, score=score,
                                                                  app_id=app_id, add_date=now, remark=ITEM_NO_MATK[item_no])
    return True


def get_nowt_zero(nowt):
    # 利用当前年份和月份获取当天00:00分的时间戳
    nowt_year = time.localtime(nowt).tm_year
    nowt_month = time.localtime(nowt).tm_mon
    nowt_day = time.localtime(nowt).tm_mday
    a = "%s-%s-%s" % (nowt_year, nowt_month, nowt_day)
    timeArray = time.strptime(a, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


def pds_share(user, app_id, school_id):
    '''
    :param user:  user
    :param app_id:  34 这次的平顶山某小学活动
    :param school_id:  学校id
    :return:
    '''
    nowt = int(time.time())
    ling_time = get_nowt_zero(nowt)  # 得到现在时间的零点
    today_do = db.default.score_user_detail.select('id').get(user_id=user.id, item_no=11, app_id=app_id,
                                                             add_date__gte=ling_time)
    if today_do:
        # 签到过的用户再次签到，返回今日已签到
        return u'今日已签到'
    else:
        # 未签到用户查询历史签到分数
        yesterday_do = db.default.score_user_detail.select('id', 'score').get(user_id=user.id, item_no=11, app_id=app_id,
                                                                 add_date__gte=ling_time-86400, add_date__lt=ling_time)
        if yesterday_do:
            # 最高30分
            score = yesterday_do.score + 10 if yesterday_do.score + 10 <= 30 else 30

            update_score(user, app_id, 11, score, nowt, school_id)
        else:
            #签到断了的用户10分
            score = 10
            update_score(user, app_id, 11, score, nowt, school_id)

        return u'签到成功+%s分' % score


def index(user, app_id):
    """
    :param user:
    :return:
    """

    data = Struct()
    # 未参加用户默认排名为0分数为0
    data['score'] = 0
    data['rank_no'] = 0
    score_user = db.default.score_user.select('score').get(user_id=user.id, app_id=app_id)
    if not score_user:
        return data
    else:
        sql = '''
        SELECT
        s.user_id,s.score
        FROM
        (SELECT user_id,MAX(add_date) AS add_date FROM score_user_detail WHERE app_id=37 GROUP BY user_id) AS p 
        INNER JOIN
        score_user s
        ON s.user_id=p.user_id AND s.app_id=37 
        ORDER BY -s.score,p.add_date;
        '''
        score_user = db.default.fetchall_dict(sql)
        for su in score_user:
            data['rank_no'] += 1
            if su.user_id == user.id:
                data['score'] = su.score
                return data


def user_rank(page_no, app_id):
    page_size = 10

    start = (page_no - 1) * page_size
    end = page_no * page_size

    sql = '''
    SELECT
    s.user_id,s.score
    FROM
    (SELECT user_id,MAX(add_date) AS add_date FROM score_user_detail WHERE app_id=37 GROUP BY user_id) AS p 
    INNER JOIN
    score_user s
    ON s.user_id=p.user_id AND s.app_id=37 
    ORDER BY -s.score,p.add_date
    limit %s, 10;
    ''' % (start)
    score_user = db.default.fetchall_dict(sql)
    # score_user = db.default.score_user.select('user_id', 'score').filter(app_id=app_id).order_by('-score', 'id')[start:end]
    # print score_user
    user_ids = [d.user_id for d in score_user]
    user_names = db.tbkt_user.auth_user.select('real_name', 'id').filter(id__in=user_ids)[:]
    user_name_map = {d.id:d.real_name for d in user_names}
    class_user_ids = db.ketang.mobile_order_region.select('user_id', 'unit_class_id').filter(user_id__in=user_ids)[:]
    class_user_id_map = {d.user_id:d.unit_class_id for d in class_user_ids}
    class_ids = [d.unit_class_id for d in class_user_ids]
    class_names = db.default.school_unit_class.select('id', 'unit_name').filter(id__in=class_ids)[:]
    class_map = {d.id : d.unit_name for d in class_names}
    # print class_user_id_map, class_map, user_name_map
    for i in score_user:
        class_id = class_user_id_map.get(i.user_id, '')
        i.class_name = class_map.get(class_id, '')
        i.user_name = user_name_map.get(i.user_id, '')
    return score_user