#!/usr/bin/env python2
from sys import argv
from fuse import FUSE
from wtfuse import WTFuse
from learn import Learn


def main(mountpoint, username, password):
    print 'Logging in'
    l = Learn()
    res = l.login(username, password)
    if not res['success']:
        print res['error']
        return
    print 'Login successfully'
    print 'Reading data'
    l.read_to_mem()
    print 'OK'
    FUSE(WTFuse(l, mountpoint), mountpoint, foreground=True)


if __name__ == '__main__':
    if len(argv) != 4:
        print 'Usage: %s <mountpoint> <username> <password>' % argv[0]
        exit(1)
    main(argv[1], argv[2], argv[3])
