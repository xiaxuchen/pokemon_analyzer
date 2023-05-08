import collections
import json
import sys

from entity.extract.Pokemon import Pokemon


def get_weakness(attrs, attrs_dict):
    """
    获取当前属性的弱点
    当同一个属性对当前的多个属性有加成，则叠加
    :param attrs:
    :param attrs_dict:
    :return:
    """
    if not attrs or not len(attrs):
        return {}
    all = {}
    # 当前属性
    for attr in attrs:
        cur = attrs_dict[attr]
        for k in cur:
            if k in all:
                all[k] *= cur[k] / 2.0
            else:
                all[k] = cur[k] / 2.0
    return all


def get_attack_point(attrs, attrs_dict):
    """
    获取攻击的加成与抗性
    :param attrs:
    :param attrs_dict:
    :return:
    """
    if not attrs or not len(attrs):
        return {}
    all = {}
    for attr in attrs:
        cur = attrs_dict[attr]
        for k in cur:
            all[f"{attr}=>{k}"] = cur[k] / 2.0
    res = {}
    for k in all:
        if all[k] != 1.0:
            res[k] = all[k]
    return res


def analyze(name, enemy_pokemon_name):
    pokemons = []
    with open("pokemons.json", "r", encoding="utf-8") as f:
        pokemons = json.load(f)
    pokemon_name_reflect = {}
    pokemons = [Pokemon(**p) for p in pokemons]
    for pokemon in pokemons:
        pokemon_name_reflect[pokemon.name] = pokemon
    if name not in pokemon_name_reflect:
        print(f"不存在名为【{name}】的宝可梦")
        sys.exit(0)
    if enemy_pokemon_name not in pokemon_name_reflect:
        print(f"不存在名为【{enemy_pokemon_name}】的宝可梦")
        sys.exit(0)
    my_pokemon: Pokemon = pokemon_name_reflect[name]
    enemy_pokemon: Pokemon = pokemon_name_reflect[enemy_pokemon_name]
    attrs_dict = {}
    with open("attr_types.json", "r", encoding="utf-8") as f:
        attrs_dict = json.load(f)
    rev_attrs_dict = collections.defaultdict(dict)
    for k in attrs_dict:
        for target in attrs_dict[k]:
            rev_attrs_dict[target][k] = attrs_dict[k][target]
    # 我方对其他属性的伤害
    attack_point = get_attack_point(my_pokemon.attr_types, attrs_dict)
    weakness_dict = get_weakness(my_pokemon.attr_types, rev_attrs_dict)
    # 获取我方相对对位精灵的弱点
    weak = {}
    resist = {}
    if enemy_pokemon_name:
        for enemy_attr in enemy_pokemon.attr_types:
            if enemy_attr in weakness_dict:
                if weakness_dict[enemy_attr] < 1.0:
                    resist[enemy_attr] = weakness_dict[enemy_attr]
                elif weakness_dict[enemy_attr] > 1.0:
                    weak[enemy_attr] = weakness_dict[enemy_attr]
    print("┎" + "-"*50 + "┒")
    if enemy_pokemon_name:
        print(f"我方【{name}】 vs 敌方【{enemy_pokemon_name}】")
    else:
        print(f"【{name}】分析")
    # 对战分析
    if len(weak):
        print(
            f"请注意【{enemy_pokemon_name}】的以下属性攻击:\r\n {','.join(map(lambda item: f'{item[0]} ×{item[1]}', weak.items()))}")
    if len(resist):
        print(
            f"【{name}】能抵抗【{enemy_pokemon_name}】以下属性攻击:\r\n {','.join(map(lambda item: f'{item[0]} ×{item[1]}', resist.items()))}")
    big_weak_list = [k for k, rate in weakness_dict.items() if rate == 4.0]
    big_resist_list = [k for k, rate in weakness_dict.items() if rate == 0.25]
    double_weak = [k for k, rate in weakness_dict.items() if rate == 2]
    half_resist = [k for k, rate in weakness_dict.items() if rate == 0.5]
    if len(big_weak_list):
        print(f"【{name}】四倍弱点:\r\n {','.join(big_weak_list)}")
    if len(big_resist_list):
        print(f"【{name}】四倍抵抗:\r\n {','.join(big_resist_list)}")
    if len(double_weak):
        print(f"【{name}】两倍弱点:\r\n {','.join(double_weak)}")
    if len(half_resist):
        print(f"【{name}】两倍抵抗:\r\n {','.join(half_resist)}")

    print("┖" + "-"*50 + "┚")


if __name__ == '__main__':
    # 分析
    while True:
        name = input("请输入我方的精灵名称(输入exit退出):").strip()
        if name == "exit":
            sys.exit(0)
        enemy_pokemon_name = input("请输入对方的精灵名称:").strip()
        if enemy_pokemon_name == "":
            enemy_pokemon_name = None
        analyze(name, enemy_pokemon_name)
        # 对方宝可梦不为空才反转分析
        if enemy_pokemon_name is not None:
            reverse = None
            while reverse not in ['y', 'n']:
                reverse = input("是否反转分析(y/n):").strip().lower()
                if reverse == 'y':
                    analyze(enemy_pokemon_name, name)
