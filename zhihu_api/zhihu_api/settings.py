#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path

# 分页时每页的条目数
NAVNUM = 10

settings = dict(
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        static_path=os.path.join(os.path.dirname(__file__), "static"),
        cookie_secret="e446976943b4e8442f099fed1f3fea28462d5832f483a0ed9a3d5d3859f==78d",
        session_secret="3cdcb1f00803b6e78ab50b466a40b9977db396840c28307f428b25e2277f1bcc",
        session_timeout=60,
        store_options={
                'redis_host': 'localhost',
                'redis_port': 6379,
                'redis_pass': ''
        },

        )

#数据库设置
db = {
    "host": 'localhost',
    "db": 'zhihuiuser',
    "port": '3306',
    "user": 'root',
    "password": '',
}
