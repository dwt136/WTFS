# WTFS
Big homework for storage technology course of 2014-2015 spring.
Mapping between learn/learn.cic of Tsinghua online learning system and local file system (WTFS).

## Requirements
python2
fusepy

## Usage
Mounting learn to local file system, run:
```
python2 wtfs.py mountpoint
```

Example:
```
mkdir /home/wtfsuser/learn
python2 wtfs.py /home/wtfsuser/learn
```
