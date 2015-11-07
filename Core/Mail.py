#!/usr/bin/env python
#-*- coding=utf8 -*-
__author__ = 'saintic'
__date__ = '2015-10-12'
__version__ = 'sdp1.1'
__doc__ = '''
If you don't have a mail server, try local mail service, this requires that your local mail service is turned on.
The following is a part of the change.

Modify this line:
smtp_server='127.0.0.1'

Comment on this line:
#password='xxxx'
#server.login(from_addr, password)

If you need't html, please modify:
msg = MIMEText(content, 'html', 'utf-8')
change to(for plain):
msg = MIMEText(content, 'utf-8')
'''

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr,formataddr
import smtplib,sys
from os.path import isfile

class SendMail():
  __init__(self, *args):
    self.from_addr = 'sdp@saintic.net'
    self.smtp_server = 'smtp.saintic.net'
    self.password = 'SaintAugur910323'
    self.mailinfo = args
    self.user = args[0]
    self.to_addr = args[1]
    self.content = args[2]
    self.msg = MIMEText(content, 'utf-8')

  def _format_addr(self, s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

  def send(self):
    self.msg['From'] = self._format_addr('SdpCloud <%s>' % self.from_addr)
    self.msg['To'] = self._format_addr('%s <%s>' % (self.user, self.to_addr))
    self.msg['Subject'] = Header('SdpCloud 用户信息', 'utf-8').encode()
    server=smtplib.SMTP(self.smtp_server, 25)
    #server.set_debuglevel(1)
    server.login(self.from_addr, self.password)
    server.sendmail(self.from_addr, [self.to_addr], self.msg.as_string())
    server.quit()
