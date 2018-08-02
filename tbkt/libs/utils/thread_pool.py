#coding: utf-8
import time
import threading
import Queue
import traceback
import logging

POOL_SIZE = 50

q = Queue.Queue()

def loop(id):
    while 1:
        f, args, kwargs = q.get()
        try:
            f(*args, **kwargs)
        except:
            logging.error(traceback.format_exc())


def call(f, *args, **kwargs):
    q.put((f, args, kwargs))


def init():
    print 'thread_pool init.'
    for i in xrange(POOL_SIZE):
        t = threading.Thread(target=loop, args=(i, ))
        t.start()

init()

if __name__ == '__main__':
    def foo(x):
        print x

    call(foo, 1)
    time.sleep(0.1)
    call(foo, 2)

    time.sleep(1)