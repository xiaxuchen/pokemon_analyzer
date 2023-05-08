import abc
import os

import requests

"""
问题：每一个页面可能都不同，可能需要一些特殊的处理，所以可以抽象一下各种情况同时提供可扩展性
"""


class Downloader(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def download(self, url, **kwargs):
        """
        下载文档
        :param url: 路径
        :return: 文档数据
        """
        pass


"""
使用requests实现的下载器
"""


class SimpleRequestsHtmlDownloader(Downloader):

    def download(self, url, **kwargs):
        r = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0"
        })
        r.encoding = "UTF-8"
        if r.status_code == 200:
            return r.text
        # if not os.path.exists("html"):
        #     os.mkdir("html")
        # with open("html/main.html", mode="w+", encoding="utf8") as f:
        #     f.write()
