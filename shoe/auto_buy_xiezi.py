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
from log import logger
from timer import Timer
import threading

#创建浏览器对象
options = webdriver.ChromeOptions()
options.add_argument('user-agent="5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36"')
driver_path='../tools/chromedriver'

def buy(url, buy_time,driver):
    '''
    购买函数
    url: 鞋子的申请地址
    buy_time:购买时间
    
    获取页面元素的方法有很多，获取得快速准确又是程序的关键
    在写代码的时候运行测试了很多次，css_selector的方式表现最佳
    '''
    driver.get(url)
    driver.implicitly_wait(10)
    time.sleep(2)
    print("正在抢购，请等待...")
    btn_buy='button'

    t = Timer(buy_time)
    t.start()

    try:
        #找到“结算按钮”，点击
        driver.find_element_by_tag_name(btn_buy).click()
    except Exception as ee:
        print("Worning: %s"%( str(ee) ))

    

if __name__ == "__main__":
    #TODO 做成配置 导入 开售时间 以及 网页ID
    url="https://i.eqxiu.com/s/Yzg6v1o9"
    buydate = datetime.date.today()
    buytime = input("请输入开售时间【默认今天 11:00:00.000】")
    buytime=buytime.strip()
    if buytime=="".strip():
        bt = str(buydate) + " 11:00:00.000"
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
    list_thread = []
    while i <  uc:
        driver = webdriver.Chrome(driver_path, chrome_options=options)
        threading.Thread(target=buy, args=(url, bt,driver)).start()
        # list_thread.append(th)
        i=i+1
        