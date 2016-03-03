# coding=utf-8
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os.path

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)


#  自定义了一个Application子类,在自定义的__init__方法中我们创建了处理列表以及一个设置的字典,然后在初始化子类的调用中传递这些值
#  在这个系统中,可以很容易的该表index的页面并保持基础模板在其他页面使用时的完好
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", MainHandler),
        ]
        settings = dict(
                template_path=os.path.join(os.path.dirname(__file__), "templates"),
                static_path=os.path.join(os.path.dirname(__file__), "static"),
                debug=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
                "index.html",
                page_title="Burt's Books | Home",
                header_text="Welcome to Burt's Books!",
        )


if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
