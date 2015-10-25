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
  '''read or write redis, set or get, mset or mget.
  析构函数需要传给类RedisObject一个tuple，包含redis连接的四个元素。'''
  def __init__(self, conn):
    if not isinstance(conn, (tuple)):
      raise TypeError('Bad Error Type, ask a tuple.')
    if len(conn) == 4:
      self.redis_object = redis.Redis(host=conn[0], port=conn[1], db=conn[2],password=conn[3])
    else:
      print 'Entry error, requires four elements.'
      return 2

  def keys(self):
    return self.redis_object.keys()

  def ping(self):
    return self.redis_object.ping()

  def set(self, k, v):
    if k == None or v == None:
      print "parameter error, key or value is none."
      return 1
    if self.redis_object.exists(k):
      print "%s exists, quit." % k
      return 1
    else:
      if self.redis_object.get(k) == v:
        print "%s exist, but equal %s, will quit." %(k,v)
        return 1
      else:
        self.redis_object.set(k,v)
        self.redis_object.save()
        return (k,v)

  def get(self, k):
    if k == None:
      print "key(%s) get error." % k
      return 1
    return self.redis_object.get(k)

  def mset(self):
    pass

  def mget(self):
    pass

connect=('127.0.0.1', 6379, 0, None)
test=RedisObject(connect)
print test.ping()
print test.keys()
print test.set('name','taochengwei')
#print test.get()

