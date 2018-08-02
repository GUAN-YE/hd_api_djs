#coding=utf-8

"""
@varsion: ??
@author: 张嘉麒
@file: urls.py
@time: 2018/1/16 17:30
"""
import json
import random
import time

from libs.utils import db, Struct, join, get_absurl
from libs.utils.common import replace_url_ziyaun
from tbkt.settings import FILE_MEDIA_URLROOT, FILE_VIEW_URLROOT
from com.com_user import get_open_status, get_portrait


def get_day_first(nowt_year, nowt_month, now_day):
    # 获取当天第一秒时间戳
    a = "%s-%s-%s" % (nowt_year, nowt_month, now_day)
    timeArray = time.strptime(a, "%Y-%m-%d")
    timeStamp = int(time.mktime(timeArray))
    return timeStamp


def get_year(nowt):
    #获取当前年份 int
    return time.localtime(nowt).tm_year


def get_month(nowt):
    #获取当前月份 int
    return time.localtime(nowt).tm_mon


def get_day(nowt):
    #获取当前日期 int
    return time.localtime(nowt).tm_mday


def operate_coin(user_id, status, operate_num, nowt, way):
    '''
    :param user_id: 用户id
    :param status:  加分 1  扣分 0
    :param operate_num:  加扣数量
    :param way:  加分途径  0：登录获得, 1：开通获得 , 2：PK获得
    :return: None
    '''
    data = db.tbkt_active.winter_user_score.select('score').get(user_id=user_id, type=1)
    remark = [u'连续登录获得', u'开通大礼包获得', u'PK获得']
    item_no = [u'login', u'open', u'pk']
    detail = u'%s月%s日通过%s<span style="color:#e42a39">%s积分</span>' % (get_month(nowt), get_day(nowt), remark[way], operate_num)
    if way == 2:
        detail = u'%s月%s日通过%s<span style="color:#e42a39">%s积分</span>, <span style="color:#e42a39">能量值-1</span>' % (get_month(nowt), get_day(nowt), remark[way], operate_num)
    if status:
        data['score'] += operate_num
    else:
        data['score'] -= operate_num
    db.tbkt_active.winter_user_score.filter(user_id=user_id, type=1).update(score=data['score'])
    score_id = db.tbkt_active.winter_user_score.select('id').get(user_id=user_id, type=1)
    score_id = score_id['id']
    score_detail_id = db.tbkt_active.winter_user_score_detail.create(
        user_id=user_id,
        score=operate_num,
        type=1,
        remark=detail,
        item_no=item_no[way],
        add_time=nowt,
    )
    return [score_id, score_detail_id]


def operate_props(user_id, status, operate_num, nowt, way):
    '''
    :param user_id: 用户id
    :param status:  加道具 1  扣道具 0
    :param operate_num={type:operate_num}:  1：鲜花，2：鸡蛋，3：墨镜，4：橡皮擦，5：放大镜，6：超级翻倍卡
    :param way:  加道具途径  0：每日赠送, 1：开通获得 , 2：PK获得， 3：登录获得， 4：PK使用消耗
    :return: None
    '''
    remark = [u'每日赠送', u'开通获得', u'PK获得', u'登录获得', u'PK使用消耗']
    types = dict.keys(operate_num)  # [1：鲜花，2：鸡蛋，3：墨镜，4：橡皮擦，5：放大镜，6：超级翻倍卡]
    props_info = db.tbkt_active.winter_tools.select('tools').get(user_id=user_id)
    props_info = json.loads(props_info['tools'])
    for _type in types:
        if status:
            props_info[str(_type)] += operate_num[_type]
        else:
            props_info[str(_type)] -= operate_num[_type]
        if operate_num[_type]:
            db.tbkt_active.winter_tools_detail.create(
                user_id=user_id,
                type=2 if not status else 1,
                tools=_type,
                remark=remark[way],
                add_time=nowt,
        )
    props_info = json.dumps(props_info)
    print props_info
    db.tbkt_active.winter_tools.filter(user_id=user_id).update(tools=props_info)


