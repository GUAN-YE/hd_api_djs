# coding: utf-8
import json
import time
from collections import defaultdict, Counter, OrderedDict

import logging

from apps.terminal2018.subject.common import create_message, get_text_content
from apps.terminal2018.subject.yw_question import get_question
from apps.yw_reading.common import filter_word_flag
from com.com_user import get_unit_students, send_sms_user_id, send_im
from libs.utils import ajax, db, join, Struct, num_to_ch
from libs.utils.tbktapi import Hub
from .yw_source import *

YW_TASK_TYPE = 103

R = '<span class="ask_right">%s</span>'
W = '<span class="ask_wrong">%s</span>'


def r_yw_preview(request):
    """
    @api {post} /huodong/terminal/yw/preview [期末提分试卷]语文试卷预览
    @apiGroup terminal
    @apiParamExample {json} 请求示例
    {"paper_id": 试卷id}
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": [
            {
                "category": 1,                  # 1 一题一问 2 一题多问
                "asks": [                       # 大题下 小题信息
                    {                               
                        "point": "",            # 断句题正确文字展示 其他类型为 ""
                        "parse": "",            # 解析
                        "no": "",               # 小题题号
                        "image": "",            # 小题图片
                        "choice_answer": [],    # 选择题正确答案
                        "options": [],          # 小题选项
                        "content": "",          # 小题题干
                        "video": "",            # 小题视频
                        "right_answer": [],     # 正确答案(断句题, 连词成句, 填空题, 连线题)
                        "refer": [],            # 解答题正确答案
                        "type": 7,              # 大题类型
                        "id": 66,               # 小题id
                        "question_id": 29       # 大题id 
                    }
                ],
                "no": "",                       # 大题题号
                "image": "",                    # 大题图片
                "content": "",                  # 大题题干
                "video": "",                    # 大题视频
                "type":                         # 大题类型
            }
        ],
        "response": "ok",
        "error": ""
    }
    
    * question => type
    1.选择题 
    2.填空题 
    3.判断 
    4.连线题  
    5.连词成句 
    6.断句 
    7.解答题
    """
    args = request.QUERY.casts(paper_id=int)
    paper_id = args.paper_id
    if not paper_id:
        return ajax.jsonp_fail(request, message="缺少paper_id")
    qids = PAPER_QUESTION.get(paper_id, ())
    data = get_question(qids)
    # data = get_question([paper_id])
    # 教师端在预览时 填空不可点击 将input标签替换为 span
    for i in data:
        for a in i.asks:
            if a.type == 2:
                a.content = a.content.replace(u'<input placeholder="点击填写">', u'<span class="kong">点击填写</span>')
    return ajax.jsonp_ok(request, data)


