# -*- coding:utf-8 -*-

from datetime import date

import os.path

import tornado.escape
import tornado.ioloop
import tornado.web


class MainPage(tornado.web.RequestHandler):
    def get(self):
        items = ["item 1", "item 2", "item 3"]
        self.render("app1.html", title="My title", items=items)


class VersionHandler(tornado.web.RequestHandler):
    def get(self):
        reponse = {'version': '3.5.1',
                   'last_build': date.today().isoformat()}
        self.write(reponse)


class GetGameByHandler(tornado.web.RequestHandler):
    def get(self, id):
        response = {'id': int(id),
                    'name': 'Crazy Game',
                    'release_date': date.today().isoformat()}
        self.write(response)


application = tornado.web.Application([
    (r"/getgamebyid/([0-9]+)", GetGameByHandler),
    (r"/version", VersionHandler),
    (r"/mainpage", MainPage),
], template_path=os.path.join(os.path.dirname(__file__), "templates")
)


if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
