import smtplib
from email.mime.text import MIMEText
import os

class SendMail():
    def __init__(self):
        self._user = os.getenv('FROMUSER')
        self._pwd = os.getenv('SMTPPWD')
        self.port = 465
        self.subject = 'Verification Mail'
    def sendm(self,to,content):
        msg = MIMEText(content)
        msg['Subject'] = self.subject
        msg['From'] = self._user
        msg['To'] = to
        try:
            s = smtplib.SMTP_SSL('smtp.qq.com',self.port)
            s.login(self._user,self._pwd)
            s.sendmail(self._user,to,msg.as_string())
            s.quit()
        except smtplib.SMTPException,e:
            print "Failed,%s"%e
if __name__=='__main__':
    sm=SendMail()
    sm.sendm(os.getenv('TOUSER'),'url you must click')


