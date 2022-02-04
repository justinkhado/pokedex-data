import os
import json

from settings import PARPATH

def _get_type_list(dirpath):
    type_list = []
    filepath = os.path.join(dirpath, 'types.json')
    with open(filepath) as f:
        types = json.load(f)
        for result in types['results']:
            if result['name'] not in ('unknown', 'shadow'):
                type_list.append(result['name'])
    
    return type_list

def _get_type_chart(damage_relations, type_list):
    type_chart = {'2': [], '1': list(type_list), '1/2': [], '0': []}
    relations = {'double_damage_from': '2', 'half_damage_from': '1/2', 'no_damage_from': '0'}
    for relation in relations:
        for type_ in damage_relations[relation]:
            type_chart[relations[relation]].append(type_['name'])
            type_chart['1'].remove(type_['name'])

    return type_chart

def save_each_type():
    type_chart = {}
    dirpath = os.path.join(PARPATH, 'raw_data', 'types')
    type_list = _get_type_list(dirpath)
    for type_file in os.listdir(dirpath):
        if type_file == 'types.json':
            continue
        
        filepath = os.path.join(dirpath, type_file)
        with open(filepath) as f:
            type_ = json.load(f)
            type_chart = _get_type_chart(type_['damage_relations'], type_list)

        print(type_['name'])
        filepath = os.path.join(PARPATH, 'data', 'types', f"{type_['name']}.json")
        with open(filepath, 'w') as f:
            json.dump(type_chart, f, indent=4)
        
if __name__ == '__main__':
    save_each_type()