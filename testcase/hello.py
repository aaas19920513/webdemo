#-*- coding:utf-8 -*-



class MyClass(object):
    val1 = 'Value 1'
    def __init__(self,val2):
        self.val2 = val2

    @staticmethod
    def staticmd():
        print '静态方法，无法访问val1和val2'

    @classmethod
    def classmd(cls):
        print '类方法，类：' + str(cls) + '，val1：' + cls.val1 + '，无法访问val2的值'

    def md(self):
        print 'teset'


def test():
    print 'test'
test()
def hello(self):
    pass