def r_yw_send(request):
    """
    @api {post} /huodong/terminal/yw/send [期末提分试卷]语文试卷发送
    @apiGroup terminal
    @apiParamExample {json} 请求示例
    {
        "unit_id": 班级id(多个逗号分隔),
        "title": "试卷名字(多个逗号分隔)",
        "content": "短信内容",
        "begin_time": "开始时间(选填定时作业需要)",
        "end_time": "结束时间",
        "sendpwd": 是否下发账号密码 1/0 (选填),
        "sendscope": "短信发送范围 1 开通 0 全部 (选填)",
        "paper_id": "多个试卷逗号分隔",
    }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": "",
        "response": "ok",
        "error": ""
    }
    """
    args = request.QUERY.casts(unit_id=str, title=unicode, content=unicode,
                               begin_time='timestamp', end_time='timestamp',
                               sendpwd=int, sendscope=int, paper_id=str, agent=int)
    now = int(time.time())
    try:
        unit_id = args.unit_id or ""
        unit_ids = map(int, unit_id.split(","))
        if not unit_ids:
            return ajax.jsonp_fail(request, message="请选择班级！")

        title = args.title or ""
        title = title.split(",")
        if not title:
            return ajax.jsonp_fail(request, message="没有找到试卷标题！")

        content = args.content
        if not content:
            return ajax.jsonp_fail(request, message='短信内容不能为空')
        if len(content) > 200:
            return ajax.jsonp_fail(request, message='短信内容不能超过200字')

        begin_time = args.begin_time or now
        end_time = args.end_time
        if not end_time:
            return ajax.jsonp_fail(request, message='请设置作业的完成时间')

        if begin_time < now:
            return ajax.jsonp_fail(request, message='定时发布时间不得小于当前系统时间')

        if begin_time >= end_time:
            return ajax.jsonp_fail(request, message='定时发布时间不得大于完成时间')

        paper_id = args.paper_id or ""
        paper_ids = map(int, paper_id.split(","))
        if not paper_id:
            return ajax.jsonp_fail(request, message="请选择发布的试卷")

        agent = args.agent or 2

    except Exception as e:
        print e
        return ajax.jsonp_fail(request, message="参数异常！")

    user = request.user
    content = get_text_content(user.grade_id, user.name, end_time, 51)

    status = 1 if begin_time <= now else 0
    send_pwd = args.sendpwd  # 是否下发密码
    send_scope = args.sendscope  # 短信发送范围 0全部 1仅开通

    sql = """
    select distinct object_id, c.unit_class_id from yw_task_new t, yw_task_class_new c
    where t.type = %s and t.add_user = %s and t.id = c.task_id and t.object_id in (%s) 
    and t.status > -1 and c.status > -1
    """ % (YW_TASK_TYPE, user.id, join(paper_ids))
    rows = db.tbkt_yuwen.fetchall_dict(sql)

    done_map = {(i.object_id, i.unit_class_id): 1 for i in rows}

    with db.tbkt_yuwen as dt:
        for k, i in enumerate(paper_ids):
            # create task
            task_id = dt.yw_task_new.create(
                add_user=user.id,
                chapter_id=0,
                type=YW_TASK_TYPE,
                status=status,
                add_time=now,
                begin_time=begin_time,
                end_time=end_time,
                title=title[k],
                object_id=i
            )

            # create task_class
            class_details = []
            send_unit = set()
            for unit_id in unit_ids:
                if done_map.get((i, unit_id)):
                    continue
                d = {'task_id': task_id,
                     'unit_class_id': unit_id,
                     'stu_ids': '',
                     'is_password': send_pwd,
                     'is_all': send_scope,
                     'status': status}
                send_unit.add(unit_id)
                class_details.append(d)
            if class_details:
                dt.yw_task_class_new.bulk_create(class_details, ignore=True)
                question_ids = PAPER_QUESTION.get(i, ())
                dt.yw_task_detail_new.create(task_id=task_id, question_id=join(question_ids), type=YW_TASK_TYPE)

                create_message(task_id, user.id, title[k], content, begin_time, end_time, send_unit, agent, 51)

        # send sms or password
        if status == 1:
            students = []
            for u in unit_ids:
                students += get_unit_students(request, u)

            user_ids = ','.join(str(s.id) for s in students if s and (send_scope == 0 or s.is_open))

            # send sms
            send_sms_user_id(request, user_ids, content)

            # send password
            if send_pwd:
                send_pwd(request, user_ids)

            # send im
            send_im(request, '', user_ids, '新作业', '你的老师布置作业了,快来看看吧!', 2)
    return ajax.jsonp_ok(request)


def r_stu_test_info(request):
    """
    @api {post} /huodong/terminal/yw/test/info [期末提分试卷]语文学生做题
    @apiGroup terminal
    @apiParamExample {json} 请求示例
    {"task_id": 作业id}
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "total": 10,                   # 全部试题                    
            "wrong": 2,                    # 错题数
            "title": "期末提分试卷-（二）",   # 试卷标题 
        },
        "response": "ok",
        "error": ""
    }
    """
    out = Struct()
    out.total = 0
    out.wrong = 0
    out.title = ""
    args = request.QUERY.casts(task_id=int, test_id=int)
    task_id = args.task_id
    test_id = args.test_id
    if not task_id and not test_id:
        return ajax.jsonp_fail(request, message="缺少作业id")
    if task_id:
        user_id = request.user_id
        detail = db.tbkt_yuwen.yw_test_detail_new.get(task_id=task_id, user_id=user_id)
    else:
        test = db.tbkt_yuwen.yw_test_new.get(id=test_id)
        task_id = test.task_id
        detail = db.tbkt_yuwen.yw_test_detail_new.get(task_id=test.task_id, user_id=test.user_id)

    if not detail or detail.status == 0:
        return ajax.jsonp_ok(request, out)
    sql = """
    select t.title, d.question_id from yw_task_new t, yw_task_detail_new d
    where t.id = d.task_id and t.id = %s
    """ % task_id
    task = db.tbkt_yuwen.fetchone_dict(sql)
    if not task or not task.question_id:
        return ajax.jsonp_ok(request, out)
    question_ids = map(int, task.question_id.split(","))
    text = map(Struct, json.loads(detail.text)) if detail and detail.text else []
    out.total = len(question_ids)
    out.wrong = len(set(i.qid for i in text if i.result == 0))
    out.title = task.title
    return ajax.jsonp_ok(request, out)


