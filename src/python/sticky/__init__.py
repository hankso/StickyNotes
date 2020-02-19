#!/usr/bin/env python
# coding=utf-8
#
# File: StickyNotes/src-python/sticky/__init__.py
# Author: Hankso
# Webpage: https://github.com/hankso
# Time: Sun 09 Feb 2020 06:32:07 PM CST

'''
1. generate random length of slug for indexing
2. edit page template
3. notes static host
4. management page
'''

import os
import sys
import json
import time
import random
import shutil
import string
import pathlib

# requirements.txt: network: bottle
import bottle
sticky = bottle.Bottle()

# Configurations
__basedir__ = os.path.dirname(os.path.abspath(__file__))
__statics__ = os.path.join(__basedir__, '../../static')
__filedir__ = pathlib.Path(__basedir__).joinpath('../../../data')
__usechar__ = string.hexdigits
__maxtry__  = 128                                                  # noqa: E221

json_dumps = json.JSONEncoder(sort_keys=True, separators=(',', ':')).encode
json_loads = json.JSONDecoder().decode


def slug_checkpath(slug):
    # server file protection: cannot access private static files
    slug = pathlib.Path(slug).absolute().name
    return slug, __filedir__.joinpath(slug)


def slug_notename(slug):
    return __filedir__.joinpath(slug, 'index.txt')


def slug_fixpath(slug):
    # TODO: fix file directory
    shutil.rmtree(str(__filedir__.joinpath(slug)))
    raise bottle.HTTPError(500, 'Broken files structure. Note deleted.')


@sticky.post('/edit/<slug>')
def note_edit(slug):
    # TODO: check editing permission
    slug, path = slug_checkpath(slug)
    filename = slug_notename(slug)
    info = {
        'title': bottle.request.POST.get('title', ''),
        'text':  bottle.request.POST.get('text', ''),
        'ctime': bottle.request.POST.get('time', time.time()),
        # 'user' = bottle.request.get_cookies('username')
    }
    if not path.exists():
        os.makedirs(path)
        info.update({
            'slug': slug,             # note ID
            'create': info['ctime'],  # create time
            'url': 'view/' + slug,    # used to view note
            'title': info['title'] or 'Note %d (created at %s)' % (
                len(list(__filedir__.iterdir())),
                time.strftime('%Y.%m.%d')
            )
        })
    elif not filename.exists():
        slug_fixpath()
    else:
        with open(filename, 'r') as f:
            tmp, info = info, json_loads(f.read())
            info.update(tmp)
    with open(filename, 'w') as f:
        f.write(json_dumps(info))


@sticky.get('/view/<slug>')
@bottle.view('noteview.html', template_lookup=[__statics__])
def note_view(slug):
    slug, path = slug_checkpath(slug)
    if not path.exists():
        return bottle.HTTPError(404, 'Notes not found.')
    filename = slug_notename(slug)
    if not filename.exists():
        slug_fixpath(slug)
    with open(filename, 'r') as f:
        info = json_loads(f.read())
        info['ts'] = time.strftime(
            '%Y-%m-%d %H:%M:%S',
            time.localtime(info['ctime'])
        )
        return info  # TODO: hide sensitive information


@sticky.get('/delete/<slug>')
def note_delete(slug):
    _, path = slug_checkpath(slug)
    if path.exists():
        shutil.rmtree(str(path))


@sticky.route('/list')
def app_list_notes():
    notes = []
    for slug in __filedir__.iterdir():
        filename = slug_notename(slug)
        if not filename.exists():
            try:
                slug_fixpath(slug)
            except Exception:
                continue
        with open(filename, 'r') as f:
            notes.append(json_loads(f.read()))
    return {'notes': sorted(notes, key=lambda n: n['create'])}


@sticky.route('/clear')
def app_clear_notes():
    for slug in __filedir__.iterdir():
        shutil.rmtree(str(__filedir__.joinpath(slug)))


@sticky.route('/generate')
def app_generate_slug(chars=string.hexdigits, length=8):
    for i in range(__maxtry__):
        slug = ''.join([random.choice(chars) for j in range(length)])
        if not __filedir__.joinpath(slug).exists():
            return slug
    return bottle.HTTPError(403, 'No space for new contents.')


@sticky.route('/')  # bottle.redirect('/dashboard')
@sticky.route('/dashboard')
@bottle.view('manager.html', template_lookup=[__statics__])
def app_root():
    return app_list_notes()


@sticky.get('/<filename:path>')
def app_static_files(filename):
    return bottle.static_file(filename, __statics__)


application = sticky


def main(args=sys.argv[1:]):
    # create directory to store notes
    if not os.path.exists(__filedir__):
        os.makedirs(__filedir__)
    bottle.run(application, port=1234, debug=True)


# THE END
