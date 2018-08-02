# coding:utf-8
# get_unit_students
import json
import time
from libs.utils import ajax, ajax_json, ajax_try, Struct, db, join
from com.com_user import get_unit_students

APP_ID = 14


def get_status(user):
    """
    是否可以参加活动领金币
    :param user_id:
    :return:
    """

    # 三门峡用户不参加此次活动
    data = Struct()
    sid = user.subject_id
    data.status = 0
    num = db.tbkt_active.active_score_gift.select("end_num").get(active_id=14)
    data.num = num.end_num
    region = db.ketang_slave.mobile_order_region.get(user_id=user.id)

    if region and region.city == "411200":
        return u"三门峡用户不参与此次活动"
    # 教师所在班级人数不足，不能参加活动
    unit_ids = [u.id for u in user.units]
    if sid == 21 and sx_task_info(user, unit_ids):
        data.status = 1
    if sid == 51 and yw_task_info(user, unit_ids):
        data.status = 1
    if sid == 91 and yy_task_info(user, unit_ids):
        data.status = 1
    if num.end_num == 0:
        data.status = 0
    user_coin = db.default.score_user_detail.get(user_id=user.id, app_id=7, remark=u"教师发作业赢金豆")
    if user_coin:
        data.status = 2
    return data


def can_get(user, sid, tea_unit_ids):
    """
    老师发作业，学生完成作业,可以领取金币状态返回
    """
    # 根据老师科目id查看当前科目发布作业和学生完成作业情况
    # 活动开始时间和结束时间

    if sid == 21 and sx_task_info(user, tea_unit_ids):
        return True
    if sid == 51 and yw_task_info(user, tea_unit_ids):
        return True
    if sid == 91 and yy_task_info(user, tea_unit_ids):
        return True
    return False


def yy_task_info(user, tea_unit_ids):
    """
    英语作业
    """

    if tea_unit_ids:
        active_time = db.tbkt_active.active.select("begin_time", "end_time").get(name=u"教师发作业领金币")
        begin_time = active_time.begin_time
        end_time = active_time.end_time
        sql = """
                select tc.task_id, t.begin_time, t.end_time, t.status,tc.unit_class_id
                from yy_task t
                inner join yy_task_class tc on tc.task_id=t.id and tc.unit_class_id in (%s)
                where t.add_user=%s and t.status!=-1 
                and t.begin_time>%s and t.end_time<%s
                """ % (join(tea_unit_ids), user.id, begin_time, end_time)
        tasks = db.tbkt_yingyu.fetchall_dict(sql)
        for i in tea_unit_ids:
            class_students_data = db.ketang.mobile_order_region.select("user_id").filter(
                unit_class_id=i, user_type=1)[:]
            if len(class_students_data) < 20:
                continue
            user_ids = [u.user_id for u in class_students_data]
            for t in tasks:
                if t.unit_class_id != i:
                    continue
                finish = db.tbkt_yingyu.yy_task_progress.filter(task_id=t.task_id, user_id__in=user_ids,
                                                                status=1)[:]
                finish_num = len(finish)
                percent = ((finish_num) * 100 / len(class_students_data)) if len(class_students_data) != 0 else 0
                if percent < 90:
                    continue
                return True
        return False


