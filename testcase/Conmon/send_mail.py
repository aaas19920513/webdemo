# coding:utf-8

import os, smtplib, os.path , time
from config import globalparameter as gl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import log

'''
邮件发送最新的测试报告
'''
day = time.strftime('%Y-%m-%d', time.localtime(time.time()))

class send_email(object):
    def __init__(self):
        self.mylog = log.log()

    # 定义邮件内容
    def email_init(self, report, reportName):

        with open(report, 'rb')as f:
            mail_body = f.read()
#        mail_body = Run_all_tests.mail_body()

        # 创建一个带附件的邮件实例
        msg = MIMEMultipart()
        # 以测试报告作为邮件正文
        msg.attach(MIMEText(mail_body, 'html', 'utf-8'))
        report_file = MIMEText(mail_body, 'html', 'utf-8')
        # 定义附件名称（附件的名称可以随便定义，你写的是什么邮件里面显示的就是什么）
        report_file["Content-Disposition"] = 'attachment;filename='+reportName
        msg.attach(report_file) # 添加附件
        msg['Subject'] = '自动化测试报告:'+reportName # 邮件标题
        msg['From'] = gl.email_name  #发件人
        msg['To'] = gl.email_To  #收件人列表
        try:
            server = smtplib.SMTP(gl.smtp_sever)
            server.login(gl.email_name, gl.email_password)
            server.sendmail(msg['From'], msg['To'].split(';'), msg.as_string())
            server.quit()
        except smtplib.SMTPException:
            self.mylog.error(u'邮件发送测试报告失败 at'+__file__)

    def sendnewReport(self):
        #获取report文件夹下的文件夹列表RepList（以时间命名的列表）

        RepList = os.listdir(gl.report_path)

        #获取report下最新报告文件夹NewRepList_son（最接近当前时间的文件夹，其实就是某天生成的报告文件夹）
        NewRepList = RepList[-2]
        NewRepList_son = os.listdir(gl.report_path+'\\'+NewRepList)
        #将最近那天生成的报告排序
        NewRepList_son.sort()
        #得到最新的报告名称
        new_report = NewRepList_son[-2]

        #获取最近生成报告的绝对路径
        new_report_path = gl.report_path+NewRepList+'\\'+new_report
        print new_report_path
        #发送邮件
        self.email_init(new_report_path, new_report)


    def sendReport(self):
        # 找到最新的测试报告
        report_list = os.listdir(gl.report_path)
        report_list.sort(key=lambda fn: os.path.getmtime(gl.report_path+fn) if not os.path.isdir(gl.report_path+fn) else 0)
        #获取最新report的文件夹名称
        new_report_list = os.path.join(gl.report_path, report_list[-1])
        #将最新report的文件夹排序
        new_report_list = new_report_list.split()
        print new_report_list

        #得到最新的report
        new_report = new_report_list[-1]
        # 发送邮件
        self.email_init(new_report, report_list[-1])
a=send_email()
a.sendnewReport()