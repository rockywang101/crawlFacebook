"""
send mail demo

"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib
from email.mime.image import MIMEImage


def sendMail(html):
    
    print('sendmail')
    
    host = "smtp.gmail.com"
    port = 587
    username = "rockywang101@gmail.com"
    password = os.environ["MY_PASSWORD"] # 在環境變數設定密碼，或是直接把這行改成明碼
    fromEmail = username
    toList = ["rockywang101@gmail.com"]
    
    print("go")
    smtp = smtplib.SMTP(host, port)
    print(smtp)
    smtp.ehlo()
    smtp.starttls()
    smtp.login(username, password)
    
    msg = MIMEMultipart()  
    msg["Subject"] = "寄信測試 from Python"  
    msg["From"] = username
    msg["To"] = ",".join(toList)
    
    # html = "<h2>Hello Python</h2>"
    # msg.attach(MIMEText(html, 'html'))
    # smtp.send_message(msg)
    # smtp.quit()

    print('send...')
    
    msg.attach(MIMEText(html, 'html'))
    smtp.send_message(msg)
    smtp.quit()

    print('end...')
    
if __name__ == "__main__":
    sendMail("<h2>Hello</h2>")