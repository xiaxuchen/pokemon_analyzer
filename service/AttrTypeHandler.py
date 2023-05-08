import collections
import json

from dataHandler.InfoHandler import InfoHandler


class AttrTypeHandler(InfoHandler):

    def handle(self, info):
        attrs = info
        attrs_dict = collections.defaultdict(dict)
        for attr in attrs:
            attrs_dict[attr.attr_type][attr.target_type] = attr.attack_rate

        with open("attr_types.json", "w+", encoding="utf-8") as p:
            json.dump(attrs_dict, p, ensure_ascii=False)
        return info