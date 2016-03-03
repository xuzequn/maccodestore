# coding=utf-8
import tornado.httpserver
import tornado.options
import tornado.ioloop
import tornado.web
import tornado.httpclient

import urllib
import json
import datetime
import time

from oauth import oauth

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)


# Tornado默认在还书处理返回是关闭客户端的链接.但是当我们处理一个需要会跳函数的异步请求是,我们需要链接保持开启状态直到回调函数执行完毕.
class IndexHandler(tornado.web.RequestHandler):
    # 你可以在你想改变其行为的方法(也就是进行异步请求的函数)上面使用@tornado.web.asynchronous装饰器
    # 装饰器告诉tornado保持连接开启,Tornado不会自己关闭连接,必须用finish方法显示的告诉Tornado关闭连接
    @tornado.web.asynchronous
    def get(self):
        query = set.get_argument('q')
        client = tornado.httpclient.AsyncHTTPClient()
        url = "https://api.twitter.com/1.1/search/tweets.json?" + \
              urllib.urlencode({"q": query, "result_type": "recent", "rpp": 100})
        client.fetch(url, headers={'Authorization': oauth(url)}, callback=self.on_response)

    def on_response(self, response):
        body = json.loads(response.body)
        result_count = len(body["statuses"])
        now = datetime.datetime.utcnow()
        raw_oldest_tweet_at = body['statuses'][-1]['created_at']
        oldest_tweet_at = datetime.datetime.strptime(raw_oldest_tweet_at,
                                                     "%a %b %d %H:%M:%S +0000 %Y")
        second_diff = time.mktime(now.timetuple()) - \
                      time.mktime(oldest_tweet_at.timetuple())
        tweers_per_second = float(result_count) / second_diff
        self.write('''
        <div style="text-align":center">
    <div style="font-size: 72px">%s</div>
    <div style="font-size: 144px">%.02f</div>
    <div style="font-size: 244px">tweets per second<div>
                </div> '''
                   % (self.get_argument('q'), tweers_per_second)
                   )
        self.finish()  # 关闭装饰器开启的持续连接


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
