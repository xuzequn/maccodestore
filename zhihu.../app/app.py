# -*- coding:utf-8 -*-
from uuid import uuid4

import os
import sys
import json
import tornado.web
import tornado.ioloop
import tornado.options
import tornado.httpserver
import tornado.gen as gen
import tornado.httpclient as httpclient
from settings import settings, NAVNUM
from code import DBload
from base import BaseHandler
from session import *
import session
from uuid import uuid4
import time

reload(sys)
sys.setdefaultencoding('utf-8')

from tornado.web import HTTPError


# 逻辑类

class Poj_logic(object):
    format = '%Y-%m-%d %H:%M:%S'

    def check(self, name, password):
        self.DBload = DBload()
        user = dict()
        try:
            user = self.DBload.selectuserinfo(self.DBload.session, name, password)
            return 1, user
        except Exception, e:
            return 0, user

    def model(self):
        news_list = []
        user_info = dict()

    def getuseraction(self, id, pageid):
        self.DBload = DBload()
        useract = []
        try:
            count, useract = self.DBload.selectuseract(self.DBload.session, id, pageid)
            return 1, count, useract
        except Exception, e:
            return 0, useract

    def timetran(value):
        value = time.localtime(value)
        dt = time.strftime(format, value)
        return dt

    def sorted(d):
        pass


# 登陆
class LoginHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("login.html")

    def post(self):
        name = self.get_argument('username')
        password = self.get_argument('password')
        # 验证密码
        res, userinfo = self.application.Poj_logic.check(name, password)

        if res == 1:
            '''
            self.session = session.Session(self.application.session_manager,self)
            self.session['username'] = userinfo['username']
            self.session['user_id'] = userinfo['user_id']
            self.session.save()
            '''
            self.redirect("/newsinfo/1")
        else:
            pass


# 最新动态页 (分页)
class LoadHandler(tornado.web.RequestHandler):
    def get(self, pageid):
        # username = self.session['username']
        pageid = int(pageid)
        print pageid
        res, count, useract = self.application.Poj_logic.getuseraction(1, pageid)
        pagenum = (count - 1) / NAVNUM + 1
        if res == 1:
            # result = json.dumps(list(useract))
            # self.render("newslist.html", content=result, page=pagenum)
            '''
            for i in useract:
                s = json.loads(json.dumps(i))
                if s['user_action_show'] == 1:
                    self.write(i)
            '''
            for i in useract:
                del i['user_action_show']
                self.write(i)
        print 'XXXXXXXXX'

    def post(self, pageid):
        id = 1
        offset = int(pageid)
        if offset != 1:
            offset = (int(pageid) - 1) * NAVNUM
        print offset
        res, count, useract = self.application.Poj_logic.getuseraction(id, offset)
        pagenum = (count - 1) / NAVNUM + 1
        if res == 1:
            # result = json.dumps(list(useract))
            self.render("newslist.html", content=useract, page=pagenum)
        print 'XXXXXXXXX'


# 长轮询
class MainHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    def get(self):
        pass


# 匿名操作
class Dename(tornado.web.RequestHandler):
    pass


class Application(tornado.web.Application):
    def __init__(self):
        self.Poj_logic = Poj_logic()
        Handlers = [
            (r'/', LoginHandler),
            (r'/newsinfo/(\d+)', LoadHandler),
            (r'/newsinfo/comet', MainHandler),
            (r'/newsinfo/dename', Dename),
        ]
        settings

        tornado.web.Application.__init__(self, Handlers, **settings)
        self.session_manager = session.SessionManager(settings['session_secret'],
                                                      settings['store_options'],
                                                      settings['session_timeout'])

if __name__ == "__main__":
    tornado.options.parse_command_line()

    app = Application()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(8000)
    tornado.ioloop.IOLoop.instance().start()
