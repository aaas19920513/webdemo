# -*- coding:utf-8 -*-
import unittest
from selenium import webdriver
from testcase.Conmon.BasePage import Action
from PO.BaiduPage import BaiduPage
from testcase.Conmon import BasePage
from time import sleep
'''
project:百度页面测试
'''


class TestBaiduSearch(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Ie()
        self.url = 'https://www.baidu.com/'
        self.keyword = 'PO'
        self.baidu_page = BaiduPage(self.driver)
        self.pagetitle = u'你好'
        self.short = BasePage.Action(self.driver)


    def test_baidu_search(self):
        u'''百度搜索'''
        try:
            self.baidu_page.open(self.url, self.pagetitle)
            self.baidu_page.input_keywords(self.keyword)
            self.baidu_page.click_submit()
            sleep(2)
            self.assertIn(self.keyword, self.driver.title)
            self.short.Screenshot(u'search', 'pass')
        except Exception as e:
            self.short.Screenshot(u'search', 'fail')
            raise e

    def tearDown(self):
        self.driver.close()


