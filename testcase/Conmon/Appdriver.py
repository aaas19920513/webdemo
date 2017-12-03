# -*-coding:utf-8 -*-
from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time, os
import log

class Appaction():
    driver = None
    desired_caps = {
        'platformName': 'Android',
        'deviceName': 'ceb44bd3',
        'platformVersion': '5.0.2',
        'appPackage': 'com.taobao.taobao',
        'appActivity': 'com.taobao.tao.welcome.Welcome',
        # 'app': "f:\\apk\\taobao.apk",
        'unicodeKeyboard': True,
        'resetKeyboard': True,
        'noReset': True,
        'fullReset': False
    }

    def __init__(self, appium_driver):
        self.driver = appium_driver
        self.applog = log.log()

    # 重写元素定位方法
    def find_element(self, *loc):
        # return self.driver.find_element(*loc)
        try:
            WebDriverWait(self.driver, 15).until(lambda driver: driver.find_element(*loc).is_displayed())
            return self.driver.find_element(*loc)
        except AttributeError:
            self.applog.error(u"%s找不到元素%s"% (self, loc))

     # 重新封装一组元素定位方法

    def find_elements(self, loc):
        try:
            if len(self.driver.find_elements(*loc)):
                return self.driver.find_elements(*loc)
        except:
            self.applog.error(u"%s 页面中未能找到 %s 元素" % (self, loc))

            # 重新封装输入方法

    # 重写定义send_keys方法,这里的loc格式为（'id','元素名'）
    def send_keys(self, loc, value, clear_first=True, click_first=True):
        try:
            if click_first:
                self.find_element(*loc).click()
            if clear_first:
                self.find_element(*loc).clear()
            self.find_element(*loc).send_keys(value)
        except AttributeError:
            self.applog.error(u"%s找不到元素%s" % (self, loc))

    # 重新封装按钮点击方法
    def clickbutton(self, tag, loc):
        print u'通过'+tag+u'，点击'+loc
        try:
            self.find_element(tag, loc).click()
        except AttributeError:
            self.applog.error(u"点击出错,找不到元素%s" % loc)

    def swipe(self, st, sy, ex, ey):
        """
        滑动
        分别为:起始点x,y。结束点x,y。与滑动速度。滑动默认800
        """
        return self.driver.swipe(st, sy, ex, ey, duration=900)

    def get_window_size(self):
        """
        获取屏幕分辨率
        :return: {u'width': 1080, u'height': 1920}
        """
        a = 0
        while a < 6:
            try:
                width = self.driver.get_window_size()['width']
                height = self.driver.get_window_size()['height']
                return width, height
            except Exception as e:
                a += 1
                self.applog.error(e)
                self.applog.error('appium failed to get resolution')

    def swipe_ratio(self, st, sy, ex, ey):
        """

        :param st: 起始点宽
        :param sy: 起始点高
        :param ex: 结束点宽
        :param ey: 结束点高
        :return: 滑动动作
        """
        width, height = self.get_window_size()
        return self.swipe(str(st * width), str(sy * height),
                          str(ex * width), str(ey * height))

    def swipe_left(self):
        """
        左滑屏幕
        """
        try:
            self.swipe_ratio(0.8, 0.5, 0.2, 0.5)
        except AttributeError:
            self.applog.error(u'左滑error')

    def swipe_right(self):
        """
        右滑屏幕
        """
        try:
            self.swipe_ratio(0.2, 0.5, 0.8, 0.5)
        except AttributeError:
            self.applog.error(u'右滑error')

    def swipe_up(self):
        """
        上滑屏幕
        """
        try:
            self.swipe_ratio(0.5, 0.8, 0.5, 0.2)
        except AttributeError:
            self.applog.error(u'上滑error')

    def swipe_down(self):
        """
        下滑屏幕
        """
        try:
            self.swipe_ratio(0.5, 0.2, 0.5, 0.8)
        except AttributeError:
            self.applog.error(u'下滑error')


    def save_screenshot(self, file_path):
        """

        :param file_path:
        :return: 获取android设备截图
        """
        try:
            return self.driver.save_screenshot(file_path)
        except AttributeError:
            self.applog.error(u'截图error')

    def start_activity(self, package, activity):
        """
        启动activity
        package:包名
        activity:.activity
        """
        return self.driver.start_activity(package, activity)

    def open_notifications(self):
        """
        打开系统通知栏
        """
        return self.driver.open_notifications()

    def is_app_installed(self, package):
        """
        检查是否安装
        package:包名
        """
        return self.driver.is_app_installed(package)

    def install_app(self, path):
        """
        安装应用
        path:安装路径
        """
        return self.driver.install_app(path)

    def remove_app(self, package):
        """
        删除应用
        package:包名
        """
        return self.driver.remove_app(package)

    def shake(self, ):
        """
        摇晃设备
        """
        return self.driver.shake()

    def close_app(self, ):
        """
        关闭当前应用
        """
        return self.driver.close_app()

    def reset_app(self, ):
        """
        重置当前应用
        """
        return self.driver.reset()

    def current_activity(self, ):
        """
        当前应用的activity
        """
        return self.driver.current_activity

    def send_key_event(self, arg):
        """
        操作实体按键
        :return:
        """
        event_list = {'entity_home':3,'entity_back':4,'entity_menu':82,'entity_volume_up':24,'entity_volume_down':25}
        if arg in event_list:
            self.driver.keyevent(int(event_list[arg]))


if __name__ == '__main__':
    pass


