# -*- coding:utf-8 -*-

# 第一步导入SQLAlchemy, 并初始化DBSession
# 导入

import json

from sqlalchemy import Column, String, create_engine, Integer, and_,  Column, desc, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from settings import db, NAVNUM

# 定义对象的基类
Base = declarative_base()


# 定义userinfo对象
class Userinfo(Base):
    # 表名
    __tablename__ = 'userinfo'

    # 表的结构
    id = Column(Integer, primary_key=True)
    user_id = Column(String(45))
    username = Column(String(45))
    password = Column(String(45))


class Useract(Base):
    __tablename__ = 'useract'

    id = Column(Integer, primary_key=True)
    user_id = Column(String(30))
    user_action = Column(String(30))
    user_action_obj = Column(String(30))
    user_action_time = Column(String(30))
    user_action_show = Column(Integer)


class DBload(object):
    def __init__(self):
        # 初始化数据库连接        数据库名+数据库驱动名称://用户名:密码@机器地址:端口号/数据库名
        engine = create_engine('mysql+pymysql://'+db['user']+':'+db['password']+'@' \
                               +db['host']+':'+db['port']+'/'+db['db'])

        # 创建DBSession
        DBSession = sessionmaker(bind=engine)
        self.session = DBSession()
        self.conn = engine.connect()
    def selectuseract(self, session, id, pageid):
        # action_list = session.query(Useract).filter(Useract.user_id == id).all()
        count = session.query(func.count("*")).filter(Useract.user_id == id).scalar()
        action_list = session.query(Useract).filter(and_(Useract.user_id.like(id), Useract.user_action_show.like(1)))\
            .order_by(desc(Useract.user_action_time)).limit(NAVNUM).offset(pageid)
        # action_list = conn.execute
        actionlist = []
        i = 0
        for action in action_list:
            action_json = dict()
            action_json['user_id'] = action.user_id
            action_json['user_action'] = action.user_action
            action_json['user_action_obj'] = action.user_action_obj
            action_json['user_action_time'] = action.user_action_time
            action_json['user_action_show'] = action.user_action_show
            actionlist.append(action_json)
            i += 1
        return count, actionlist

    def selectuserinfo(self, session, name, password):
        user = session.query(Userinfo).filter(and_(Userinfo.username.like(name), Userinfo.password.like(password))).one()
        if user:
            user_info = dict()
            user_info['user_id'] = user.user_id
            user_info['username'] = user.username
            user_info['password'] = user.password
            return user_info

    def sortedlist(self, session, id):
        query = session.query(Useract).filter(Useract.user_id.like(id)).order_by(desc(Useract.user_action_time))
        query.all()






