#!/usr/bin/env python2
from sys import argv
from fuse import FUSE
from wtfuse import WTFuse
from learn import Learn


def main(mountpoint, username, password):
    print 'Logging in'
    l = Learn()
    if not l.login(username, password):
        return
    print 'Login successfully'
    print 'Reading data'
    if not l.read_to_mem():
        return
    print 'OK'
    FUSE(WTFuse(l, mountpoint), mountpoint, foreground=True)


if __name__ == '__main__':
    if len(argv) != 4:
        print 'Usage: %s <mountpoint> <username> <password>' % argv[0]
        exit(1)
    main(argv[1], argv[2], argv[3])
