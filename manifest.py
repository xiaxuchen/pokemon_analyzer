import extract_const
from content_handler.PythonSetUrlManager import PythonSetUrlManager
from content_handler.DocParser import PokemonListParser, AttrTypeParser
from content_handler.Downloader import SimpleRequestsHtmlDownloader
from content_handler.UrlHandler import UrlHandler
from dataHandler.InfoHandler import InfoHandlers, EMPTY_INFO_HANDLER
from exception import IllegalStateException
from service.AttrTypeHandler import AttrTypeHandler
from service.PokemonListHandler import PokemonListHandler

# url处理器
urlHandler = UrlHandler()
# url管理器
urlManager = PythonSetUrlManager(exclude=extract_const.LINK_TYPE_POKEMON_DETAIL)
# 解析器
parsers = [
    PokemonListParser(),
    AttrTypeParser()
]
# 下载器
downloader = SimpleRequestsHtmlDownloader()
# 信息处理器的映射
info_handler_dict = {
    extract_const.INFO_POKEMON_LIST: [PokemonListHandler()],
    extract_const.INFO_TYPE_ATTR: [AttrTypeHandler()]
}
"""
获取解析的字典映射
"""


def get_parser_dict():
    inner_parser_dict = {}
    for parser in parsers:
        for t in parser.handle_types():
            if t in inner_parser_dict:
                raise IllegalStateException(
                    f"相同类型的节点有多个处理器处理{inner_parser_dict[t].__class__},{parser.__class__}")
            else:
                inner_parser_dict[t] = parser
    return inner_parser_dict


parser_dict = get_parser_dict()


def get_parser(t):
    if t in parser_dict:
        return parser_dict.get(t)
    else:
        return None


def get_info_handler(t):
    """
    获取信息处理器
    :param t: 信息类型
    :return: 处理器
    """
    if t in info_handler_dict and len(info_handler_dict[t]) > 0:
        return InfoHandlers(info_handler_dict[t])
    return EMPTY_INFO_HANDLER
