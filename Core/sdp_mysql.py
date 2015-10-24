#!/usr/bin/env python
#-*- coding=utf8 -*-
__author__ = 'saintic'
__date__ = '2015-10-24'
__doc__ = 'read or write mysql'
__version__ = 'sdp1.1'

try:
  import MySQLdb as mysql
except ImportError as errmsg1:
  import mysql
except ImportError as Errmsg2:
  print __file__, "import MySQLdb and mysql-connector-python modules failed, because %s,%s" %(Errmsg1, Errmsg2)
  exit(1)

class MySQLObject():
  def __init__(self, conn):
    '''析构函数__init__需要两个参数，除了self，还需要传给类MySQLObject一个conn tuple，包含连接的五个元素。'''
    if not isinstance(conn, (tuple)):
      raise TypeError('Bad Error Type, ask a tuple.')
    if len(conn) == 5:
      self.redis_object = mysql.connect(host=conn[0], port=conn[1], db=conn[2], user=conn[3], password=conn[4])
    else:
      print 'Entry error, requires five elements.'
      exit(2)

connect=('127.0.0.1', 6379, 1, 'root', 'passwd)'
test=MySQLObject(connect)
