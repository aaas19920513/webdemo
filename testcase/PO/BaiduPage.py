# coding:utf-8

from selenium.webdriver.common.by import By
from testcase.Conmon import BasePage
from selenium.webdriver.common.action_chains import ActionChains


class BaiduPage(BasePage.Action):
    # 定位器
    keywords_loc = (By.ID, 'kw')
    submit_loc = (By.ID, 'su')
    hao123_loc = (By.NAME, 'tj_trhao123')
    more_loc = (By.LINK_TEXT, u'更多产品')
    zhidao_loc = (By.NAME,'tj_zhidao')
    name = 'searchbaidu'
    #   打开页面
    def openbaidu(self,url,pagetitle):
        self.open(url,pagetitle)

    #   输入关键词
    def input_keywords(self, keywords):
        self.find_element(*self.keywords_loc).send_keys(keywords)

    #   点击搜索按钮
    def click_submit(self):
        self.find_element(*self.submit_loc).click()

    #   点击hao123链接
    def click_hao123(self):
        self.find_element(*self.hao123_loc).click()

    #   鼠标悬停在"更多产品"上
    def ActionChains_more(self):
        mouse = self.find_element(*self.more_loc)
        ActionChains(self.driver).move_to_element(mouse).perform()

    #   点击“全部产品”
    def click_zhidao(self):
        self.find_element(*self.zhidao_loc).click()

    def screenshot(self, Bool):
        self.Screenshot(self.name, Bool)


