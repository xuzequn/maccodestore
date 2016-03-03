# -*- coding:utf-8 -*-
# 创建一个定义继承Tornado的RequestHandler类,在给定的端口监听请求,并在根目录("/")响应请求

# 必须的四个模块在这个例子中
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

#
from tornado.options import define, options  # 从命令行中读取设置,这个模块指定我们的应用监听端口
define("port", default=8000, help="run on given port", type=int)  # define语句中设置的命令被给出,则将成为全局options的属性
# port作为options.port的参数来访问程序,--help执行help的制定文本,type参数进行基本参数类型验证

# Tornado请求处理函数类,定义了一个get方法,这个处理函数将对HTTP的GET请求做出响应
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        greeting = self.get_argument('greeting', 'Hello')  # RequestHandler类的内建方法,从第一个查询字符串中取得参数的值给
        # greeting,若没有使用第二个参数的默认值
        self.write(greeting + ', friendly user!')  # RequestHandler类的write内建方法,以第一个字符串为函数的参数,并写入HTTP响应中.


if __name__ == "__main__":
    tornado.options.parse_command_line()  # 调用options模块来解析命令行,
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])  # 在元组中使用正则表达式来匹配HTTP请求路径
    # 创建Application实例.传递给Application类__init__的参数Handler,通过参数来指定哪个类响应请求.
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
    # 一但Application对象被创建,我们将其传递给HTTPServer对象,使用我们在命令行指定的端口进行监听.程序准备好接受请求后我们创建IOLoop实例
