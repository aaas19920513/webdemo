from selenium import webdriver
dr = webdriver.Ie()
dr.get('www.baidu.com')
print dr.title