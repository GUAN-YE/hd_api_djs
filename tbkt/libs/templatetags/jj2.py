# coding: utf-8
"""添加自定义过滤器"""
import time
from datetime import datetime
from jinja2 import Environment
from jinja2.runtime import Undefined

from django.conf import settings
from libs.utils import get_absurl


def do_date(date, format):
    """时间格式化, 支持整数时间戳
    ~ 用法：{{xxx|date('%Y-%m-%d %H:%M:%S')}}
    """
    if not date:
        return u''
    if isinstance(date, (int, long)):
        t = time.localtime(date)
        date = datetime(*t[:6])
    s = date.strftime(format.encode('utf-8'))
    return s.decode('utf-8')


def do_default(value, default_value=u''):
    "默认值"
    if isinstance(value, Undefined) or (not value):
        return default_value
    return value


def num_to_ch(num):
    """
    功能说明：讲阿拉伯数字转换成中文数字（转换[0, 10000)之间的阿拉伯数字 ）
    ----------------------------------------------------------------------------
    修改人                修改时间                修改原因
    ----------------------------------------------------------------------------
    陈龙                2012.2.9
    """
    num = int(num)
    _MAPPING = (u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九',)
    _P0 = (u'', u'十', u'百', u'千',)
    _S4 = 10 ** 4
    if 0 > num and num >= _S4:
        return None
    if num < 10:
        return _MAPPING[num]
    else:
        lst = []
        while num >= 10:
            lst.append(num % 10)
            num = num / 10
        lst.append(num)
        c = len(lst)  # 位数
        result = u''
        for idx, val in enumerate(lst):
            if val != 0:
                result += _P0[idx] + _MAPPING[val]
            if idx < c - 1 and lst[idx + 1] == 0:
                result += u'零'
        return result[::-1].replace(u'一十', u'十')


def short_cityname(name):
    if name.endswith(u'市'):
        name = name[:-1]
    return name


def do_weekcn(now):
    "过滤成中文星期几"
    return [u'一', u'二', u'三', u'四', u'五', u'六', u'日'][now.weekday()]


def do_cut(s, length, end='...'):
    "截取字符"
    if s:
        return s[:length] + (end if len(s) > length else '')
    return ''


def do_image(path):
    "图片地址转成绝对地址"
    if not path:
        return ''
    return get_absurl(path)


def do_strip(s):
    "取出两端空白"
    return s.strip()


def addslashes(value):
    """
    Adds slashes before quotes. Useful for escaping strings in CSV, for
    example. Less useful for escaping JavaScript; use the ``escapejs``
    filter instead.
    """
    return value.replace('\\', '\\\\').replace('"', '\\"').replace("'", "\\'")


def addgrade(s, num):
    "截取字符"
    if s:
        return s + num
    return ''


def lazypaper(num, num2=2):
    "去5的余数"
    if int(num) == 1:
        return 0
    else:
        return int(num) % int(num2)


filters = {
    'date': do_date,
    'd': do_default,
    'default': do_default,
    'cn': num_to_ch,
    'short_cityname': short_cityname,
    'weekcn': do_weekcn,
    'cut': do_cut,
    'image': do_image,
    'strip': do_strip,
    'addslashes': addslashes,
    'add': addgrade,
    'lazypaper': lazypaper,
}


def finalize(o):
    "把None换成空"
    return '' if o is None else o


class MyUndefined(object):
    "把未定义变量处理为None"

    def __init__(self, *args, **kwargs):
        pass

    def __getattr__(self, name):
        if name[:2] == '__':
            raise AttributeError(name)
        return None

    def __str__(self):
        return u''

    def __len__(self):
        return 0

    def __iter__(self):
        if 0:
            yield None

    def __nonzero__(self):
        return False

    __bool__ = __nonzero__

    def __repr__(self):
        return ''


class Env(Environment):
    def __init__(self, *args, **kw):
        kw['extensions'] = ('jinja2.ext.with_',)  # 启用with语句
        Environment.__init__(self, *args, **kw)
        # 把未定义变量和None处理为空字符串
        self.finalize = finalize
        self.undefined = MyUndefined
        self.filters.update(filters)
