#coding: utf-8
import datetime, requests
import time
import traceback
import logging
import json
import re
import pypinyin
from . import ajax

from django.template import RequestContext, loader, Context
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.conf import settings
from tbkt.settings import FILE_MEDIA_URLROOT, FILE_VIEW_URLROOT

log = logging.getLogger(__name__)

RE_CHINAMOBILE = re.compile(r"^1(([3][456789])|([5][012789])|([8][23478])|([4][7]))[0-9]{8}$")


class Struct(dict):
    """
    - 为字典加上点语法. 例如:
    >>> o = Struct({'a':1})
    >>> o.a
    >>> 1
    >>> o.b
    >>> None
    """
    def __init__(self, *e, **f):
        if e:
            self.update(e[0])
        if f:
            self.update(f)

    def __getattr__(self, name):
        # Pickle is trying to get state from your object, and dict doesn't implement it.
        # Your __getattr__ is being called with "__getstate__" to find that magic method,
        # and returning None instead of raising AttributeError as it should.
        if name.startswith('__'):
            raise AttributeError
        return self.get(name)

    def __setattr__(self, name, val):
        self[name] = val

    def __delattr__(self, name):
        self.pop(name, None)

    def __hash__(self):
        return id(self)


def render_template_data(request, template_path, context):
    t = loader.get_template(template_path)
    if hasattr(request, 'user'):
        user = request.user
        context['user'] = user
    context['settings'] = settings
    s = t.render(context, request)
    return s


def render_template(request, template_path, context={}):
    s = render_template_data(request, template_path, context)
    return HttpResponse(s)


def safe(path):
    """
    功能说明：       安全修饰器, path: 模板路径
    如果页面报错, 至少给用户返回一个无数据的模板页面
    ----------------------------------------------------------------------------
    修改人                修改时间                修改原因
    ----------------------------------------------------------------------------
    王晨光                2016.5.27
    """
    def _safe(f):
        def wrap(request, *args, **kw):
            try:
                o = f(request, *args, **kw)
                if o is None:
                    o = {}
                if isinstance(o, dict):
                    return render_template(request, path, o)
                else:
                    return o
            except:
                exc = traceback.format_exc()
                log.error(exc)
                r = render_template(request, path, {})
                r.status_code = 500
                return r
        return wrap
    return _safe


