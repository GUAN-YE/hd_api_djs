#coding=utf-8

"""
@varsion: ??
@author: 张帅男
@file: com_user.py
@time: 2017/4/7 15:33
"""


import pypinyin
import re
from datetime import date
from django.conf import settings
from libs.utils import db, get_absurl
from libs.utils.common import Struct

def format_ziyuan_url(url):
    """
    文件url 添加前缀2天之内的用江西的前缀，否则河南的前缀
    zsn
    """
    return get_absurl(url)
    # if not url:
    #     return url
    # if url.startswith("http"):
    #     return url
    # date_ziyuan = re.findall(r'/(\d+)/(\d+)/(\d+)/', url)
    # today = date.today()
    # ziyuan_source = ''
    # if date_ziyuan and len(date_ziyuan[0]) == 3:
    #     date_ziyuan = map(int, [d for d in date_ziyuan[0]])
    #     ziyuan_date = date(date_ziyuan[0], date_ziyuan[1], date_ziyuan[2])
    #     ctime = (today - ziyuan_date).days
    #     if ctime <= 2:
    #         ziyuan_source = settings.FILE_TBKT_UPLOAD_URLROOT
    #     else:
    #         ziyuan_source = settings.FILE_WEB_URLROOT
    # else:
    #     ziyuan_source = settings.FILE_WEB_URLROOT
    # if url.endswith("mp3"):
    #     return "%s/upload_media/tts/%s" % (ziyuan_source, url)
    # return "%s/upload_media/%s" % (ziyuan_source, url)

def get_class_students_all(unit_class_id):
    """
    功能说明：           获取班级所有学生
    ----------------------------------------------------------------------------
    修改人                修改时间                修改原因
    ----------------------------------------------------------------------------
    张帅男             2017-1-7                   增加首字母选项
    :param unit_class_id: 班级ID 或 班级ID列表
    """

    if not isinstance(unit_class_id, list):
        unit_class_id = [unit_class_id]

    if unit_class_id and (not all([int(u) for u in unit_class_id])):
        return []

    unit_class_id = [str(u) for u in unit_class_id]

    sql = """
    select
    b.id, b.user_id, b.user_name, b.phone_number, u.portrait, p.sex
    from ketang.mobile_order_region rg
    inner join ketang.mobile_user_bind b on b.id=rg.user_bind_id and b.type=1
    left join tbkt.auth_user u on u.id=b.user_id
    left join tbkt.account_profile p on p.user_id=u.id
    where rg.unit_class_id in (%s) and rg.is_update=0
    """ % ','.join(unit_class_id)

    rows = db.slave.fetchall(sql)

    users = []
    for row in rows:
        bind_id, uid, real_name, phone, portrait, sex = row
        student = Struct()
        student.id = uid or 0
        student.bind_id = bind_id
        student.real_name = real_name or ''
        student.type = 1
        student.portrait = portrait or ''
        student.portrait = get_portrait(portrait, 1)
        student.phone = phone or ''
        student.sex = sex or 1
        student.first_name = get_first_pinyin(real_name)
        users.append(student)
    return users


def get_portrait(portrait, type):
    """
    功能说明:获取用户头像
    ---------------------------------------------------------------------------
    修改人            修改时间                修改原因
    ------------------------------------------------------------------------------
    张帅男            2017-1-6
    """
    if portrait:
        portrait = portrait.strip()
    if portrait:
        return format_ziyuan_url(portrait)
    else:
        if type == 1:
            return 'http://student.tbkt.cn/site_media/images/profile/default-student.png'
        elif type == 2:
            return 'http://student.tbkt.cn/site_media/images/profile/default-parents.png'
        elif type == 3:
            return 'http://student.tbkt.cn/site_media/images/profile/default-teacher.png'
        elif type == 4:
            return 'http://student.tbkt.cn/site_media/images/profile/default-teacher.png'


def get_first_pinyin(unicode):
    if unicode == '':
        return '#'
    rows = pypinyin.pinyin(unicode, style=pypinyin.NORMAL)
    a = ''.join(row[0][0] for row in rows if len(row) > 0)
    return a[0]


def get_user_class(user_id):
    """
    功能说明：获取用户班级数量
  -------------------------------------------------------
    修改人                修改时间                修改原因
    -----------------------------------------------------
    徐威                2015-03-27
    -----------------------------------------------------
    """
    sql = """
        SELECT mor.unit_class_id
        FROM ketang.mobile_order_region mor
        join ketang.mobile_user_bind mub on mub.id=mor.user_bind_id
        join tbkt.school_unit_class c on c.id=mor.unit_class_id
        where mub.user_id = %s
        """ % user_id
    result = db.ketang_slave.fetchall_dict(sql)
    return result


def get_user_info(bind_id):
    """
    功能说明：                获得用户的信息
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-1-12
    """
    sql = " select b.user_name, b.phone_number, u.portrait from ketang.mobile_user_bind b " \
          "left join tbkt.auth_user u on u.id=b.user_id " \
          "where b.id = %s and b.type=1" % bind_id

    user_info = db.tbkt_user.fetchone_dict(sql)
    user_info.portrait = get_portrait(user_info.portrait, 1)
    return user_info