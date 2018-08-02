# coding: utf-8
"""用户常用函数"""
import inspect
from django.conf import settings

from com.com_cache import cache
from libs.utils import ajax, Struct, tbktapi, time, db, from_unixtime, get_absurl

STUDENT_CODES = {2: 'A', 3: 'B', 4: 'C', 9: 'D', 5: 'E'}
TEACHER_CODES = {2: 'J', 3: 'K', 4: 'L', 9: 'M', 5: 'N'}


def users_info(user_ids):
    """
    批量获取用户信息
    :param user_ids: [user_id,]
    :return: {user_id:{name: '',}}
    """
    if not isinstance(user_ids, list):
        user_ids = [user_ids]
    names = db.tbkt_user.auth_user.filter(id__in=user_ids).select('id', 'real_name')[:]
    schools = db.ketang.mobile_order_region.filter(user_id__in=user_ids).select('user_id', 'school_name',
                                                                                'city').group_by('user_id')[:]

    profiles = db.tbkt_user.auth_profile.select("user_id", "portrait").filter(user_id__in=user_ids)[:]

    name_dict = {n.id: n.real_name for n in names}
    school_dict = {s.user_id: s for s in schools}
    profile_dict = {p.user_id: p for p in profiles}
    user_dict = {}
    for uid in user_ids:
        user_dict[uid] = school_dict.get(uid, {'city': '', 'user_id': uid, 'school_name': ''})
        user_dict[uid]['real_name'] = name_dict.get(uid, '')
        portrait = profile_dict.get(uid, {}).get('portrait', '')
        portrait = portrait.strip()
        user_dict[uid][
            "portrait"] = portrait if portrait else "%s/user_media/images/profile/default-student.png" % settings.FILE_MEDIA_URLROOT
    return user_dict


def get_portrait(user, type, portrait=None):
    """
    功能说明:获取用户头像
    ------------------------------------------------------------------------
    修改人            修改时间                修改原因
    ------------------------------------------------------------------------
    杜祖永            2010-7-19
    """
    if portrait:
        return get_absurl(portrait)
    elif user and user.profile and user.profile.portrait.strip():
        return get_absurl(user.profile.portrait)
    else:
        if type == 1:
            return '%s/user_media/images/profile/default-student.png' % settings.FILE_MEDIA_URLROOT
        elif type == 2:
            return '%s/user_media/images/profile/default-parents.png' % settings.FILE_MEDIA_URLROOT
        elif type == 3:
            return '%s/user_media/images/profile/default-teacher.png' % settings.FILE_MEDIA_URLROOT
        elif type == 4:
            return '%s/user_media/images/profile/default-teacher.png' % settings.FILE_MEDIA_URLROOT


def get_open_status(user_id, sids):
    """
    获取学科开通状态
    -----------------------
    2017-6-19    王晨光
    -----------------------
    :param user: User
    :param sids: [学科ID]
    :return: {学科ID: 开通状态(1/0)}
    """
    mslist = db.ketang_slave.mobile_subject.filter(user_id=user_id, subject_id__in=sids).select('subject_id',
                                                                                                'open_date',
                                                                                                'cancel_date',
                                                                                                'pay_type')[:]
    data = []
    nowt = int(time.time())
    msdict = {m.subject_id: m for m in mslist}
    for sid in sids:
        m = msdict.get(sid)
        if m:
            status = 1 if nowt >= m.open_date and (
            m.cancel_date <= 0 or nowt < m.cancel_date) and m.open_date > 0 else 0
            data.append({
                'status': status,
                'subject_id': sid,
                'open_date': from_unixtime(m.open_date),
                'cancel_date': from_unixtime(m.cancel_date) if m.cancel_date > 0 else '',
                'pay_type': m.pay_type,
            })
        else:
            data.append({
                'status': 0,
                'subject_id': sid,
                'open_date': '',
                'cancel_date': '',
                'pay_type': 0,
            })
    return data


def need_login(f):
    """
    ajax强制登录修饰器

    王晨光     2016-10-11
    """

    def wrap(request, *args, **kw):
        user_id = request.user_id
        if not user_id:
            return ajax.jsonp_fail(request, error='no_user', message="请您先登录")
        else:
            return f(request, *args, **kw)

    return wrap


def need_teacher(f):
    """
    教师强制登录修饰器

    王晨光     2017-1-3
    """

    def wrap(request, *args, **kw):
        user = request.user
        if not user:
            return ajax.jsonp_fail(request, error='no_user', message="请您先登录")
        elif not user.is_teacher:
            return ajax.jsonp_fail(request, error='no_user', message="请用教师帐号登录")
        elif not user.units:
            return ajax.jsonp_fail(request, error='no_class', message="请先加入一个班级")
        else:
            return f(request, *args, **kw)

    return wrap