def sx_task_info(user, tea_unit_ids):
    """
    数学作业
    """

    # tea_unit_ids = [u.id for u in user.units]

    # 活动期间教师布置的作业
    if tea_unit_ids:
        active_time = db.tbkt_active.active.select("begin_time", "end_time").get(name=u"教师发作业领金币")
        sx_begin_time = active_time.begin_time
        sx_end_time = active_time.end_time
        sql = """
            select  tc.task_id, t.begin_time, t.end_time, t.add_time, tc.unit_class_id,tc.status
            from sx_task t
            inner join sx_task_class tc on tc.task_id=t.id and tc.unit_class_id in (%s)
            where t.add_user=%s and t.status!=-1 and tc.status != -1
            and t.begin_time>%s and t.end_time<%s
          
            """ % (join(tea_unit_ids), user.id, sx_begin_time, sx_end_time)
        tasks = db.tbkt_shuxue.fetchall_dict(sql)
        task_ids = [i.task_id for i in tasks]
        task_info = db.tbkt_shuxue.sx_task_content.select("text", "task_id").filter(task_id__in=task_ids)[:]

        for i in tea_unit_ids:
            class_students_data = db.ketang.mobile_order_region.select("user_id").filter(
                unit_class_id=i, user_type=1)[:]
            if len(class_students_data) < 40:
                continue
            user_ids = [u.user_id for u in class_students_data]
            if task_info:
                for f in task_info:
                    # if len(json.loads(f.text)) < 3:
                    if len(f["text"]) < 3:
                        continue
                for s in tasks:
                    if s.unit_class_id != i and s.task_id not in task_ids:
                        continue
                    finish = db.tbkt_shuxue.sx_task_test.filter(task_id=s.task_id, user_id__in=user_ids,
                                                                status=1)[:]
                    finish_num = len(finish)
                    percent = ((finish_num) * 100 / len(class_students_data)) if len(
                        class_students_data) != 0 else 0
                    if percent < 90:
                        continue
                    return True
        return False


def yw_task_info(user, tea_unit_ids):
    """
    语文作业
    """

    # 活动期间教师布置的作业

    if tea_unit_ids:
        active_time = db.tbkt_active.active.select("begin_time", "end_time").get(name=u"教师发作业领金币")
        begin_time = active_time.begin_time
        end_time = active_time.end_time
        sql = """
                select u.task_id ,t.add_user,t.type,
                t.add_time,t.begin_time,t.end_time,t.title,t.chapter_id,u.unit_class_id,t.status,
                u.status class_status from yw_task_new t
                inner join yw_task_class_new u on u.task_id=t.id and t.add_user=%s
                where u.unit_class_id in (%s) and t.status =1  and u.status > -1
                and t.begin_time>%s and t.end_time<%s
                """ % (user.id, join(tea_unit_ids), begin_time, end_time)
        yw_task = db.tbkt_yuwen.fetchall_dict(sql)
        for i in tea_unit_ids:
            class_students_data = db.ketang.mobile_order_region.select("user_id").filter(
                unit_class_id=i, user_type=1)[:]
            if len(class_students_data) < 20:
                continue
            user_ids = [u.user_id for u in class_students_data]
            for s in yw_task:
                if s.unit_class_id != i:
                    continue
                finish = db.tbkt_yuwen.yw_test_new.filter(task_id=s.task_id, user_id__in=user_ids, status=1)[:]
                finish_num = len(finish)
                percent = ((finish_num) * 100 / len(class_students_data)) if len(class_students_data) != 0 else 0
                if percent < 90:
                    continue
                return True
        return False


def get_coin(user_id):
    """
    用户是否领取过金币 保存领取记录
    """
    # 用户领取金币
    nowt = int(time.time())
    score = 20
    user_coin_info = db.default.score_user_detail.filter(user_id=user_id, remark=u"教师发作业赢金豆", app_id=7)
    num = db.tbkt_active.active_score_gift.select("end_num").get(active_id=14)
    if user_coin_info:
        return u"已经领过金币"
    with db.default as coin:
        coin.score_user_detail.create(
            user_id=user_id,
            item_no="tea_voucher_bak",
            score=score,
            cycle_num=1,
            remark=u"教师发作业赢金豆",
            add_date=nowt,
            app_id=7
        )
    user_score = db.default.score_user.get(user_id=user_id, app_id=7)
    if user_score:
        coin.score_user.filter(id=user_score.id).update(score=int(user_score.score) + int(score))
    else:
        coin.score_user.create(
            user_id=user_id,
            score=score,
            app_id=7
        )
    # 用户领取之后更新活动总积分
    db.tbkt_active.active_score_gift.filter(active_id=14).update(end_num=int(num.end_num) - int(score))
