# -*- coding:utf-8 -*-
import re
import urlparse
import urllib2
import os.path
import MySQLdb

from bs4 import BeautifulSoup

class DB(object):

    def __init__(self):
        print("连上了")
        # cnx = mysql.connector..connect(user='root', password='', host='localhost', database='zhihuiuser')
        print("连上了")

    def conn(self):
        pass

if __name__ == "__main__":

    # response = urllib2.urlopen("http://www.zhihu.com/people/xu-ze-qun")

    user_id_web = 2;
    response = open('徐泽群 - 知乎_all副本.html', 'r')
    html_cont = response.read()
    soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
    content_act_set = dict()
    content_act = soup.find_all("div", class_="zm-profile-section-item zm-item clearfix")
    for content_act_peo in content_act:
        data_time = content_act_peo['data-time']
        data_type_detail = content_act_peo["data-type-detail"]

        if data_type_detail == 'member_follow_topic':       # 关注话题
            content_act_a = content_act_peo.find("a", class_="topic-link")
            act_no = 4
            data_obj_href = int(str(content_act_a['href'])[-8:])
        elif data_type_detail == 'member_voteup_answer':     # 赞同
            content_act_a = content_act_peo.find("a", class_="question_link")
            act_no = 3
            data_obj_href = int(str(content_act_a['href'])[-8:])
        elif data_type_detail == 'member_follow_question':   # 关注问题
            content_act_a = content_act_peo.find('a', class_="question_link")
            act_no = 5
            data_obj_href = int(str(content_act_a['href'])[-8:])
        elif data_type_detail == 'member_answer_question':    # 回答
            content_act_a = content_act_peo.find('a', class_="question_link")
            act_no = 2
            data_obj_href = int(str(content_act_a['href'])[-24:-16])
        elif data_type_detail == 'member_ask_question':      # 提问
            content_act_a = content_act_peo.find('a', class_="question_link")
            act_no = 1
            data_obj_href = int(str(content_act_a['href'])[-8:])
        elif data_type_detail == 'member_follow_column':     # 关注专栏
            content_act_a = content_act_peo.find('a', class_="question_link")
            act_no = 6
            data_obj_href = 33060708
        elif data_type_detail == 'member_create_article':   # 发表文章
            content_act_a = content_act_peo.find('a', class_="post-link")
            act_no = 7
            data_obj_href = int(str(content_act_a['href'])[-8])
        # content_act_a = content_act_peo.find("a", class_="zg-link")
        # data_peo_name = content_act_a.get_text()
        print data_time, ' ', act_no, ' ',data_obj_href
        cnx = MySQLdb.connect(host='localhost', user='root', passwd='', db='zhihuiuser')
        user = cnx.cursor()
        insert_userinfo = "insert into zhihuiuser.useract (user_id,user_action,user_action_obj,user_action_time)  VALUES(%s,%s,%s,%s)" \
                          % (str(user_id_web),str(act_no), str(data_obj_href), str(data_time))
        try:
             print user.execute(insert_userinfo)
             cnx.commit()
        except Exception, e:
            print e
        user.close()
        print "成功"







