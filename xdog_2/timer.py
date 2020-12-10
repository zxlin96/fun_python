# -*- coding:utf-8 -*-
import time
from datetime import datetime

from log import logger
import json
import requests



class Timer(object):

    def __init__(self, buy_time, sleep_interval=0.05):

        # '2018-09-28 22:45:50.000'
        self.buy_time_input = buy_time
        self.buy_time = datetime.strptime(buy_time, "%Y-%m-%d %H:%M:%S.%f")
        self.sleep_interval = sleep_interval

    def start(self):
        logger.info('正在等待到达设定时间:%s' % self.buy_time)
        now_time = datetime.now
        while True:
            if now_time() >= self.buy_time:
                logger.info('时间到达，开始执行……')
                break
            else:
                time.sleep(self.sleep_interval)
    def get_time_stamp(self):
        time_stamp_st = time.strptime(self.buy_time_input, "%Y-%m-%d %H:%M:%S.%f")
        time_stamp = int(time.mktime(time_stamp_st))
        print(self.buy_time)
        return time_stamp
    def get_server_difference(self,url):    
        t0 = time.clock_gettime_ns(time.CLOCK_REALTIME)
        try:
            ret = requests.session().get(url).text
            js = json.loads(ret)
            t = int(js["serverTime"])*1000000
        except Exception as e:
            logger.error(e)
            return 0

        t1 = time.clock_gettime_ns(time.CLOCK_REALTIME)
        server_time = t+((t1-t0)/2)
        logger.info("diff_time: %d", t1-server_time)
        return t1-server_time
    def start_by_time_stamp(self,time_stamp,url,sleep_interval=0.05):
        logger.info('正在等待到达设定时间:%d',  time_stamp)
        diff_time = 0
        i = 0
        while True:
            if(i % (10/sleep_interval) == 0 and len(url) > 0):
                diff_time = self.get_server_difference(url=url)
            if time.clock_gettime_ns(time.CLOCK_REALTIME) >= time_stamp*1000*1000*1000 + diff_time:
                logger.info('时间到达，开始执行……')
                break
            else:
                time.sleep(self.sleep_interval)
                i=i+1