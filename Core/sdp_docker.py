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

  def build(self):
    pass

  def container_create(self, **kw):
    self.connect.create_container(image=img,stdin_open=True, tty=True, name=imgname)

  def container_run(self):
    pass

  def push(self):
    pass
