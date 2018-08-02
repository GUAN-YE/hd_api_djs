# coding: utf-8
import datetime
import inspect
import json

import time

import logging

from libs.utils import ajax_json as ajax, ajax_try, db, tbktapi, Struct
from com.com_user import need_teacher


@ajax_try({})
@need_teacher
def p_give_web(request):
    """
    @api {post} /huodong/sx_sem/task/send [数学活动]布置活动作业
    @apiGroup hd-tea-sx
    @apiParamExample {json} 请求示例
        {
            "type": 2
            "unit_id": "555428,515192", # 班级ID
            "title": "作业标题",
            "content": "短信内容",
            "begin_time": "2017-01-05 09:10:00", # (可选)定时作业时间
            "end_time": "2017-02-05 23:59:59",   # 作业截止时间(必须大于当前时间和begin_time)
            "sendpwd": 1/0,   # 是否下发帐号密码
            "sendscope": 1/0,  # 短信发送范围 0给所有学生发短信 1只给开通的学生发短信
            "object_id":"试卷ID，可多个"
        }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data":""，
        "response": "ok",
        "error": ""
    }
    @apiSuccessExample {json} 失败返回
    {
        "message": "请设置作业的完成时间",
        "next": "",
        "data": "",
        "response": "fail",
        "error": ""
    }
    """
    args = request.QUERY.casts(type=int, unit_id=str, title=unicode, content=unicode,
                               begin_time='timestamp', end_time='timestamp', sendpwd=int, sendscope=int, details='json',
                               object_id=str)
    type = 101
    unit_id = args.unit_id or ''
    unit_ids = [int(s) for s in unit_id.split(',') if s]
    content = args.content or u''
    now = int(time.time())
    begin_time = args.begin_time or now
    end_time = args.end_time
    sendpwd = args.sendpwd or 0
    sendscope = args.sendscope or 0
    object_id = args.object_id or ''
    object_ids = [int(s) for s in object_id.split(',') if s]
    title = [s for s in args.title.split('|') if s]
    if not type:
        return ajax.jsonp_fail(request, message='作业类型不能为空')

    if not unit_id:
        return ajax.jsonp_fail(request, message='请选择您要发布的班级')

    if not content:
        return ajax.jsonp_fail(request, message='短信内容不能为空')

    if len(content) > 200:
        return ajax.jsonp_fail(request, message='短信内容不能超过200字')

    if not end_time:
        return ajax.jsonp_fail(request, message='请设置作业的完成时间')

    if begin_time < now:
        return ajax.jsonp_fail(request, message='定时发布时间不得小于当前系统时间')

    if begin_time >= end_time:
        return ajax.jsonp_fail(request, message='定时发布时间不得大于完成时间')

    user = request.user

    # title = title or "%s作业" % begin_time.strftime("%m月%d日")

    # 1已发 2待发
    status = 1 if begin_time <= now else 2

    with db.tbkt_shuxue as dt:
        for k, i in enumerate(object_ids):
            # create task
            task_id = dt.sx_task.create(
                type=type,
                object_id=i,
                title=title[k],
                add_user=user.id,
                sms_content=content,
                status=status,
                add_time=now,
                begin_time=begin_time,
                end_time=end_time,
                is_sendpwd=sendpwd,
            )

            # create task_class
            class_details = []
            for unit_id in unit_ids:
                d = {'task_id': task_id,
                     'unit_class_id': unit_id,
                     'type': sendscope,
                     'add_time': now,
                     'student_id': ''}
                class_details.append(d)
            dt.sx_task_class.bulk_create(class_details, ignore=True)
            sql = """
            select d.paper_id,d.question_id from
            sx_paper_question_number n inner join sx_paper_detail d on n.paper_id = %s
            and n.paper_id = d.paper_id and n.type = 2 and n.object_id = d.question_id
            """ % i
            papers = db.ziyuan_slave.fetchall_dict(sql)
            create_ordinary_task(task_id, papers, user.id, now, dt)
            create_message(task_id, user.id, title[k], content, begin_time, end_time, type, unit_ids)

        # send sms or password
        if status == 1:
            students = []
            for i in unit_ids:
                students += get_unit_students(request, i)

            user_ids = ','.join(str(s.id) for s in students if s and (sendscope == 0 or s.is_open))

            # send sms
            send_sms_user_id(request, user_ids, content)

            # send password
            if sendpwd:
                send_pwd(request, user_ids)

            # send im
            send_im(request, '', user_ids, '新作业', '你的老师布置作业了,快来看看吧!', 2)
    return ajax.jsonp_ok(request)


def create_message(task_id, user_id, title, content, begin_time, end_time, task_type, unit_ids):
    """
    创建 tbkt_com.messages
    :param task_id:  sx_task_id -> message object_Id
    :param user_id:  
    :param title:    作业标题
    :param content:  短信内容
    :param begin_time:  作业开始时间
    :param end_time:  作业结束时间
    :param task_type: 作业类型 1：普通作业,2：试卷作业 , 4：知识点视频作业, 5：速算作业
    :param unit_ids:  班级id集合
    :return: 
    """
    print "------------------------"
    print locals()
    print "------------------------"
    with db.default as dd:
        msg_id = dd.message.create(
            type=101,
            subject_id=21,
            object_id=task_id,
            add_user=user_id,
            title=title,
            content=content,
            status=1,
            add_time=int(time.time()),
            begin_time=begin_time,
            end_time=end_time
        )
        msg_class = []
        for i in unit_ids:
            d = {'message_id': msg_id, 'unit_class_id': i, 'student_ids': ''}
            msg_class.append(d)
        dd.message_class.bulk_create(msg_class)


