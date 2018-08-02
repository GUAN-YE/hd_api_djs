# coding: utf-8
"""
同步课堂缓存模块

存储格式:
为了通用, KEY也是字符串而且不能有空格, VALUE数据约定用JSON格式.

内部KEY一般长这样:
:1:user_units:897447

内部VALUE一般长这样:
[{"city": "410100", "name": "304\u73ed", "class_id": 4, "type": 1}]

用法:
from apps.common.com_cache import cache

cache.user.set(630445, 'hello')
print cache.user.get(630445)

相当于:
cache.set('user:630445', 'hello', TIMEOUT)
print cache.get('user:630445')
"""
import datetime
import simplejson as json
from simplejson.encoder import JSONEncoder

from django.core.cache import cache as inner_cache
from django.conf import settings

from libs.utils import Struct


class XJSONEncoder(JSONEncoder):
    """
    JSON扩展: 支持datetime和date类型
    """
    def default(self, o):
        if isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')
        else:
            return JSONEncoder.default(self, o)


class CacheProxy:
    """
    存进去的值都强制传为json格式.
    """
    def __init__(self, alias):
        # assert alias in settings.CACHE_KEYS, 'Wrong alias: %s' % alias
        if not alias in settings.CACHE_KEYS:
            print 'APP:Wrong alias:ERROR,%s' % alias
        o = settings.CACHE_KEYS.get(alias, "")
        self.prefix, self.timeout = "", 0
        if o:
            self.prefix = o['realkey']
            self.timeout = o['timeout']

    def make_key(self, arg):
        assert arg
        if isinstance(arg, (tuple, list)):
            arg = ','.join(str(a) for a in arg)
            arg = '[%s]' % arg
        return '%s:%s' % (self.prefix, arg)

    def encodev(self, o):
        return json.dumps(o, cls=XJSONEncoder, encoding='utf-8')

    def decode(self, data):
        if isinstance(data, dict):
            return Struct(data)
        elif isinstance(data, (list, tuple)):
            return [self.decode(d) for d in data]
        return data

    def decodev(self, o):
        if not isinstance(o, basestring):
            return o
        data = json.loads(o)
        return self.decode(data)

    def get(self, arg):
        key = self.make_key(arg)
        v = inner_cache.get(key)
        return self.decodev(v)

    def set(self, arg, value):
        key = self.make_key(arg)
        value = self.encodev(value)
        return inner_cache.set(key, value, timeout=self.timeout)

    def delete(self, arg):
        key = self.make_key(arg)
        return inner_cache.delete(key)

    def get_many(self, args):
        if not args:
            return {}
        keyd = {self.make_key(k):k for k in args}
        results = inner_cache.get_many(keyd.keys())
        prefix_len = len(self.prefix) + 1
        return {keyd[k]:self.decodev(v) for k,v in results.iteritems() if k in keyd}

    def set_many(self, items):
        mapping = {self.make_key(k):self.encodev(v) for k, v in items.iteritems()}
        return inner_cache.set_many(mapping, timeout=self.timeout)

class Cache:
    def __getattr__(self, name):
        return CacheProxy(name)


cache = Cache()

if __name__ == '__main__':
    print cache.user.get(630445)