import logging


def get_user(request, user_id):
    """
    成功返回User对象
    失败返回None

    王晨光     2016-12-22
    """
    data = cache.user_profile.get(user_id)
    if not data:
        url = '/account/profile'
        hub = tbktapi.Hub(request)
        r = hub.com.post(url)
        if r['response'] == 'fail':
            return
        data = Struct(r['data'])
        cache.user_profile.set(user_id, data)
    user = User(data, request)
    return user


# 平台配置缓存 {platform_id: {is_sms:bool, is_open:bool, is_setprofile:bool, open_type:[]}}
_platforms = {}
_platforms_expire = 0
PLATFORM_CACHE_TIMEOUT = 3600


def get_platforms():
    """
    获取所有平台配置

    :return:
    {
        平台ID: {
            is_sms:bool, # 是否允许发短信
            is_open:bool, # 是否允许开通
            is_setprofile: bool, # 是否允许个人设置
            open_type:[] # 开通方式: 1微信 2支付宝 3验证码开通
        }
    }
    """
    global _platforms
    global _platforms_expire

    now = time.time()
    if now < _platforms_expire:
        return _platforms or {}

    hub = tbktapi.Hub()
    r = hub.com.get('/system/platforms')
    if not r:
        return {}
    data = r.data
    data = map(Struct, data)
    _platforms = {r.id: r for r in data}
    _platforms_expire = now + PLATFORM_CACHE_TIMEOUT
    return _platforms

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
        logging.info(url)
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


class User:
    """同步课堂用户类, 取代django的User模型

    用法:
    user = User(profile接口数据)
    if user: ...
    """

    def __init__(self, auser, request):
        """
        @param auser auth_user表数据
        """
        self.auser = auser or {}
        for k, v in self.auser.iteritems():
            if k == 'units':
                v = map(Struct, v) if v else []
            setattr(self, k, v)
        self.request = request

    def __len__(self):
        if hasattr(self, 'id'):
            return 1
        return 0

    @property
    def is_sms(self):
        """是否允许发短信()"""
        psettings = get_platforms()
        psetting = psettings.get(self.platform_id) or {}
        return bool(psetting.get('is_sms'))

    @property
    def is_open(self):
        """是否允许开通学科(bool)"""
        psettings = get_platforms()
        psetting = psettings.get(self.platform_id) or {}
        return bool(psetting.get('is_open'))

    @property
    def is_setprofile(self):
        """是否允许个人设置(bool)"""
        psettings = get_platforms()
        psetting = psettings.get(self.platform_id) or {}
        return bool(psetting.get('is_setprofile'))

    @property
    def open_types(self):
        """可用的开通方式(list)"""
        psettings = get_platforms()
        psetting = psettings.get(self.platform_id) or {}
        open_types = psetting.get('open_type') or ''
        open_types = [int(s) for s in open_types.split(',') if s]
        open_types = [i for i in open_types if i > 0]
        return open_types

    def openstatus(self, subject_id):
        """获取指定科目开通状态"""
        hub = tbktapi.Hub(self.request)
        param = dict(subject_id=subject_id, platform_id=self.platform_id)
        r = hub.bank.get('/status', param)
        if not r:
            return 0
        data = Struct(r.data[0])
        return data.status

    @property
    def unit(self):
        """
        学生: 返回学生当前班级
        """
        units = self.units
        return units[0] if units else None

    @property
    def old_user_id(self):
        """
        学生:
        """
        return self.id

    @property
    def is_teacher(self):
        return self.type == 3

    @property
    def city(self):
        units = self.units
        return int(units[0].city) if units else 0

    @property
    def county(self):
        units = self.units
        return int(units[0].county) if units else 0

    @property
    def school_id(self):
        units = self.units
        return int(units[0].school_id) if units else 0

    @property
    def grade_id(self):
        units = self.units
        return int(units[0].grade_id) if units else 0

    def get_mobile_order_region(self, is_slave=True):
        # is_slave 是否读取从库数据
        if is_slave:
            dt = db.ketang_slave
        else:
            dt = db.ketang

        region_map = {
            2: dt.mobile_order_region_jx,  # 江西
            3: dt.mobile_order_region_gx,  # 广西
            4: dt.mobile_order_region_js,  # 江苏
            5: dt.mobile_order_region_sx,  # 山西
            6: dt.mobile_order_region_qg  # 北京(全国)
        }
        return region_map.get(self.platform_id, dt.mobile_order_region)


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
            info.portrait = i.portrait   # i.units
            out.append(info)
    return out
