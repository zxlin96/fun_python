#python3.6.5
#coding:utf-8

'''
@author:抢口罩定制
@time:2020-04-27
程序利用自动测试工具模拟用户下单操作，完成商品的抢购
仅作为学习过程中的实践，无商业用途
'''

from selenium import webdriver
import datetime
import time
from timer import Timer
from datetime import date
from log import logger
from datetime import datetime
import threading

#创建浏览器对象
options = webdriver.ChromeOptions()
options.add_argument('user-agent="5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"')
# driver = webdriver.Chrome('./chromedriver', chrome_options=options)
driver_path='../tools/chromedriver'

#窗口最大化显示
# driver.maximize_window()

def login(url,mall,driver):
    '''
    登陆函数
    
    url:商品的链接
    mall：商城类别
    '''
    logger.info("请登录")
    driver.get(url)
    driver.implicitly_wait(10)
    time.sleep(2)
    #淘宝和天猫的登陆链接文字不同
    logger.info("mall2: %d", mall)
    if mall==1:
        #找到并点击淘宝的登陆按钮
        driver.find_element_by_link_text("亲，请登录").click()
    elif mall==3:
        logger.info("30秒后开始自动抢购")
        time.sleep(30)
    else:
        #找到并点击天猫的登陆按钮
        driver.find_element_by_link_text("请登录").click()
    #用户扫码登陆
    if mall!=3:
        logger.info("30秒后开始自动抢购")
        time.sleep(30)
    
def buy(buy_time,mall,driver):
    '''
    购买函数
    
    buy_time:购买时间
    mall:商城类别
    
    获取页面元素的方法有很多，获取得快速准确又是程序的关键
    在写代码的时候运行测试了很多次，css_selector的方式表现最佳
    '''
    logger.info("正在抢购，请等待...")

    if mall==1:
        #"立即购买"的css_selector
        btn_buy='#J_juValid > div.tb-btn-buy > a'
        #"立即下单"的css_selector
        btn_order='#submitOrder_1 > div.wrapper > a'
    elif mall==3:
        btn_buy="结 算"
        btn_order="提交订单"
    else:
        btn_buy='#J_LinkBuy'
        btn_order='#submitOrderPC_1 > div > a'

    if mall==3:
        #找到“结算按钮”，点击
        driver.find_element_by_link_text(btn_buy).click()
    else:
        #找到“立即购买”，点击
        driver.find_element_by_css_selector(btn_buy).click()

    while True:
        try:
            if mall==3:
                #找到“提交订单”，点击
                driver.find_element_by_link_text(btn_order).click()
            else:
                driver.find_element_by_css_selector(btn_order).click()
            #下单成功，跳转至支付页面
            logger.info("订单提交成功")
            break
        except Exception as ee:
            logger.info(str(ee))
            time.sleep(0.01)
    

if __name__ == "__main__":
    #url = "https://detail.tmall.com/item.htm?spm=a1z0d.6639537.1997196601.4.b42a7484vqMOeS&id=523741145509"
    url="https://cart.tmall.com/cart.htm?from=bmini&tpId=725677994"
    mall=int(input("请选择商城（淘宝 1  天猫 2  天猫超市 3输入数字即可）： "))
    buydate = date.today()
    logger.info("mall %d", mall)
    buydate = date.today()
    buytime = input("请输入开售时间【默认今天 20:00:00.000】")
    buytime=buytime.strip()
    if buytime=="".strip():
        bt = str(buydate) + " 20:00:00.000"
    else:
        bt = str(buydate) + " " + buytime
    logger.info("选定的抢购时间：%s"%(bt))
    user_count = input("请输入所要抢购的人数 【默认为 1】")
    if user_count=="".strip():
        uc = 1
    else:
        uc = int(user_count)
    logger.info("选定的抢购人数：%d"%(uc))
    
    i = 0
    bt_2 = datetime.strptime(bt, "%Y-%m-%d %H:%M:%S.%f")
    prepare_time = int(time.mktime(bt_2.timetuple()))
    while i <  uc:
        driver = webdriver.Chrome(driver_path, chrome_options=options)
        login(url,mall,driver)
        # threading.Thread(target=buy, args=(url, bt,driver)).start()
        threading.Timer(prepare_time-time.time(), function=buy, args=(bt,mall,driver)).start()
        # timer_test()
        i=i+1
    while 1:
    	time.sleep(10)
