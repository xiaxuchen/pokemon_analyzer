import abc


class InfoHandler(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def handle(self, info):
        """
        对信息进行处理
        :param info:
        :return: 处理后给后续其他处理器的数据
        """
        pass


class InfoHandlers(InfoHandler):

    def __init__(self, handlers):
        self.handlers = handlers

    def handle(self, info):
        for handler in self.handlers:
            info = handler.handle(info)


"""
空实现的信息处理器
"""


class EmptyInfoHandler(InfoHandler):

    def handle(self, info):
        ...


EMPTY_INFO_HANDLER = EmptyInfoHandler()
