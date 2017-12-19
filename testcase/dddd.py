# -*-coding:utf-8 -*-

from assertpy import assert_that
# from selenium import webdriver
# dr = webdriver.Firefox()
# dr.get('https://www.baidu.com/')
# value = dr.find_elements_by_id('su')
# print type(value)
# print value

# a = 1
# b = 2
# if assert_that(dr.title).contains(u'百度'):
#     print 'aaa'
# if assert_that('C:\\Python27').exists():
#     print 'sssss'

def judge(that,ways,value):

    if ways.lower() == 'contains':
        return assert_that(that).contains(value)
    if ways.lower() == 'equal':
        return assert_that(that).contains(value)
    if ways.lower() == 'startwith':
        return assert_that(that).starts_with(value)
# if judge(dr.title, 'contains', u'百度'):
#     print 'pass'
#
# if judge(dr.find_elements_by_id('su').get_attribute('value'),'contains',u'百度'):
#     print 'tests'

try:
    if assert_that('百度一下').contains('百度11'):
        print 'pass'
except:
    print 'fail'