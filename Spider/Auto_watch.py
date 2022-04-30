# -*- coding:utf-8 -*-
import re
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from get_url import from_page_get_url, get_package_url
from get_time import get_sleeptime
from selenium.webdriver.chrome.options import Options
import os

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--disable-dev-shm-usage')
chromedriver = "/usr/bin/chromedriver"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chrome_options=chrome_options,executable_path=chromedriver)

# 打开浏览器输入密码并登录
def open_website(driver, url, account, password):
    driver.get(url)
    time.sleep(1)
    driver.find_element(By.ID, "txtUserName2").send_keys(account)
    driver.find_element(By.ID, "txtPassword2").send_keys(password)
    waitJs(driver, select=By.CLASS_NAME, condition="forgetpwd")
    driver.find_element(By.ID, "btnLogin2").click()


# 显性等待函数，等待浏览器加载出需要的元素
def waitJs(driver, select, condition):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((select, condition))
        )
        if driver.find_element(select, condition):
            return driver.find_element(select, condition)
        else:
            pass
    finally:
        pass


def continue_watch():
    if driver.find_element(By.CSS_SELECTOR, ".btnok:nth-child(5)"):
        driver.find_element(By.CSS_SELECTOR, ".btnok:nth-child(5)").click()
    else:
        pass

def print_time(sleep_time):
    for l in range(sleep_time + 1, 0, -1):
        time.sleep(1)
        print("\r{}".format(l), end="")

# 分类别进行条件选择
def  watch(driver, url, choose):
    driver.get(url)
    time.sleep(3)  # 取决于网络状况
    data = driver.page_source  # 获取当前页面源码
    
    
    # 判断是视频
    if "video" in url:
        sleep_time = get_sleeptime(data)
        if choose == True:
            print("点击视频开始按钮")
            driver.find_element(By.CSS_SELECTOR, ".jw-icon-playback").click()
            time.sleep(2)
            data = driver.page_source  # 获取当前页面源码
            time.sleep(2)
            sleep_time = get_sleeptime(data) # 获取时长
            if sleep_time > 1200:
                print("视频类型:时长超过20分钟，跳过")
                pass

            # 如果时长为数字且不等于0，则开始等待
            elif str(sleep_time).isdigit() and 0 < sleep_time < 1200:
                print("视频类型:视频时长小于20分钟，开始计时观看")
                print_time(sleep_time)

            elif sleep_time == 0:
                print_time(15)



        # 判断是视频且点击播放选项为False则直接开始观看视频并等待时长
        elif choose == False:
            if str(sleep_time).isdigit() and sleep_time > 1200:
                print("视频类型:时长超过20分钟，跳过")
                pass

            # 如果时长为数字且不等于0，则开始等待
            elif str(sleep_time).isdigit() and 0 < sleep_time < 1200:
                print("视频类型:视频时长小于20分钟，开始计时观看")
                print_time(sleep_time)


            # 否则等待3秒并退出
            else:
                print("视频类型:遇到额外情况，尝试点击视频开始按钮选")
                watch(driver, url, True)
        


    # 如果是文档，且无法获取时长，则跳过
    elif "document" in url:
        sleep_time = get_sleeptime(data)
        if sleep_time == "['\xa00']" or sleep_time == 0:
            print("文档类型:识别剩余时间错误，跳过")
            pass
        elif str(sleep_time).isdigit() and 0 < sleep_time <1200:
            print("文档类型:识别剩余时间成功")
            print_time(sleep_time)
        elif sleep_time > 1200:
            print("文档类型:时长超过20分钟，跳过")
            pass
        else:
            pass
            print("文档类型:剩余时间识别失败，跳过")

    # 如果是课程包
    elif "package" in url:
        print("课程包类型:进入包内并查看")
        data = driver.page_source  # 获取当前页面源码
        url_list = get_package_url(data)

        for i in range(len(url_list)):
            print("课程包的{}/{}个链接".format(i+1,len(url_list)))
            watch(driver, url_list[i], False)

    # 如果遇到试卷，则跳过
    elif "exam" in url:
        print("试卷类型:遇到试卷，跳过")
        pass

    else:
        print("未识别的链接，跳过")
        pass

        


# 刷视频用的
def brush_video():
    # 登录网址
    url = "http://luxshare-ict.yunxuetang.cn"
    open_website(driver, url, account, password)
    time.sleep(1)
    # 选择目录页
    for i in range(115, 100,-1):
        url = "http://luxshare-ict.yunxuetang.cn/kng/knowledgecatalogsearch.htm?sf=UploadDate&s=dc&pi="
        driver.get(url + str(i))
        URL = from_page_get_url(driver.page_source)
        print("视频总数：", len(URL))
        j = 0
        for url in URL:
            j += 1
            print("\n第{}页第{}/{}个".format(str(i), str(j), str(len(URL))))
            print(url)
            watch(driver, url, False)
    driver.close()


def main():
    brush_video()


if __name__ == "__main__":
    account = 75123180
    account2 = 20000740
    password = 123456
    main()
