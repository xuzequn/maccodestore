# -*- coding:utf-8 -*-

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.httpclient

import urllib
import json
import datetime
import time



from tornado.options import define, options
define("port", default=8000, help="run on the given port", type=int)

from oauth import oauth

#  本Handler类的功能是从查询字符串中抓去参数q,然后用它执行一个到Twtter搜索的API的请求.
class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        query = self.get_argument('q')
        client = tornado.httpclient.HTTPClient()  # 实例化一个httpclient类,
        url = "https://api.twitter.com/1.1/search/tweets.json?" + \
				urllib.urlencode({"q": query, "result_type": "recent", "rpp": 100})
        response = client.fetch(url, headers={'Authorization': oauth(url)})
        # 调用结果对象的fetch方法使用要获取的url作为参数,rpp参数指定我们想获取搜索结果首页的100个推文,
        # 而result_type参数指定我么你想获取匹配搜索的最近推文,fetch方法会返回一个HTTPResponse对象,其中body为从远端URL获取的任何数据,
        # Twitter将返回一个json格式的结果,所以我们可以使用python的json模块来从结果中创建一个python数据结构.
        body = json.loads(response.body)
        result_count = len(body["statuses"])
        now = datetime.datetime.utcnow()
        raw_oldest_tweet_at = body['statuses'][-1]['created_at']
        oldest_tweet_at = datetime.datetime.strptime(raw_oldest_tweet_at,
                                                     "%a %b %d %H:%M:%S +0000 %Y")
        second_diff = time.mktime(now.timetuple()) - \
                      time.mktime(oldest_tweet_at.timetuple())
        tweet_per_second = float(result_count) / second_diff
        self.write("""
<div style="text-align":center">
    <div style="font-size: 72px">%s</div>
    <div style="font-size: 144px">%.02f</div>
    <div style="font-size: 244px">tweets per second<div>
                </div>
        """ % (query, tweet_per_second,))

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = tornado.web.Application(handlers=[(r"/", IndexHandler)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
