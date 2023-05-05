import json
import re
import random

import requests


def calculate_monster_health_stats(monster):
    response_body = {
        'max_health': 0,
        'min_health': 0,
        'avg_health': 0,
        'random_health': 0
    }

    response = requests.get(f"https://www.dnd5eapi.co/api/monsters/{monster}", verify=False)

    monster = response.json()

    hit_dice_splited = re.split(r'd|\+', monster['hit_points_roll'])

    number_of_dice = int(hit_dice_splited[0])
    dice_value = int(hit_dice_splited[1])
    if len(hit_dice_splited) == 3:
        con_modifier = int(hit_dice_splited[2])
    else:
        con_modifier = 0

    max_health_value = number_of_dice * dice_value + con_modifier
    min_health_value = number_of_dice + con_modifier
    avg_health_value = number_of_dice * (int(dice_value / 2 + 1)) + con_modifier

    random_value_dice = 0
    for x in range(number_of_dice):
        random_value_dice += random.randint(1, dice_value)

    random_health_value = random_value_dice + con_modifier

    response_body['max_health'] = max_health_value
    response_body['min_health'] = min_health_value
    response_body['avg_health'] = avg_health_value
    response_body['random_health'] = random_health_value

    return response_body


def calculate_each_monster_random_health(monster, count):
    response_body = {
        'monstros': []
    }

    for x in range(count):
        response_item_body = {'monster_id': x+1, 'monster_stats': calculate_monster_health_stats(monster)}
        response_body['monstros'].append(response_item_body)

    return response_body


monsters = calculate_each_monster_random_health('hobgoblin', 5)

print(json.dumps(monsters,indent=1))