def operate_power(user_id, status, operate_num, nowt):
    '''
    :param user_id: 用户id
    :param status:  加能量值 1  扣能量值 0   邀请获得 2   礼包获得 3
    :param operate_num： 加扣数量
    :return: None
    '''
    nowday = get_day(nowt)
    data = db.tbkt_active.winter_user_score.select('score').get(user_id=user_id, type=2, day=nowday)
    if not data:
        db.tbkt_active.winter_user_score.create(
            user_id=user_id,
            score=5,
            type=2,
            day=nowday,
            add_time=nowt
        )
        data['score'] = 5
    remark = [u'PK扣除', u'连续登录获得', u'邀请获得', u'开通大礼包获得']
    if status == 0:
        # PK只扣除能量值返回明细id， PK成功则删除这一条数据
        if status:
            data['score'] += operate_num
        else:
            data['score'] -= operate_num
        db.tbkt_active.winter_user_score.filter(user_id=user_id, type=2).update(score=data['score'])
        detail = u'%s月%s日未完成PK，<span style="color:#e42a39">能量值-%s</span>' % (get_month(nowt), nowday, operate_num)
        pk_id = db.tbkt_active.winter_user_score_detail.create(
            user_id=user_id,
            score=1,
            type=2,
            remark=detail,
            item_no='energy',
            add_time=nowt,
        )
        return pk_id
    else:
        detail = u'%s月%s日通过%s<span style="color:#e42a39">%s个能量值</span>' % (get_month(nowt) ,nowday, remark[status], operate_num)
        item_no = [u'energy', u'share']
        if status:
            data['score'] += operate_num
        else:
            data['score'] -= operate_num
        db.tbkt_active.winter_user_score.filter(user_id=user_id, type=2).update(score=data['score'])
        db.tbkt_active.winter_user_score_detail.create(
            user_id=user_id,
            score=operate_num,
            type=2,
            remark=detail,
            item_no=item_no[0] if status != 2 else item_no[1],
            add_time=nowt,
        )
        return None


def operate_happy_coin(user_id, operate_num, nowt):
    nowday = get_day(nowt)
    data = db.tbkt_active.winter_user_score.select('score').get(user_id=user_id, type=1)
    remark = u'%s月%s日欢乐竞技场获得<span style="color:#e42a39">%s积分</span>' % (get_month(nowt), nowday, operate_num)
    item_no = u'pk'
    data['score'] += operate_num
    db.tbkt_active.winter_user_score.filter(user_id=user_id, type=1).update(score=data['score'])
    score_id = db.tbkt_active.winter_user_score.select('id').get(user_id=user_id, type=1)
    score_id = score_id['id']
    score_detail_id = db.tbkt_active.winter_user_score_detail.create(
        user_id=user_id,
        score=operate_num,
        type=1,
        remark=remark,
        item_no=item_no,
        add_time=nowt,
    )
    data = db.tbkt_active.winter_happy_score.select('score').get(user_id=user_id, day=nowday)
    if not data:
        happy_score_id = db.tbkt_active.winter_happy_score.create(
            user_id=user_id,
            score=operate_num,
            day=nowday,
            add_time=nowt
        )
    else:
        data = db.tbkt_active.winter_happy_score.select('score').get(user_id=user_id, day=nowday)
        data['score'] += operate_num
        db.tbkt_active.winter_happy_score.filter(user_id=user_id, day=nowday).update(score=data['score'])
        happy_score_id = db.tbkt_active.winter_happy_score.select('id').get(user_id=user_id, day=nowday)
        happy_score_id = happy_score_id['id']
    return [score_id, score_detail_id, happy_score_id]


def get_user_open_status(user_id):
    #验证用户开通数量
    subject_num = 0
    open_datas = get_open_status(user_id, [2, 5, 9])
    for open_data in open_datas:
        if open_data['status'] == 1:
            subject_num += 1

    return subject_num