def r_stu_test_result(request):
    """
    @api {post} /huodong/terminal/yw/test/result [期末提分试卷]语文学生结果页
    @apiGroup terminal
    @apiParamExample {json} 请求示例
    {
        "task_id": 作业id, 
        "test_id": "测试记录id",
        "show_wrong": 0/1   # 是否只展示错题
    }
    * 两个参数传其中一个
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": [
            {
                "category": 2,    # 是否是一题多问  1一题一问 / 2一题多问
                "asks": [
                    {
                        "parse": "111",    # 解析
                        "no": "(1)",       # 小题号
                        "image": "http:/file.m.xueceping.cn/upload_media/yuwen/2018/04/26/20180426155918610447.jpg", # 题干图片
                        "options": [  # 选项
                            {
                                "option": "A",   # 选项
                                "image": "",     # 选项图片
                                "ask_id": 78,    # 小题id
                                "is_right": 1,   # 是否是正确答案
                                "content": "A1", # 小题题干
                                "link_id": "-1", # 连线题使用
                                "id": 494        # 选项id
                            }
                        ],
                        "content": "我是选择题第一题",  # 小题题干
                        "video": "http:/file.m.xueceping.cn/upload_media/yuwen/2018/04/26/20180426155923366948.mp4", # 小题视频 
                        "right_answer": [   # 正确答案
                            {
                                "option": "A",
                                "image": "",
                                "ask_id": 78,
                                "is_right": 1,
                                "content": "A1",
                                "link_id": "-1",
                                "id": 494
                            }
                        ],
                        "type": 1,   # 小题类型
                        "id": 78,    # 小题id
                        "question_id": 28,  # 大题id
                        "user_answer": "A", # 用户答案
                        "user_result": "1", # 用户是否答对 0/1
                    }
                ],
                "no": "一",
                "image": "http:/file.m.xueceping.cn/upload_media/yuwen/2018/04/26/20180426155820813269.jpg",
                "content": "我是选择题公共题干",
                "video": "http:/file.m.xueceping.cn/upload_media/yuwen/2018/04/26/20180426155826832087.mp4",
                "type": 1
            }
        ],
        "response": "ok",
        "error": ""
    }
    
    * question => type
    1.选择题 
    2.填空题 
    3.判断 
    4.连线题  
    5.连词成句 
    6.断句 
    7.解答题
    """
    args = request.QUERY.casts(task_id=int, test_id=int, show_wrong=int)
    task_id = args.task_id
    test_id = args.test_id
    show_wrong = args.show_wrong
    if not task_id and not test_id:
        return ajax.jsonp_fail(request, message="缺少主要参数")

    if task_id:
        user_id = request.user_id
        detail = db.tbkt_yuwen.yw_test_detail_new.get(task_id=task_id, user_id=user_id)
    else:
        test = db.tbkt_yuwen.yw_test_new.get(id=test_id)
        task_id = test.task_id
        detail = db.tbkt_yuwen.yw_test_detail_new.get(task_id=test.task_id, user_id=test.user_id)

    if not detail or detail.status != 1:
        return ajax.jsonp_ok(request, [])
    task = db.tbkt_yuwen.yw_task_detail_new.get(task_id=task_id)
    question = map(int, task.question_id.split(","))
    text = map(Struct, json.loads(detail.text)) if detail and detail.text else []
    text_map = {int(i.ask_id): (i.answer, i.result) for i in text}
    question = get_question(question)
    for i in question:
        for a in i.asks:
            answer, result = text_map.get(a.id, ("", 0))
            a["user_answer"] = answer
            a["user_result"] = result
            if not answer:
                continue
            if a.type == 6:
                _option = map(int, json.loads(answer or []))
                temp = a.content.split("<span class=\"point\"></span>")
                _option.sort(key=lambda x: x)
                for r, o in enumerate(_option):
                    if r >= len(a.right_answer):
                        continue
                    style = R if a.right_answer[r] == o else W
                    temp.insert(o, style % u"/")
                a["user_answer"] = "".join(temp)
                a["user_result"] = result
            elif a.type == 5:
                _option = map(int, json.loads(answer))
                temp = []
                for r, o in enumerate(_option):
                    style = R if r == o else W
                    temp.append(style % a.right_answer[o])
                a["user_answer"] = temp
                a["user_result"] = result

            elif a.type == 2:
                a.content = a.content.replace(u'<input placeholder="点击填写">', u'<span class="kong">点击填写</span>')
                a["user_answer"] = a.content
                for r, o in enumerate(answer):
                    if r >= len(a.right_answer):
                        continue
                    style = R if a.right_answer[r] == o else W
                    style = style % filter_word_flag(o)
                    a["user_answer"] = a["user_answer"].replace(u'<span class="kong">点击填写</span>', style, 1)
                a["user_result"] = result

            if a.type in (7, ):
                # 敏感词过滤
                a["user_answer"] = filter_word_flag(a["user_answer"])

    if show_wrong:
        out = []
        temp = []
        for i in question:
            for a in i.asks:
                if a.get("user_result") == 0:
                    if i.id not in temp:
                        out.append(i)
                        temp.append(i.id)
        question = out
    return ajax.jsonp_ok(request, question)


