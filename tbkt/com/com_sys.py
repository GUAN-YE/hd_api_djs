# coding: utf-8
import time
import threading
import json
from libs.utils import db, get_ip

from django.conf import settings

cache_versions = {}
cache_time = 0
cache_timeout = 60
cache_lock = threading.Lock()


def get_app_version(app_type):
    """
    获取最新APP版本缩略信息
    --------------------
    2017-2-6    王晨光
    --------------------
    :param app_type:
        9   安卓学生端
        10  安卓教师端
        11  苹果学生端
        12  苹果教师端
    :return: {'must':0不强制 1强制升级安装包, 'api':内部版本号}
    """
    global cache_versions, cache_time, cache_timeout, cache_lock

    cache_version = cache_versions.get(app_type)
    nowt = int(time.time())
    if cache_version is not None and (cache_lock.locked() or cache_time >= nowt - cache_timeout):
        return cache_version

    # 避免并发造成多余查询
    with cache_lock:
        version = db.slave.system_version.filter(type=app_type).order_by('release_date', 'id').select('must',
                                                                                                      'api').last()

    cache_versions[app_type] = version
    cache_time = nowt
    return version or {}


def send_im(user_ids, config_id, title, content, payload={}):
    """
    发推送消息
    --------------------
    2017-2-26   王晨光
    --------------------
    :param user_ids: [用户ID]
    :param config_id: 1Demo 2APP学生 3APP教师
    :param title: 消息标题
    :param content: 消息内容
    :param payload: 透传参数
    """
    messages = []
    nowt = int(time.time())
    for user_id in user_ids:
        if user_id:
            m = {
                'user_id': user_id,
                'config_id': config_id,
                'template_type': 1,
                'title': title,
                'content': content,
                'transmission_content': json.dumps(payload),
                'push_status': 0,
                'add_time': nowt,
                'return_value': '',
                'success_time': 0
            }
            messages.append(m)
    if messages:
        db.default.gt_message.bulk_create(messages)


def guess_agent(request):
    """
    猜测客户端类型
    :return: unknown, iphone, android, win
    """
    agent = request.META.get('HTTP_USER_AGENT', '')
    if agent.find('Android') >= 0:
        return 'android'
    elif agent.find('iPhone') >= 0:
        return 'iphone'
    elif agent.find('Win') >= 0:
        return 'win'
    return 'unknown'


def add_access_log(request):
    """
    添加接口访问日志
    --------------------
    2017-6-7    王晨光
    --------------------
    :param request: django Request对象
    """
    # host = request.META.get('HTTP_HOST', '')
    # if not host:
    #     host = settings.URLROOT
    #     host = host.lstrip('http://').lstrip('https://').rstrip('/')
    #
    # path = request.META.get('PATH_INFO', '')
    # ip = get_ip(request)
    # agent = guess_agent(request)
    # nowt = int(time.time())
    # user_id = request.user_id or 0
    # db.default.access_log.create(
    #     host=host,
    #     path=path,
    #     agent=agent,
    #     ip=ip,
    #     user_id=user_id,
    #     add_time=nowt,
    # )
    pass
