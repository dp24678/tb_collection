# _*_coding:utf-8 _*_
#@Time    :2019/6/21 14:48
#@Author  :Dapan
#@Email : 248312738@qq.com

#邮件服务封装
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from tb_collection.settings import MAIL_CONFIG



class EmailHandler(object):

    def __init__(self,sender_email,sender_password, type = 0):
        """
        :param sender_email:str 发送人邮箱地址（用户名）
        :param sender_password:str 发送人在QQ或163申请的授权码
        :param type:int 1 为QQ邮箱 0 为163邮箱
        """
        self.__QQ = {'smtp':'smtp.qq.com','port':465}
        self.__163 = {'smtp':'smtp.163.com','port':25}
        self.sender_email = sender_email
        self.sender_password = sender_password

        if type == 0:
           self.server=smtplib.SMTP(self.__163['smtp'],self.__163['port'])
           self.server.login (self.sender_email,self.sender_password)
        elif type == 1:
           self.server=smtplib.SMTP(self.__QQ['smtp'],self.__QQ['port'])
           self.server.login (self.sender_email,self.sender_password)


    def send_mail(self,To,subject,content):
        """
        :param To:str 接收人邮箱地址
        :param subject:str 邮件标题
        :param content:str 邮件内容
        :return:bool True 成功 False 失败
        """
        try:
            msg = MIMEText(content,'plain','utf-8')
            msg['From'] = formataddr(['淘宝爬虫异常报警系统',self.sender_email])
            msg['To'] = formataddr(['',To])
            msg['Subject'] = subject

            self.server.sendmail(self.sender_email,To,msg.as_string())
            print("【%s】邮件发送成功"%subject)
            return True
        except Exception as e:
            print("【%s】邮件发送失败,请检查信息：%s"%(subject,e))
            return False


emailer = EmailHandler(MAIL_CONFIG['sender_email'], MAIL_CONFIG['sender_password'])



if __name__ == '__main__':
    # emailer = EmailHandler(MAIL_CONFIG['sender_email'], MAIL_CONFIG['sender_password'])
    emailer.send_mail(MAIL_CONFIG['receive_email'],MAIL_CONFIG['mail_title'], "恭喜你被阿里巴巴录取了,hh")

#
# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header
#
# qqAccout='245545357@qq.com'   #邮箱账号,换成自己的!!
# qqCode='*****'   #授权码   换成自己的!!
# smtp_server='smtp.qq.com'
# smtp_port=465
#
#
# #配置服务器
# stmp=smtplib.SMTP_SSL(smtp_server,smtp_port)
# stmp.login(qqAccout,qqCode)
#
# #组装发送内容
# message = MIMEText('我是发送的内容', 'plain', 'utf-8')   #发送的内容
# message['From'] = Header("Python邮件预警系统", 'utf-8')   #发件人
# message['To'] = Header("管理员", 'utf-8')   #收件人
# subject = 'Python SMTP 邮件测试'
# message['Subject'] = Header(subject, 'utf-8')  #邮件标题
#
# try:
#     stmp.sendmail(qqAccout, qqAccout, message.as_string())
# except Exception as e:
#     print '邮件发送失败--' + str(e)
# print '邮件发送成功'