def r_stu_test_submit(request):
    """
    @api {post} /huodong/terminal/yw/test/submit [期末提分试卷]语文学生提交
    @apiGroup terminal
    @apiParamExample {json} 请求示例
    {
        "task_id": 作业id,
        "status": 是否作业 0/1,
        "detail": [
                    {
                        "qid": 大题id,
                        "ask_id"：小题id,
                        "answer": "用户答案",
                        "result": "正确/错误 1/0"
                     }
                 ]
    }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": "",
        "response": "ok",
        "error": ""
    }
    """
    args = request.QUERY.casts(task_id=int, status=int, detail="json")
    task_id = args.task_id
    now = int(time.time())
    user = request.user
    if not task_id:
        return ajax.jsonp_fail(request, message="缺少作业id")
    status = args.status
    detail = args.detail
    if not detail:
        return ajax.jsonp_fail(request, message="缺少提交详情")

    with db.tbkt_yuwen as dt:
        test = dt.yw_test_new.get(task_id=task_id, user_id=user.id)
        if test and test.status == 1:
            return ajax.jsonp_ok(request, [])
        if test:
            dt.yw_test_new.filter(id=test.id).update(status=status)

        test_detail = dt.yw_test_detail_new.get(task_id=task_id, user_id=user.id)
        text = map(Struct, json.loads(test_detail.text)) if test_detail and test_detail.text else []
        text += map(Struct, detail)
        right_num = 0
        total = len(text)
        for i in text:
            if i.result == 1:
                right_num += 1
        score = int(right_num/float(total) * 100) if total else 0
        if test_detail:
            dt.yw_test_detail_new.filter(id=test_detail.id).update(text=json.dumps(text), status=status, score=score)
        else:
            dt.yw_test_new.create(
                task_id=task_id,
                user_id=user.id,
                class_id=user.unit.id,
                use_time=0,
                status=status,
                score=score,
                test_time=now
            )

            dt.yw_test_detail_new.create(
                user_id=user.id,
                task_id=task_id,
                text=json.dumps(text),
                score=score,
                type=0,
                class_id=user.unit.id,
                json_info="",
                status=status,
                test_time=now
            )
    return ajax.jsonp_ok(request, [])


