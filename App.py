#!/usr/bin/env python
#-*- coding=utf8 -*-
__author__ = 'saintic'
__date__ = '2015-10-14'
__doc__ = 'Apps'
__version__ = 'sdp1.1'

import sys,os
import Core.Docker
import start
PORT = str(8000)
portfile = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.port')

if len(sys.argv) == 6:
  user=(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5])
else:
  print 'Error in parameter'
  sys.exit(1)

if os.path.isfile(portfile):
  try:
    with open(portfile, 'r') as f:
      PORT=f.read()
  except:
    print "No port file, init to 8000"
else:
  with open(portfile, 'w') as f:
    f.write(PORT)

PORT=int(PORT)

'''
c=Core.Docker.Docker()
info=c.create(image='registry.saintic.com/base',ports=[PORT,])
c.start(info)
'''
print start.DOCKER_CONF
print start.DOCKER_PUSH
print start.DOCKER_TAG
print start.DOCKER_REGISTRY


