# -*- coding:utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import pymongo

from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

from pymongo import MongoClient

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/(\w+)", WordHandler)]
        conn = MongoClient("localhost", 27017)
        self.db = conn["example"]
        tornado.web.Application.__init__(self, handlers, debug=True)


class WordHandler(tornado.web.RequestHandler):
    def get(self, word):
        coll = self.application.db.words
        word_doc = coll.find_one({"word": word})
        if word_doc:
            del word_doc["_id"]
            print word_doc
            self.write(word_doc)
        else:
            self.set_status(404)
            self.write({"error": "word not found"})


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

