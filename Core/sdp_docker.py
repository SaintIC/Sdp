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
    connect = docker.Client(base_url='unix://var/run/docker.sock')

  def image_build(self):
    pass

  def image_push(self):
    pass

  def container_create(self, **kw):
    if not isinstance(kw, (dict)):
      raise TypeError('Bad Type, ask a dict.')
    image=kw['image', None]
    mem=kw['mem', None]
    cpu=kw['cpu', None]
    name=kw['name', None]
    self.connect.create_container(image=image, stdin_open=True, tty=True, cpu=cpu, mem=mem, name=name)
    return container_id

  def container_start(self, container_id):
    self.connect.start(resource_id=container_id)
    return sucess or fail

  def container_ci(self, *info):
    'info=(push_start image, tag, registry)'
    if not isinstance(info, (list)):
      raise TypeError('Bad type, ask a list, (push_start, image, tag, registry)')
    if push_start == On or push_start == on:
      self.connect.push()
    return sucess or fail
