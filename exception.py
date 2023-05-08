from errorCode import ILLEGAL_ARGS, ILLEGAL_STATE


class PokemonException(Exception):

    def __init__(self, code, message):
        self.code = code
        self.message = message


"""
代码写错,或者调用错误
"""


class CodeErrorException(PokemonException):

    def __init__(self, code, message):
        super().__init__(code, message)


class IllegalArgumentException(CodeErrorException):

    def __init__(self, message=""):
        super().__init__(ILLEGAL_ARGS, message)


class IllegalStateException(CodeErrorException):
    def __init__(self, message=""):
        super().__init__(ILLEGAL_STATE, message)
