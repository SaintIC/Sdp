#!/usr/bin/env python
#-*- coding=utf8 -*-
__author__ = 'saintic'
__date__ = '2015-10-14'
__doc__ = 'Webs'
__version__ = 'sdp1.1'

import sys,os,json
import Core.Docker
import Core.Public
from Core.Redis import RedisObject
from Core.Mail import SendMail

if len(sys.argv) == 6:
  name, passwd, time, service, email = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
  dn = name + '.sdp.py.saintic.com'
  userfile = os.path.join(Core.Public.SDP_USER_DATA_HOME, name)
else:
  print "\033[0;31;40mError, ask six parameters.\033[0m"
  sys.exit(1)

if not os.path.isdir(Core.Public.SDP_DATA_HOME):os.mkdir(Core.Public.SDP_DATA_HOME)
if not os.path.isdir(Core.Public.SDP_USER_DATA_HOME):os.mkdir(Core.Public.SDP_USER_DATA_HOME)
if not os.path.isdir(Core.Public.SDP_LOGS_DATA_HOME):os.mkdir(Core.Public.SDP_LOGS_DATA_HOME)
if not os.path.isdir(Core.Public.NGINX_CONF_DIR):os.mkdir(Core.Public.NGINX_CONF_DIR)
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

#start docker
dockerinfo = {
    "image":image,
    "name":name,
    "port":Core.Public.PORTNAT['web'],
    "bind":('127.0.0.1', PORT)
  }
c=Core.Docker.Docker()
cid=c.Create(**dockerinfo)
c.Start(cid)

#define info for user and admin
userinfo_admin = {"name":name, "passwd":passwd, "time":int(time), "service":service, "email":email, 'image':image, 'container':cid, 'ip':'127.0.0.1', 'port':int(PORT), 'dn':dn}
userinfo_user = r'''
Dear %s, 以下是您的SdpCloud服务使用信息！
Your Name:%s;
Your Password:%s;
Your UseTime:%d;
Your Service:%s;
Your Email:%s;
Your Connection:%s

祝您使用愉快。如果有任何疑惑，欢迎与我们联系:
QQ:   1663116375
Mail: staugur@saintic.com
官网: https://saintic.com/
微博: http://weibo.com/staugur/
淘宝: https://shop126877887.taobao.com/
''' %(name, name, passwd, int(time), service, email, dn)

#start nginx proxy

#start write data
with open(Core.Public.SDP_UC, 'a+') as f:f.write(json.dumps(userinfo_admin))
redisconn=(Core.Public.REDIS_HOST, Core.Public.REDIS_PORT, Core.Public.REDIS_DATADB, Core.Public.REDIS_PASSWORD)
userconn=(name, email, userinfo_user)
adminconn=('Administrator', 'staugur@saintic.net', json.dumps(userinfo_admin))
rc=RedisObject(redisconn)
ec=SendMail()

#end web, write data and sendmail
if rc.ping():
  rc.hashset(**userinfo_admin)
  print '\033[0;32;40m'
  print rc.hashget(name)
  print '\033[0m'
  ec.send(*userconn)
  ec.send(*adminconn)
  with open(userfile, 'w') as f:
    f.write(json.dumps(userinfo_admin))
else:
  print "\033[0;31;40mConnect Redis Server Error,Quit.\033[0m"
  sys.exit(7)

