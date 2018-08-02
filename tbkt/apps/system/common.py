#coding: utf-8
import threading
import thread
import time
import datetime
import hashlib
from libs.utils import sockurl, db
from com.com_cache import cache

from django.conf import settings


# {app_type: Lock}
g_locks = {}


def raw_student_url():
    """抓学生端APK商店地址"""
    #url = "http://apk.hiapk.com/appdown/com.tbkt.student/28"
    #if sockurl.ping(url):
    #   return url, 1

    url = "http://shouji.baidu.com/software/22607078.html"
    data = sockurl.get(url, 200000)
    if not data:
        return None, 2
    s, _ = sockurl.find(data, 0, '<div class="area-download">', 'href="', '"')
    return s, 2


def raw_teacher_url():
    """抓教师端APK商店地址"""
    #url = "http://apk.hiapk.com/appinfo/com.tbkt.teacher/11"
    #if sockurl.ping(url):
    #   return url, 1

    url = "http://shouji.baidu.com/software/22607076.html"
    data = sockurl.get(url, 200000)
    if not data:
        return None, 2
    s, _ = sockurl.find(data, 0, '<div class="area-download">', 'href="', '"')
    return s, 2


def callback(type):
    """下载线程"""
    global g_locks

    # 如果其他线程正在爬, 就先返回失败
    lock = g_locks.setdefault(type, threading.Lock())
    if lock.locked():
        return

    with lock:
        if type == 9:
            url, _ = raw_student_url()
        elif type == 10:
            url, _ = raw_teacher_url()
        else:
            url = None
        if url:
            cache.download_url.set(type, url)
        return url


def get_download_url(type):
    """
    抓取应用商店下载地址
    --------------------
    2017-3-3    王晨光
    --------------------
    :type: 9学生APK 10教师APK
    :return: 成功返回APK下载地址,  失败返回None
    """
    url = cache.download_url.get(type)
    if url:
        return url

    thread.start_new_thread(callback, (type,))


def get_upload_key():
    """
    生成uploadkey
    -------------------------------
    王晨光     2016-12-27
    -------------------------------
    """
    now = datetime.datetime.now()
    m = hashlib.md5()
    m.update('%s%s' % (settings.FILE_UPLOAD_SECRET, now.strftime("%Y%m%d")))
    return m.hexdigest()


def active_info(user):
    """
    当前用户是否有参与活动的权限
    ----------------------
    王世成    2017-3-16
    ----------------------
    @param user: 用户对象
    """
    sql = """
    select a.id, a.name,c.city_id,c.county_id, c.is_open, a.user_type, c.school_id,c.grade_id,
    if(c.extend,c.extend,"") extend, c.begin_time, c.end_time, c.banner_url,
    c.begin_url, a.begin_time as banner_begin, a.end_time as banner_end
    from active a, active_config c
    where a.id = c.active_id and is_open != 0
    """
    active = db.slave.fetchall_dict(sql)
    out = []
    for a in active:
        if a.user_type and user.type != a.user_type:
            continue
        if a.city_id and (not user.city or a.city_id != int(user.city)):
            continue
        if a.county_id and (not user.county or a.county_id != int(user.county)):
            continue
        if a.school_id and (not user.school_id or a.school_id != user.school_id):
            continue
        if a.grade_id:
            if user.unit.grade_id not in map(int, a.grade_id.split(',')):
                continue

        now = time.time()

        a.banner_begin = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(a.banner_begin))
        a.banner_end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(a.banner_end))

        if a.begin_time:
            if a.begin_time >= now or now >= a.end_time:
                continue

        d = dict(active_id=a.id,
                 name=a.name,
                 is_open=a.is_open,
                 extend=a.extend or {},
                 banner_begin=a.banner_begin or '',
                 banner_end=a.banner_end or '',
                 banner_url=a.banner_url or '',
                 begin_url=a.begin_url or '')
        if d not in out:
            out.append(d)
    return out


def get_user_block_info(user, type_alias):
    """
    获取用户可见模块接口
    
    @author 王晨光 2017-6-2
    @param user 用户对象
    @param type_alias 模块类型别名
    @return {
        "opensubject_alert": 开通学科提示语,
        "blocks": [{
            "alias": "模块别名",
            "charge": 是否收费,
        }]
    }
    失败返回None
    """
    platform_id = user.platform_id
    bp = db.slave.block_province.get(platform_id=platform_id, type_alias=type_alias)
    if not bp:
        return
    sql = """
    SELECT b.alias, d.charge FROM block_detail d
    inner join block b on b.id=d.block_id
    where d.platform_id=%s and d.visible=1
    """ % platform_id
    blocks = db.slave.fetchall_dict(sql)
    out = {
        'opensubject_alert': bp.opensubject_alert,
        'blocks': blocks,
    }
    return out