def r_stu_test_question(request):
    """
    @api {post} /huodong/terminal/yw/test/question [期末提分试卷]语文学生做题
    @apiGroup terminal
    @apiParamExample {json} 请求示例
    {"task_id": 作业id}
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": [
            {
                "category": 2,    # 是否是一题多问  1一题一问 / 2一题多问
                "asks": [
                    {
                        "parse": "111",    # 解析
                        "no": "(1)",       # 小题号
                        "image": "http:/file.m.xueceping.cn/upload_media/yuwen/2018/04/26/20180426155918610447.jpg", # 题干图片
                        "options": [  # 选项
                            {
                                "option": "A",   # 选项
                                "image": "",     # 选项图片
                                "ask_id": 78,    # 小题id
                                "is_right": 1,   # 是否是正确答案
                                "content": "A1", # 小题题干
                                "link_id": "-1", # 连线题使用
                                "id": 494        # 选项id
                            }
                        ],
                        "content": "我是选择题第一题",  # 小题题干
                        "video": "http:/file.m.xueceping.cn/upload_media/yuwen/2018/04/26/20180426155923366948.mp4", # 小题视频 
                        "right_answer": [   # 正确答案
                            {
                                "option": "A",
                                "image": "",
                                "ask_id": 78,
                                "is_right": 1,
                                "content": "A1",
                                "link_id": "-1",
                                "id": 494
                            }
                        ],
                        "type": 1,   # 小题类型
                        "id": 78,    # 小题id
                        "question_id": 28,  # 大题id
                        "user_answer": "A", # 用户答案
                        "user_result": "1", # 用户是否答对 0/1
                    }
                ],
                "no": "一",
                "image": "http:/file.m.xueceping.cn/upload_media/yuwen/2018/04/26/20180426155820813269.jpg",
                "content": "我是选择题公共题干",
                "video": "http:/file.m.xueceping.cn/upload_media/yuwen/2018/04/26/20180426155826832087.mp4",
                "type": 1
            }
        ],
        "response": "ok",
        "error": ""
    }

    * 已完成的题 不会出现
    """
    user_id = request.user_id
    args = request.QUERY.casts(task_id=int)
    task_id = args.task_id
    if not task_id:
        return ajax.jsonp_fail(request, message="缺少作业id")
    detail = db.tbkt_yuwen.yw_test_detail_new.get(task_id=task_id, user_id=user_id)
    if detail and detail.status == 1:
        return ajax.jsonp_ok(request, [])
    task = db.tbkt_yuwen.yw_task_detail_new.get(task_id=task_id)
    if not task or not task.question_id:
        return ajax.jsonp_ok(request, [])
    question_ids = map(int, task.question_id.split(","))
    text = map(Struct, json.loads(detail.text)) if detail and detail.text else []
    done_qid = [i.qid for i in text]
    text_map = {i.ask_id: (i.answer, i.result) for i in text}
    question = get_question(question_ids)
    out = []
    total = len(question)
    for i in question:
        if i.id in done_qid:
            continue
        for a in i.asks:
            option, result = text_map.get(i.id, ("", ""))
            a["user_answer"] = option
            a["user_result"] = result
        i.total = total
        out.append(i)
    return ajax.jsonp_ok(request, out)


def yw_paper_list(user, subject_id):
    """
    语文试卷列表
    :param user: 
    :param subject_id: 
    :return: 
    """
    from apps.terminal2018.common import p_yw_user_book
    book_info = p_yw_user_book(user.id)
    if not book_info:
        return []
    book_id = book_info.id
    paper_ids = BOOK_PAPER.get(book_id)
    if not paper_ids:
        return []
    sql = """
    select t.object_id, count(DISTINCT unit_class_id) num 
    from yw_task_new t, yw_task_class_new c
    where t.id = c.task_id and t.type = %s and t.add_user = %s and c.status > -1
    and t.object_id in %s and c.unit_class_id in (%s) group by t.object_id
    """ % (YW_TASK_TYPE, user.id, str(paper_ids), ",".join(str(i.id) for i in user.units))
    data = db.tbkt_yuwen.fetchall_dict(sql)
    unit_num = len(user.units) if user.units else 0

    paper_map = {i.object_id: i.num for i in data}
    out = []
    for i in paper_ids:
        d = Struct()
        name = PAPER.get(i)
        d.id = i
        d.name = name
        send_num = paper_map.get(i, 0)
        d.status = 1 if send_num >= unit_num else 0
        out.append(d)
    return out


