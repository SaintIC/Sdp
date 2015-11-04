#!/usr/bin/env python
#-*- coding=utf8 -*-
__author__ = 'saintic'
__date__ = '2015-10-14'
__doc__ = 'Apps'
__version__ = 'sdp1.1'

import sys,os
import Core.Docker
import Core.Public
if len(sys.argv) == 6:
  name, passwd, time, service, email = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
else:
  print "\033[0;31;40mError in parameter.\033[0m"
  sys.exit(1)

if not os.path.isdir(Core.Public.SDP_DATA_HOME):os.mkdir(Core.Public.SDP_DATA_HOME)
portfile = os.path.join(Core.Public.SDP_DATA_HOME, '.aport')

if os.path.exists(portfile):
  with open(portfile, 'r') as f:
    PORT=f.read()
    PORT=int(PORT) + 1
else:
  PORT = str(8000)
with open(portfile, 'w') as f:
  f.write(str(PORT))
PORT = int(PORT)

if not Core.Public.DOCKER_TAG:
  image=Core.Public.DOCKER_REGISTRY + '/' + service
else:
  image=Core.Public.DOCKER_REGISTRY + '/' + Core.Public.DOCKER_TAG + '/' + service

userinfo = {
    "image":image,
    "name":name,
    "port":Core.Public.PORTNAT[service],
    "bind":('0.0.0.0', PORT)
  }
c=Core.Docker.Docker()
cid=c.Create(**userinfo)
c.Start(cid)
