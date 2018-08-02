#coding: utf-8
import MySQLdb
from .common import *
from .sms import common as sms
from .db import Hub
from django.conf import settings

db = Hub(MySQLdb)
for alias, config in settings.DATABASES.items():
    db.add_pool(alias,
        host=config['HOST'],
        port=int(config.get('PORT', 3306)),
        user=config['USER'],
        passwd=config['PASSWORD'],
        db=config['NAME'],
        charset='utf8',
        autocommit=True,
        pool_size=settings.DB_POOL_SIZE,
        wait_timeout=settings.DB_WAIT_TIMEOUT,
    )
