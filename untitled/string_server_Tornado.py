import textwrap

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)


class ReverseHandler(tornado.web.RequestHandler):
    def get(self, input):
        self.write(input[::-1])


class WrapHandler(tornado.web.RequestHandler):
    def post(self):
        text = self.get_argument('text')  # 获取要求查询字符串的参数
        width = self.get_argument('width', 40)
        self.write(textwrap.fill(text, int(width)))


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
            handlers={
                (r"/reverse/(\w+)", ReverseHandler),  # 正则表达式告诉Tornado匹配任何字符串/reverse/开始并跟着一个或多个字母的路径
                (r"/wrap", WrapHandler)
            }
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