def update_check_status(task_id, unit_id):
    # 检查列表 更新检查状态
    sql = """
    select t.id,t.end_time from yw_task_new t join yw_task_class_new tc on t.id=tc.task_id
    where tc.unit_class_id=%s and t.id=%s and tc.status in (0,1,2)
    """ % (unit_id, task_id)
    task = db.tbkt_yuwen.fetchone_dict(sql)
    if task and task.end_time <= int(time.time()):
        db.tbkt_yuwen.yw_task_class_new.filter(task_id=task_id, unit_class_id=unit_id).update(status=4)


def r_check_task(request):
    """
    @api {post} /huodong/terminal/yw/check/task/info [期末提分试卷]语文检查作业
    @apiGroup terminal
    @apiParamExample {json} 请求示例
    {
        "task_id": 作业id,    
        "unit_id": 班级id
    }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "is_end": 1,                        # 是否已截止
            "task_date": "05-16 9:00(星期三)"    # 作业时间
            "finish_num": 0                     # 完成人数
            "unfinish_num": 0                   # 未完成人数
            "list":[
                {
                    "user_name": "张三",   # 学生姓名
                    "status": 0,          # 1 完成 2 未完成
                    "score": 0,           # 用户成绩 
                    "is_after": 1/0,      # 1补交 0不是
                    "test_id": 0          # 测试id                
                    "date": "作业完成时间"
                }, ...
            ],
            "wrong_info": [
                {
                    "no": 题号
                    "rate": 错误率
                    "ask_id": 小题id
                },
            ]
        },
        "response": "ok",
        "error": ""
    }
    
    * list 班级学生完成情况
      wrong_info  错题率
      已排序
    """
    args = request.QUERY.casts(task_id=int, unit_id=int)
    task_id = args.task_id
    unit_id = args.unit_id
    if not task_id:
        return ajax.jsonp_fail(request, message="缺少作业id")
    if not unit_id:
        return ajax.jsonp_fail(request, message="缺少班级id")
    update_check_status(task_id,unit_id)
    sql = """
    select t.end_time, d.question_id, t.object_id from yw_task_new t, yw_task_detail_new d 
    where t.id = %s and t.id = d.task_id
    """ % task_id
    task = db.tbkt_yuwen.fetchone_dict(sql)
    out = Struct()
    out.is_end = 0
    if not task:
        return ajax.jsonp_ok(request, out)
    now = int(time.time())

    if task.end_time < now:
        out.is_end = 1
    out.task_date = format_stamp(task.test_time) + u"(星期%s)" % num_to_ch(time.localtime(task.test_time).tm_wday + 1)
    stu_map = dict()
    r = Hub(request).com.post("/class/students", dict(unit_id=unit_id))
    if r and r.response == "ok":
        stus = map(Struct, r.data["students"])
        stu_map = {i.user_id: i for i in stus}

    stu_test = db.tbkt_yuwen.yw_test_new.filter(
        task_id=task_id, user_id__in=stu_map.keys(), status=1)[:]
    stu_score = db.tbkt_yuwen.yw_test_detail_new.filter(
        task_id=task_id, user_id__in=stu_map.keys(), status=1)[:]
    score_map = {s.user_id: s.score for s in stu_score}
    test_map = {i.user_id: i for i in stu_test}
    out.finish_num = 0
    out.unfinish_num = 0
    out.paper_id = task.object_id
    out.list = []
    for user_id, info in stu_map.iteritems():
        d = Struct()
        d.user_id = info.user_id      # 学生id
        d.user_name = info.user_name  # 学生姓名
        d.status = 0                  # 是否完成
        d.score = 0                   # 成绩
        d.is_after = 0                # 是否补交
        d.date = ""                   # 完成时间
        d.test_time = 0               # 完成时间戳(排序使用)
        d.test_id = 0
        test = test_map.get(user_id)
        if not test:
            out.unfinish_num += 1
        else:
            out.finish_num += 1
            if test.test_time > task.end_time:
                d.is_after = 1
            d.score = score_map.get(user_id)
            d.status = 1
            d.date = format_stamp(test.test_time)
            d.test_time = test.test_time
            d.test_id = test.id
        out.list.append(d)
    out.list.sort(key=lambda x: (-x.score, x.test_time))
    out.wrong_info = check_wrong_info(task_id, stu_map.keys(), task.question_id.split(","))
    return ajax.jsonp_ok(request, out)


