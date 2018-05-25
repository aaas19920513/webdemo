import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from selenium import webdriver
dr = webdriver.Ie()
dr.get('www.baidu.com')
print dr.title