def get_user_info(user_id):
    '''
    获取活动入口所需数据
    '''

    nowt = time.time()
    nowday = get_day(nowt)

    # 获取开通科目数量  0 1 2 3
    open_status = get_user_open_status(user_id)

    # 获取连续登录日期, 并增加积分与道具
    login_info = db.tbkt_active.winter_user_sign.select('num', 'update_time', 'had_receive').get(user_id=user_id)
    # 头一次登录，增加道具信息，积分信息与登录信息
    if not login_info:
        db.tbkt_active.winter_user_sign.create(
            user_id=user_id,
            num=1,
            update_time=nowt,
        )
        login_day = 1
        had_receive = 0
        # 首次登录增加道具信息， 但不增加道具
        add_stage_property_and_score(login_day, user_id, nowt)
    # 连续登录增加道具
    else:
        login_info_update_time = get_day(login_info['update_time'])
        if login_info_update_time == 31:
            login_info_update_time = 0
        if login_info_update_time < nowday: # 判断是否连续登录 更新连续登录日期 添加道具与积分
            if nowday - login_info_update_time == 1:
                # 开通用户每日头一次登录每种道具送一个
                if open_status:
                    operate_props(user_id, 1, {1:1,2:1,3:1,4:1,5:1,6:1}, nowt, 0)

                # 连续登录增加道具
                login_day = login_info['num'] + 1
                add_stage_property_and_score(login_day, user_id, nowt)
                if login_day == 8:
                    # 第八天要还原成上个周期来赠送道具和积分 也就是第九天登录按第二天计算
                    login_day = 1
                    db.tbkt_active.winter_user_sign.filter(user_id=user_id).update(num=login_day, update_time=nowt)
                    login_day = 8
                else:
                    db.tbkt_active.winter_user_sign.filter(user_id=user_id).update(num=login_day, update_time=nowt)
            else:
                db.tbkt_active.winter_user_sign.filter(user_id=user_id).update(num=1, update_time=nowt)
                login_day = 1
        elif login_info_update_time == nowday:
            # 今天登陆过 不增加道具
            login_day = login_info['num']
        else:
            db.tbkt_active.winter_user_sign.filter(user_id=user_id).update(update_time=nowt)
            login_day = 1
        had_receive = login_info['had_receive']

    # 获取能量值
    data = db.tbkt_active.winter_user_score.select('score').get(user_id=user_id, type=2, day=nowday)
    if not data:
        score = 5 if open_status > 0 else 3
        db.tbkt_active.winter_user_score.create(
            user_id=user_id,
            type=2,
            day=nowday,
            add_time=nowt,
            score=score,
        )
        db.tbkt_active.winter_user_score_detail.create(
            user_id=user_id,
            score=score,
            type=2,
            remark='%s月%s日登陆获取<span style="color:#e42a39">%s个能量值</span>' % (get_month(nowt), nowday, score),
            item_no='energy',
            add_time=nowt,
        )
    data = db.tbkt_active.winter_user_score.select('score').get(user_id=user_id, type=2, day=nowday)
    data['power_num'] = data.score

    # 判断是否领取过大礼包
    if open_status - had_receive > 0:
        take_a_big_gift = open_status - had_receive
        for i in range(take_a_big_gift):
            get_a_big_gift(user_id, nowt)
        db.tbkt_active.winter_user_sign.filter(user_id=user_id).update(had_receive=open_status)
        # 获取领取大礼包后的能量值
        data = db.tbkt_active.winter_user_score.select('score').get(user_id=user_id, type=2, day=nowday)
        data['power_num'] = data.score
    else:
        take_a_big_gift = 0


    # 获奖通知
    notice = db.tbkt_active.winter_user_award.select('award_id', 'day').get(user_id=user_id, notice_status=0)
    if notice:
        award_day = notice['day']
        notice = notice['award_id']
        db.tbkt_active.winter_user_award.filter(user_id=user_id, notice_status=0).update(notice_status=1)
    else:
        award_day = 0
        notice = 0

    # 获取积分
    score = db.tbkt_active.winter_user_score.select('score').get(user_id=user_id, type=1)
    if not score:
        db.tbkt_active.winter_user_score.create(
            user_id=user_id,
            type=1,
            day=0,
            add_time=nowt,
            score=0
        )
        score = 0
    else:
        score = score.score

    # 获取奖品列表
    award_info = db.tbkt_active.winter_award.select('id', 'name', 'image_url').filter(status=1).order_by('seq')[:]
    for award in award_info:
        award['image_url'] = get_absurl(award['image_url'])

    # 获取排名
    range_num = db.tbkt_active.winter_user_score.select('id').filter(score__gt=score, type=1)
    range_num = range_num.count() + 1

    data['notice'] = notice
    data['range_num'] = range_num
    data['award_info'] = award_info
    data['login_day'] = login_day
    data['open_status'] = open_status
    data['score'] = score
    data['take_a_big_gift'] = take_a_big_gift
    data['award_day'] = award_day

    return data


def add_stage_property_and_score(day_num, user_id, nowt):
    '''
    连续登录增加道具积分
    '''
    if day_num % 8 == 1:
        # 头一天登录增加道具与积分信息
        stage_info = db.tbkt_active.winter_tools.select('id').get(user_id=user_id)
        if not stage_info:
            data = {1:0, 2:0, 3:0, 4:0, 5:0, 6:0} # 1：鲜花，2：鸡蛋，3：墨镜，4：橡皮擦，5：放大镜，6：超级翻倍卡
            json_str = json.dumps(data)
            db.tbkt_active.winter_tools.create(
                user_id=user_id,
                add_time=nowt,
                tools=json_str,
            )
        score_info = db.tbkt_active.winter_user_score.get(user_id=user_id, type=1)
        if not score_info:
            db.tbkt_active.winter_user_score.create(
                user_id=user_id,
                score=0,
                type=1,
                day=0,
                add_time=nowt
            )
    if day_num % 8 == 2:
        add_score_and_stage(1, user_id, nowt, 2, 11) # 鲜花+11积分
    if day_num % 8 == 3:
        add_score_and_stage(2, user_id, nowt, 3, 22) # 鸡蛋+22积分
    if day_num % 8 == 4:
        add_score_and_stage(3, user_id, nowt, 4, 33) # 墨镜+33积分
    if day_num % 8 == 5:
        add_score_and_stage(4, user_id, nowt, 5, 44) # 橡皮擦+44积分
    if day_num % 8 == 6:
        add_score_and_stage(5, user_id, nowt, 6, 55) # 放大镜+55积分
    if day_num % 8 == 7:
        add_score_and_stage(6, user_id, nowt, 7, 66) # 超级翻倍卡+66积分
    if day_num % 8 == 0:
        add_score_and_stage(6, user_id, nowt, 8, 66, 2)# 超级翻倍卡+66积分


