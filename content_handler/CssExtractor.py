from exception import IllegalArgumentException


# css解析器
class CssExtractor:

    def __init__(self, urls=None, nodes=None):
        """
        :param urls: link的
        :param nodes: style节点
        """
        if self.urls is None and self.node is None:
            raise IllegalArgumentException("css提取器至少要urls或node其中之一")
        if isinstance(urls, str):
            urls = [urls]
        self.urls = urls
        self.nodes = nodes
        self.css_list = []
        # 解析
        self.__parse()

    def parse_urls(self, urls):
        pass

    def parse_node(self, node):
        pass

    def __parse(self):
        """
        解析
        :return:
        """
        self.url_results = self.parse_urls(self.urls)
        self.node_results = self.parse_node(self.nodes)

    def get_style(self, query):
        pass
