# -*- coding -*-
from zhihu_spider import url_manager


class SpiderMain(object):

    def __init__(self):

        self.urls = url_manager.Urlmanager()
        self.dowloader = html_dowloader.HtmlDowloader()
        self.parser = html_parser.HtmlParser()
        self.output = html_output.HtmlOutput()


    def craw(self, root_url):
        count = 1