# coding: utf-8
import time
import json
from apps.terminal2018.subject.common import create_message, get_text_content
from libs.utils import ajax_json as ajax, ajax_try, db, join
from com.com_user import need_teacher
from com.com_user import send_pwd, send_im, get_unit_students, send_sms_user_id


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


@ajax_try({})
@need_teacher
def r_sx_send(request):
    """
    @api {post} huodong/terminal/math/send [期末提分试卷]数学布置作业
    @apiGroup terminal
    @apiParamExample {json} 请求示例
    {
        "type": 103
        "unit_id": "555428,515192",     # 班级ID
        "title": "作业标题",             # 对应paper_id 多个title以竖线|分割
        "content": "短信内容",           
        "begin_time": "2017-01-05 09:10:00",    # (可选)定时作业时间
        "end_time": "2017-02-05 23:59:59",      # 作业截止时间(必须大于当前时间和begin_time)
        "sendpwd": 1/0,                         # 是否下发帐号密码
        "sendscope": 1/0,                       # 短信发送范围 0给所有学生发短信 1只给开通的学生发短信
        "object_id":"试卷ID，可多个"              # 需要与title对应,多个以逗号分割
    }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": "",
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
    user = request.user
    grade_id = user.grade_id
    args = request.QUERY.casts(type=int, unit_id=str, title=unicode, content=unicode, object_id=str,
                               begin_time='timestamp', end_time='timestamp', sendpwd=int, sendscope=int, details='json',
                               agent=int)

    task_type = 103  # 期末试卷
    paper_id = args.object_id  # 如果为试卷作业 则为试卷id 否则 为0
    paper_ids = [int(s) for s in paper_id.split(',') if s]
    unit_id = args.unit_id or ''  # 发送作业班级 作业必须要班级id
    unit_ids = [int(s) for s in unit_id.split(',') if s]
    content = args.content or u''
    agent = args.agent or 2
    now = int(time.time())  # 当前时间
    begin_time = args.begin_time or now  # 作业开始时间 如果不是定时作业开始时间=当前时间
    end_time = args.end_time  # 作业结束时间
    sendpwd = args.sendpwd  # 是否下发密码
    sendscope = args.sendscope  # 短信发送范围 0全部 1仅开通
    tea_name = user.name
    open_content = get_text_content(grade_id, tea_name, end_time, subject_id=21)
    # 作业标题 如果为空 则按时间进行保存展示
    title = [s for s in args.title.split('|') if s]
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

    # 1:实时发送展示 2：定时作业
    status = 1 if begin_time <= now else 2

    sql = """
    select distinct object_id, c.unit_class_id from sx_task t, sx_task_class c
    where t.type = 103 and t.add_user = %s and t.id = c.task_id 
    and t.status > -1 and c.status > -1 and t.object_id in (%s)
    """ % (user.id, join(paper_ids))
    rows = db.tbkt_shuxue.fetchall_dict(sql)
    # {(paper_id, unit_id): 1}
    done_map = {(i.object_id, i.unit_class_id): 1 for i in rows}

    # 使用事务保证 数据完整
    with db.tbkt_shuxue as dt:
        for k, i in enumerate(paper_ids):
            # create task
            task_id = dt.sx_task.create(
                type=task_type,
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
            unsent = set()
            for unit_id in unit_ids:
                if done_map.get((i, unit_id)):
                    continue
                d = {'task_id': task_id,
                     'unit_class_id': unit_id,
                     'type': sendscope,
                     'add_time': now,
                     'student_id': '',
                     'status': status}
                unsent.add(unit_id)
                class_details.append(d)

            if class_details:
                dt.sx_task_class.bulk_create(class_details, ignore=True)
                sql = """
                select DISTINCT d.paper_id,d.question_id from
                sx_paper_question_number n inner join sx_paper_detail d on n.paper_id = %s
                and n.paper_id = d.paper_id and n.type = 2 and n.object_id = d.question_id
                """ % i
                papers = db.ziyuan_slave.fetchall_dict(sql)
                create_ordinary_task(task_id, papers, user.id, now, dt)
                create_message(task_id, user.id, title[k], content, begin_time, end_time, unsent, agent, 21)

        # send sms or password
        if status == 1:
            students = []
            for u in unit_ids:
                students += get_unit_students(request, u)

            user_ids = ','.join(str(s.id) for s in students if s and (sendscope == 0 or s.is_open))

            # send sms
            send_sms_user_id(request, user_ids, open_content)

            # send password
            if sendpwd:
                send_pwd(request, user_ids)

            # send im
            send_im(request, '', user_ids, '新作业', '你的老师布置作业了,快来看看吧!', 2)
    return ajax.jsonp_ok(request)



