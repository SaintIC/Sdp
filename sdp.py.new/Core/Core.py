#!/usr/bin/env python
#-*- coding=utf8 -*-
__author__ = 'saintic'
__date__ = '2015-11-10'
__doc__ = 'Webs And Apps'
__version__ = 'sdp1.1'

import sys,os,json
import Docker
import Public
from Redis import RedisObject
from Mail import SendMail

def StartAll(SdpType, **kwargs):
  if SdpType:
    raise TypeError('%s need a type, app or web.' % __name__)
  if isinstance(kwargs, (dict)):
    name, passwd, time, service, email = user['name'], user['passwd'], str(user['time']), user['service'], user['email']
    dn = name + '.sdpy.saintic.com'
    userfile = os.path.join(Public.SDP_USER_DATA_HOME, name)
    portfile = os.path.join(Public.SDP_DATA_HOME, '.aport')

  if not os.path.isdir(Public.SDP_DATA_HOME):os.mkdir(Public.SDP_DATA_HOME)
  if not os.path.isdir(Public.SDP_USER_DATA_HOME):os.mkdir(Public.SDP_USER_DATA_HOME)
  if not os.path.isdir(Public.SDP_LOGS_DATA_HOME):os.mkdir(Public.SDP_LOGS_DATA_HOME)
  if not os.path.isdir(Public.NGINX_CONF_DIR):os.mkdir(Public.NGINX_CONF_DIR)

  #set portfile, read and write(update)
  if os.path.exists(portfile):
    with open(portfile, 'r') as f:
      PORT=f.read()
      PORT=int(PORT) + 1
  else:
    PORT = Public.STARTPORT
  with open(portfile, 'w') as f:
    f.write(str(PORT))
  PORT = int(PORT)

  #define image_name
  """
  if not Public.DOCKER_TAG:
    image = Public.DOCKER_REGISTRY + '/' + service
  else:
    image = Public.DOCKER_REGISTRY + '/' + Public.DOCKER_TAG + '/' + service
  """
  image = Public.DOCKER_REGISTRY + '/' + service

  #Web start docker
  dockerinfo = {"image":image, "name":name}
  if SdpType == "web" or SdpType == "WEB":
    dockerinfo["port"] = Public.PORTNAT['web']
    dockerinfo["bind"] = ('127.0.0.1', PORT)
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


  #App start docker
  if SdpType == "app" or SdpType == "APP":
    dockerinfo["port"] = Public.PORTNAT[service]
    dockerinfo["bind"] = (Public.SERVER_IP, PORT)
    #define info for user and admin
    userinfo_admin = {"name":name, "passwd":passwd, "time":int(time), "service":service, "email":email, 'image':image, 'container':cid, 'ip':Public.SERVER_IP, 'port':int(PORT)}
    userinfo_user = r'''
Dear %s, 以下是您的SdpCloud服务使用信息！
Your Name:%s;
Your Password:%s;
Your UseTime:%d;
Your Service:%s;
Your Email:%s;
Your Connection:%s:%d

祝您使用愉快。如果有任何疑惑，欢迎与我们联系:
QQ:   1663116375
Mail: staugur@saintic.com
官网: https://saintic.com/
微博: http://weibo.com/staugur/
淘宝: https://shop126877887.taobao.com/
''' %(name, name, passwd, int(time), service, email, Public.SERVER_IP, int(PORT))

  #start docker
  C = Docker.Docker()
  cid = C.Create(**dockerinfo)
  C.Start(cid)

  #define connection for redis and mailserver.
  redisconn = (Public.REDIS_HOST, Public.REDIS_PORT, Public.REDIS_DATADB, Public.REDIS_PASSWORD)
  userconn = (name, email, userinfo_user)
  adminconn = ('Administrator', Public.ADMIN_EMAIL, json.dumps(userinfo_admin))
  rc = RedisObject(redisconn)
  ec = SendMail()

  #start write data
  if rc.ping():
    rc.hashset(**userinfo_admin)
    print '\033[0;32;40m'
    print rc.hashget(name)
    print '\033[0m'
    ec.send(*userconn)
    ec.send(*adminconn)
    with open(Public.SDP_UC, 'a+') as f:f.write(json.dumps(userinfo_admin))
    #with open(userfile, 'w') as f:f.write(json.dumps(userinfo_admin))
  else:
    print "\033[0;31;40mConnect Redis Server Error,Quit.\033[0m"
    sys.exit(7)
