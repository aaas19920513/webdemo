#-*- coding:utf-8 -*-

import sys

from selenium.webdriver.common.by import By

from testcase.Conmon import BasePage
from testcase.Conmon import saveScreenshot
reload(sys)
sys.setdefaultencoding('utf-8')
class baiduPage(BasePage.Action):
#    filepath = '\\Data\\baidu_data.xls'
#    loc = BasePage.Action
#    search_loc1 = loc.locate('ele_001',filepath)
    url = 'http://www.baidu.com/'
    search_loc = (By.ID, 'kw')
    pagetitle = '百度一下，你就知道'
    driver = None
    def open_baidu(self):
#        self.startBroswer()

        self._open(self.url, self.pagetitle)
        saveScreenshot.saveScreenshot(self.driver, 'login')

    def search_input(self, word):

        self.send_keys(self.search_loc, word, click_first=True)




