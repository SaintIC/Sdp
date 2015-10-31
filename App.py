#!/usr/bin/env python
#-*- coding=utf8 -*-
__author__ = 'saintic'
__date__ = '2015-10-14'
__doc__ = 'Apps'
__version__ = 'sdp1.1'

try:
  import start
except ImportError as errmsg:
  print __file__,'import module fail, because %s' % errmsg

PORT=[8000,]
#PORT:Start the port

print start.user()

