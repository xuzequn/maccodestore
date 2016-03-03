# -*- coding:utf-8 -*-

import tornado.ioloop as ioloop
import tornado.httpclient as httpclient
import time


start = time.time()
step = 3


def handler_request(reponse):
    global step
    if reponse.error:
        print 'ERROR', reponse.error
    else:
        print reponse.body

    step -= 1
    if not step:
        finish()


def finish():
    global start
    end = time.time()
    print '一共用了 Used %0.2f secend(s)' %float(end-start)
    ioloop.IOLoop.instance().stop()

http_client = httpclient.AsyncHTTPClient()
http_client.fetch("http://www.baidu.com", handler_request)
http_client.fetch("http://www.baidu.com", handler_request)
http_client.fetch("http://www.baidu.com", handler_request)
ioloop.IOLoop.instance().start()
