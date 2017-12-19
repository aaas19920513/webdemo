# -*-coding:utf-8 -*-

from keyword_driver import Action
from config import globalparameter as gl

# 构建测试步骤
def buildStep( keyword, tag=None, loc=None, param=None, wish=None):

    key = keyword.lower()
    params = [tag, loc, param, wish]
    # 构建调用关键字方法的参数
    param_text = ""
    for index in range(0, len(params)):
        if params[index] == None or params[index] == "":
            continue
  #      if type(params[index]) == float:
        param_text += "'" + params[index] + "',"
    param_text = param_text[0:-1]

    if len(param_text) != 0 and key != 'judge':
        step = 'A.action_sign'+"(" + "\'" + key+'\',' + param_text + ")"
    elif key == 'judge':
        step = 'A.action_sign'+"(\'" + key + '\',' + tag + ',\'' + loc + '\',\'' + param + '\',\''+wish + "\')"
    else:
        step = 'A.action'+"(" + "\'" + key+'\''+")"
    return step

# 运行buildStep，filepath为测试用例文件，sheetno测试用例表名
def runStep(filepath =gl.project_path + '\\Data\\test1.xlsx',sheetno = 0):

    table = Action.readtable(filepath, sheetno)
    rows = table.nrows
    A = Action()
    for i in range(1, rows):
        value = table.row_values(i)[2:7]
        desc = table.row_values(i)[1]
        key_word, tag, loc, para, judge = value[0], value[1], value[2], value[3], value[4]
        step = buildStep(key_word, tag, loc, para, judge)
        print desc+':' + step
#        print type(key_word), type(tag), type(loc), type(para), type(judge)
        eval(step)

if __name__ == "__main__":
    runStep()