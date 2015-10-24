#!/usr/bin/env python
#-*- coding=utf8 -*-
__author__ = 'saintic'
__date__ = '2015-10-18'
__doc__ = 'read or write redis'
__version__ = 'sdp1.1'

try:
  import redis
except ImportError as Errmsg:
  print __file__, "import redis module failed, because %s" % Errmsg
  exit(1)

class RedisObject():
  '''read or write redis, set or get, mset or mget.'''
  def __init__(self, conn):
    '''析构函数__init__需要两个参数，除了self，还需要传给类RedisObject一个conn tuple，包含redis连接的四个元素。'''
    if not isinstance(conn, (tuple)):
      raise TypeError('Bad Error Type, ask a tuple.')
    if len(conn) == 4:
      self.redis_object = redis.Redis(host=conn[0], port=conn[1], db=conn[2],password=conn[3])
    else:
      print 'Entry error, requires four elements.'
      exit(2)

  def keys(self):
    return self.redis_object.keys()

  def ping(self):
    return self.redis_object.ping()

  def set(self, cid,cip):
  if cid == None or cip == None:
    sys.exit(1)
  if db.exists(cid) ==  True:
    print "cid Exists\n"
    sys.exit(3)
  else:  #cid = False
    if db.get(cid) == cip:
      print "cip Exists\n"
      sys.exit(1)
    else:
      db.set(cid,cip)
      db.save()
      return (cid,cip)

  def get(self,cid):
  if cid == None:
    sys.exit(1)
  cip=db.get(cid)
  return cip

  def mset(self):
    pass

  def mget(self):
    pass

connect=('127.0.0.1', 6379, 1, None)
test=RedisObject(connect)
print test.ping()
print test.keys()


