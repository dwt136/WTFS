import errno
import os
from stat import S_IFDIR, S_IFREG
from fuse import FuseOSError, Operations
from const import *
from time import time


def path_type(path):
    path = path.strip()
    if path.endswith('/'):
        path = path[:-1]
    if len(path) == 0 or not path.startswith('/'):
        path = '/' + path
    for key, pattern in PATTERNS.iteritems():
        if pattern.match(path):
            return key
    return None


def is_dir_type(t):
    return t in (
        'ROOT', 'COURSES', 'COURSE', 'NOTIFICATIONS', 'FILES', 'HOMEWORKS',
        'HOMEWORK', 'HOMEWORK_ATTACH', 'HOMEWORK_SUBMIT', 'DISCUSS')


class WTFuse(Operations):

    def __init__(self, l, mountpoint):
        self.learn = l
        self.mountpoint = mountpoint

    def getattr(self, path, fh=None):
        t = path_type(path)
        if t is None:
            raise FuseOSError(errno.ENOENT)
        print t, path
        mode = S_IFREG | 0444
        if t == 'HOMEWORK_ATTACH':
            mode = S_IFDIR | 0777
        elif t == 'HOMEWORK_ATTACH_FILE':
            mode = S_IFREG | 0666
        elif is_dir_type(t):
            mode = S_IFDIR | 0555
        now = time()
        return dict(
            st_atime=now,
            st_ctime=now,
            st_mtime=now,
            st_mode=mode,
            st_nlink=2,
        )

    def create(self, path, mode):
        return 0

    def read(self, path, size, offset, fh):
        return 'wow'

    def readdir(self, path, fh):
        t = path_type(path)
        if t is None:
            raise FuseOSError(errno.ENOENT)
        l = ['.', '..']
        if t == 'ROOT':
            l.extend([NEW, OLD])
        elif t == 'COURSES':
            l.extend(self.learn.get_courses())
        return l

    def rename(self, old, new):
        pass

    def statfs(self, path):
        return dict(f_bsize=512, f_blocks=4096, f_bavail=2048)

    def truncate(self, path, length, fh=None):
        pass

    def write(self, path, data, offset, fh):
        return len(data)
