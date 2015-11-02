#!/usr/bin/env python
#-*- coding:utf8 -*-
__author__ = 'saintic'
__date__ = '2015-10-12'
__version__ = 'sdp1.1'
__doc__ = 'some functions'

try:
  import os,re
except ImportError as Errmsg:
  print __file__,"import module failed, because %s" % Errmsg

def genpasswd(L=15):
  if not isinstance(L, (int)):
    raise TypeError('Bad operand type, ask Digital.')
  from random import Random
  stri = ''
  chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
  length = len(chars) - 1
  random = Random()
  for i in range(L):
    stri+=chars[random.randint(0, length)]
  return stri

def read_conf(f,i):
  if not isinstance(f, (str)):
    raise TypeError('Bad operand type, ask a file.')
  if not isinstance(i, (str)):
    raise TypeError('bad operand type, ask string.')
  from configobj import ConfigObj
  try:
    return ConfigObj(f)[i]
  except:
    print 'Get configuration information failure.'
    return 1

CONF_NAME = 'sdp.conf'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_CONF = os.path.join(BASE_DIR, str(CONF_NAME))
APPS = ("mongodb", "mysql", "redis", "memcache", "tair")
WEBS = ("nginx", "tengine", "httpd", "lighttpd", "tomcat", "resin")
SERVICES = APPS + WEBS

#get variables from sdp.conf, format is dict.
GLOBAL_CONF = read_conf(BASE_CONF, 'globals')
REDIS_CONF = read_conf(BASE_CONF, 'redis')
MYSQL_CONF = read_conf(BASE_CONF, 'mysql')
DOCKER_CONF = read_conf(BASE_CONF, 'docker')

#set global variables
LANG = GLOBAL_CONF['LANG']
SDP_HOME = GLOBAL_CONF['SDP_HOME']
SDP_DATA_HOME = GLOBAL_CONF['SDP_DATA_HOME']
SDP_USER_DATA_HOME = os.path.join(SDP_DATA_HOME, str(GLOBAL_CONF['SDP_USER_DATA_HOME']))
SDP_LOGS_DATA_HOME = os.path.join(SDP_DATA_HOME, str(GLOBAL_CONF['SDP_LOGS_DATA_HOME']))
SDP_UC = os.path.join(SDP_DATA_HOME, str(GLOBAL_CONF['SDP_UC']))

#set redis variables
REDIS_HOST = REDIS_CONF['host']
REDIS_PORT = REDIS_CONF['port']
REDIS_DB = REDIS_CONF['db']
REDIS_PASSWORD = REDIS_CONF['password']

#set mysql variables
MYSQL_HOST = MYSQL_CONF['host']
MYSQL_PORT = MYSQL_CONF['port']
MYSQL_DB = MYSQL_CONF['db']
MYSQL_USER = MYSQL_CONF['user']
MYSQL_PASSWORD = MYSQL_CONF['password']

#set docker variables
DOCKER_PUSH = DOCKER_CONF['push']
DOCKER_TAG = DOCKER_CONF['imgtag']
DOCKER_REGISTRY = DOCKER_CONF['registry']

class PreCheck():
  pass

