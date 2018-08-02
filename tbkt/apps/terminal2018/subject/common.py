# coding: utf-8
import time

from libs.utils import db


def create_message(task_id, user_id, title, content, begin_time, end_time, unit_ids, agent, subject_id):
    """
    创建 tbkt_com.messages
    :param task_id:  各科作业表主键 -> message object_Id
    :param user_id:
    :param title:    作业标题
    :param content:  短信内容
    :param begin_time:  作业开始时间
    :param end_time:  作业结束时间
    :param agent: 
    :param unit_ids:  班级id集合
    :param subject_id:  班级id集合
    :return:
    """
    with db.default as dd:
        msg_id = dd.message.create(
            type=103,
            subject_id=subject_id,
            object_id=task_id,
            add_user=user_id,
            title=title,
            content=content,
            status=1,
            add_time=int(time.time()),
            begin_time=begin_time,
            end_time=end_time,
            agent=agent
        )
        msg_class = []
        for i in unit_ids:
            d = {'message_id': msg_id, 'unit_class_id': i, 'student_ids': '', 'status': 1}
            msg_class.append(d)
            dd.message_class.bulk_create(msg_class, ignore=True)


def get_text_content(grade_id, tea_name, end_time, subject_id):
    date_string = time.localtime(end_time)
    date_string = time.strftime("%Y-%m-%d", date_string)
    subject_name = "数学"
    if subject_id == 91:
        subject_name = "英语"
    if subject_id == 51:
        subject_name = "语文"
    if grade_id == 6:
        content = u"""家长您好，孩子面临升初中，小学阶段重要知识的系统回顾有益于为初中学习打好基础。我在同步课堂精选了一套%s专项训练卷，帮助孩子做好复习，请及时督促孩子完成。【%s老师】（截止时间：%s，网站地址：www.tbkt.cn,APP下载:m.tbkt.cn）""" % (subject_name, tea_name, date_string)
    else:
        content = u"""家长您好，马上面临期末考试了，我精选了%s复习试卷，帮助孩子做好考前复习，请您及时督促孩子完成试卷并进行错题订正【%s老师】（截止时间：%s，网站地址：www.tbkt.cn,APP下载:m.tbkt.cn）""" % (subject_name, tea_name, date_string)
    return content