def add_score_and_stage(add_item, user_id, nowt, login_day, add_score, add_item_num=1):
    # 增加道具与积分
    stage_info = {1:u'鲜花', 2:u'鸡蛋', 3:u'墨镜', 4:u'橡皮擦', 5:u'放大镜', 6:u'超级翻倍卡'}
    json_str = db.tbkt_active.winter_tools.select('tools').get(user_id=user_id)
    json_str = json.loads(json_str['tools'])
    json_str[str(add_item)] += add_item_num
    json_str = json.dumps(json_str)
    db.tbkt_active.winter_tools.filter(user_id=user_id).update(tools=json_str)
    db.tbkt_active.winter_tools_detail.create(
        user_id=user_id,
        type=1,
        tools=1,
        remark='连续登陆%s天获得%s个%s' % (login_day, add_item_num, stage_info[add_item]),
        add_time=nowt,
    )
    score = db.tbkt_active.winter_user_score.select('score').get(user_id=user_id, type=1)
    db.tbkt_active.winter_user_score.filter(user_id=user_id, type=1).update(score=score.score+add_score)
    db.tbkt_active.winter_user_score_detail.create(
        user_id=user_id,
        score=add_score,
        type=1,
        remark='连续登陆%s天获得<span style="color:#e42a39">%s积分</span>' % (login_day, add_score),
        item_no='login',
        add_time=nowt,
    )


def get_a_big_gift(user_id, nowt):
    # 获得大礼包
    operate_props(user_id, 1, {1:1, 2:1, 3:1, 4:1, 5:1, 6:1}, nowt, 1)
    operate_coin(user_id, 1, 500, nowt, 1)
    operate_power(user_id, 3, 5, nowt)


def get_user_match(user_id, school_id, class_id, province_id, pk_type):
    """
    成语游戏模块选择对手、获取信息
    :return:
    """

    # 通过用户id取出用户边框
    sql_one = "SELECT id  FROM winter_pk_record_new where type = %s and user_id <> %s " % (pk_type, user_id)
    sql_data = "SELECT user_id,user_object,user_time,score,right_num FROM winter_pk_record_new where type = %s and user_id <> %s " % (
        pk_type, user_id)

    sql1 = "and class_id= %s" % class_id
    sql2 = "and school_id= %s" % school_id
    sql3 = "and province_id= %s" % province_id
    data = ""
    for i in [sql1, sql2, sql3, ' ']:
        sql_begin = sql_one + i + " order by id limit 1"
        sql_last = sql_one + i + " order by id desc limit 1"
        pk_record_begin = db.tbkt_active.fetchone(sql_begin)
        pk_record_last = db.tbkt_active.fetchone(sql_last)
        if pk_record_begin and pk_record_last:
            id_begin = pk_record_begin[0]
            # return id_begin
            id_last = pk_record_last[0]
            count = random.randint(id_begin, id_last)
            count = count - 1
            sql = sql_data + i + " and id > %s limit 1" % count
            data = db.tbkt_active.fetchone_dict(sql)
            break

    return data


def pk_user_info(user_id, school_id, class_id, province, pk_type):
    """
    :param user_id:
    :param school_id:
    :param class_id:
    :param province:
    :param pk_type:
    :return:
    """
    info = get_user_match(user_id, school_id, class_id, province, pk_type)
    pk_user_id = info.user_id
    pk_border = db.default.user_border_detail.get(user_id=pk_user_id, status=1)
    pk_user_profile = db.tbkt_user_slave.auth_profile.select("portrait").get(user_id=pk_user_id)
    pk_user_img = get_portrait(None, 1, pk_user_profile.portrait)
    if not pk_border:
        info['border_url'] = ""
    else:
        pk_user_border = db.default.border.get(id=pk_border.border_id)
        if not pk_user_border:
            info['border_url'] = ""
        else:
            pk_border_url = pk_user_border.border_url
            info['border_url'] = get_absurl(pk_border_url)
    user_object = json.loads(info.user_object or {})
    user_object["img"] = pk_user_img
    info.user_object = json.dumps(user_object)
    return info


def get_user_props(user_id):
    # 获取用户的道具
    props_info = db.tbkt_active.winter_tools.select('tools').get(user_id=user_id)
    props_value = decode_json_get_value(props_info.tools)
    return props_value


