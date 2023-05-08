import re
from exception import IllegalArgumentException


class UrlHandler:

    def extract_url_path(self, url:str):
        """
        提取url的路径，去除参数、最后的/以及锚点
        :param url:
        :return:
        """
        if url is None:
            return None
        match = re.match(r'^(.*?)(\?|#|$)', url)
        if match:
            extracted_url = match.group(1)
            return extracted_url
        return None

    def handle_url(self, context_url:str, url):
        """
        处理相对路径
        :param context_url: 当前文档的url
        :param url: 目标url
        :return: 绝对url
        """
        # 去除尾部/
        context_url = self.extract_url_path(context_url)
        if context_url is None:
            raise IllegalArgumentException("当前url不能为空")
        if url is None:
            return None
        if url.startswith("http"):
            return url
        # 处理../与./
        while True:
            if url.startswith("./"):
                url = url[2:]
            elif url.startswith("../"):
                context_url = context_url[0:context_url.rindex("/")]
                url = url[3:]
            elif url.startswith("/"):
                return context_url + url
            else:
                return context_url + "/" + url

