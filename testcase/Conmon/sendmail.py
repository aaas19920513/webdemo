# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import random, time, os
from config import globalparameter as gl
string = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'


"""

带不同类型附件和内容发送邮件！

"""

mailto_list = ['345203857@qq.com', '873969472@qq.com']
mail_host = "smtp.163.com"  #设置服务器
mail_user = "18566774520"    #用户名
mail_pass = "liaoguanghua202"   #口令
mail_postfix = "163.com"  #发件箱的后缀
day = time.strftime('%Y-%m-%d', time.localtime(time.time()))

def send_mail(to_list, sub):
    me = "tuihou"+"<"+mail_user+"@"+mail_postfix+">"
    #如名字所示Multipart就是分多个部分
    msg = MIMEMultipart()
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    report_path = gl.report_path+'\\'+day
    report_lsit = os.listdir(report_path)
    report_name = report_path+'\\'+report_lsit[-2]
    #---这是文字部分---
    part = MIMEText(u"这是自动化测试报告，请知悉！", _subtype='plain', _charset='utf-8')
    msg.attach(part)

    #---这是附件部分---
    #xlsx类型附件
#    part = MIMEApplication(open('foo.xlsx','rb').read())
#    part.add_header('Content-Disposition', 'attachment', filename="foo.xlsx")
#    msg.attach(part)

    #txt类型附件
#    part = MIMEApplication(open('foo.txt','rb').read())
#    part.add_header('Content-Disposition', 'attachment', filename="foo.txt")
#    msg.attach(part)

    #pdf类型附件
#    part = MIMEApplication(open('foo.pdf','rb').read())
#    part.add_header('Content-Disposition', 'attachment', filename="foo.pdf")
#    msg.attach(part)

    #doc类型附件
#    part = MIMEApplication(open('foo.doc','rb').read())
#    part.add_header('Content-Disposition', 'attachment', filename="foo.doc")
#    msg.attach(part)

    #html类型附件
    part = MIMEApplication(open(report_name, 'rb').read())
    part.add_header('Content-Disposition', 'attachment', filename=report_name)
    msg.attach(part)


    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False
def send_report():
    send_mail(mailto_list, u'selenium自动化测试报告')

if __name__ == '__main__':
    for i in xrange(1):
        time.sleep(1)
        if send_mail(mailto_list, u"selenium自动化测试报告" + str(random.random())):
            print u"发送成功，邮件ID:" + str(i)
        else:
            print u"发送失败，邮件ID:" + str(i)



