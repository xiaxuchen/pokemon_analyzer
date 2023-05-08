import json

from dataHandler.InfoHandler import InfoHandler


class PokemonListHandler(InfoHandler):

    def handle(self, info):
        """
        保存到数据库中
        :param info: 宝可梦的信息列表
        :return:
        """
        pokemons = info
        with open("pokemons.json", "w+", encoding="utf-8") as p:
            json.dump([p.__dict__ for p in pokemons], p, ensure_ascii=False)
        return pokemons