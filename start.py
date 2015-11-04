#!/usr/bin/env python
#-*- coding=utf8 -*-
__author__ = 'saintic'
__date__ = '2015-10-13'
__doc__ = 'Entry file, all the start.'
__version__ = 'sdp1.1'

try:
  import sys
  from Core.Public import *
  from subprocess import check_call
except ImportError as Errmsg:
  print __file__,"import module failed, because %s" % Errmsg

def main(**user):
  reload(sys)
  sys.setdefaultencoding(LANG)
  if not isinstance(user, (dict)):
    raise('Bae Parameter, ask dict.')

  if user['service'] in WEBS:
    check_call(['python ' + os.path.join(BASE_DIR, 'Web.py') + ' ' + user['name'] + ' ' + user['passwd'] + ' ' + str(user['time']) + ' ' + user['service'] + ' ' + user['email']], shell=True)
  elif user['service'] in APPS:
    check_call(['python ' + os.path.join(BASE_DIR, 'App.py') + ' ' + user['name'] + ' ' + user['passwd'] + ' ' + str(user['time']) + ' ' + user['service'] + ' ' + user['email']], shell=True)
  else:
    print "\033[0;31;40mErr,Quit!!!\033[0m"
    sys.exit(3)

if __name__ == "__main__":
  main(**args_check())
