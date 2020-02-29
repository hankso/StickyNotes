#!/usr/bin/env python
# coding=utf-8
#
# File: StickyNotes/src/python/sticky/__init__.py
# Author: Hankso
# Webpage: https://github.com/hankso
# Time: Thu 20 Feb 2020 03:20:18 PM CST

'''

Configuration
-------------
This program automatically loads configuration files from::

    asdf

Note
----
Template is not used to render webpage, because Python is not the
only distribution in this project. C based server or GitHub Pages
(which provides pure static file hosting) may be used in backend.
'''

# built-ins
import sys
import argparse

# requirements.txt: network: bottle
# requirements.txt: optional: bottle_sqlite
import bottle

from .configs import CONFIG

try:                                 # Check if we have bottle_sqlite installed
    assert CONFIG.backend == 'db'
    import bottle.ext.sqlite
except Exception:                    # No. Use disk files backend
    from .fs_api import API
    print('Using FS backend')
else:                                # Yes. Then use database backend
    from .db_api import API
    print('Using DB backend')


def make_app():
    global application  # provide WSGI Application for Servers like Apache
    app = application = bottle.Bottle()

    API['app_init'](app)

    @app.route('/')
    def app_redirect():
        bottle.redirect('index.html')

    app.route('/note/<slug>', 'GET',        API['note_view'])      # noqa: F405
    app.route('/note/<slug>', 'POST',       API['note_edit'])      # noqa: F405
    app.route('/note/<slug>', 'DELETE',     API['note_delete'])    # noqa: F405

    app.route('/new',   ['GET', 'PUT'],     API['app_new'])        # noqa: F405
    app.route('/list',   'GET',             API['app_list'])       # noqa: F405
    app.route('/clear', ['GET', 'DELETE'],  API['app_clear'])      # noqa: F405

    @app.route('/<filename:path>')
    def app_static_files(filename):
        return bottle.static_file(filename, CONFIG.statics)

    return app


def make_parser():
    parser = argparse.ArgumentParser(prog=__name__, description=(
        'StickyNotes Python Server entry script. Default listen on ' +
        'http://{}:{}').format(CONFIG.host, CONFIG.port))
    parser.add_argument(
        '-H', '--host', default=CONFIG.host, type=str, help='listen address')
    parser.add_argument(
        '-P', '--port', default=CONFIG.port, type=int, help='port number')
    parser.add_argument(
        '-D', '--debug', default=int(CONFIG.debug),
        action='count', help='supply to enable debug mode')
    return parser


def main(args=sys.argv[1:]):
    args = make_parser().parse_args(args)

    for k, v in vars(args).items():
        if hasattr(CONFIG, k):
            setattr(CONFIG, k, v)

    bottle.run(
        app=make_app(),
        host=CONFIG.host,
        port=CONFIG.port,
        debug=bool(CONFIG.debug),
    )


# THE END
