#coding: utf-8
import datetime
import time
import copy
import sys
import logging
from .common import Struct
from django.db import connections, transaction
from django.db.backends.mysql.base import DatabaseWrapper
from MySQLdb import escape_string

from django.conf import settings
from . import mysql_pool

# 启用连接池
#mysql_pool.enable(settings.DB_POOL_SIZE, settings.DB_WAIT_TIMEOUT)


# django每次会插入一个多余查询:SET SQL_AUTO_IS_NULL = 0
# 1.10版已经去掉了
DatabaseWrapper.init_connection_state = lambda self: None


class ConnectionProxy:
    def __init__(self, conn):
        #conn.close_if_unusable_or_obsolete()
        conn.ensure_connection()
        self.c = conn
        self._c = self.c.connection  # real MySQLdb connection

    def escape(self, s):
        if isinstance(s, datetime.datetime):
            return s.strftime('%Y-%m-%d %H:%I:%S')
        return self._c.escape(s)

    def literal(self, s):
        if isinstance(s, datetime.datetime):
            s = s.strftime('%Y-%m-%d %H:%I:%S')
        return self._c.literal(s)

    def fetchall(self, sql, args=()):
        cursor = self.c.cursor()
        cursor.execute(sql, args)
        rows = cursor.fetchall()
        cursor.close()
        return rows

    def fetchone(self, sql, args=()):
        cursor = self.c.cursor()
        cursor.execute(sql, args)
        row = cursor.fetchone()
        cursor.close()
        return row

    def fetchall_dict(self, sql, args=()):
        cursor = self.c.cursor()
        cursor.execute(sql, args)
        fields = [r[0] for r in cursor.description]
        rows = cursor.fetchall()
        cursor.close()
        return [Struct(zip(fields,row)) for row in rows]

    def fetchone_dict(self, sql, args=()):
        cursor = self.c.cursor()
        cursor.execute(sql, args)
        row = cursor.fetchone()
        cursor.close()
        if not row:
            return
        fields = [r[0] for r in cursor.description]
        return Struct(zip(fields, row))

    def execute(self, sql, args=()):
        """
        Returns affected rows and lastrowid.
        """
        with transaction.atomic(self.c.alias):
            try:
                cursor = self.c.cursor()
                cursor.execute(sql, args)
                cursor.close()
                return cursor.rowcount, cursor.lastrowid
            except:
                logging.error("db execute error2")
                raise

    def execute_many(self, sql, args=()):
        """
        Execute a multi-row query. Returns affected rows.
        """
        with transaction.atomic(self.c.alias):
            cursor = self.c.cursor()
            rows = cursor.executemany(sql, args)
            cursor.close()
            return rows

    def callproc(self, procname, *args):
        """Execute stored procedure procname with args, returns result rows"""
        with transaction.atomic(self.c.alias):
            cursor = self.c.cursor()
            cursor.callproc(procname, args)
            rows = cursor.fetchall()
            cursor.close()
            return rows

    def begin(self):
        """Begin transaction."""
        self.c.begin()

    def commit(self):
        """Commit changes to stable storage"""
        self.c.commit()

    def rollback(self):
        """Roll back the current transaction"""
        self.c.rollback()

    def __getattr__(self, table_name):
        return QuerySet(self, table_name)


class Hub:
    def __getattr__(self, alias):
        """返回一个库的连接"""
        conn = connections[alias]  # django.db.backends.mysql.base.DatabaseWrapper
        return ConnectionProxy(conn)

"""
用法:

>>> db.default.auth_user.get(id=1)
"""
db = Hub()


def atomic(using):
    """
    保证原子操作, 失败会回滚
    写法: 修饰器或with语句
    @atomic(...) or context manager: with atomic(...): ...
    """
    return transaction.atomic(using)


LOOKUP_SEP = '__'


