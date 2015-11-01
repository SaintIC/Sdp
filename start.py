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
  '''exec file for service'''
  reload(sys)
  sys.setdefaultencoding(LANG)
  if not isinstance(user, (dict)):
    raise('Bae Parameter, ask dict.')

  if user_service in WEBS:
    check_call(['python ' + os.path.join(BASE_DIR, 'Web.py') + ' ' + user['name'] + ' ' + user['passwd'] + ' ' + str(user['time']) + ' ' + user['service'] + ' ' + user['email']], shell=True)
  elif user_service in APPS:
    check_call(['python ' + os.path.join(BASE_DIR, 'App.py') + ' ' + user['name'] + ' ' + user['passwd'] + ' ' + str(user['time']) + ' ' + user['service'] + ' ' + user['email']], shell=True)
  else:
    print "\033[0;31;40mErr,Quit!!!\033[0m"
    sys.exit(3)

if __name__ == "__main__":
  if len(sys.argv) == 5:
    user_name = str(sys.argv[1])
    user_passwd = str(genpasswd())
    user_time = int(sys.argv[2])
    user_service = str(sys.argv[3])
    user_email = str(sys.argv[4])
    if not isinstance(user_time, (int)) or user_time <= 0:
      raise ValueError('Bad Value, demand is greater than 0 of the number.')
      sys.exit(127)

    if not user_service in SERVICES:
      print "\033[0;31;40mUnsupport service\033[0m"
      sys.exit(128)

    if re.match(r'[a-zA-Z\_][0-9a-zA-Z\_]{1,19}', user_name) == None:
      print '\033[0;31;40muser_name illegal:A letter is required to begin with a letter or number, and the range number is 1-19.\033[0m'
      sys.exit(128)

    if re.match(r'([0-9a-zA-Z\_*\.*\-*]+)@([a-zA-Z0-9\-*\_*\.*]+)\.([a-zA-Z]+$)', user_email) == None:
      print "\033[0;31;40mMail format error.\033[0m"
      sys.exit(129)

    if user_name and user_passwd and user_time and user_service and user_email:
      user={"name":user_name, "passwd":user_passwd, "time":user_time, "service":user_service, "email":user_email}
      main(**user)
    else:
      print "\033[0;31;40mERROR:Has false argument\033[0m"
      exit(1)

  else:
    print "\033[0;31;40mUsage:user time service email\033[0m"
    exit(1)
