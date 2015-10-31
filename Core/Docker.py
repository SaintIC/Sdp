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

class Docker():
  '''Operation docker, maybe json format'''
  def __init__(self):
    self.connect = docker.Client(base_url='unix://var/run/docker.sock')

  def create(self, **kw):
    '''{image_name, mem, cpu, name, port(tuple)}'''
    if not isinstance(kw, (dict)):
      raise TypeError('Bad Type, ask a dict.')
    image=kw.get('image', None)
    mem=kw.get('mem', None)
    cpu=kw.get('cpu', None)
    name=kw.get('name', None)
    ports=kw.get('ports', None)
    cid=self.connect.create_container(image=image,stdin_open=True,tty=True,ports=ports)['Id']
    return cid

  def start(self, container_id):
    runid=self.connect.start(resource_id=container_id)
    if runid == container_id:
      return "Successful"
    else:
      return "Failed"

  def ci(self, *info):
    'info={push_start image, tag, registry}'
    if not isinstance(info, (list)):
      raise TypeError('Bad type, ask a list, (push_start, image, tag, registry)')
    if push_start == On or push_start == on:
      self.connect.push()
    return