def num_to_ch(num):
    """
    功能说明：讲阿拉伯数字转换成中文数字（转换[0, 10000)之间的阿拉伯数字 ）
    ----------------------------------------------------------------------------
    修改人                修改时间                修改原因
    ----------------------------------------------------------------------------
    陈龙                2012.2.9
    """
    num = int(num)
    _MAPPING = (u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', )
    _P0 = (u'', u'十', u'百', u'千', )
    _S4 = 10 ** 4
    if 0 > num and num >= _S4:
        return None
    if num < 10:
        return _MAPPING[num]
    else:
        lst = [ ]
        while num >= 10:
            lst.append(num % 10)
            num = num / 10
        lst.append(num)
        c = len(lst) # 位数
        result = u''
        for idx, val in enumerate(lst):
            if val != 0:
                result += _P0[idx] + _MAPPING[val]
            if idx < c - 1 and lst[idx + 1] == 0:
                result += u'零'
        return result[::-1].replace(u'一十', u'十')


def strxor(s, key):
    "异或加密"
    key = key & 0xff
    a = bytearray(s)
    b = bytearray(len(a))
    for i, c in enumerate(a):
        b[i] = c ^ key
    return str(b)


def type_default_value(type):
    "返回基本类型默认值, 没有识别的类型返回None"
    tab = {str:"", unicode:u"", list:[], int:0}
    return tab.get(type)


def casts(self, **kw):
    """
    功能说明：       批量转换url参数类型
    用法:
    >>> request.GET.__class__ = casts
    >>> args = request.GET.casts(keyword=str, page=int, a="(\d+)")
    >>> print args
    >>> {'keyword': '', 'page':0, 'a':''}
    ----------------------------------------------------------------------------
    修改人                修改时间                修改原因
    ----------------------------------------------------------------------------
    王晨光                2016-6-26
    """
    args = Struct()
    for k, typ in kw.iteritems():
        v = self.get(k)
        if isinstance(typ, basestring):
            if typ == 'json':
                try:
                    v = json.loads(v) if v else {}
                except:
                    pass
            elif typ == 'datetime':
                if v:
                    t = time.strptime(v, "%Y-%m-%d %H:%M:%S")
                    v = datetime.datetime(*t[:6])
                else:
                    v = None
            elif typ == 'timestamp':
                if v:
                    t = time.strptime(v, "%Y-%m-%d %H:%M:%S")
                    d = datetime.datetime(*t[:6])
                    v = int(time.mktime(d.timetuple()))
            else:
                m = re.match(typ, v or '')
                groups = m.groups() if m else ()
                groups = [g for g in groups if g is not None]
                v = groups[0] if groups else ''
        else:
            defv = type_default_value(typ)
            try:
                v = typ(v) if v is not None else defv
            except:
                v = defv
        args[k] = v
    return args


def loads(self):
    """
    功能说明：      解析json格式参数
    用法:
    >>> request.__class__ = loads
    >>> args = request.loads()
    >>> print args
    >>> {}
    解析失败返回空字典
    ----------------------------------------------------------------------------
    修改人                修改时间                修改原因
    ----------------------------------------------------------------------------
    王晨光                2016-10-10
    """
    try:
        o = json.loads(self.body)
    except:
        o = {}
    return Struct(o)


def is_chinamobile(phone):
    """
    功能说明：       判断是否为移动手机号
    ----------------------------------------------------------------------------
    修改人                修改时间                修改原因
    ----------------------------------------------------------------------------
    王晨光                2016-10-10
    """
    if not isinstance(phone, basestring):
        return False
    return RE_CHINAMOBILE.match(phone)


def pinyin_abb(name):
    """
    功能说明：       将姓名转换为拼音首字母缩写
    >>> pinyin_abb(u'王晨光')
    >>> wcg
    ----------------------------------------------------------------------------
    修改人                修改时间                修改原因
    ----------------------------------------------------------------------------
    王晨光                2016-10-10
    """
    if not isinstance(name, unicode):
        name = name.decode('utf-8')
    rows = pypinyin.pinyin(name, style=pypinyin.NORMAL)
    return ''.join(row[0][0] for row in rows if len(row)>0)


def is_chinese_word(s, minlen=2, maxlen=5):
    """
    功能说明：           判断字符串(Unicode)是否为全中文
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    王晨光                    2015-5-18
    """
    if not s:
        return False
    if not isinstance(s, unicode):
        s = s.decode('utf-8')
    for ch in s:
        if u'\u4e00' <= ch <= u'\u9fff':
            pass
        else:
            return False
    if len(s) < minlen or len(s) > maxlen:
        return False
    return True


def guess_client_type(request):
    """
    猜测客户端类型
    -----------------------------------
    王晨光     2016-11-9
    -----------------------------------
    :return: 1:Android 2:iPhone 0:其他
    """
    agent = request.META.get('HTTP_USER_AGENT', '')
    if agent.find('Android') >= 0:
        return 1
    elif agent.find('iPhone') >= 0:
        return 2
    return 0


def get_absurl(path):
    """
    获得文件绝对路径
    -----------------------------------
    王晨光     2016-11-9
    吕杨       2017-5-?   
        判断上传日期在两天以内的用江西的文件服务器, 否则就用河南的文件服务器
    -----------------------------------
    get_absurl("/score/gift/2016/03/03/20160303164135334193.png")
    返回
    http://file.tbkt.cn/upload_media/score/gift/2016/03/03/20160303164135334193.png
    """
    if not path:
        return ''
    if path.startswith("http"):
        return path
    date_ziyuan = re.findall(r'/(\d+)/(\d+)/(\d+)/', path)
    today = datetime.date.today()
    if date_ziyuan and len(date_ziyuan[0]) == 3:
        date_ziyuan = map(int, [d for d in date_ziyuan[0]])
        ziyuan_date = datetime.date(date_ziyuan[0], date_ziyuan[1], date_ziyuan[2])
        ctime = (today - ziyuan_date).days
        if ctime <= 2:
            ziyuan_source = settings.FILE_VIEW_URLROOT
        else:
            ziyuan_source = settings.FILE_VIEW2_URLROOT
    else:
        ziyuan_source = settings.FILE_VIEW2_URLROOT
    if path.endswith("mp3"):
        return "%s/upload_media/tts/%s" % (ziyuan_source, path)
    return "%s/upload_media/%s" % (ziyuan_source, path)


def get_videourl(path):
    """
    返回视频绝对地址
    """
    if not path:
        return ''
    return "%s/upload_media/%s" % (settings.FLV_WEB_URLROOT, path)


def from_unixtime(stamp):
    """时间戳转Datetime"""
    if not isinstance(stamp, (int, long)):
        return stamp
    st = time.localtime(stamp)
    return datetime.datetime(*st[:6])


def join(o):
    """
    把数组用逗号连接成字符串
    
    例如:
    >>> join([1, 2])
    >>> '1,2'
    """
    if isinstance(o, (list, tuple)):
        return ','.join(str(i) for i in o)
    return str(o)


def ajax_try(data=""):
    """
    接口异常修饰器
    ---------------------
    王晨光     2017-2-17
    ---------------------
    :param data: 默认data
    """
    def foo(f):
        def wrap(request, *args, **kw):
            try:
                return f(request, *args, **kw)
            except:
                exc = traceback.format_exc()
                log.error(exc)
                return ajax.jsonp_fail(request, error="500", data=data, message="抱歉，服务器开小差了，请联系客服12556185")
        return wrap
    return foo


def get_ip(request):
    """
    获取用户IP

    王晨光     2016-09-19

    :returns: ip address
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return x_forwarded_for or ''


def dedupe(items):
    """
    去重
    :param items: list集合
    :return:
    """
    seen = set()
    for i in items:
        if i not in seen:
            yield i
            seen.add(i)


def format_url(data_url, tts=None):
    """根据日期判断 资源所用服务器"""
    if not data_url:
        return ''
    if data_url.startswith("http") or data_url.startswith("https"):
        return data_url
    tts_root = '/upload_media/tts/' if tts else '/upload_media/'
    _url = settings.FILE_VIEW2_URLROOT + tts_root + data_url
    try:
        date = re.findall(r'/(\d+)\.', data_url)
        today = datetime.date.today()
        if date and len(date[-1]) >= 8:
            date_num = date[-1]
            video_date = datetime.date(year=int(date_num[:4]), month=int(date_num[4:6]), day=int(date_num[6:8]))
            ctime = (today - video_date).days
            if ctime <= 2:
                _url = settings.FILE_VIEW_URLROOT + tts_root + data_url
    except:
        return _url
    return _url


def get_ling_time():
    """
    功能说明：                获取当前时间 零点的时间戳
    -----------------------------------------------
    修改人                    修改时间
    -----------------------------------------------
    张帅男                    2017-9-13
    """
    today = datetime.datetime.today()
    ling = datetime.datetime(today.year, today.month, today.day, 0, 0, 0)
    ling = time.mktime(ling.timetuple())
    return int(ling)


def replace_url_ziyaun(path):

    '''
    topic.cy_Tupian = FILE_VIEW_URLROOT + topic.cy_Tupian.replace("/UploadFileS/","/upload_media/yuwen/")
    :param request:
    :param path:
    :return:
    '''

    return FILE_VIEW_URLROOT + path.replace("/UploadFileS/","/upload_media/yuwen/")