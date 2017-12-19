# -*- coding:utf-8 -*-
import unittest
from selenium import webdriver
from PO import LoginPage
from parameterized import parameterized

class Testlogin(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print 'test start'
        cls.driver = webdriver.Ie()
        cls.url = 'https://www.mingdao.com/login.htm'
        cls.login = LoginPage.LoginPage(cls.driver,)
        cls.title = u"明道"

    @parameterized.expand([('case01', '3555', 'sadfasdf', u'密码不正确'),
                           ('case02', 'asdfsaf', '', u'用户名不正确'),
                           ('case03', 'sdfa', 'ddddddddddd', u'密码用户名不正确')
                           ])

    def test_login(self,case_id, username, password,case_summary):
        u'''登陆测试用例'''
        try:
            print u"========【" + case_id + u"】" + case_summary + "============="
            print '用户名：'+username
            print '密码：'+password
            self.login.open(self.url, self.title)
            self.login.input_username(username)
            self.login.input_password(password)
            self.login.click_submit()
        except:
            print ' login faild'



    @classmethod
    def tearDownClass(cls):
        cls.driver.close()
        print 'test end'
if __name__ == '__main__':
    unittest.main(verbosity=2)