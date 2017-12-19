# -*- coding:utf-8 -*-
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium .webdriver.support.wait import WebDriverWait
from selenium import webdriver
import os, time, sys
import xlrd.sheet
from testcase.Conmon import log
from selenium.webdriver.common.action_chains import ActionChains
from assertpy import assert_that
reload(sys)
sys.setdefaultencoding('utf-8')
from config import globalparameter as gl


class Action(object):

    driver = None

    def __init__(self, command_executor='http://127.0.0.1:4444/wd/hub',
                 desired_capabilities=None,
                 browser_profile=None,
                 proxy=None,
                 keep_alive=None
                 ):
        self.command_executor = command_executor
        self.desired_capabilities = desired_capabilities
        self.proxy = proxy
        self.keep_alive = keep_alive
        self.keyword_log = log.log()

    # 定义启动浏览器关键字
    def startbrowser(self, browser='firefox '):
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
            self.keyword_log.error(u'未能正确打开驱动：'+browser)

    # 定义打开网址关键字
    def get(self, url):
        try:
            self.driver.get(url)
            self.driver.maximize_window()
        except AttributeError:
            self.keyword_log.error(u'未能正确打开页面:' + url)

    # 检查打开网址title
    def on_page(self, pagetitle):
        return pagetitle in self.driver.title


    # 重写元素定位方法
    def find_element(self, *loc):
        # return self.driver.find_element(*loc)
        try:
            WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element(*loc).is_displayed())
            return self.driver.find_element(*loc)
        except AttributeError:
            self.keyword_log.error(u"%s找不到元素%s" % (self, loc))

    # 重写一组元素定位方法
    def find_elements(self, *loc):
        # return self.driver.find_element(*loc)
        try:
            if len(self.driver.find_elements(*loc)):
                return self.driver.find_elements(*loc)
        except AttributeError:
            self.keyword_log.error(u"%s找不到元素%s" % (self, loc))

    # 重写switch_frame方法
    def switch_frame(self, loc):
        try:
            return self.driver.switch_to_frame(loc)
        except AttributeError:
            self.keyword_log.error(u"%s找不到元素%s" % (self, loc))

    # 重写定义send_keys方法,这里的loc格式为（'id','元素名'）
    def send_keys(self, loc, value, clear_first=True, click_first=True):
        try:
            if click_first:
                self.find_element(*loc).click()
            if clear_first:
                self.find_element(*loc).clear()
            self.find_element(*loc).send_keys(value)
        except AttributeError:
            self.keyword_log.error(u"%s找不到元素%s" % (self, loc))

    # 定义script方法，用于执行js脚本，范围执行结果
    def script(self, src):
        self.driver.execute_script(src)

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

    # PngName:生成图片的名称
    def PngName(self, name, Bool):
        """
        name：自定义图片的名称
        """
        day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        fp = gl.report_path + day + "\\image" +'\\'+ Bool
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
    def Screenshot(self, name, Bool):
        """
        快照截图
        name:图片名称
        """
        # 获取当前路径
        # print os.getcwd()
        image = self.driver.save_screenshot(self.PngName(name, Bool))
        return image

    # 带参数的反射函数
    def action_sign(self, action_name, *args):
        try:
            act = getattr(self, action_name)
            func = act(*args)
            return func
        except AttributeError:
            print u'请检查函数名或者参数是否有误'

    # 不带参数的反射函数
    def action(self, action_name):
        act = getattr(self, action_name)
        return act()

    # 查找元素,tag为定位方法, loc为元素定位参数
    def sendtext(self, tag, loc, text):
        try:
            if tag.lower() == 'id':
                ele_loc = (By.ID, loc)
                self.find_element(*ele_loc).send_keys(text)
            elif tag.lower() == 'class_name':
                ele_loc = (By.CLASS_NAME, loc)
                self.find_element(*ele_loc).send_keys(text)
            elif tag.lower() == 'css_selector':
                ele_loc = (By.CSS_SELECTOR, loc)
                self.find_element(*ele_loc).send_keys(text)
            elif tag.lower() == 'name':
                ele_loc = (By.NAME, loc)
                self.find_element(*ele_loc).send_keys(text)
            elif tag.lower() == 'link_text':
                ele_loc = (By.LINK_TEXT, loc)
                self.find_element(*ele_loc).send_keys(text)
            elif tag.lower() == 'xpath':
                ele_loc = (By.XPATH, loc)
                self.find_element(*ele_loc).send_keys(text)
            elif tag.lower() == 'tag_name':
                ele_loc = (By.TAG_NAME, loc)
                self.find_element(*ele_loc).send_keys(text)
            elif tag.lower() == 'partial_link_text':
                ele_loc = (By.PARTIAL_LINK_TEXT, loc)
                self.find_element(*ele_loc).send_keys(text)
                print u'方法名%s输入不对' %tag
        except AttributeError:
            self.keyword_log.error(u"%s找不到元素%s" % (self, loc))

    # 定义click关键字
    def click(self, tag, loc):
        try:
            self.find_element(tag, loc).click()
        except AttributeError:
            self.keyword_log.error(u"点击出错,找不到元素%s" % loc)

    # 定义点击一组元素的关键字 clickmore
    def clickmore(self, tag, loc):
        try:
            self.find_elements(tag, loc)
        except AttributeError:
            self.keyword_log.error(u"%s点击出错，找不到元素%s" % (self, loc))

    # 定义input关键字
    def input(self, tag, loc, text):
        try:
            ele = self.find_element(tag, loc)
            ele.click()
            ele.clear()
            ele.send_keys(text)
        except AttributeError:
            self.keyword_log.error(u"%s输入出错%s" % (self, text))

    # 定义waittingi关键字
    @staticmethod
    def waitting(time):
        try:
            return time.sleep(float(time))
        except AttributeError:
            print 'waitting error'
            log.log().error(u"延时出错%s" %time)

    #退出浏览器
    def quit(self):
        try:
            self.driver.quit()
        except AttributeError:
            self.keyword_log.error(u"%s退出浏览器失败%s" % self)

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

    @staticmethod
    def not_empty(s):
        return s and s.strip()

    # 定义获取元素文本属性的关键字
    def gettext(self, tag, loc):
        try:
            text = self.find_element(tag, loc).text()
            print text
        except AttributeError:
            self.keyword_log.error(u"获取text信息失败")

    # 定义获取输入框尺寸的关键字
    def getsize(self, tag, loc):
        try:
            size = self.find_element(tag, loc).size()
            print size
        except AttributeError:
            self.keyword_log.error(u'获取输入框尺寸失败')

    # 定义获取元素属性值的关键字，其中attribute代表获取的属性类型（id,name...）
    def getattribute(self, tag, loc, attribute):
        try:
            attri = self.find_element(tag, loc).get_attribute(attribute)
            print attri
        except AttributeError:
            self.keyword_log.error(u'获取元素属性失败')

    # 定义鼠标操作,鼠标拖动操作需要四个参数
    def mouse_operate(self, tag, loc, operate, tagert =None):
        try:
            element = self.find_element(tag, loc)
            if operate == 'right':
                ActionChains(self.driver).context_click(element).perform()
            elif operate == 'double':
                ActionChains(self.driver).double_click(element).perform()
            elif operate == 'move':
                ActionChains(self.driver).move_to_element(element).perform()
            elif operate == 'drop':
                ActionChains(self.driver).drag_and_drop(element, tagert).perform()
            else:
                print u'您输入的参数有误，第三个参数应为right,double,move,drop之一'
        except AttributeError:
            self.keyword_log.error(u'鼠标操作参数输入有误')

    # 定义隐式等待关键字
    def implicitlywait(self, time):
        try:
            self.driver.implicitly_wait(time)
        except AttributeError:
            self.keyword_log.error(u'隐式等待出错')

    # 定义页面加载超时关键字
    def pageloadtimeout(self, time):
        try:
            self.driver.set_page_load_timeout(float(time))
        except AttributeError:
            self.keyword_log.error(u'超时设置出错')

     # 定义切换Alert关键字
    def switchtoalert(self):
        try:
            self.driver.switch_to_alert()
        except AttributeError:
            self.keyword_log.error(u'切换Alrt出错')

    # 定义确认Alert关键字
    def confirmalert(self):
        try:
            self.driver.switch_to_alert().accept()
        except AttributeError:
            self.keyword_log.error(u'Alert确认出错')
    # 取消Alert
    def cancelalert(self):
        try:
            self.driver.switch_to_alert().dismiss()
        except AttributeError:
            self.keyword_log.error(u'Alert取消出错')

    # 定义按键盘关键字
    def keypress(self, tag, loc, key):
        try:
            ele = self.find_element(tag, loc)
            ele.clear()
            ele.send_keys(key)
        except AttributeError:
            self.keyword_log.error(u"%s按键出错%s" % (self,key))

    # 定义切换frame关键字
    def switchtoframe(self, frame):
        try:
            self.driver.switch_to_frame(frame)
        except AttributeError:
            self.keyword_log.error(u'切换frame：%s出错' % frame)

    # 切换到默认frame
    def switchtodefaultframe(self):
        try:
            self.driver.switch_to_default_content()
        except AttributeError:
            self.keyword_log.error(u'切换默认frame出错')

    # 清理cookie
    def clearcookie(self, name):
        try:
            self.driver.delete_cookie(name)
        except AttributeError:
            self.keyword_log.error(u'清理cookie出错')

    # 关闭当前窗口
    def close(self):
        try:
            self.driver.close()
        except AttributeError:
            self.keyword_log.error(u'关闭窗口出错')

    def judge(self, that, ways, value, name):
        """
        断言并截图
        :param that: 断言对象
        :param ways: 断言方法，例如相等，包含，以xx字符开头
        :param value: 断言文本
        :param name: 截图的名字
        :return:     返回断言布尔值
        """
        try:
            if ways.lower() == 'contains':
                try:
                    if assert_that(that).contains(value):
                        self.Screenshot(name, 'Pass')
                        print '='*10+u'testcase pass'+'='*10
                except:
                    self.Screenshot(name, 'Fail')
                    print '='*10+u'testcase fail'+'='*10
 #               return assert_that(that).contains(value)
            if ways.lower() == 'equal':
                try:
                    if assert_that(that).contains(value):
                        self.Screenshot(name, 'Pass')
                        print '='*10+u'testcase pass'+'='*10
                except:
                    self.Screenshot(name, 'Fail')
                    print '='*10+u'testcase fail'+'='*10

            if ways.lower() == 'startwith':
                try:
                    if assert_that(that).contains(value):
                        self.Screenshot(name, 'Pass')
                        print '='*10+u'testcase pass'+'='*10
                except:
                    self.Screenshot(name, 'Fail')
                    print '='*10+u'testcase fail'+'='*10

        except AttributeError:
            self.keyword_log.error(u'断言出错:%s' % value)

if __name__ == '__main__':
    A = Action()
#    sheetno = 0
#    filepath = 'C:\\Users\\Administrator\\Desktop\\test.xls'
 #   table = Action.readtable(filepath, sheetno)
#    rows = table.nrows


#    def build_para():

#        for i in range(1, rows):
#            value = table.row_values(i)[1:6]
            # 关键字
#           key_word, tag, loc, para, judge = value[0], value[1], value[2], value[3], value[4]
#            print key_word, tag, loc, para, judge
 #           print type(key_word), type(tag), type(loc),type(para),type(judge)

#    build_para()
    A.action_sign('startbrowser','ie')
    A.action_sign('get','https://www.baidu.com/')
    A.action_sign('input','id','kw','23333')
    A.action_sign('judge',A.driver.title,'contains','测试')
