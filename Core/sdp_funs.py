#!/usr/bin/env python
#-*- coding:utf8 -*-
__author__ = 'saintic'
__date__ = '2015-10-12'
__version__ = 'sdp1.1'
__doc__ = 'some functions'

def genpasswd(L=15):
  if not isinstance(L, (int)):
    raise TypeError('Bad operand type, ask Digital.')
  from random import Random
  stri = ''
  chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
  length = len(chars) - 1
  random = Random()
  for i in range(L):
    stri+=chars[random.randint(0, length)]
  return stri

def read_conf(f,i):
  if not isinstance(f, (str)):
    raise TypeError('Bad operand type, ask a file.')
  if not isinstance(i, (str)):
    raise TypeError('bad operand type, ask string.')
  from configobj import ConfigObj
  try:
    return ConfigObj(f)[i]
  except:
    print 'Get configuration information failure.'
    return 1

