# -*- coding:utf-8 -*-

import os.path
import random

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)


# 应用定义了两个请求处理类IndexHandler和MungedPageHandler,IndexHandler类简单渲染了index.html中的模板,之中包括一个允许用户POST一个
# 源文本在(source域中)和一个替换文本(在change域中)到/poem的表单
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


# MungedPageHandeler类用于处理/poem的POST请求.当一个请求到达时,它对传入的数据进行一些基本的处理,然后为浏览器渲染模板.
class MungedPageHandler(tornado.web.RequestHandler):
    def map_by_first_letter(self, text):  # 将传入的文本(从source域)分割成单词,然后创建一个字典,其中每个字母表中的字母对应文本中所有
        # 以其开头的单词(我们将其放入一个叫做source_map的变量).再把这个字典和用户在替代文本(表单的change域)中指定的内容一起传给模板munged.html
        mapped = dict()
        for line in text.split('\r\n'):  # 文本段里面取行
            for word in [x for x in line.split(' ') if len(x) > 0]:  # 文本行里面取单词
                if word[0] not in mapped: mapped[word[0]] = []  # 如果单词的首字母没有添加到字典,将此首字母添加到字典索引中
                mapped[word[0]].append(word)  # 给新的字典索引添加单词

        return mapped

    # 将各个参数和模板munged.html渲染成响应的页面
    def post(self):
        source_text = self.get_argument('source')
        text_to_change = self.get_argument('change')
        source_map = self.map_by_first_letter(source_text)  # 得到索引字典
        change_lines = text_to_change.split('\r\n')
        self.render('munged.html', source_map=source_map, change_lines=change_lines,
                    choice=random.choice)
        # random.choice 以一个列表作为输入,返回列表中的任一元素


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(
            handlers=[(r'/', IndexHandler), (r'/poem', MungedPageHandler)],
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),  # static_path参数指定了应用程序放置的静态资源
            debug=True  # 调用了一个便利的测试模式:tornado.autoreload模块, 一旦主要的python文件被修改,Tornado将会尝试重启服务器,
            # 并在模板改变时进行刷新
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
