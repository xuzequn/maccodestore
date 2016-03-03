# -*- coding:utf-8 -*-
import os.path
import tornado.locale
import tornado.httpserver
import tornado.options
import tornado.web
import tornado.ioloop

from tornado.options import define, options

define("port", default=8000, help="on the given port", type=int)

from pymongo import MongoClient


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
            (r"/recommended/", RecommendedHandler),
        ]
        settings = dict(
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                ui_modules={"Book": BookModule},
                debug=True,
        )
        conn = MongoClient("localhost", 27017)
        self.db = conn["bookstore"]
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
                "index.html",
                page_title="Burt's Book | Home",
                header_text="Welcome to Burt's Books!",
        )


class RecommendedHandler(tornado.web.RequestHandler):
    def get(self):
        coll = self.application.db.books
        books = coll.find()
        self.render(
                "recommended.html",
                page_title="Burt's Book | Recommended Reading",
                header_text="Recommended Reading",
                books=books
        )


class BookModule(tornado.web.UIModule):
    def render(self, book):
        return self.render_string(
                "modules/book.html",
                book=book,
        )

    def css_files(self):
        return "/static/css/recommended.css"

    def javascript_files(self):
        return "static/js/recommended.js"


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
