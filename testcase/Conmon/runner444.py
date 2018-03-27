# -*- coding:utf-8 -*-
__author__ = 'tuihou'

from keyword_driver import Action
from config import globalparameter as gl
import locate
import unittest

filepath = gl.test_data_path

class Runstep(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
    # cls.driver = webdriver.Firefox()
	# cls.driver.implicitly_wait(30)
        print "start"


    def buildStep(self, keyword, tag=None, loc=None, param=None, wish=None):
        key = keyword.lower()
        params = [tag, loc, param, wish]
        # 构建调用参数
        param_text = ""
        for index in range(0, len(params)):
            if params[index] == None or params[index] == "":
                continue
            param_text += '"' + params[index] + '",'
        param_text = param_text[0:-1]
        if len(param_text) != 0:
            step = 'A.action_sign' + "(" + "\'" + key + '\',' + param_text + ")"
        # elif key == 'gettext':
        #     step = 'A.action_sign' + "(\'" + key + '\',' + tag + ',\'' + loc + '\',\'' + param + '\',\'' + wish + "\')"
        else:
            step = 'A.action' + "(" + "\'" + key + '\'' + ")"
        return step

    def action(self, *data):
        # casestep
        steps = Action.readxls(filepath, 1)
        A = Action()
        k = 4
        for step in steps:
            if step[0] == data[0]:
                desc = step[2]
                key_word, sign, param, wish = step[3], step[4], step[5], step[7]
                if sign != "":
                    ele = locate.locate(sign, filepath, 3)
                    tag, loc = ele[0], ele[1]
                    if key_word.lower() == 'input':
                        param = data[4]
                        step = self.buildStep(key_word, tag, loc, param)
                        print desc + ':' + step
                        k += 1
                        eval(step)
                    elif key_word.lower() == 'gettext':
                        step = self.buildStep(key_word, tag, loc)
                        text = eval(step)
                        if text == wish:
                            A.action_sign('Screenshot', data[0], 'PASS')
                        else:
                            A.action_sign('Screenshot', data[0], 'FAIL')

                    else:
                        step = self.buildStep(key_word, tag, loc, param)
                        print desc + ':' + step
                        eval(step)
                else:
                    step = self.buildStep(key_word, param)
                    print desc + ':' + step
                    eval(step)
    @staticmethod
    def getTestFunc(*txt):
        def func(self):
            self.action(*txt)
        return func

    @classmethod
    def tearDownClass(cls):
        print "End"
        # cls.driver.quit()

def __generateTestCases():
    cases = Action.readxls(filepath, 0)
    for case in cases:
        if case[2] == "Y":
            print "【Run】" + case[1] + "："
            print " + -" * 8
            datas = Action.readxls(filepath, 2)
            for data in datas:
                if (data[3] == "Y") & (data[0] == case[0]):
                    print data
                    setattr(Runstep, 'test_%s_%s' % (data[0], data[1]), Runstep.getTestFunc(*data))
__generateTestCases()

if __name__ == "__main__":
    unittest.main()
