import errno
import os
import learn
from stat import S_IFDIR, S_IFREG
from fuse import FuseOSError, Operations
from const import *
from time import time
from collections import defaultdict


def path_type(path):
    path = path.strip()
    if path.endswith('/'):
        path = path[:-1]
    if len(path) == 0 or not path.startswith('/'):
        path = '/' + path
    for key, pattern in PATTERNS.iteritems():
        match = pattern.match(path)
        if match:
            return key, match
    return None, None


def is_dir_type(t):
    return t in (
        'ROOT', 'COURSE', 'NOTIFICATIONS', 'FILES', 'HOMEWORKS', 'HOMEWORK',
        'HOMEWORK_SUBMIT', 'DISCUSSES')


class WTFuse(Operations):

    def __init__(self, l, mountpoint):
        self.learn = l
        self.mountpoint = mountpoint
        self.file_cache = dict()
        self.buf = {}

    def _cache_file(self, path, t, match):
        if self.file_cache.has_key(path):
            return self.file_cache[path]
        res = None
        if t == 'INFO':
            res = self.learn.get_info(match.group(1))
        elif t == 'NOTIFICATION':
            res = self.learn.get_notification(match.group(1), match.group(2))
        elif t == 'DISCUSS':
            res = self.learn.get_discuss(match.group(1), match.group(2))
        elif t == 'HOMEWORK_DETAIL':
            res = self.learn.get_homework_detail(match.group(1), match.group(2))
        elif t == 'FILE':
            res = self.learn.get_file(match.group(1), match.group(2))
        self.file_cache[path] = res
        return res

    def _get_submit_file(self, path, course_name, hw_name):
        if self.file_cache.has_key(path):
            return self.file_cache[path]
        res, name = self.learn.get_submit_file(course_name, hw_name)
        if name == '':
            return '', ''
        self.file_cache[path] = (res, name)
        self.file_cache[path + '/' + name] = (res, name)
        return (res, name)

    def getattr(self, path, fh=None):
        t, match = path_type(path)
        if t is None:
            raise FuseOSError(errno.ENOENT)
        if t != 'ROOT' and match.group(1) not in self.learn.courses:
            raise FuseOSError(errno.ENOENT)
        if t == 'NOTIFICATION' and match.group(
            2) not in self.learn.notifications[match.group(1)]:
            raise FuseOSError(errno.ENOENT)
        if t == 'FILE' and match.group(
            2) not in self.learn.files[match.group(1)]:
            raise FuseOSError(errno.ENOENT)
        if t in ('HOMEWORK', 'HOMEWORK_DETAIL', 'HOMEWORK_SUBMIT', 'HOMEWORK_SUBMIT_FILE') and match.group(
            2) not in self.learn.homeworks[match.group(1)]:
            raise FuseOSError(errno.ENOENT)
        if t == 'DISCUSS' and match.group(
            2) not in self.learn.discusses[match.group(1)]:
            raise FuseOSError(errno.ENOENT)
        if t == 'HOMEWORK_SUBMIT_FILE' and (not self.file_cache.has_key(
            path) or match.group(3) != self.file_cache[path][1]):
            raise FuseOSError(errno.ENOENT)

        print 'getattr\t', t, path
        mode = S_IFREG | 0444
        if t == 'HOMEWORK_SUBMIT':
            mode = S_IFDIR | 0777
        elif t == 'HOMEWORK_SUBMIT_FILE':
            mode = S_IFREG | 0644
        elif is_dir_type(t):
            mode = S_IFDIR | 0555

        size = 0
        if t in ('INFO', 'NOTIFICATION', 'FILE', 'HOMEWORK_DETAIL', 'DISCUSS'):
            size = len(self._cache_file(path, t, match))
        elif t == 'HOMEWORK_SUBMIT_FILE':
            size = len(self._cache_file(path, t, match)[0])
        now = time()
        return dict(
            st_atime=now,
            st_ctime=now,
            st_mtime=now,
            st_mode=mode,
            st_nlink=2,
            st_size=size,
        )

    def create(self, path, mode):
        t, match = path_type(path)
        if t != 'HOMEWORK_SUBMIT_FILE':
            return 0
        print 'create\t', path
        parent = path[:path.rfind('/')]
        name = learn.dealName(path[path.rfind('/') + 1 : ])
        self.file_cache[parent] = ('', name)
        self.file_cache[parent + '/' + name] = ('', name)
        print 'mode', mode
        return 0

    def open(self, path, flags):
        print 'open\t', path
        return 1

    def release(self, path, fh):
        print 'release\t', path
        return 1

    def read(self, path, size, offset, fh):
        t, match = path_type(path)
        try:
            self.getattr(path, None)
        except:
            return
        print 'read\t', path
        f = self._cache_file(path, t, match)
        if isinstance(f, tuple):
            f = f[0]
        return f[offset : offset + size]

    def readdir(self, path, fh):
        t, match = path_type(path)
        if t is None:
            raise FuseOSError(errno.ENOENT)
        print 'readdir\t', path
        l = ['.', '..']
        if t == 'ROOT':
            l.extend(self.learn.get_courses())
        elif t == 'COURSE':
            l.extend([INFO, NOTIFICATION, FILE, HOMEWORK, DISCUSS])
        elif t == 'NOTIFICATIONS':
            l.extend(self.learn.get_notifications(match.group(1)))
        elif t == 'FILES':
            l.extend(self.learn.get_files(match.group(1)))
        elif t == 'HOMEWORKS':
            l.extend(self.learn.get_homeworks(match.group(1)))
        elif t == 'HOMEWORK':
            l.extend([HOMEWORK_DETAIL, HOMEWORK_SUBMIT])
        elif t == 'DISCUSSES':
            l.extend(self.learn.get_discusses(match.group(1)))
        elif t == 'HOMEWORK_SUBMIT':
            res, name = self._get_submit_file(path, match.group(1), match.group(2))
            if name != '':
                l.extend([name])
        return l

    def statfs(self, path):
        return dict(f_bsize=512, f_blocks=4096, f_bavail=2048)

    def truncate(self, path, length, fh=None):
        t, match = path_type(path)
        if t != 'HOMEWORK_SUBMIT_FILE':
            return
        print 'truncate\t', path, length
        parent = path[:path.rfind('/')]
        name = path[path.rfind('/') + 1 : ]
        res = self.file_cache[path][0]
        self.file_cache[parent] = (res[:length], name)
        self.file_cache[path] = (res[:length], name)

    def write(self, path, data, offset, fh):
        t, match = path_type(path)
        if t != 'HOMEWORK_SUBMIT_FILE':
            return 0
        if not self.file_cache.has_key(path) or not path.endswith(self.file_cache[path][1]):
            return 0
        print 'write\t', path
        self.file_cache[path] = (self.file_cache[path][0][:offset] + data,
                self.file_cache[path][1])
        self.learn.submit(match.group(1), match.group(2),
                self.file_cache[path][0], self.file_cache[path][1])
        return len(data)