def get_poetry():
    """
    学生端 诗词pk模块资源接口
    :return:
    """
    sql = "SELECT po_ID,qu_TitleDry,qu_OptionA,qu_OptionB,qu_OptionC,qu_OptionD,qu_TrueOption FROM yw_poetry_question where qu_Status = 0 and enable_flag=0  ORDER BY rand() LIMIT 10"
    topic_db = db.tbkt_yw_slave.fetchall_dict(sql)
    po_ids = [int(topic.po_ID) for topic in topic_db]

    sql = "select po_ID,po_Name,po_Author from yw_poetry where po_ID in  %s " % str(tuple(po_ids))
    poetry_db = db.tbkt_yw_slave.fetchall_dict(sql)

    po_Name_dict = {poetry.po_ID: [poetry.po_Name, poetry.po_Author] for poetry in poetry_db}
    for topic in topic_db:
        topic.have_glass = 1 if random.randint(0, 24) == 0 else 0
        po_name = po_Name_dict.get(int(topic.po_ID))
        topic['po_Name'] = po_name[0] if po_name else ''
        topic['po_Author'] = po_name[1] if po_name else ''
        # 获取答案 返回给前端   测试将所有Unicode字符串str
        _key = 'qu_Option' + str(topic['qu_TrueOption'])
        answer1 = topic[_key]
        answer2 = str(topic['qu_TitleDry']).replace('_', '').replace('。', '').replace('，', '')
        answer3 = str(topic['qu_TitleDry'])
        if answer3.startswith('_'):
            answer = answer1 + '，' + answer2 + '。'
        else:
            answer = answer2 + '，' + answer1 + '。'
        topic['answer'] = answer.decode('utf-8')

    return topic_db


def get_idiom():
    """
    学生端 成语pk模块资源接口
    :return:
    """
    sql = "SELECT cy_Content,cy_Explain,cy_Tupian,cy_Source FROM yw_phrase where cy_Status = 0 and enable_flag=0 and cy_Type=0  ORDER BY rand() LIMIT 5"
    topic_db = db.tbkt_yw_slave.fetchall_dict(sql)
    sql = '''SELECT wl_Content from yw_wordslib where wl_Type = 0 and wl_Status = 0 and enable_flag = 0 ORDER BY RAND() LIMIT 14'''
    wordslib = db.tbkt_yw_slave.fetchall(sql)
    wordslib = [words[0] for words in wordslib]
    for topic in topic_db:
        topic.have_glass = 1 if random.randint(0, 24) == 0 else 0
        topic.cy_Tupian = replace_url_ziyaun(topic.cy_Tupian)
        print 111, topic.cy_Tupian
        li = wordslib + list(topic.cy_Content)
        random.shuffle(li)
        topic['words_list'] = li

    return topic_db


def post_pk_details(user_id, add_time, right_num, user_time, score, user_object, pk_user, result, school_id,
                    province_id, class_id, is_type, pk_id):
    """

    :param user_id: 用户id
    :param add_time: pk开始时间
    :param right_num: 答对题数
    :param user_time: 时长
    :param score: 总数
    :param user_object: 用户的信息:头像路径、姓名、user_id、学校名称
    :param pk_user: 挑战对象的信息:头像路径、姓名、user_id
    :param result: 结果1.赢了，2.输了
    :param school_id: 学校id
    :param province_id: 省份id
    :param class_id: 班级id
    :param is_type: 1.诗词大战pk,2.成语游戏pk
    :return:
    """
    # 增加用户对战记录，增加用户积分以及道具，增加积分明细和道具明细
    add_time = int(time.time())
    pk_record_id = db.tbkt_active.winter_pk_record_new.create(type=is_type,
                                          user_id=user_id,
                                          right_num=right_num,
                                          user_time=user_time,
                                          score=score,
                                          user_object=json.dumps(user_object),
                                          pk_user=json.dumps(pk_user),
                                          result=result,
                                          add_time=add_time,
                                          school_id=school_id,
                                          class_id=class_id,
                                          province_id=province_id
                                          )
    if result == 1:
        score = score + 5
        # 胜利随机给1个道具增加与记录增加
        add_type = random.randint(1,6)
        props_dict = {add_type:1}
        operate_props(user_id, 1, props_dict, add_time, 2)
    else:
        add_type = 0

    # 积分增加与记录增加
    if pk_id:
        db.tbkt_active.winter_user_score_detail.filter(id=pk_id).delete()
    coin_id = operate_coin(user_id, 1, score, add_time, 2)
    data = Struct()
    data['add_type'] = add_type
    coin_id.append(pk_record_id)
    data['ids'] = coin_id
    return data


