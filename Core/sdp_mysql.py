#!/usr/bin/env python
#-*- coding=utf8 -*-
__author__ = 'saintic'
__date__ = '2015-10-24'
__doc__ = 'read or write mysql'
__version__ = 'sdp1.1'

try:
  import MySQLdb as mysql
except ImportError as errmsg:
  print __file__, "fail: %s" % errmsg
  exit(1)

class MySQLObject():
  def __init__(self, conn):
    if not isinstance(conn, (tuple)):
      raise TypeError('Bad Error Type, ask a tuple, (host,port,db,user,password)')
    if len(conn) == 5:
      self.mysql_object = mysql.connect(host=conn[0], port=conn[1], db=conn[2], user=conn[3], passwd=conn[4])
    else:
      print 'Entry error, requires five elements.'
      exit(2)

  def insert(self, sql):
    #check sql
    op=self.mysql_object.cursor()
    rs=op.execute(sql)
    op.close()
    self.mysql_object.close()
    return rs

connect=('127.0.0.1', 33061, 'sdp', 'sdp', 'passwd')
test=MySQLObject(connect)
print test.insert('show tables;')

