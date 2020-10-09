#python3.6.5
#coding:utf-8

'''
@author:抢口罩定制
@time:2020-04-27
程序利用自动测试工具模拟用户下单操作，完成商品的抢购
仅作为学习过程中的实践，无商业用途
'''

from selenium import webdriver
from datetime import date
import time
from log import logger
from timer import Timer
import threading
from datetime import datetime
import configparser
import os
from read_config import ConfigHandler

config_handle=ConfigHandler()

#创建浏览器对象
options = webdriver.ChromeOptions()
options.add_argument('user-agent="5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"')
driver_path = config_handle.read('basic', 'driver_path')

def open_url(url,driver):
    driver.get(url)
    driver.implicitly_wait(10)
    time.sleep(2)

def buy(buy_time,driver):
    '''
    购买函数
    url: 鞋子的申请地址
    buy_time:购买时间
    
    获取页面元素的方法有很多，获取得快速准确又是程序的关键
    在写代码的时候运行测试了很多次，css_selector的方式表现最佳
    '''
    logger.info("正在抢购，请等待...")
    btn_buy='button'

    # t = Timer(buy_time)
    # t.start()

    try:
        #找到“结算按钮”，点击
        driver.find_element_by_tag_name(btn_buy).click()
    except Exception as ee:
        logger.info("Worning: %s"%( str(ee) ))

    

if __name__ == "__main__":
    buydate = date.today()
    #TODO 做成配置 导入 开售时间 以及 网页ID
    if (os.path.exists("./config.txt")==False):
        url="https://i.eqxiu.com/s/msLDPDG9"
        buytime = input("请输入开售时间【默认今天 11:00:00.000】")
        buytime = buytime.strip()
        user_count = input("请输入所要抢购的人数 【默认为 1】")
    else:
        url = config_handle.read('basic', 'address')
        buytime = config_handle.read('basic', 'buytime')
        user_count = config_handle.read('basic', 'user_count')

    if buytime=="".strip():
        bt = str(buydate) + " 11:00:00.000"
    else:
        bt = str(buydate) + " " + buytime
    if user_count=="".strip():
        uc = 1
    else:
        uc = int(user_count)
    
    logger.info("抢购地址：%s"%(url))
    logger.info("选定的抢购时间：%s"%(bt))
    logger.info("选定的抢购人数：%d"%(uc))

    i = 0
    bt_2 = datetime.strptime(bt, "%Y-%m-%d %H:%M:%S.%f")
    prepare_time = int(time.mktime(bt_2.timetuple()))
    while i <  uc:
        driver = webdriver.Chrome(driver_path, chrome_options=options)
        open_url(url,driver)
        # threading.Thread(target=buy, args=(url, bt,driver)).start()
        threading.Timer(prepare_time-time.time(), function=buy, args=(bt,driver)).start()
        # timer_test()
        i=i+1
        