def get_unit_students(request, unit_id):
    """
    获取班级学生信息
    :param request: 
    :param unit_id: 
    :return: 
    """
    url = '/class/students'
    args = dict(unit_id=unit_id)
    hub = tbktapi.Hub(request)
    r = hub.com.post(url, args)
    out = []
    if r.response == 'ok':
        stu = map(Struct, r.data.get('students'))
        for i in stu:
            info = Struct()
            info.phone = i.phone_number
            info.id = int(i.user_id)
            info.is_open = 1 if i.status in (2, 9) else 0
            info.user_name = i.user_name
            info.portrait = i.portrait
            out.append(info)
    return out


def send_sms_user_id(request, user_id, content, schedule_time=''):
    """
    发送短信
    :param request: 
    :param user_id: 以逗号分割
    :param schedule_time: 可选, 定时发送时间, 如: 140415112622 代表14年04月15日11点26分22秒
    :param content: 
    :return: 
    """
    try:
        url = '/sms/send'
        data = dict(user_id=user_id, content=content, schedule_time=schedule_time)
        hub = tbktapi.Hub(request)
        hub.sms.post(url, data)
    except Exception as e:
        logging.error("send_sms ERROR %s:%s" % (inspect.stack()[0][3], e))


def send_pwd(request, user_id):
    """
    下发短信
    :param request: 
    :param user_id: 
    :return: 
    """
    try:
        url = '/class/sendpwd'
        data = dict(user_id=user_id)
        hub = tbktapi.Hub(request)
        hub.com.post(url, data)
    except Exception as e:
        logging.error("send_pwd ERROR %s:%s" % (inspect.stack()[0][3], e))


def send_im(request, unit_ids, user_ids, title, content, type):
    """
    发送IM短信
    :param request: 
    :param unit_ids: 
    :param user_ids: 
    :param title: 
    :param content: 
    :return: 
    """
    try:
        url = '/im/sendim'
        data = dict(unit_id=unit_ids,
                    user_id=user_ids,
                    config_id=2,
                    title=title,
                    type=type,
                    content=content)
        hub = tbktapi.Hub(request)
        hub.com.post(url, data)
    except Exception as e:
        logging.error("send_im ERROR %s:%s" % (inspect.stack()[0][3], e))


def create_ordinary_task(task_id, details, user_id, now, database):
    """
    创建普通作业\试卷作业 详情
    :param task_id: sx_task pk
    :param details: [{"catalog_id":练习册章节ID, "text_catalog_id":教材章节ID, "question_id":题目ID, "content_type":0}]
    :param user_id: 
    :param now: 主记录添加时间
    :param database:  数据库connection
    :return: 
    """
    task_qids = []
    for d in details:
        question_id = int(d.get('question_id', 0))
        task_qids.append(question_id)

    # create task_details
    task_details = []
    # create publish_question
    publish_question = []
    for d in details:
        question_id = int(d.get('question_id', 0))
        if not question_id:
            continue
        arg = dict(cid=d.get('catalog_id', 0),
                   qid=question_id,
                   tcid=d.get('text_catalog_id', 0))
        task_details.append(arg)
        pub = dict(user_id=user_id,
                   task_id=task_id,
                   subject_id=21,
                   question_id=question_id,
                   add_time=now,
                   status=0,
                   type=0,
                   object_id=0)
        publish_question.append(pub)
    database.sx_task_content.create(task_id=task_id, text=json.dumps(task_details), add_time=now)
    database.publish_question.bulk_create(publish_question, ignore=True)

    asks = db.ziyuan_slave.sx_question_ask.filter(question_id__in=task_qids).select('id', 'question_id')[:]

    # create sx_task_qstat 作业按试题统计分析表
    task_qstat = []
    for qid in task_qids:
        for ask in asks:
            if ask.question_id == qid:
                d = dict(task_id=task_id,
                         ask_id=ask.id,
                         finish_student='',
                         wrong_student='',
                         add_time=now)
                if d not in task_qstat:
                    task_qstat.append(d)
    if task_qstat:
        database.sx_task_qstat.bulk_create(task_qstat, ignore=True)

    # create sx_task_kstat 作业按知识点统计分析表
    task_kstat = []
    knowledge = get_question_knowledge(task_qids)
    for k in knowledge:
        d = dict(task_id=task_id,
                 knowledge_id=k.id,
                 knowledge_name=k.name,
                 finish_student='',
                 wrong_student='',
                 add_time=now)
        if d not in task_kstat:
            task_kstat.append(d)
    if task_kstat:
        database.sx_task_kstat.bulk_create(task_kstat, ignore=True)


def get_question_knowledge(qids):
    if not qids:
        return []
    qids = ','.join(str(i) for i in qids)
    sql = """
    select distinct k.id,if(k.name!='',k.name,r.name) name, a.question_id from sx_knowledge k
    inner join sx_ask_relate_knowledge a on a.question_id in (%s) and a.knowledge_id = k.id and k.status = 1
    inner join sx_text_book_catalog_relate_knowledge r on r.knowledge_id = k.id;
    """ % qids
    rows = db.ziyuan_slave.fetchall_dict(sql)
    return rows
