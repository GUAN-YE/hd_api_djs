# coding: utf-8
import SMSInfo

SmsInfo = SMSInfo.SMSInfo()


def send_one(phone_number, sms_content, sender={}):
    """
    功能说明：发送短信根据手机号列表
    ----------------------------------------------------
    修改人                修改时间                修改原因
    ----------------------------------------------------
    徐威                 2015-03-12
    ----------------------------------------------------
    phone_number : 手机号
    sms_content:短信内容
    sender = {
            send_phone  发送手机号
            unit_class_id 发送者班级(主针对教师或学校管理员发送，便于后期短信统计)
            object_id     主记录ID
            object_type   主记录类型默认
            send_user 发送者账号
            accept_user  接收用户姓名
            }
    """
    return SmsInfo.send_one(phone_number, sms_content, sender=sender)


def send_many(phone_list, sms_content, sender={}, ScheduleTime=""):
    """
    功能说明：发送短信根据手机号
    ----------------------------------------------------
    修改人                修改时间                修改原因
    ----------------------------------------------------
    徐威                 2015-03-12
    ----------------------------------------------------
    phone_number_list: ["15290883111","13800002365"]
    sms_content:短信内容
    sender = {
            send_phone  发送手机号
            unit_class_id 发送者班级(主针对教师或学校管理员发送，便于后期短信统计)
            object_id     主记录ID
            object_type   主记录类型默认
            send_user 发送者账号
            accept_user  接收用户姓名
            }
    ScheduleTime:定时发送时间，格式:yymmddhhmmss
    """
    return SmsInfo.send_batch(phone_list, sms_content, ScheduleTime=ScheduleTime, sender=sender)


def remove_timer_sms(sender):
    """
    移除定时短信
    ----------------------
    王晨光     2017-4-11
    ----------------------
    :param sender: {
        'object_id': object_id,
        'object_type': OBJECT_TYPE,
        'schedule_time': schedule_time,
    }
    :return: 成功True 失败False
    """
    return SmsInfo.remove_timer_sms(sender)
