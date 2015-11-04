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

def _format_addr(s):
  name, addr = parseaddr(s)
  return formataddr((Header(name, 'utf-8').encode(), addr))

if len(sys.argv) == 4:
  user=sys.argv[1]
  to_addr=sys.argv[2]
  content_file=sys.argv[3]
  if not isfile(content_file):
    print "The third parameter need a file."
    sys.exit(1)
else:
  print "Into the reference error, three parameters are required."
  print "Usage:user user_email user_info_html_file"
  sys.exit(1)

with open(content_file) as f: content=f.read()
from_addr='sdp@saintic.net'
smtp_server='smtp.saintic.net'
password='SaintAugur910323'
msg = MIMEText(content, 'html', 'utf-8')
msg['From'] = _format_addr('SdpCenter <%s>' % from_addr)
msg['To'] = _format_addr('%s <%s>' % (user,to_addr))
msg['Subject'] = Header('来自Sdp系统的消息', 'utf-8').encode()
server=smtplib.SMTP(smtp_server, 25)
#server.set_debuglevel(1)   #if failed, please remove comments.
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()

