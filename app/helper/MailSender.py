__author__ = 'tang'
import smtplib
from email.mime.text import MIMEText


class MailSender:
    def __init__(self, host="smtp.mail.yahoo.com",
                 port=465,
                 username="alston_tang@yahoo.com",
                 password="for I:=1 to 100 do"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.s = smtplib.SMTP_SSL()

    def confirm_password(self, email_addr, data):
        self.s.connect(self.host, self.port)
        self.s.login(self.username, self.password)
        self.s.sendmail(self.username, email_addr, data)
        self.s.quit()
