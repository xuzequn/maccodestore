# -*- coding:utf-8 -*-

import tornado.ioloop
import tornado.web
import json


class hello(tornado.web.RequestHandler):
    def get(self):
        self.write('hello')


class add(tornado.web.RequestHandler):
    def post(self):
        res = Add(json.loads(self.request.body))  # self.request.body 是请求的主体
        self.write(json.dumps(res))  # 加载json


def Add(input):  # input 是客户端请求的json数据,是一个将请求数据以json格式加载的数据
    print input
    sum = input['num1'] + input['num2']
    result = {}
    result['sum'] = sum
    return result


application = tornado.web.Application([
    (r"/", hello),
    (r"/add", add),
])


if __name__ == '__main__':
    application.listen(8888)
    tornado.ioloop.IOLoop.instance().start()
