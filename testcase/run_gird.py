# encoding:utf-8

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time, os.path
import gird

for host, browser in gird.grid().items():
    driver = webdriver.Remote(
        command_executor=host,
        desired_capabilities={
            'platform': 'ANY',
            'browserName': browser,
            'version': '',
            'javascriptEnabled': True
        }
    )
    driver.get("http://www.baidu.com")
    driver.find_element_by_id("kw").send_keys(u"中国")
    driver.find_element_by_id("su").click()
    time.sleep(3)
    if driver.title == u"中国_百度搜索":
        print("title匹配！")
    else:
        print("title不匹配！")
    driver.close()