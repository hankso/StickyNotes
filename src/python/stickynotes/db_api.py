#!/usr/bin/env python
# coding=utf-8
#
# File: StickyNotes/src/python/sticky/db_api.py
# Author: Hankso
# Webpage: https://github.com/hankso
# Time: Thu 20 Feb 2020 09:15:02 PM CST

'''__doc__'''

import time
import random
import sqlite3
import os.path as op

import bottle
import bottle.ext.sqlite

from .configs import CONFIG


def db_has(db, slug):
    c = db.execute('SELECT * FROM notes WHERE slug=?', (slug, ))
    return bool(c.fetchall())


def note_edit(db, slug):
    # TODO: check editing permission
    info = {
        'title':   bottle.request.params.getunicode('title', u''),
        'content': bottle.request.params.getunicode('content', u''),
        'mtime':   bottle.request.params.get('mtime', time.time(), type=int),
        # 'user' = bottle.request.get_cookies('username')
    }
    if not db_has(db, slug):
        info.update({
            'slug':  slug,           # note id
            'atime': info['mtime'],  # access time
            'title': info['title'] or u'Note %d (created at %s)' % (
                len(app_list_notes(db, col='slug', sort=None)),
                time.strftime('%Y.%m.%d')
            )
        })
        db.execute('INSERT INTO notes ({}) VALUES ({})'.format(
            ','.join(info.keys()), ','.join(['?'] * len(info))
        ), tuple(info.values()))
    else:
        db.execute('UPDATE notes SET {} WHERE slug=?'.format(
            ','.join(['%s=?' % _ for _ in info.keys()])
        ), tuple(info.values()) + (slug, ))


def note_view(db, slug):
    if not db_has(db, slug):
        return bottle.HTTPError(404, 'Note not found.')
    info = app_list_notes(db, slug)
    return info


def note_delete(db, slug):
    db.execute('DELETE FROM notes WHERE slug=?', (slug, ))


def app_generate_slug(db):
    usechar = bottle.request.params.get('usechar', CONFIG.usechar)
    sluglen = bottle.request.params.get('sluglen', CONFIG.sluglen, type=int)
    for i in range(CONFIG.maxtry):
        slug = ''.join([random.choice(usechar) for _ in range(sluglen)])
        if not db_has(db, slug):
            return slug
    return bottle.HTTPError(403, 'No space for new contents.')


def app_list_notes(db, slug=None, col='*', sort='atime'):
    _slug = bottle.request.params.get('slug', slug)
    _sort = bottle.request.params.get('sort', sort)

    if _slug is not None:
        c = db.execute('SELECT %s FROM notes WHERE slug=?' % col, (_slug, ))
    elif _sort:
        if _sort != sort and _sort not in map(
            lambda c: c['name'],
            db.execute('PRAGMA table_info(notes)').fetchall()
        ):
            _sort = sort
        c = db.execute('SELECT %s FROM notes ORDER BY %s' % (col, _sort))
    else:
        c = db.execute('SELECT %s FROM notes' % col)
    # TODO: check permission to get full info
    notes = list(map(dict, c.fetchall()))
    return {'notes': notes} if _slug is None else notes[0]


def app_clear_data(db, slug=None):
    slug = bottle.request.params.get('slug', slug)
    if slug is not None:
        return note_delete(db, slug)
    db.execute('DELETE FROM notes')


def app_init(app, *a):
    '''register SQLite plugin for app context'''
    if not CONFIG.storage.endswith('.db'):
        CONFIG.storage += '.db'
    if not op.exists(CONFIG.storage):
        conn = sqlite3.connect(CONFIG.storage)
        conn.execute('CREATE TABLE notes (%s)' % ','.join([
            'slug    TEXT PRIMARY KEY',
            'user    TEXT',
            'title   TEXT',
            'content TEXT',
            'atime   INTEGER',  # We cannot os.stat a record to get access
            'mtime   INTEGER',  # time etc. So add them as a SQLite INTEGER.
        ]))
        conn.commit()
        conn.close()
    app.install(bottle.ext.sqlite.Plugin(dbfile=CONFIG.storage))


API = {
    'backend': 'db',
    'note_view': note_view,
    'note_edit': note_edit,
    'note_delete': note_delete,
    'app_new': app_generate_slug,
    'app_list': app_list_notes,
    'app_clear': app_clear_data,
    'app_init': app_init,
}

# THE END
