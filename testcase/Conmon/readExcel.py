# -*- coding:utf-8 -*-


import xlrd
from config import globalparameter as gl

class ReadExcel():


    def __init__(self, excelPath, sheetName):
        self.data = xlrd.open_workbook(excelPath)
        self.table = self.data.sheet_by_name(sheetName)
        # 获取第一行作为key值
        self.keys = self.table.row_values(0)
        print self.keys
        # 获取总行数
        self.rowNum = self.table.nrows
        print self.rowNum
        # 获取总列数
        self.colNum = self.table.ncols
        print self.colNum

    def dict_data(self):
        if self.rowNum <= 1:
            print("总行数小于1")
        else:
            r = []
            j = 1
            for i in range(self.rowNum-1):
                s = {}
                # 从第二行取对应values值
                values = self.table.row_values(j)
                for x in range(self.colNum):
                    s[self.keys[x]] = values[x]
                r.append(s)
                j += 1
            return r

if __name__ == "__main__":
    filepath = gl.project_path + '\\data\\case_data.xls'
    sheetName = "Sheet1"
    data = ReadExcel(filepath, sheetName)
    dict = data.dict_data()
    for i in range(6):
          print dict[i]