# -*- coding: utf-8 -*-
# @Time    : 2021/12/8 上午10:06
# @Author  : mozhouqiu
# @FileName: worker.py
# @Email    ：15717163552@163.com
import configparser
import os
import uuid
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

import redis


proDir = os.path.split(os.path.realpath(__file__))[0]
configPath = os.path.join(proDir, "config.ini")
conf = configparser.ConfigParser()
conf.read(configPath)


class AsyncTask():

    @staticmethod
    def call_back(res):
        rc = redis.StrictRedis(host=conf.get("redis","host"), port=conf.get("redis","port"), db=conf.get("redis","db"))
        key = uuid.uuid4()
        rc.hset(str(key), "data", res.result() if res.result() else "None")

    @classmethod
    def async_task(self,func):
        @wraps(func)
        def inner(*args, **kwargs):
            pool = ThreadPoolExecutor(max_workers=1, )
            pool.submit(func, *args, **kwargs).add_done_callback(AsyncTask.call_back)
        return inner








