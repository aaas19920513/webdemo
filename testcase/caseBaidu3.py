# coding:utf-8

import unittest
from selenium import webdriver
from testcase.Conmon.BasePage import Action
from PO.BaiduPage import BaiduPage
from time import sleep
'''
project:百度页面测试
'''


class TestBaiduSearch(unittest.TestCase):
    def setUp(self):
        print 'test start'
        self.driver = webdriver.Firefox()
        self.url = 'https://www.baidu.com/'
        self.keyword = 'python'
        self.baidu_page = BaiduPage(self.driver, self.url, u'百度')

    def test_baidu_search(self):
        u'''百度搜索'''
        try:
            self.baidu_page.open()
            self.baidu_page.input_keywords(self.keyword)
            self.baidu_page.click_submit()
            sleep(2)
            self.assertIn(self.keyword, self.driver.title)
        except Exception as e:
#            self.baidu_page.img_screenshot(u'百度搜索')
            raise e




    def tearDown(self):
        self.driver.close()
        print 'test end'