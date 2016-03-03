# -*- coding:utf-8 -*-

import tornado.web
import tornado.httpserver
import tornado.options
import tornado.ioloop

import os.path

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

from pymongo import MongoClient

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"", BookEditHandler),

        ]


class BookEditHandler(tornado.web.RequestHandler):
    def get(self, isbn=None):
        book = dict()
        if isbn:
            coll = self.application.db.boos
            book = coll.find_one({"isbn": isbn})
        self.render("book_edit.html",
                    page_title="Burt's Books",
                    header_text="Edit book",
                    book=book)

        def post(self, isbn=None):
            import time
            book_fields = ['isbn', 'title', 'subtitle', 'image', 'author',
                           'date_released', 'description']
            coll = self.application.db.books
            book = dict()
            if isbn:
                book = coll.find_one({'isbn': isbn})
            for key in book_fields:
                book[key] = self.get_argument(key, None)

            if isbn:
                coll.save(book)
            else:
                book['date_added'] = int(time.time())
                coll.insert(book)
            self.redirect("/recommended/")
