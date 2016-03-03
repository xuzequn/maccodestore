# -*- coding:utf-8 -*-

import tornado.httpserver
import tornado.web
import tornado.options
import tornado.ioloop
import tornado.httpclient
import tornado.gen


import urllib
import json
import datetime
import time


from tornado.options import define, options
define("port", default=8000, help="on the given port", type=int)

from oauth import oauth

class IndexHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.engine
    def get(self):
        query = self.get_argument('q')
        client = tornado.httpclient.AsyncHTTPClient()
        #   yield 和tornado.gen.Task 形成了一个新的生成器对Task函数迭代执行
        # yield的使用返回程序对Tornado的控制,允许在HTTP请求进行中执行其他任务.当HTTP请求完成式RequsetHandler方法在其停止的地方恢复.
        # 在请求处理程序中返回HTTP响应而不是回调还书中.
        url = "https://api.twitter.com/1.1/search/tweets.json?" + \
				urllib.urlencode({"q": query, "result_type": "recent", "rpp": 100}
        response = yield tornado.gen.Task(client.fetch,
                url, headers={'Authorization': oauth(url))
        body = json.loads(response.body)
        result_count = len(body["statuses"])
        now = datetime.datetime.utcnow()
        raw_oldest_tweet_at = body["results"][-1]['created_at']
        oldest_tweet_at = datetime.datetime.strptime(raw_oldest_tweet_at,
                "%a %b %d %H:%M:%S +0000 %Y")
        second_diff = time.mktime(now.timetuple() - \
                time.mktime(oldest_tweet_at.timetuple()))
        tweets_per_second = float(result_count) / second_diff
        self.write('''"%a %b %d %H:%M:%S +0000 %Y")
           <div style="text-align: center">
    <div style="font-size: 72px">%s</div>
    <div style="font-size: 144px">%.02f</div>
    <div style="font-size: 24px">tweets per second</div>
</div>
        ''' % (query, second_diff))
        self.finish()


if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application([(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


