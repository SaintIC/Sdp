#!/usr/bin/python -O
#-*- coding=utf8 -*-
__author__ = 'taochengwei'
__date__ = '2015-12-08'
__doc__ = 'Sdp entry file, all the start.'

import sys,os
try:
    from Core.Public import Sysinfo,Time,Precheck,genuserinfo
    from Core.Config import LANG,WEBS,APPS
    from Core.Handler import StartAll
    from Core import __version__
    from Core.Log import SdpLog
except ImportError as errmsg:
    print __file__,"import module failed, because %s" % errmsg
    sys.exit(1)

def SdpCloudRun(**user):
    reload(sys)
    sys.setdefaultencoding(LANG)
    if not isinstance(user, (dict)):
        raise('Bae Parameter, ask dict.')

    if user['service'] in WEBS:
        StartAll('WEB', **user)
    elif user['service'] in APPS:
        StartAll('APP', **user)
    else:
        print "\033[0;31;40mError,Quit!!!\033[0m"
        sys.exit(3)

if __name__ == "__main__":
    try:

        if os.geteuid() != 0:
            print "\033[0;31;40mAborting:this program must be run as root.\033[0m"
            sys.exit(1)
        else:
            user = genuserinfo()
            Precheck(**user).checkargs()
            SdpCloudRun(**user)
            #user append for idetail
            print "\033[0;32;40m"
            for (k,v) in user.iteritems():
                print k + '    => ' + v
            print "\033[m"
            '''
            print """\033[0;32;40mUser(%s, %s, %s) build sucessfully.
    CreateTime      => %s
    ExpireTime      => %s
    Hostname        => %s
    Sdp Version     => %s
    Kernel Version  => %s
    CPUs            => %d
    Total Memory    => %s\033[m"""%(user['name'], user['email'], user['service'], Time(), Time(user['time']), Sysinfo.Hostname,  __version__, Sysinfo.Kernel, Sysinfo.CPUs, Sysinfo.Mem)
            '''

    except KeyboardInterrupt:
        SdpLog("捕获到终止信号，程序非正常退出!")
        print "捕获到终止信号，程序非正常退出!"
        exit(1)

    except IOError as e:
        SdpLog(e)
        raise IOError('System IO Error, %s' % e)

    except EOFError as e:
        SdpLog(e)
        raise EOFError('意外终止, %s' % e)
