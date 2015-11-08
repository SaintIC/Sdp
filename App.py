#!/usr/bin/env python
#-*- coding=utf8 -*-
__author__ = 'saintic'
__date__ = '2015-10-14'
__doc__ = 'Apps'
__version__ = 'sdp1.1'

import sys,os,json
import Core.Docker
import Core.Public
from Core.Redis import RedisObject
from Core.Mail import SendMail
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
'''start docker'''
c=Core.Docker.Docker()
cid=c.Create(**dinfo)
c.Start(cid)
userinfo={"name":name,
 "passwd":passwd,
 "time":int(time),
 "service":service,
 "email":email,
 'image':image,
 'container':cid,
 'ip':Core.Public.SERVER_IP,
 'port':int(PORT)}

'''start write data'''
with open(Core.Public.SDP_UC, 'a+') as f:f.write(json.dumps(userinfo))
redisconn=(Core.Public.REDIS_HOST, Core.Public.REDIS_PORT, Core.Public.REDIS_DATADB, Core.Public.REDIS_PASSWORD)
userconn=(name, email, json.dumps(userinfo))
adminconn=('Administrator', 'staugur@vip.qq.com', json.dumps(userinfo))

rc=RedisObject(redisconn)
ec=SendMail()

if rc.ping():
  rc.hashset(**userinfo)
  print '\033[0;32;40m'
  print rc.hashget(name)
  print '\033[0m'
  ec.send(*userconn)
  ec.send(*adminconn)
else:
  print "\033[0;31;40mConnect Redis Server Error,Quit.\033[0m"
  sys.exit(7)

