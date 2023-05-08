import abc
import logging

import bs4
from bs4 import BeautifulSoup

from entity.extract.AttrType import AttrType
from entity.extract.Pokemon import Pokemon
import extract_const

"""
文档解析器
"""


class DocParser(metaclass=abc.ABCMeta):

    def __init__(self, context=None):
        self.context = context

    @abc.abstractmethod
    def handle_types(self):
        """
        处理的文档类型
        :return:
        """
        pass

    @abc.abstractmethod
    def parse(self, doc, url):
        """
        解析文档
        :param doc: html文档
        :param url: 当前文档路径
        :return: (文档的数据,需要添加的链接信息)
        """
        pass


"""
宝可梦图鉴列表的解析
"""


class PokemonListParser(DocParser):

    def __init__(self, context=None):
        super().__init__(context)

    def handle_types(self):
        return [extract_const.LINK_TYPE_POKEMON_BOOK]

    def acquire_spirit_img(self, node):
        """
        获取节点中精灵图中的图片地址
        :param node:
        :return: 图片路径
        """
        return ""

    def acquire_pokemon_list(self, soup: BeautifulSoup):
        # 宝可梦数据
        pokemons = []
        # 链接信息
        links = []
        # 1. 找到表格
        tables = soup.find_all("table", class_="roundy eplist bgl-帕底亚 bd-帕底亚")
        for table in tables:
            # 跳过表头
            tr_list = table.find_all("tr")[1:]
            # 解析tr
            for tr in tr_list:
                # 2. 将td转化为列表
                row = [td for td in tr.children if not isinstance(td, bs4.NavigableString)
                       and td.name == 'td']
                if len(row) and len(row) < 5:
                    logging.info(f"【解析html】row not fit the require len >= 5 row:{row}")
                # 3. 解析宝可梦的信息
                pokemon = Pokemon(local_num=int(row[0].text.strip()[1:]),
                                  global_num=int(row[1].text.strip()[1:]),
                                  name=row[3].a.text.strip(),
                                  attr_types=[att.a.text for att in row[4:] if
                                              "hide" not in att.get('class')],
                                  pic_url=self.acquire_spirit_img(row[2].a.span))
                # 4. 解析链接信息
                links.append((row[3].a.get("href"), extract_const.LINK_TYPE_POKEMON_DETAIL))
                pokemons.append(pokemon)
        return (extract_const.INFO_POKEMON_LIST, pokemons), links

    def parse(self, doc, url):
        # 只管文档解析
        return self.acquire_pokemon_list(doc)


"""
属性克制解析
"""


class AttrTypeParser(DocParser):

    def handle_types(self):
        return [extract_const.LINK_TYPE_ATTR_RELATION]

    def get_attr_type(self, node):
        span = node.find("span", class_="type-box-9-text")
        if not span:
            return None
        return span.text

    def get_rate(self, node):
        """
        获取倍率
        :param node:
        :return: 倍率的两倍的整数
        """
        class_ = node.get("class")
        if class_ is None:
            class_ = []
        else:
            class_ = set(class_)
        if "zero" in class_:
            return 0
        elif "half" in class_:
            return 1
        elif class_ is None or len(class_) == 0:
            return 2
        elif "double" in class_:
            return 4
        else:
            logging.error(f"extract rate error,format not fit require:{node}")

    def parse(self, doc, url):
        attrs = []
        # 属性表
        att_table = doc.find("table", class_="roundy hover at-c")
        # 获取所有行，跳过第一行
        trs = att_table.find_all("tr")
        trs = trs[1:len(trs) - 1]
        target_attrs = [self.get_attr_type(td) for td in trs[0].find_all("td")]
        for tr in trs[1:]:
            tds = tr.find_all("td")
            attr_type = self.get_attr_type(tds[0])
            if not attr_type:
                logging.warning(f"tr has error attr_type node,tr:{tr} td:{tds[0]}")
                continue
            for i, td in enumerate(tds[1:]):
                attrs.append(AttrType(attr_type=attr_type, attack_rate=self.get_rate(td), target_type=target_attrs[i]))
        return (extract_const.INFO_TYPE_ATTR, attrs), []