def check_wrong_info(task_id, stu_ids, question_ids):
    """
    作业错误率以小题为主
    :param task_id: 作业id 
    :param stu_ids: 学生id 
    :param question_ids: 题目id list 
    :return: 
    """
    stu_test = db.tbkt_yuwen.yw_test_detail_new.select("user_id", "text").filter(
        task_id=task_id, user_id__in=stu_ids, status=1)[:]
    total = len(stu_test)
    wrong_ask = []
    for i in stu_test:
        txt = json.loads(i.text)
        for t in txt:
            if t["result"] == 0:
                wrong_ask.append(t["ask_id"])
    result_map = Counter(wrong_ask)
    asks = db.tbkt_yw.yw_question_ask.select("id", "question_id").filter(question_id__in=question_ids)

    q_map = OrderedDict()
    for i in asks:
        q_map.setdefault(i.question_id, []).append(i.id)
    wrong_info = []
    for i, qid in enumerate(q_map, start=1):
        asks = q_map.get(qid)
        for j, ask_id in enumerate(asks, start=1):
            d = Struct()
            d.no = i if len(asks) == 1 else "%s(%s)" % (i, j)
            d.rate = result_map.get(ask_id, 0)/total * 100 if total else 0
            d.ask_id = ask_id
            wrong_info.append(d)
    return wrong_info


def get_ask_info(request):
    """
    @api {post} /huodong/terminal/yw/check/task/ask [期末提分试卷]语文检查作业
    @apiGroup terminal
    @apiParamExample {json} 请求示例
    {
        "task_id": 作业id,    
        "unit_id": 班级id,
        "ask_id": 小题id
    }
    @apiSuccessExample {json} 成功返回
    {
        "message": "",
        "next": "",
        "data": {
            "wrong": ["错误学生姓名"],
            "right": ["正确学生姓名"],
            "question": [题目信息]
        },
        "response": "ok",
        "error": ""
    }
    """
    args = request.QUERY.casts(task_id=int, unit_id=int, ask_id=int)
    task_id = args.task_id
    unit_id = args.unit_id
    ask_id = args.ask_id
    if not task_id:
        return ajax.jsonp_fail(request, message="缺少作业id")
    if not unit_id:
        return ajax.jsonp_fail(request, message="缺少班级id")
    if not ask_id:
        return ajax.jsonp_fail(request, message="缺少小题id")
    stu_map = dict()
    r = Hub(request).com.post("/class/students", dict(unit_id=unit_id))
    if r and r.response == "ok":
        stus = map(Struct, r.data["students"])
        stu_map = {i.user_id: i for i in stus}
    stu_test = db.tbkt_yuwen.yw_test_detail_new.select("user_id", "text").filter(
        task_id=task_id, user_id__in=stu_map.keys(), status=1)[:]
    ask = db.tbkt_yw.yw_question_ask.get(id=ask_id)
    qid = ask.question_id
    question = get_question([qid])
    out = Struct()
    wrong = set()
    right = set()
    for i in stu_test:
        txt = json.loads(i.text)
        stu = stu_map.get(i.user_id)
        if not stu:
            continue
        for t in txt:
            if ask_id != t['ask_id']:
                continue
            if t["result"] == 1:
                right.add(stu.user_name)
            else:
                wrong.add(stu.user_name)
    for i in question:
        for a in i.asks:
            if a.type == 2:
                a.content = a.content.replace(u'<input placeholder="点击填写">', u'<span class="kong">点击填写</span>')
            if a["id"] == ask_id:
                i.asks = [a]
                break
    out.question = question
    out.wrong = list(wrong)
    out.right = list(right)
    return ajax.jsonp_ok(request, out)


def format_stamp(stamp):
    return time.strftime("%m-%d %H:%M", time.localtime(stamp))
