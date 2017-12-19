# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import unittest
#from NewHtml import HTMLTestRunner
import time
import os.path
from config import globalparameter as gl
from  testcase.Conmon import send_mail
from testcase.Conmon import HTMLTestRunner



casepath = "."
#result = "D:\\test_d\\MySelenium\\report\\"
result = gl.report_path

def Creatsuite():

	#定义单元测试容器
	testunit = unittest.TestSuite()

	#定搜索用例文件的方法
	discover = unittest.defaultTestLoader.discover(casepath, pattern='case*.py', top_level_dir=None)

	#将测试用例加入测试容器中
	for test_suite in discover:
		for casename in test_suite:
			testunit.addTest(casename)
		print testunit
	return testunit


test_case = Creatsuite()

#获取系统当前时间
now = time.strftime('%Y-%m-%d-%H_%M_%S', time.localtime(time.time()))
day = time.strftime('%Y-%m-%d', time.localtime(time.time()))

#定义个报告存放路径，支持相对路径
tdresult = result + day
if os.path.exists(tdresult):
	filename = tdresult + "\\" + now + "_result.html"
	fp = file(filename, 'wb+')
	#定义测试报告
	runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'自动化测试报告', description=u'用例执行情况：')
	#运行测试用例
	runner.run(test_case)
	fp.close()  #关闭报告文件
	time.sleep(10)
	send_mail=send_mail.send_email()
	send_mail.sendnewReport()


else:
	os.mkdir(tdresult)
	filename = tdresult + "\\" + now + "_result.html"
	fp = file(filename, 'wb')
	#定义测试报告
	runner = HTMLTestRunner.HTMLTestRunner(stream=fp, title=u'自动化测试报告', description=u'用例执行情况：')

	#运行测试用例
	runner.run(test_case)
	fp.close()  #关闭报告文件




