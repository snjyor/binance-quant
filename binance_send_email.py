from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header

def send_email(email_title='',email_content=''):
    pwd = '*********'	#your pwd

    qq = '*********'	#your qq number
    sender = '**********@qq.com'	#your qq email address
    receiver = '******@163.com'		#your receive email address
    host = 'smtp.qq.com'

    smtp = SMTP_SSL(host)
    smtp.ehlo(host)
    smtp.login(qq, pwd)

    msg = MIMEText(email_content, 'plain', 'utf-8')
    msg['subject'] = Header(email_title, 'utf-8')
    msg['from'] = 'trading_report'	#The name who send email, you can change this char
    msg['to'] = 'nobody'	#The name of yourself email name, you can change this char

    smtp.send_message(msg, sender, receiver)
    print('成功发送邮件！')
    smtp.quit()