def post_props_details(user_id, has_use_double, has_use_flower, has_use_egg, has_use_sunglasses, has_use_magnifier,
                       has_use_eraser, add_time):
    # 将使用过的道具扣除，并更新使用道具明细表
    props_dict = {1: has_use_flower, 2: has_use_egg, 3: has_use_sunglasses, 4: has_use_eraser,
                  5: has_use_magnifier, 6: has_use_double}
    props_name_dict = {1: '鲜花', 2: '鸡蛋', 3: '墨镜', 4: '橡皮擦',
                  5: '放大镜', 6: '超级翻倍卡'}

    # 道具数量小于0则不让使用
    props_info = db.tbkt_active.winter_tools.select('tools').get(user_id=user_id)
    for i in range(1,7):
        if props_info['tools'][i] < props_dict[i]:
            return u'您的%s道具数量不足' % props_name_dict[i]

    add_time = int(time.time())
    operate_props(user_id, 0, props_dict, add_time, 4)
    return None


def get_user_power(user_id):
    # 获取用户的能量值
    nowday = get_day(time.time())
    power_num = db.tbkt_active.winter_user_score.select('score').get(user_id=user_id, type=2, day=nowday)
    if power_num.score > 0:
        return True
    else:
        return False


def time_limmit():
    # 时间是否在18-20店内 是则返回True 不是则返回False
    nowt = time.time()
    nowhour = time.localtime(nowt).tm_hour
    if nowhour >= 18 and nowhour < 20:     # 上正式的时候加上限制 大于等于18 小于20
        return True
    else:
        return False


def get_type(user_id):
    # 看下一场参加啥项目 单数参加成语 双数参加唐诗
    type = db.tbkt_active.winter_pk_record_new.select('id').filter(user_id=user_id, type=3).count()
    if type % 2 == 0:
        type = 1
    else:
        type = 2
    data = Struct()
    data['type'] = type
    return data


def post_happy_pk_details(user_id, add_time, right_num, user_time, score, user_object, pk_user, result, school_id,
                    province_id, class_id, is_type):
    """

    :param user_id: 用户id
    :param add_time: pk开始时间
    :param right_num: 答对题数
    :param user_time: 时长
    :param score: 总数
    :param user_object: 用户的信息:头像路径、姓名、user_id、学校名称
    :param pk_user: 挑战对象的信息:头像路径、姓名、user_id
    :param result: 结果1.赢了，2.输了
    :param school_id: 学校id
    :param province_id: 省份id
    :param class_id: 班级id
    :param is_type: 1.诗词大战pk,2.成语游戏pk
    :return:
    """
    # 增加用户欢乐竞技场对战记录，增加用户积分以及道具，增加积分明细和道具明细
    add_time = int(time.time())
    pk_happy_record_id = db.tbkt_active.winter_pk_record_new.create(type=3,
                                          user_id=user_id,
                                          right_num=right_num,
                                          user_time=user_time,
                                          score=score,
                                          user_object=json.dumps(user_object),
                                          pk_user=json.dumps(pk_user),
                                          result=result,
                                          add_time=add_time,
                                          school_id=school_id,
                                          class_id=class_id,
                                          province_id=province_id
                                          )
    print user_id
    if result == 1:
        score = score + 5
        # 胜利随机给1个道具增加与记录增加
        add_type = random.randint(1,6)
        props_dict = {add_type:1}
        operate_props(user_id, 1, props_dict, add_time, 2)
    else:
        add_type = 0

    # 积分增加与记录增加
    ids = operate_happy_coin(user_id, score, add_time)
    ids.append(pk_happy_record_id)
    data = Struct()
    data['add_type'] = add_type
    data['ids'] = ids
    return data


def use_user_power(user_id):
    # 参与诗词大战 成语大战 活动消耗1能量
    nowt = time.time()
    pk_id = operate_power(user_id, 0, 1, nowt)
    return pk_id


def get_heros_info(p):
    # 获取英雄榜展示所需数据
    page_size = 20

    start = (p - 1) * page_size

    data = db.tbkt_active.winter_user_score.select('user_id',
                                                   'score').filter(type=1, score__gt=0).order_by('-score', 'add_time')[start: page_size*p]
    user_id_array = []
    for da in data:
        user_id_array.append(da.user_id)
    schools = db.ketang_slave.mobile_order_region.select("user_id", 'school_name').filter(user_id__in=user_id_array)[:]
    user_names = db.tbkt_user_slave.auth_user.select('real_name', "id").filter(id__in=user_id_array)[:]
    user_names_map = {i.id: i.real_name for i in user_names}
    schools_map = {i.user_id: i.school_name for i in schools}
    for i in data:
        i.real_name = user_names_map.get(i.user_id, "")
        i.school_name = schools_map.get(i.user_id, "")

    #第1页前3个用户要返回头像
    if p == 1:
        for i in range(len(data)):
            if i == 3:
                break
            data[i]['border_url'] = get_user_border(data[i]['user_id']).url
            data[i]['img'] = get_user_portrait(data[i]['user_id'])
    return data


