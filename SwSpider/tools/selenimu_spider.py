# -*- coding: utf-8 -*-
__author__ = 'Sam'
__date__ = '2018/10/25 18:13'

# from selenium import webdriver
#
# browser = webdriver.Chrome(executable_path="D:\project\Swspider\chromedriver.exe")
#
# browser.get("https://detail.tmall.com/item.htm?spm=608.7065813.ne.1.1f8b5aa7Xpl9PY&id=532675606116&tracelog=jubuybigpic")
#
# print(browser.page_source)

import requests

from selenium import webdriver
from time import sleep
from bs4 import BeautifulSoup

browser = webdriver.Chrome(executable_path="D:\project\Swspider\chromedriver.exe")

url = 'https://www.zhihu.com/'
zh_username = '18810072059'
zh_password = 'lds123456'

s = requests.Session()
s.headers.clear()  # 清除requests头部中的Python机器人信息，否则登录失败
browser.get(url)

browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[2]/span').click()  # 避免屏幕失去焦点
browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[1]/div[2]/div[1]/input').send_keys(zh_username)
browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[2]/div/div[1]/input').send_keys(zh_password)

try:
    img = browser.find_element_by_xpath('//*    [@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[3]/div/div[2]/img')  # 验证码图片链接--倒立文字
    sleep(20)
except:
    img = browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/div[3]/div/span/div/img').get_attribute("src")  # 验证码图片链接--字母数字
    sleep(20)  # 填写验证码



browser.find_element_by_xpath('//*[@id="root"]/div/main/div/div/div/div[2]/div[1]/form/button').submit()  # 登录
sleep(5)  # 等待Cookies加载
cookies = browser.get_cookies()
browser.quit()

for cookie in cookies:
    s.cookies.set(cookie['name'], cookie['value'])  # 为session设置cookies

html = s.get(url).text
soup = BeautifulSoup(html)

items = soup.find_all('a', attrs={'data-za-detail-view-element_name': "Title"})  # 获取登录后加载出的前几个话题的标题

for item in items:
    print(item.string)
