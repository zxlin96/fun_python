#!/usr/bin/env python
# -*- coding:utf-8 -*-
from jd_assistant import Assistant
from datetime import date
from log import logger
from datetime import datetime
import time
from timer import Timer

if __name__ == '__main__':
    """
    重要提示：此处为示例代码之一，请移步下面的链接查看使用教程👇
    https://github.com/tychxn/jd-assistant/wiki/1.-%E4%BA%AC%E4%B8%9C%E6%8A%A2%E8%B4%AD%E5%8A%A9%E6%89%8B%E7%94%A8%E6%B3%95
    """

    sku_ids = '100012043978'  # 商品id
    area = '16_1303_48716_48765'  # 区域id
    asst = Assistant()  # 初始化
    asst.login_by_QRcode()  # 扫码登陆
    # asst.buy_item_in_stock(sku_ids=sku_ids, area=area, wait_all=False, stock_interval=5)  # 根据商品是否有货自动下单
    buydate = date.today()
    bt = str(buydate) + " 10:00:00.000"
    logger.error(bt)
    time_c = Timer(bt)
    buy_time = time_c.get_time_stamp() # ns
    # TODO 之后将上面的方法写成库 获取时间戳 再获取到对应的网络时间， 我们就可以知道要间隔多久的时间了 之后 只要看时间戳到位没有就可以进行抢购了
    logger.error(buy_time)
    # diff_time = int(time_c.get_server_difference(url='https://a.jd.com//ajax/queryServerData.html'))
    # logger.info(diff_time)
    # asst.add_item_to_cart(sku_ids=sku_ids)
    asst.exec_seckill_by_time_stamp(sku_ids=sku_ids,buy_time=bt,url='https://a.jd.com//ajax/queryServerData.html',retry=2,interval=1,num=2)
    # 6个参数：
    # sku_ids: 商品id。可以设置多个商品，也可以带数量，如：'1234' 或 '1234,5678' 或 '1234:2' 或 '1234:2,5678:3'
    # area: 地区id
    # wait_all: 是否等所有商品都有货才一起下单，可选参数，默认False
    # stock_interval: 查询库存时间间隔，可选参数，默认3秒
    # submit_retry: 提交订单失败后重试次数，可选参数，默认3次
    # submit_interval: 提交订单失败后重试时间间隔，可选参数，默认5秒
