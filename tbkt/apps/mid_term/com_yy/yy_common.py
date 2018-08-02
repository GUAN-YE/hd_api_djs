# coding: utf-8
import inspect
import datetime
import re
import random

from libs.utils import sms, db

yidong_mobile_pattern = "^1(([3][456789])|([5][012789])|([8][23478])|([4][7])|(78))[0-9]{8}$"


def open_subject(user_id, user_bind_id, subject_id, sn_code='', add_user_id=0, send_open_msg=1):
    """
    功能说明：开通科目科目状态, user_id 或 user_bind_id 必须有一个值,剩余一个可以默认为0
    -------------------------------------------
    修改人     修改时间        修改原因
    -------------------------------------------
    徐威      2015-03-19
    ===========================================
    参数说明：
    send_open_msg 是否发送开通科目短信 0:不发送 1:发送， 默认为发送
    """
    result = {"success": True, "data": {}, "message": ""}
    subject_code_dict = {2: "A", 3: "B", 4: "C", 5:"E", 9: "D"}
    sub_code = subject_code_dict[int(subject_id)]
    if user_bind_id:
        user_bind = db.ketang_slave.mobile_user_bind.get(id=user_bind_id)
    else:
        user_bind = db.ketang_slave.mobile_user_bind.get(user_id=user_id)
    if not add_user_id:
        add_user_id = user_bind.user_id
    # 手机号不是移动不能直接开通
    if not re.match(yidong_mobile_pattern, user_bind.phone_number):
        result["success"] = False
        result["message"] = "不是移动手机号,无法开通"
        return result
    # 已开通了就不能再开通
    if db.ketang_slave.mobile_subject.filter(order_id=user_bind.order_id, code=sub_code, status=2).exists():
        result["success"] = False
        result["message"] = "已经开通过了"
        return result
    region = db.ketang_slave.mobile_order_region.get(user_bind_id=user_bind.id)
    if not region:
        result["success"] = False
        result["message"] = "请先加入班级"
        return result
    school = db.slave.school.get(id=region.school_id)
    open_option = "open"  # "tuiding" or "yongjiushiyong"
    tiyan_remind = ""  # 体验说明备注
    priority = 3  # 优先级别
    if user_bind.order_id <= 0:
        result["success"] = False
        result["message"] = "用户数据异常"
        return result
    fetchall = db.ketang.callproc("sp_add_phone_subject", user_bind.order_id, school.ecid, user_bind.id, user_bind.type, subject_id, open_option, sn_code, user_bind.phone_number, tiyan_remind, add_user_id, priority, 0)
    if fetchall[0][0] <= 0:
        if send_open_msg:  # 发送开通短信
            pass
        result["success"] = False
    return result


