#!/usr/bin/env python
# coding=utf-8
#
# File: StickyNotes/src/python/setup.py
# Author: Hankso
# Webpage: https://github.com/hankso
# Time: Sat 29 Feb 2020 04:21:01 PM CST

from setuptools import setup

setup(
    name         = 'stickynotes',
    version      = '1.0.0',
    url          = 'https://github.com/hankso/StickyNotes',
    author       = 'hankso',
    author_email = 'hankso1106@gmail.com',
    license      = 'MIT',
    description  = 'Create, edit and manage your cloud notes with QRCode',
    package_data = {},
    install_requires = ['bottle', ],
)
