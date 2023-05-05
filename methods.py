from flask import render_template, request, url_for, redirect, flash
import smtplib
from email.mime.text import MIMEText
import random
#设置服务器所需信息
#163邮箱服务器地址
mail_host = 'smtp.163.com'  
#163用户名
mail_user = 'm13552897186'  
#密码(部分邮箱为授权码) 
mail_pass = 'FDNWTMEQHMSZBKQM'
#邮件发送方邮箱地址
sender = 'm13552897186@163.com'

#设置email信息
#邮件内容设置
message = MIMEText('content','plain','utf-8')
#邮件主题       
message['Subject'] = 'email validation' 
#发送方信息
message['From'] = sender 

def send_email(to_email, code):
    #设置email信息
    #邮件内容设置
    message = MIMEText("your validation code is " + code, 'plain', 'utf-8')
    #邮件主题       
    message['Subject'] = 'email validation' 
    #发送方信息
    message['From'] = sender 
    #接受方信息     
    message['To'] = to_email
    #邮件接受方邮箱地址，注意需要[]包裹，这意味着你可以写多个邮件地址群发
    receivers = [to_email]  
    #登录并发送邮件
    try:
        smtpObj = smtplib.SMTP() 
        #连接到服务器
        smtpObj.connect(mail_host,25)
        #登录到服务器
        smtpObj.login(mail_user,mail_pass) 
        #发送
        smtpObj.sendmail(
            sender,receivers,message.as_string()) 
        #退出
        smtpObj.quit() 
    except smtplib.SMTPException as e:
        print('error', e) #打印错误
        
def generate_code():
    code = random.randint(0, 999999)
    code = "%06d"%code
    return code

def get_ipaddr():
    if request.access_route:
        return request.access_route[0]
    else:
        return request.remote_addr or '127.0.0.1'