def get_my_things(user_id):
    # 获取用户道具 奖品 积分记录

    #道具
    data = Struct()
    props = db.tbkt_active.winter_tools.select('tools').get(user_id=user_id)
    data['props'] = decode_json_get_value(props.tools)

    #奖品
    awards = db.tbkt_active.winter_user_award.select('award_id', 'add_time').filter(user_id=user_id)[:]
    # [{award_id = 1},{}]
    if not awards:
        data['awards'] = []
    else:
        award_id = []
        for award in awards:
            award_id.append(award.award_id)
        award_names = db.tbkt_active.winter_award.select('name').filter(id__in=award_id)[:]
        for i in range(len(awards)):
            awards[i]['name'] = award_names[i]['name']
            awards[i]['add_time'] = get_day(awards[i]['add_time'])
            awards[i]['add_month'] = get_month(awards[i]['add_time'])
        data['awards'] = awards

    return data


def get_user_name(lottry_user_id):
    name = db.tbkt_user_slave.auth_user.select('real_name').get(id=lottry_user_id)
    return name['real_name']


def get_happy_ranking(p):
    res = []
    # 获取欢乐榜所需信息
    nowt = time.time()
    nowday = get_day(nowt)
    nowhour = time.localtime(nowt).tm_hour
    nowmin = time.localtime(nowt).tm_min
    now_month = get_month(nowt)
    time_string = nowhour * 100 + nowmin
    if time_string < 2010:  # 20:10分
        nowday -= 1
        if nowday == 0:
            nowday = 31
            now_month -= 1

    # 获取用户参与信息，实时参与的则为要显示的日期
    now_join_user = db.tbkt_active.winter_happy_score.select('add_time').order_by('-add_time').get()
    if not now_join_user:
        return res
    display_day = get_day(now_join_user['add_time'])
    display_mon = get_month(now_join_user['add_time'])

    print display_day, nowday
    # 判断是否需要开奖 也就是Now_day 大于 目前显示的排行榜日期  也就是八点十分以后才会去开今天的奖
    if nowday >= display_day and now_month >= display_mon:
        user_award = db.tbkt_active.winter_user_award.select('user_id').get(day=nowday)
        if not user_award:
            # 执行开奖
            lottry_user_id = lottery(nowt, display_day)
        else:
            lottry_user_id = user_award.user_id
    else:
        # 6-8点之间的逻辑 无当日获奖用户
        lottry_user_id = 0

    if not p:
        limit_array = ['0','10']
    else:
        limit_array = [str(p), '10']

    # 实时显示对应日期的排行榜
    sql = """
        select h.user_id, h.score, w.award_id 
        from winter_happy_score h
        left join winter_user_award w on h.user_id = w.user_id 
        where h.day=%s
        order by h.score desc limit %s, %s;
        """ % (display_day, limit_array[0], limit_array[1])

    data = db.tbkt_active.fetchall_dict(sql)[:]

    user_id_array = []
    for da in data:
        user_id_array.append(da.user_id)
    schools = db.ketang_slave.mobile_order_region.select("user_id", 'school_name').filter(user_id__in=user_id_array)[:]
    user_names = db.tbkt_user_slave.auth_user.select('real_name', "id").filter(id__in=user_id_array)[:]
    user_names_map = {i.id: i.real_name for i in user_names}
    schools_map = {i.user_id: i.school_name for i in schools}
    for i in data:
        i.real_name = user_names_map.get(i.user_id, "")
        i.school_name = schools_map.get(i.user_id, "")



    # 获取获奖用户的头像 和排行榜日期
    res.append(data)
    border_img = Struct()
    border_img['border_url'] = get_user_border(lottry_user_id).url if lottry_user_id != 0 else ''
    border_img['img'] = get_user_portrait(lottry_user_id)  if lottry_user_id != 0 else ''
    border_img['nowday'] = display_day
    border_img['nowmon'] = display_mon
    border_img['name'] = get_user_name(lottry_user_id)  if lottry_user_id != 0 else ''
    res.append(border_img)

    return res


def invite_get_power(user_id):
    # 邀请用户获得1点能量 每天最高通过邀请获得5个
    nowt = time.time()
    begin = get_day_first(get_year(nowt), get_month(nowt), get_day(nowt))
    if get_day(nowt) == 31:
        end = get_day_first(get_year(nowt), get_month(nowt) + 1, 1)
    else:
        end = get_day_first(get_year(nowt), get_month(nowt), get_day(nowt) + 1)
        
    sql = """
        select count(id)
        from winter_user_score_detail
        where user_id = %s and add_time between %s and %s and item_no="share"
    """ % (user_id, begin, end)
    num = db.tbkt_active.fetchone(sql)
    num = num[0]
    if num >= 5:
        return False
    nowt = time.time()
    operate_power(user_id, 2, 1, nowt)
    return True


