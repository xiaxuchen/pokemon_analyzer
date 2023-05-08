import json
import logging
import re

import bs4
from bs4 import BeautifulSoup

from entity.extract.Pokemon import Pokemon

html_doc = ""
with open("html/main.html", mode="r", encoding="utf8") as f:
    html_doc = f.read()

soup = BeautifulSoup(html_doc, "html.parser", from_encoding="utf8")
# 获取节点的所有CSS样式信息
css_styles = {}
for tag in soup.find_all(True):
    css = tag.get('style', '').strip()
    if css:
        css_list = css.split(';')
        for item in css_list:
            if ':' in item:
                key, value = item.split(':', 1)
                css_styles.setdefault(tag.name, {})
                css_styles[tag.name][key.strip()] = value.strip()
print("节点的所有CSS样式信息：", css_styles.get('div', {}))


def acquire_spirit_img(node):
    """
    获取节点中精灵图中的图片地址
    :param node:
    :return:
    """
    return ""


def acquire_pokemon_list(soup: BeautifulSoup):
    pokemons = []
    # 找到表格
    tables = soup.find_all("table", class_="roundy eplist bgl-帕底亚 bd-帕底亚")
    for table in tables:
        # 跳过表头
        tr_list = table.find_all("tr")[1:]
        for tr in tr_list:
            row = [td for td in tr.children if not isinstance(td, bs4.NavigableString)
                   and td.name == 'td']
            if len(row) and len(row) < 5:
                logging.info(f"【解析html】row not fit the require len >= 5 row:{row}")
            # 解析宝可梦的信息
            pokemon = Pokemon(local_num=int(row[0].text.strip()[1:]),
                              global_num=int(row[1].text.strip()[1:]),
                              name=row[3].text.strip(), attr_types=[att.a.text for att in row[4:] if
                                                                    "hide" not in att.get('class')],
                              pic_url=acquire_spirit_img(row[2].a.span))
            pokemons.append(pokemon)
        with open("pokemons.json", "w+", encoding="utf-8") as p:
            json.dump([p.__dict__ for p in pokemons], p)


acquire_pokemon_list(soup)
