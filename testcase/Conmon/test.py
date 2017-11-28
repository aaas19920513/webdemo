# -*- coding:utf-8 -*-

import xlrd
import  re
import pandas
from config import globalparameter as gl
filepath ='C:\\Users\\Administrator\\Desktop\\test.xls'
data = xlrd.open_workbook(filepath)
sheet =data.sheet_by_index(0)




def readtable(filepath, sheetno):
    """
    filepath:文件路径
    sheetno：Sheet编号
    """
    data = xlrd.open_workbook(filepath)
    # 通过索引顺序获取Excel表
    table = data.sheets()[sheetno]
    return table


# 读取xls表格，获取第colnum列数据
def get_keyword(colnum=1, sheetno=0,filepath='C:\\Users\\Administrator\\Desktop\\test.xls'):
    """
    filepath:文件路径
    sheetno：Sheet编号

    """
    L = []
    table = readtable(filepath, sheetno)
    rows = table.nrows
    for i in range(1, rows):

        value = table.cell(i, colnum)
        L.append(value)
    return L

    #从第2行开始，获取excle第3-6列数据
def get_param( sheetno=0,filepath='C:\\Users\\Administrator\\Desktop\\test.xls'):
    table = readtable(filepath, sheetno)
    rows = table.nrows
    L = []
    for i in range(1, rows):
        if i in table.row_values(i):
           value = table.row_values(i)[1:6]

           yield value


def ddd(ttt):

    for i in range(4):
        L = ttt[i]
        for y in range(4):
            List = L[y]
            print List

def not_empty(s):
    return s and s.strip()

a=get_param()
print a.next()

class T:
    @staticmethod
    def addd(a,b):
        sum = a+b
        return sum

print eval('T.addd(2,3)')




def gen_var_a(N):
    for i in range(N):
         yield get_param()

L = ['ss','aaa','dddd']
A = tuple(L)
print A