def lottery(nowt, display_day):
    # 开奖函数
    sql = """
        select user_id, add_time
        from winter_happy_score
        where user_id not in (select user_id from winter_user_award) and day = %s
        order by score desc 
		limit 1;
        """ % display_day

    get_first_man = db.tbkt_active.fetchone(sql)
    if not get_first_man:
        return 0
    first_id = get_first_man[0]
    db.tbkt_active.winter_user_award.create(
        user_id=first_id,
        award_id=1,
        add_time=nowt,
        notice_status=0,
        day=get_day(get_first_man[1])
    )
    return first_id


def get_user_border(user_id):
    # 获取用户头像边框url
    data = Struct()
    border_id = db.slave.user_border_detail.select('border_id').get(user_id=user_id, status=1)
    if not border_id:
        data.url = ''
    else:
        border_url = db.slave.border.select('border_url').get(id=border_id.border_id)
        if border_url:
            data.url = get_absurl(border_url.border_url)
        else:
            data.url = ''

    return data


def decode_json_get_value(json_str):
    # json 转 dict
    props_value = []
    props_dict = json.loads(json_str)
    for i in range(1,7):
        props_value.append(props_dict[str(i)])
    return props_value


def get_my_detail(user_id, p):
    # 获取用户积分记录
    # records = db.tbkt_active.winter_user_score_detail.select(
    #     'remark').filter(user_id=user_id).order_by('-add_time')[p:10]
    sql = '''
    select remark
    from winter_user_score_detail
    where user_id = %s 
    order by add_time DESC
    limit %s, %s;
    ''' % (user_id, p, 10)

    records = db.tbkt_active.fetchall_dict(sql)[:]

    data = [x.remark for x in records]
    return data


def get_user_portrait(user_id):
    # 获取用户头像
    user_portrait = db.tbkt_user_slave.auth_profile.select('portrait').get(user_id=user_id)
    portrait = user_portrait.portrait.strip() if user_portrait.portrait else None
    return get_portrait(None, 1, portrait)


def use_double(ids, user_id, add_time):
    # 使用双倍积分卡后修改积分与记录

    # 查询双倍积分卡数量
    props_info = db.tbkt_active.winter_tools.select('tools').get(user_id=user_id)
    props = decode_json_get_value(props_info.tools)
    if props[5] > 0:
        nowt = time.time()
        if len(ids) == 4:
            # 欢乐竞技场使用双倍积分卡逻辑
            # ids: [score_id, score_detail_id, happy_score_id, pk_happy_record_id]
            score_detail = db.tbkt_active.winter_user_score_detail.select('score', 'remark').get(id=ids[1])
            limit = score_detail['score'] * 2 if score_detail['score'] * 2 < 140 else 140
            remark = u'%s月%s日欢乐竞技场获得<span style="color:#e42a39">%s积分</span>（双倍积分）' % (get_month(nowt), get_day(nowt), limit)
            db.tbkt_active.winter_user_score_detail.filter(id=ids[1]).update(score=limit, remark=remark)
            if limit >= 140:
                limit = 0
            score = db.tbkt_active.winter_user_score.select('score').get(id=ids[0])
            db.tbkt_active.winter_user_score.filter(id=ids[0]).update(score=score['score']+limit/2)
            happy_score = db.tbkt_active.winter_happy_score.select('score').get(id=ids[2])
            db.tbkt_active.winter_happy_score.filter(id=ids[2]).update(score=happy_score['score']+limit/2)
        if len(ids) == 3:
            # 普通PK使用双倍积分卡逻辑
            # ids : [score_id， score_detail_id, pk_record_id]   //分数id 分数详情id  PK记录ID
            score_detail = db.tbkt_active.winter_user_score_detail.select('score', 'remark').get(id=ids[1])
            limit = score_detail['score'] * 2 if score_detail['score'] * 2 < 140 else 140
            remark = u'%s月%s日通过PK获得<span style="color:#e42a39">%s积分</span>, <span style="color:#e42a39">能量值-1</span>（双倍积分）' % (get_month(nowt), get_day(nowt), limit)
            db.tbkt_active.winter_user_score_detail.filter(id=ids[1]).update(score=limit, remark=remark)
            if limit >= 140:
                limit = 0
            score = db.tbkt_active.winter_user_score.select('score').get(id=ids[0])
            db.tbkt_active.winter_user_score.filter(id=ids[0]).update(score=score['score'] + limit/2)
        # 使用双倍积分卡
        post_props_details(user_id, 1, 0, 0, 0, 0, 0, add_time)
    else:
        print '%s用户的双倍积分卡已经用完，不能使用' % (user_id)

def end_acitvtiy():
    nowt = time.time()
    if nowt >= 1519833600:  #1519833600 3.1日 0.00分
        return False
    else:
        return True