class QuerySet:

    def __init__(self, conn, table_name, db_name=''):
        "conn: a Connection object"
        self.conn = conn
        self.db_name = db_name
        self.table_name = "%s.%s" % (db_name, table_name) if db_name else table_name
        self.select_list = []
        self.cond_list = []
        self.cond_dict = {}
        self.order_list = []
        self.group_list = []
        self.having = ''
        self.limits = []
        self.row_style = 0 # Element type, 0:dict, 1:2d list 2:flat list
        self._result = None
        self._exists = None
        self._count  = None

    def escape(self, value):
        return self.conn.escape(value)

    def literal(self, value):
        if hasattr(value, '__iter__'):
            return '(' + ','.join(self.conn.literal(v) for v in value) + ')'
        return self.conn.literal(value)

    def make_select(self, fields):
        if not fields:
            return '*'
        return ','.join(fields)

    def make_expr(self, key, v):
        "filter expression"
        row = key.split(LOOKUP_SEP, 1)
        field = row[0]
        op = row[1] if len(row)>1 else ''
        if not op:
            if v is None:
                return field + ' is null'
            else:
                return field + '=' + self.literal(v)
        if op == 'gt':
            return field + '>' + self.literal(v)
        elif op == 'gte':
            return field + '>=' + self.literal(v)
        elif op == 'lt':
            return field + '<' + self.literal(v)
        elif op == 'lte':
            return field + '<=' + self.literal(v)
        elif op == 'ne':
            if v is None:
                return field + ' is not null'
            else:
                return field + '!=' + self.literal(v)
        elif op == 'in':
            if not v:
                return '0'
            return field + ' in ' + self.literal(v)
        elif op == 'startswith':
            return field + ' like ' + "'%s%%%%'" % escape_string(str(v))
        elif op == 'endswith':
            return field + ' like ' + "'%%%%%s'" % escape_string(str(v))
        elif op == 'contains':
            return field + ' like ' + "'%%%%%s%%%%'" % escape_string(str(v))
        elif op == 'range':
            return field + ' between ' + "%s and %s" % (self.literal(v[0]), self.literal(v[1]))
        return key + '=' + self.literal(v)

    def make_where(self, args, kw):
        # field loopup
        a = ' and '.join('(%s)'%v for v in args)
        b_list = [self.make_expr(k, v) for k,v in kw.iteritems()]
        b_list = [s for s in b_list if s]
        b = ' and '.join(b_list)
        if a and b:
            s = a + ' and ' + b
        elif a:
            s = a
        elif b:
            s = b
        else:
            s = ''
        return "where %s" % s if s else ''

    def make_order_by(self, fields):
        if not fields:
            return ''
        real_fields = []
        for f in fields:
            if f == '?':
                f = 'rand()'
            elif f.startswith('-'):
                f = f[1:] + ' desc'
            real_fields.append(f)
        return 'order by ' + ','.join(real_fields)

    def reverse_order_list(self):
        if not self.order_list:
            self.order_list = ['-id']
        else:
            orders = []
            for s in self.order_list:
                if s == '?':
                    pass
                elif s.startswith('-'):
                    s = s[1:]
                else:
                    s = '-' + s
                orders.append(s)
            self.order_list = orders

    def make_group_by(self, fields):
        if not fields:
            return ''
        having = ' having %s'%self.having if self.having else ''
        return 'group by ' + ','.join(fields) + having

    def make_limit(self, limits):
        if not limits:
            return ''
        start, stop = limits
        if not stop:
            return ''
        if not start:
            return 'limit %s' % stop
        return 'limit %s, %s' % (start, stop-start)

    def make_query(self, select_list=None, cond_list=None, cond_dict=None,
                   group_list=None, order_list=None, limits=None):
        if select_list is None:
            select_list = self.select_list
        if cond_list is None:
            cond_list = self.cond_list
        if cond_dict is None:
            cond_dict = self.cond_dict
        if order_list is None:
            order_list = self.order_list
        if group_list is None:
            group_list = self.group_list
        if limits is None:
            limits = self.limits
        select = self.make_select(select_list)
        cond = self.make_where(cond_list, cond_dict)
        order = self.make_order_by(order_list)
        group = self.make_group_by(group_list)
        limit = self.make_limit(limits)
        sql = "select %s from %s %s %s %s %s" % (select, self.table_name, cond, group, order, limit)
        return sql

    @property
    def sql(self):
        return self.make_query()

    def flush(self):
        if self._result:
            return self._result
        sql = self.make_query()
        if self.row_style == 1:
            self._result = self.conn.fetchall(sql)
        elif self.row_style == 2:
            rows = self.conn.fetchall(sql)
            vals = []
            for row in rows:
                vals += row
            self._result = vals
        else:
            self._result = self.conn.fetchall_dict(sql)
        return self._result

    def clone(self):
        new = copy.copy(self)
        new._result = None
        new._exists = None
        new._count  = None
        return new

    def group_by(self, *fields, **kw):
        q = self.clone()
        q.group_list += fields
        q.having = kw.get('having') or ''
        return q

    def order_by(self, *fields):
        q = self.clone()
        q.order_list = fields
        return q

    def select(self, *fields):
        q = self.clone()
        q.row_style = 0
        if fields:
            q.select_list = fields
        return q

    def values(self, *fields):
        q = self.clone()
        q.row_style = 1
        if fields:
            q.select_list = fields
        return q

    def flat(self, *fields):
        q = self.clone()
        q.row_style = 2
        if fields:
            q.select_list = fields
        return q

    def get(self, *args, **kw):
        cond_dict = dict(self.cond_dict)
        cond_dict.update(kw)
        cond_list = self.cond_list + list(args)
        sql = self.make_query(cond_list=cond_list, cond_dict=cond_dict, limits=(None,1))
        if self.row_style == 1:
            return self.conn.fetchone(sql)
        else:
            return self.conn.fetchone_dict(sql)

    def filter(self, *args, **kw):
        q = self.clone()
        q.cond_dict.update(kw)
        q.cond_list += args
        return q

    def first(self):
        return self[0]

    def last(self):
        return self[-1]

    def create(self, ignore=False, **kw):
        tokens = ','.join(['%s']*len(kw))
        fields = ','.join(kw.iterkeys())
        ignore_s = ' IGNORE' if ignore else ''
        sql = "insert%s into %s (%s) values (%s)" % (ignore_s, self.table_name, fields, tokens)
        _, lastid = self.conn.execute(sql, kw.values())
        return lastid

    def bulk_create(self, obj_list, ignore=False):
        "Returns affectrows"
        if not obj_list:
            return
        kw = obj_list[0]
        tokens = ','.join(['%s']*len(kw))
        fields = ','.join(kw.iterkeys())
        ignore_s = ' IGNORE' if ignore else ''
        sql = "insert%s into %s (%s) values (%s)" % (ignore_s, self.table_name, fields, tokens)
        args = [o.values() for o in obj_list]
        return self.conn.execute_many(sql, args)

    def count(self):
        if self._count is not None:
            return self._count
        if self._result is not None:
            return len(self._result)
        sql = self.make_query(select_list=['count(*) n'], order_list=[], limits=[None,1])
        row = self.conn.fetchone(sql)
        n = row[0] if row else 0
        self._count = n
        return n

    def exists(self):
        if self._result is not None:
            return True
        if self._exists is not None:
            return self._exists
        sql = self.make_query(select_list=['1'], order_list=[], limits=[None,1])
        row = self.conn.fetchone(sql)
        b = bool(row)
        self._exists = b
        return b

    def make_update_fields(self, kw):
        return ','.join('%s=%s'%(k,self.literal(v)) for k,v in kw.iteritems())

    def update(self, **kw):
        "return affected rows"
        if not kw:
            return 0
        cond = self.make_where(self.cond_list, self.cond_dict)
        update_fields = self.make_update_fields(kw)
        sql = "update %s set %s %s" % (self.table_name, update_fields, cond)
        n, _ = self.conn.execute(sql)
        return n

    def delete(self, *names):
        "return affected rows"
        cond = self.make_where(self.cond_list, self.cond_dict)
        limit = self.make_limit(self.limits)
        d_names = ','.join(names)
        sql = "delete %s from %s %s %s" % (d_names, self.table_name, cond, limit)
        n, _ = self.conn.execute(sql)
        return n

    def __iter__(self):
        rows = self.flush()
        return iter(rows)

    def __len__(self):
        return self.count()

    def __getitem__(self, k):
        if self._result is not None:
            return self._result.__getitem__(k)
        q = self.clone()
        if isinstance(k, (int, long)):
            if k < 0:
                k = -k - 1
                q.reverse_order_list()
            q.limits = [k, k+1]
            rows = q.flush()
            return rows[0] if rows else None
        elif isinstance(k, slice):
            start = None if k.start is None else int(k.start)
            stop = None if k.stop is None else int(k.stop)
            assert k.step is None, 'Slice step is not supported.'
            if stop == sys.maxint:
                stop = None
            if start and stop is None:
                stop = self.count()
            q.limits = [start, stop]
            return q.flush()

    def __bool__(self):
        return self.exists()

    def __nonzero__(self):      # Python 2 compatibility
        return self.exists()

    def wait(self, *args, **kw):
        "扩展: 重复读取从库直到有数据, 表示数据已同步"
        delays = [0, 0.2, 0.4, 0.8, 1.2, 1.4]
        for dt in delays:
            if dt > 0:
                time.sleep(dt)
            r = self.get(*args, **kw)
            if r:
                return r
        logging.warning('slave db sync timeout: %s' % self.table_name)
