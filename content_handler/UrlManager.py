import abc


class UrlManager(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def add_url(self, url, tag):
        """
        添加一个待爬取的url，若url已经存在，则忽略
        :param url
        :param tag url标签
        :return: None
        """
        pass

    @abc.abstractmethod
    def pop_url(self):
        """
        获取一个待爬取的url
        :return: (url,tag)
        """
        pass

    def add_urls(self, urls):
        if urls and len(urls) > 0:
            for url in urls:
                self.add_url(*url)


    @abc.abstractmethod
    def has_next(self):
        pass