def create_ketang_user(user_type, phone_number, username="", password="", real_name="", gender=1, user_id=0, add_user_id=0,
                       add_user_type=2, subject_id=0):
    """
    功能说明：创建课堂用户信息
    -------------------------------------------
    修改人     修改时间        修改原因
    -------------------------------------------
    徐威      2015-03-19
    --------------------------------------
    参数：
     user_type：1学生，3老师
     phone_number：手机号
     username：用户名（账号）
     password：密码
     real_name：用户姓名
     gender：1男  2女
     subject_id：2数学，3物理，4化学，9英语。老师学科（学生用户subject_id=0）
     add_user_id:操作者id
     add_user_type:#1后台添加，2前台添加 （用户类别）
    返回：
    result = {"success": True, "data": {"user_bind_id":12,"phone_order_id":22}, "message": ""}
    """
    result = {"success": True, "data": {}, "message": ""}
    _mobile_pattern = "^1(([3][456789])|([5][012789])|([8][23478])|([4][7]))[0-9]{8}$"

    user_type = int(user_type)
    bind_status = 1  # 用户状态
    now = datetime.datetime.now()
    order = db.ketang_slave.mobile_phone_order.get(phone_number=phone_number)
    if order:
        order_id = order.id
    else:
        order_id = db.ketang.mobile_phone_order.create(phone_number=phone_number, add_user_id=0, add_user_type=1,
                                                add_date=now, del_state=0, data_type=0, add_type=0, add_username='')
    if user_type == 1: # 学生同一个手机可以有多个账号
        user_bind = db.ketang_slave.mobile_user_bind.get(phone_number=phone_number, user_name=real_name, type=user_type)
    else:
        user_bind = db.ketang_slave.mobile_user_bind.get(phone_number=phone_number, type=user_type)
    if user_bind:
        if user_id:
            db.ketang.mobile_user_bind.filter(id=user_bind.id).update(user_id=user_id)  # 绑定用户ID
    else:
        if not username:
            username = "%s%s" % (phone_number, ("xs" if user_type == 1 else "js"))
        if not password:
            password = "".join(random.sample('1234567890', 6))  # 随机生成6位密码
        if re.match(_mobile_pattern, phone_number):
            phone_type = 1
        else:
            phone_type = 0
            bind_status = 0
        is_shield = 1
        if user_type == 3:
            is_shield = 0
        user_bind = db.ketang.mobile_user_bind.create(
                            user_name=real_name,
                            par_name="",
                            type=user_type,
                            sex=gender,
                            relation="",
                            username=username,
                            password=password,
                            phone_number=phone_number,
                            phone_type=phone_type,
                            status=bind_status,
                            subject_id=subject_id,
                            send_flag=0,
                            user_id=user_id,
                            add_user_id=add_user_id,
                            add_user_type=add_user_type,
                            order_id=order_id,
                            is_shield=is_shield
                        )

    result["data"]["phone_order_id"] = order_id
    result["data"]["user_bind_id"] = user_bind.id
    return result


def send_password(user_bind_id, sender={}):
    """
    功能说明：发送账号密码
    -------------------------------------------
    修改人     修改时间        修改原因
    -------------------------------------------
    徐威      2015-03-22
    -------------------------------------------
    """
    sql = """select id, order_id, phone_number, username, password, add_user_id  from mobile_user_bind where id=%s""" % user_bind_id
    bind = db.ketang_slave.fetchone_dict(sql)
    if bind:
        sms_content = u"您的同步课堂账号是:%s 密码是：%s,做作业功能免费，请放心使用。客户端点此m.tbkt.cn下载安装。咨询电话：12556185" % (bind.username, bind.password)
        sms.send_many([bind.phone_number], sms_content, sender)
        now = datetime.datetime.now()
        sql = u"""
        INSERT INTO mp_account_record (order_id, bind_id, batch_id, username, password, phone_number, send_status, add_time, add_user_name, send_date)
        VALUES (%s, %s, 0, '%s', '%s', '%s', 1, "%s", '下发账号', '%s');
        """ %(bind.order_id, bind.id, bind.username, bind.password, bind.phone_number, now, now)
        if db.ketang.execute(sql):
            db.ketang.mobile_user_bind.filter(id=user_bind_id).update(send_flag=1)


def batch_send_password(bind_ids, sender={}):
    """
    批量发送帐号密码
    ---------------------
    王晨光     2017-1-5
    ---------------------
    """
    binds = db.ketang_slave.mobile_user_bind.filter(id__in=bind_ids).select('id', 'order_id', 'phone_number', 'username', 'password')

    # async send
    for b in binds:
        content = u"您的同步课堂账号是:%s 密码是：%s,做作业功能免费，请放心使用。客户端点此m.tbkt.cn下载安装。咨询电话：12556185" % (b.username, b.password)
        sms.send_many([b.phone_number], content, sender)

    # batch write log
    now = datetime.datetime.now()
    records = []
    for b in binds:
        r = {
            'order_id': b.order_id,
            'bind_id': b.id,
            'batch_id': 0,
            'username': b.username,
            'password': b.password,
            'phone_number': b.phone_number,
            'send_status': 1,
            'add_time': now,
            'add_user_name': '下发帐号',
            'send_date': now,
        }
        records.append(r)
    db.ketang.mp_account_record.bulk_create(records)

    # batch update send_flag
    db.ketang.mobile_user_bind.filter(id__in=bind_ids).update(send_flag=1)


