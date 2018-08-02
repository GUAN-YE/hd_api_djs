# coding: utf-8
"""基于socket的快速爬虫工具包"""
import math
import socket


class Struct(dict):
    """
    Dict to object. e.g.:
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


def parse(url):
    """
    将url分解为协议, 主机名, 端口, 路径

    :param url: http://apk.hiapk.com/appinfo/com.tbkt.student/28
    :return: {'protocal':'http', 'host':'apk.hiapk.com', 'port':80, 'scheme':'apk.hiapk.com', 'path':'/appinfo/com.tbkt.student/28'}
    """
    r = url.split('://', 1)
    if len(r) == 2:
        protocal, s = r
    else:
        protocal = 'http'
        s = url

    r = s.split('/', 1)
    if len(r) == 2:
        scheme, path = r
        path = '/' + path
    else:
        host = r[0]
        path = '/'

    r = scheme.rsplit(':', 1)
    if len(r) == 2:
        host, port = r
        port = int(port)
    else:
        host = r[0]
        port = 443 if protocal=='https' else 80

    out = Struct()
    out.protocal = protocal
    out.scheme = scheme
    out.host = host
    out.port = port
    out.path = path
    return out

    return protocal, host, port, path


def get(url, size, timeout=2.0):
    """
    返回请求结果

    :param size: 截取多少字节
    :return: 响应数据 None请求失败
    """
    p = parse(url)
    c = socket.socket()
    c.settimeout(timeout)
    try:
        c.connect((p.host, p.port))
        req = "GET %s HTTP/1.1\r\nHost: %s\r\n\r\n" % (p.path, p.scheme)
        c.sendall(req)
        block_size = 8192
        bn = int(math.ceil(1.0*size/block_size))
        data = ''
        for i in xrange(bn):
            s = c.recv(block_size)
            if not s:
                break
            data += s
        return data
    except socket.error:
        return
    finally:
        c.close()


def ping(url, ok_status=[200,301,302], timeout=2.0):
    """
    检测url是否能正常点击

    :return: True正常 False不正常
    """
    data = get(url, 100, timeout)
    if not data:
        return False
    reqline = data.split('\r\n', 1)[0]
    r = reqline.split(' ')
    if len(r) != 3:
        return False
    code = int(r[1])
    return code in ok_status


def find(src, pos, *tags):
    """
    查找标签内字符串
    >>> find('abc <a href=x>vvvv</a>', 'abc', 'href=x>', '</a>')
    >>> vvvvv, 23

    :param pos: 起始位置
    :param tags: [定位串, ..., 闭合串]
    :return: 结果串, 失败返回None, None
    """
    assert len(tags) >= 2
    begins, end = tags[:-1], tags[-1]
    for begin in begins:
        pos = src.find(begin, pos)
        if pos < 0:
            return None, None
        pos += len(begin)
    e = src.find(end, pos)
    if e < 0:
        return None, None
    return src[pos:e], e+len(end)


def get_download_url():
    """尝试获取可用下载地址, 失败返回None"""
    url = "http://apk.hiapk.com/appdown/com.tbkt.student/28"
    if ping(url):
       return url

    url = "http://shouji.baidu.com/software/10319290.html"
    data = get(url, 200000)
    s, _ = find(data, 0, '<div class="area-download">', 'href="', '"')
    return s


if __name__ == '__main__':
    #print parse('http://apk.hiapk.com/appinfo/com.tbkt.student/28')
    #print ping('http://apk.hiapk.com/appdown/com.tbkt.student/28')
    #print ing('http://211.142.194.137/apk.r1.market.hiapk.com/data/upload/apkres/2016/11_11/17/com.tbkt.student_052907.apk?wsiphost=local')
    #print get('http://shouji.baidu.com/software/10319290.html', 1000)
    #print find('abc <div class="area-download">123456789</div>', 0, 'abc', 'download">', '</div>')
    print get_download_url()