#!/usr/bin/env python
#-*- coding=utf8 -*-
__author__ = 'saintic'
__date__ = '2015-10-19'
__version__ = 'sdp1.1'
__doc__ = 'docker functions, for images, for containers'

try:
  import docker
  from Public import DOCKER_PUSH
except ImportError as errmsg:
  print __file__, 'import docker module failed, because %s' % errmsg

class Docker():
  '''Operation docker, maybe json format'''
  def __init__(self):
    self.connect = docker.Client(base_url='unix://var/run/docker.sock')

  def test(self,**kw):
    if not isinstance(kw, (dict)):
      raise TypeError('TypeError')
    print type(kw),kw

  def Create(self, **kw):
    '''{image, name, mem, cpu, port(tuple), host_ip_port{port:wan_port+ip}}
    eg:{"image":"registry.saintic.com/mysql", "name":"taochengwei", "port":3306, "bind":('127.0.0.1',10000)}
    '''
    if not isinstance(kw, (dict)):
      raise TypeError('Bad Type, ask a dict.')
    image=kw['image']
    name=kw.get('name', None)
    container_port=kw.get('port', None)#container open port,int,attach cports
    host_ip_port=kw.get('bind', None)#should be tuple,(host_ip,host_port),all is {container_port, (host_ip, host_port)}
    cports=[]
    cports.append(container_port)
    r=self.connect.create_container(image=image, name=name, stdin_open=True, tty=True, ports=cports, host_config=self.connect.create_host_config(port_bindings={container_port:host_ip_port}), mem_limit=None, memswap_limit=None, cpu_shares=None)
    cid=r['Id'][:12]
    print '\033[0;32;40mSuccess Create Container %s\033[0m' % cid
    return cid

  def Start(self, cid):
    r=self.connect.start(resource_id=cid)
    if r == None:
      print '\033[0;32;40mSuccess Start Container %s\033[0m' % cid
      return 0
    else:
      print "\033[0;31;40mStart Failed.\033[0m"
      return 1

  def Ci(self, image):
    if not isinstance(image, (str)):
      raise TypeError('Bad type, ask an image')
    if DOCKER_PUSH == On or DOCKER_PUSH == on:
      self.connect.push(image)
    return

