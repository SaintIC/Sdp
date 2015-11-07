#!/usr/bin/env python
#-*- coding=utf8 -*-
__author__ = 'saintic'
__date__ = '2015-10-14'
__doc__ = 'Apps'
__version__ = 'sdp1.1'

import sys,os,json
import Core.Docker
import Core.Public
import Core.Redis.RedisObject
import Core.Mail.SendMail
if len(sys.argv) == 6:
  name, passwd, time, service, email = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
else:
  print "\033[0;31;40mError, ask six parameters.\033[0m"
  sys.exit(1)

if not os.path.isdir(Core.Public.SDP_DATA_HOME):os.mkdir(Core.Public.SDP_DATA_HOME)
portfile = os.path.join(Core.Public.SDP_DATA_HOME, '.aport')

if os.path.exists(portfile):
  with open(portfile, 'r') as f:
    PORT=f.read()
    PORT=int(PORT) + 1
else:
  PORT = Core.Public.STARTPORT
with open(portfile, 'w') as f:
  f.write(str(PORT))
PORT = int(PORT)

if not Core.Public.DOCKER_TAG:
  image=Core.Public.DOCKER_REGISTRY + '/' + service
else:
  image=Core.Public.DOCKER_REGISTRY + '/' + Core.Public.DOCKER_TAG + '/' + service

dinfo = {
    "image":image,
    "name":name,
    "port":Core.Public.PORTNAT[service],
    "bind":(Core.Public.SERVER_IP, PORT)
  }
c=Core.Docker.Docker()
cid=c.Create(**dinfo)
c.Start(cid)
userinfo={"name":name, "passwd":passwd, "time":time, "service":service, "email":email, 'image':image, 'container':cid, 'ip':Core.Public.SERVER_IP, 'port':PORT}

redisconn=('127.0.0.1', 6379, 8)
useremailconn=(name, email, json.dumps(userinfo))
adminemailconn=('Administrator', 'staugur@vip.qq.com', json.dumps(userinfo))
rc=RedisObject(redisconn)
ec=SendMail(emailconn)
if rc.ping() == 'PONG':
  rc.hashset(**userinfo)
  ec.send(useremailconn)
  ec.send(adminemailconn)
else:
  print "\033[0;31;40mConnect Redis Server Error,Quit.\033[0m"
  sys.exit(7)
