# -*- coding:uft-8 -*-

import hashlib
import web
import time
import os


class XeibofunsInterface(object):
    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        i = web.input()
        signature = i.signature
        timestamp = i.timestamp
        nonce = i.nonce
        echostr = i.echostr

        appsercret=''
        list = [appsercret, timestamp, nonce]
        list.sort()
        sha1 = hashlib.sha1()
        map(sha1.update, list)
        hashcode = sha1.hexdigest()

        if hashcode == signature:
            return echostr


