#!/usr/bin/env python
# coding=utf-8
#
# File: StickyNotes/src/python/sticky/configs.py
# Author: Hankso
# Webpage: https://github.com/hankso
# Time: Sat 29 Feb 2020 03:30:19 PM CST

import string
import os.path as op
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

BASEDIR = op.dirname(op.abspath(__file__))

POSSIBLE_CONFIG_FILES = list(filter(op.exists, [
    op.join(BASEDIR, 'config.conf'),
    op.join(BASEDIR, 'config.ini'),
    op.abspath('./stickynotes.conf'),
    op.expanduser('~/.stickynotes.conf'),
]))

# Default configurations
CONFIG = config = type('Config', (object, ), {
    'statics': op.join(BASEDIR, 'statics'),
    'storage': op.join(BASEDIR, 'data'),
    'usechar': string.hexdigits,
    'sluglen': 8,
    'maxtry': 128,
    'host': '127.0.0.1',
    'port': 8080,
    'debug': False,
    'backend': 'db',
})()


# Load config files
def load_config():
    if not POSSIBLE_CONFIG_FILES:
        return
    cp = configparser.ConfigParser()
    cp.read(POSSIBLE_CONFIG_FILES)
    for key, sec in [(k, s) for s in cp.values() for k in s.keys()]:
        try:
            if not hasattr(config, key):
                continue
            elif key in ['sluglen', 'maxtry', 'port', ]:
                value = sec.getint(key)
            elif key in ['debug', ]:
                value = sec.getboolean(key)
            elif key in ['statics', 'storage', ]:
                value = op.abspath(op.join(BASEDIR, sec.get(key)))
            else:
                value = sec.get(key)
        except Exception:
            print('Warning: Invalid configuration `{}`=`{}`!'
                  .format(key, sec.get(key)))
            continue
        setattr(config, key, value)


load_config()

# THE END