def join_unit_class(user_id, dept_id, grade_number, class_number, add_user_id, add_user_type):
    """
    功能说明：加入班级
    -------------------------------------------
    修改人     修改时间        修改原因
    -------------------------------------------
    徐威      2015-03-22
    -------------------------------------------
    参数：
    dept_id：部门ID
    grade_number：年级 1|2|3...
    class_number：班级 101|102...
    add_user_id:操作者id
    add_user_type:#1后台添加，2前台添加 （用户类别）
    """
    result = {"success": True, "data": {}, "message": ""}
    data = db.ketang.callproc("sp_join_unit_class",
                    user_id, dept_id, grade_number, class_number, add_user_id, add_user_type)
    result["data"]["unit_class_id"] = new_class_id = data[0][0]
    return result


def join_unit_class_by_id(user_id, user_bind_id, unit_class_id, add_user_id, add_user_type=2):
    """
    功能说明：指定班级ID加入，user_id 或 user_bind_id 可以只传其中一个，另一个默认为0
    -------------------------------------------
    修改人     修改时间        修改原因
    -------------------------------------------
    徐威      2015-03-22
    -------------------------------------------
    参数：
    unit_class_id:加入班级ID
    user_id：用户ID
    user_bind_id：账号绑定ID
    add_user_id:操作者id
    add_user_type:#1后台添加，2前台添加 （用户类别）
    """
    result = {"success": True, "data": {}, "message": ""}
    db.ketang.callproc("sp_join_unit_class_by_id", user_id, user_bind_id, unit_class_id, add_user_id, add_user_type)
    return result


def remove_unit_class(user_id, user_bind_id, unit_class_id):
    """
    功能说明：移除班级
    -------------------------------------------
    修改人     修改时间        修改原因
    -------------------------------------------
    徐威      2015-03-22
    -------------------------------------------
    """
    result = {"success": True, "data": {}, "message": ""}
    data = db.ketang.callproc("sp_remove_unit_class", user_id, user_bind_id, unit_class_id)
    result["data"] = data
    return result


def import_user(user_type, phone_number, real_name, gender=1, join_unit_class_id=0, open_option="", sn_code="", subject_id=0, send_pwd=0, add_user_id=0, add_user_type=2, send_open_msg=0):
    """
    功能说明：导入用户资料, 如果是短信开通则open_option="open"，如果验证码开通sn_code不能为空，二者选其一
    -------------------------------------------
    修改人     修改时间        修改原因
    -------------------------------------------
    徐威      2015-03-22
    -------------------------------------------
    参数说明：
    add_user_id:操作者id
    add_user_type:#1后台添加，2前台添加 （用户类别）
    open_option: "open"--下发二次确认短信开通
    open_option 和 sn_code 都为空则暂不开通
    send_open_msg 是否发送开通科目短信 0:不发送 1:发送
    """
    result = {"success": True, "data": {}, "message": ""}
    # 创建ketang库用户信息，auth_user信息在登录的时候自动创建
    ketang_data = create_ketang_user(user_type, phone_number, "", "", real_name, gender, 0, add_user_id, add_user_type, 0)
    user_bind_id = ketang_data["data"]["user_bind_id"]
    phone_order_id = ketang_data["data"]["phone_order_id"]
    # 加入班级
    join_unit_class_by_id(0, user_bind_id, join_unit_class_id, add_user_id, add_user_type)

    if open_option == "open" or sn_code:
        open_subject(0, user_bind_id, subject_id, sn_code, add_user_id, send_open_msg)  # 开通科目
    # 是否发送账号密码
    if send_pwd:
        send_password(user_bind_id)
    return result
