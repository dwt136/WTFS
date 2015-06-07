# WTFS
Big homework for storage technology course of 2014-2015 spring.
Mapping between learn(Old) of Tsinghua online learning system and local file system (WTFS).

## Requirements
python2

fusepy

pyquery

webob

greenlet

gevent

All these dependencies can be aquired by pip.

## Features
Login and get courses of the current semester on old learn.

Read notifications of a course.

Get course files.

Read assignment details, and submit assignment attachment.

Read discussions of a course.

## Usage
Mounting learn to local file system, run:
```
python2 wtfs.py <mountpoint> <username> <password>
```

Example:
```
mkdir /home/wtfsuser/learn
python2 wtfs.py /home/wtfsuser/learn 20120113xx p@5Sw0Rd
```

To unmount, use fusermount:
```
fusermount -u <mountpoint>
```
