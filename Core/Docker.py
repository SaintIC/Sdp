#!/usr/bin/env python
#-*- coding=utf8 -*-
__author__ = 'saintic'
__date__ = '2015-10-19'
__version__ = 'sdp1.1'
__doc__ = 'docker functions, for images, for containers'

try:
  import docker
except ImportError as errmsg:
  print __file__, 'import docker module failed, because %s' % errmsg

class Docker:
  '''Operation docker, maybe json format'''
  def __init__(self):
    self.connect = docker.Client(base_url='unix://var/run/docker.sock')

  def Create(self, **kw):
    '''{image, name, mem, cpu, port(tuple), host_ip_port{port:wan_port+ip}}
    eg:
    {
     "image":"registry.saintic.com/mysql",
     "name":"taochengwei",
     "port":3306,
     "bind":('127.0.0.1',10000),
     "mem":512
    }
    '''
    if not isinstance(kw, (dict)):
      raise TypeError('Bad Type, ask a dict.')

    image=kw['image']
    name=kw.get('name', None)
    container_port=kw.get('port', None)#container open port,int,attach cports
    host_ip_port=kw.get('bind', None)#should be tuple,(host_ip,host_port),all is {container_port, (host_ip, host_port)}
    mem_limit=kw.get('mem', None)#ask int,unit:m
    memswap_limit=kw.get('mem',None)#mem(int)
    cpu_shares =kw.get('cpu', None)
    cports=[]
    cports.append(container_port)

    print "image:%s, name:%s ,cports:%s, bind=%s, mem:%s, cpu:%s" %(image,name,cports,host_ip_port,mem,cpu_shares)
    cid=self.connect.create_container(image=image, name=name, stdin_open=True, tty=True, ports=cports, host_config=docker.utils.create_host_config(port_bindings={container_port:host_ip_port}), mem_limit=mem_limit+'m', memswap_limit=mem_limit, cpu_shares=cpu_shares).get('Id')
    return cid

  def Start(self, cid):
    runid=self.connect.start(resource_id=cid)
    if runid == cid:
      print "Successful"
      return 0
    else:
      print "Failed"
      return 1

  def Ci(self, image):
    '''info={push_start image, tag, registry}'''
    if not isinstance(info, (list)):
      raise TypeError('Bad type, ask a list, (push_start, image, tag, registry)')
    if push_start == On or push_start == on:
      self.connect.push(image)
    return

  def test_create(self):
    cid=self.connect.create_container(image='registry.saintic.com/redis', stdin_open=True, tty=True, ports=[6379,], host_config=self.connect.create_host_config(port_bindings={6379: ('127.0.0.1', 9989)}))
    return cid

  def test_start(self, cid):
    #self.connect.start(resource_id=cid, port_bindings={9300:6379,9301:9989})
    self.connect.start(resource_id=cid)

if __name__ == "__main__":
  conn=Docker()
  j={
     "image":"registry.saintic.com/mysql",
     "name":"taochengwei",
     "port":3306,
     "bind":('127.0.0.1',10000),
     "mem":512
    }
  cid=conn.Create(123)
  print "Create Container Id:%s" % cid
  c.Start(cid)


