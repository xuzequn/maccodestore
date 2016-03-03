# -*- coding:utf-8 -*-
from code import DBload

DBload = DBload()
act = DBload.selectuseract(DBload.session,'1')
for x in act:
    print x
try:
    user = DBload.selectuserinfo(DBload.session, 'yanwei', password='123')
    print type(user)
    print user
except Exception, e:
    print "账号密码错误"

