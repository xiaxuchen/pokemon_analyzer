import logging

import bs4

import extract_const
from manifest import urlHandler, urlManager, get_parser, downloader, get_info_handler

if __name__ == '__main__':
    urlManager.add_url(
        "https://wiki.52poke.com/wiki/%E5%AE%9D%E5%8F%AF%E6%A2%A6%E5%88%97%E8%A1%A8%EF%BC%88%E6%8C%89%E5%B8%95%E5%BA%95%E4%BA%9A%E5%9B%BE%E9%89%B4%E7%BC%96%E5%8F%B7%EF%BC%89",
        extract_const.LINK_TYPE_POKEMON_BOOK)

    urlManager.add_url("https://wiki.52poke.com/wiki/%E5%B1%9E%E6%80%A7%E7%9B%B8%E5%85%8B%E8%A1%A8",
                       extract_const.LINK_TYPE_ATTR_RELATION)

    while urlManager.has_next():
        context_url, tag = urlManager.pop_url()
        parser = get_parser(tag)
        if parser is None:
            logging.warning(f"url【{tag}】{context_url} has no parser to handle")
            continue
        content = downloader.download(context_url)
        doc = bs4.BeautifulSoup(content, "html.parser", from_encoding="utf8")
        (info_type, info), links = parser.parse(doc, context_url)
        links = list(map(lambda link: (urlHandler.handle_url(context_url, link[0]), link[1]), links))
        urlManager.add_urls(links)
        info_handler = get_info_handler(info_type)
        info_handler.handle(info)

