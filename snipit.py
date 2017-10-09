#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright © 2013 Karim S.
# This work is free. You can redistribute it and/or modify it under the
# terms of the Do What The Fuck You Want To Public License, Version 2,
# as published by Sam Hocevar. See the COPYING file for more details.

import os
import tempfile
from datetime import datetime

import tornado.web
import tornado.options
import tornado.template

from tornado.options import define, options
define("path", default='snippets', help="Specifies where to store snippets")
define("port", default=8888, help="run on the given port", type=int)

# Store brush name and displayable name
LANGUAGES = {"shell": "Bash", "cpp": "C/C++", "csharp": "C#", "css": "CSS",
             "diff": "Diff", "edi": "Edifact", "java": "Java", "js": "Javascript",
             "perl": "Perl", "php": "PHP", "plain": "Plain", "py": "Python",
             "rb": "Ruby", "sql": "SQL", "xml": "XML"}

PASTES_DIR = "/gctmp/ksenhaji/Snippets"


class MainHandler(tornado.web.RequestHandler):
    ''' Handler for the form (index page) '''

    def create_snippet(self, language, text):
        ''' Writes snippet to disk, returns filename '''
        prefix = datetime.today().date().isoformat() + "_" + language + "_"
        paste_dir = self.settings["snippets_path"]
        fd, path = tempfile.mkstemp(dir=paste_dir, text=True, prefix=prefix)
        with os.fdopen(fd, 'w') as f:
            f.write(text.encode('utf-8'))
        return os.path.basename(path)

    def get(self):
        ''' Form page '''
        self.render("templates/form.html", languages=LANGUAGES.iteritems())

    def post(self):
        ''' Saves Paste to a file and sends result to client '''
        language = self.get_argument("language")
        snippet = self.create_snippet(language, self.get_argument("text"))
        target_url = '/{0}/{1}'.format(snippet, language)

        if "application/json" in self.request.headers.get("Accept", ""):
            self.write({"code": 201, "message": "Created", "data": target_url})
        else:
            self.redirect(target_url)


class PasteHandler(tornado.web.RequestHandler):
    ''' Handler for loading already saved paseds '''
    def get(self, paste_id, language="plain"):
        snip_path = os.path.join(self.settings["snippets_path"], paste_id)
        if not os.path.exists(snip_path):
            raise tornado.web.HTTPError(404)
        with open(snip_path) as f:
            snippet = f.read()
        self.render("templates/paste.html", lang=language, snippet=snippet)


def start_server():
    application = tornado.web.Application([
        (r"/", MainHandler),
        (r"/([^/]+)", PasteHandler),
        (r"/([^/]+)/([a-z]+)", PasteHandler),
    ], static_path="static", debug=True)

    if not os.path.exists(options.path):
        os.mkdir(options.path)

    application.settings["snippets_path"] = options.path
    application.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    start_server()
