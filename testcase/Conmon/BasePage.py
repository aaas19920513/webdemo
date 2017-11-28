#-*- coding:utf-8 -*-
from selenium.webdriver.common.by import By
from selenium .webdriver.support.wait import WebDriverWait
from selenium import webdriver
import os, time, sys
import xlrd.sheet
from testcase.Conmon import log
reload(sys)
sys.setdefaultencoding('utf-8')
from config import globalparameter as gl


class Action(object):
    driver = None
#    base_url = None
#    pagetitle = None

#    def __init__(self, command_executor='http://127.0.0.1:4444/wd/hub',
#                 desired_capabilities=None,
#                 browser_profile=None,
#                 proxy=None,
#                 keep_alive=None
#                 ):
#        self.command_executor = command_executor
#        self.desired_capabilities = desired_capabilities
#        self.proxy = proxy
#        self.keep_alive = keep_alive
    def __init__(self, driver=None, url=None, pagetitle=None):
        self.driver = driver
        self.url = url
        self.pagetitle = pagetitle
        self.mylog = log.log()
    def startbrowser(self, browser = 'firefox '):
        print u'启动浏览器'
        try:
            if browser.lower() == 'firefox':
                self.driver = webdriver.Firefox()
            elif browser.lower() == 'ie':
                self.driver = webdriver.Ie()
            elif browser.lower() == 'chrome':
                self.driver = webdriver.Chrome()
            else:
                print u'启动浏览器失败'
        except AttributeError:
            self.mylog.error(u'未能正确打开驱动：'+browser)

    # 定义open方法
    def _open(self, url, pagetitle):
        print u'正在打开网址：'+url
        # 使用get打开访问链接地址
        try:
            self.driver.get(url)
            self.driver.maximize_window()
        # 使用assert进行校验，打开的链接地址是否与配置的地址一致。调用on_page()方法
            assert self.on_page(pagetitle), u"打开页面失败 %s" % url
        except AttributeError:
            self.mylog.error(u'未能正确打开页面:' + url)

    # 重写元素定位方法
    def find_element(self, *loc):
        # return self.driver.find_element(*loc)
        try:
            WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element(*loc).is_displayed())
            return self.driver.find_element(*loc)
        except AttributeError:
            self.mylog.error(u"%s找不到元素%s"% (self, loc))

    # 重写一组元素定位方法
    def find_elements(self, *loc):
        # return self.driver.find_element(*loc)
        try:
            if len(self.driver.find_elements(*loc)):
                return self.driver.find_elements(*loc)
        except AttributeError:
            self.mylog.error(u"%s找不到元素%s" % (self, loc))

    # 重写switch_frame方法
    def switch_frame(self, loc):
        try:
            return self.driver.switch_to_frame(loc)
        except AttributeError:
            self.mylog.error(u"%s找不到元素%s" % (self, loc))

    # 使用current_url获取当前窗口Url地址，进行与配置地址作比较，返回比较结果（True False）
    def on_page(self, pagetitle):
        return pagetitle in self.driver.title

    # 定义script方法，用于执行js脚本，范围执行结果
    def script(self, src):
        self.driver.execute_script(src)

    # 重写定义send_keys方法,这里的loc格式为（'id','元素名'）
    def send_keys(self, loc, value, clear_first=True, click_first=True):
        try:
            if click_first:
                self.find_element(*loc).click()
            if clear_first:
                self.find_element(*loc).clear()
            self.find_element(*loc).send_keys(value)
        except AttributeError:
            self.mylog.error(u"%s找不到元素%s" % (self, loc))

    # 读取excel文件的table
    @staticmethod
    def readtable(filepath, sheetno):
        """
        filepath:文件路径
        sheetno：Sheet编号
        """
        data = xlrd.open_workbook(filepath)
        # 通过索引顺序获取Excel表
        table = data.sheets()[sheetno]
        return table

    # 读取xls表格，使用生成器yield进行按行存储
    @staticmethod
    def readxls(filepath, sheetno):
        """
        filepath:文件路径
        sheetno：Sheet编号
        """
        table = Action.readtable(filepath, sheetno)
        for args in range(1, table.nrows):
            # 使用生成器 yield
            yield table.row_values(args)

    # 读取元素标签和元素唯一标识
    @staticmethod
    def locate(index, filepath, sheetno=0):
        """
        filepath: 文件路径
        sheetno：Sheet编号
        index: 元素编号
        返回值内容为：("id","inputid")、("xpath","/html/body/header/div[1]/nav")格式
        """
        table = Action.readtable(filepath, sheetno)
        #从第2行开始，获取每行第2、3个的值
        for i in range(1, table.nrows):
            if index in table.row_values(i):
                return table.row_values(i)[1:3]

    # savePngName:生成图片的名称
    def savePngName(self, name):
        """
        name：自定义图片的名称
        """
        day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        fp = gl.report_path + day + "\\image"
        tm = self.saveTime()
        type = ".png"
        if os.path.exists(fp):
            filename = str(fp) + "\\" + str(tm) + str("_") + str(name) + str(type)
            print u'截图已保存：'+filename
            return filename
        else:
            os.makedirs(fp)
            filename = str(fp) + "\\" + str(tm) + str("_") + str(name) + str(type)
            print u'截图已保存：'+filename
            return filename

    # 获取系统当前时间
    def saveTime(self):
        """
        返回当前系统时间以括号中（2014-08-29-15_21_55）展示
        """
        return time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))

    # saveScreenshot:通过图片名称，进行截图保存
    def saveScreenshot(self, driver, name):
        """
        快照截图
        name:图片名称
        """
        # 获取当前路径
        # print os.getcwd()
        image = driver.save_screenshot(self.savePngName(name))
        return image

    def get(self, url):
        print u'正在打开网址：'+url
        # 使用get打开访问链接地址
        try:
            self.driver.get(url)
            self.driver.maximize_window()

        except AttributeError:
            self.mylog.error(u'未能正确打开页面:' + url)

    #带参数的反射函数
    def action_sign(self, action_name, *args):
        try:
            act = getattr(self, action_name)
            func = act(*args)
            return func
        except AttributeError:
            print u'请检查函数名或者参数是否有误'

    #不带参数的反射函数
    def action(self, action_name):

        act = getattr(self, action_name)
        return act()




    #查找元素,tag为定位方法, loc为元素定位参数
    def sendtext(self, tag, loc,text):
        try:
            if tag.lower() == 'id':
                ele_loc = (By.ID, loc)
                self.find_element(*ele_loc).send_key(text)
            elif tag.lower() == 'class_name':
                ele_loc = (By.CLASS_NAME, loc)
                self.find_element(*ele_loc).send_key(text)
            elif tag.lower() == 'css_selector':
                ele_loc = (By.CSS_SELECTOR, loc)
                self.find_element(*ele_loc).send_key(text)
            elif tag.lower() == 'name':
                ele_loc = (By.NAME, loc)
                self.find_element(*ele_loc).send_key(text)
            elif tag.lower() == 'link_text':
                ele_loc = (By.LINK_TEXT, loc)
                self.find_element(*ele_loc).send_key(text)
            elif tag.lower() == 'xpath':
                ele_loc = (By.XPATH, loc)
                self.find_element(*ele_loc).send_key(text)
            elif tag.lower() == 'tag_name':
                ele_loc = (By.TAG_NAME, loc)
                self.find_element(*ele_loc).send_key(text)
            elif tag.lower() == 'partial_link_text':
                ele_loc = (By.PARTIAL_LINK_TEXT, loc)
                self.find_element(*ele_loc).send_key(text)
                print u'方法名%s输入不对' %tag
        except AttributeError:
            self.mylog.error(u"%s找不到元素%s" % (self, tag))

    def click(self, tag, loc):
        print u'通过'+tag+u'，点击'+loc
        try:
            self.find_element(tag, loc).click()
        except AttributeError:
            self.mylog.error(u"点击出错,找不到元素%s" % loc)

    def input(self, tag, loc, text):
        print u'输入：'+text
        try:
            ele = self.find_element(tag,loc)
            ele.clear()
            ele.send_keys(text)

        except AttributeError:
            self.mylog.error(u'输入'+text+u'出错')

    @staticmethod
    def waitting(time):
        try:
            return time.sleep(time)
        except AttributeError:
            log.log.error(u'waitting'+time+u'出错')







if __name__ =='__main__':
    a = Action()
    a.action_sign('startbrowser', 'ie')
    a.action_sign(u'get', u'https://www.baidu.com/')
  #  a.action_sign('click', 'xpath', './/*[@id=\'u1\']/a[1]')
    aaa = 'id', 'kw', 'selenium'
    a.action_sign('input', *aaa)
   # a.action_sign('input', 'id', 'kw', 'selenium')
    a.action_sign('click', 'id', 'su')

