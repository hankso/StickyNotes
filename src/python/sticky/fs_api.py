#!/usr/bin/env python
# coding=utf-8
#
# File: StickyNotes/src/python/sticky/fs_api.py
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
import json
import time
import random
import shutil
import os.path as op

import bottle

from .configs import CONFIG

json_dumps = json.JSONEncoder(sort_keys=True, separators=(',', ':')).encode
json_loads = json.JSONDecoder().decode


def slug_info(slug):
    # server file protection: cannot access private static files
    slug = slug.split('/')[-1]
    path = op.join(CONFIG.storage, slug)
    note = op.join(path, 'index.txt')
    return slug, path, note


def slug_fixpath(path):
    # TODO: fix file directory
    if op.isdir(path):
        slug = op.basename(path)
    else:
        slug, path, _ = slug_info(path)
    shutil.rmtree(path)
    raise bottle.HTTPError(
        500, 'Broken files structure. Note %s deleted.' % slug)


def note_edit(slug):
    # TODO: check editing permission
    slug, path, filename = slug_info(slug)
    info = {
        'title':   bottle.request.params.getunicode('title', u''),
        'content': bottle.request.params.getunicode('content', u''),
        'mtime':   bottle.request.params.get('mtime', time.time(), type=int),
        # 'user' = bottle.request.get_cookies('username')
    }
    if not op.exists(path):
        os.makedirs(path)
        info.update({
            'slug':  slug,           # note id
            'atime': info['mtime'],  # access time
            'title': info['title'] or u'Note %d (created at %s)' % (
                len(os.listdir(CONFIG.storage)), time.strftime('%Y.%m.%d')
            )
        })
    elif not op.exists(filename):
        slug_fixpath(path)
    else:
        with open(filename, 'r') as f:
            tmp, info = info, json_loads(f.read())
            info.update(tmp)
    with open(filename, 'w') as f:
        f.write(json_dumps(info))


def note_delete(slug):
    path = slug_info(slug)[1]
    if op.exists(path):
        shutil.rmtree(path)


def app_generate_slug():
    usechar = bottle.request.params.get('usechar', CONFIG.usechar)
    sluglen = bottle.request.params.get('sluglen', CONFIG.sluglen, type=int)
    for i in range(CONFIG.maxtry):
        slug = ''.join([random.choice(usechar) for _ in range(sluglen)])
        slug, path, _ = slug_info(slug)
        if not op.exists(path):
            return slug
    return bottle.HTTPError(403, 'No space for new contents.')


def app_list_notes(slug=None, sort='atime'):
    _slug = bottle.request.params.get('slug', slug)
    _sort = bottle.request.params.get('sort', sort)

    notes = []
    for slug in os.listdir(CONFIG.storage) if _slug is None else [_slug]:
        slug, path, filename = slug_info(slug)
        if not op.exists(path):
            raise bottle.HTTPError(404, 'Note not found.')
        if not op.exists(filename):
            slug_fixpath(path)
        with open(filename, 'r') as f:
            info = json_loads(f.read())
        # TODO: check permission to get full info
        notes.append(info)

    try:
        notes = sorted(notes, key=lambda n: n[_sort])
    except KeyError:
        pass
    return {'notes': notes} if _slug is None else notes[0]


def app_clear_data(slug=None):
    slug = bottle.request.params.get('slug', slug)
    if slug is not None:
        return note_delete(slug)
    for slug in os.listdir(CONFIG.storage):
        shutil.rmtree(op.join(CONFIG.storage, slug))


def app_prepare(*a):
    # Create files directory to store data
    if not op.exists(CONFIG.storage):
        os.makedirs(CONFIG.storage)


API = {
    'backend':     'fs',
    'note_view':   app_list_notes,
    'note_edit':   note_edit,
    'note_delete': note_delete,
    'app_new':     app_generate_slug,
    'app_list':    app_list_notes,
    'app_clear':   app_clear_data,
    'app_init':    app_prepare,
}

# THE END
