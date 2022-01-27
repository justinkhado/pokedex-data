import os
import json

from settings import PARPATH

def _handle_flavor_text(entries):
    for entry in reversed(entries):
        if entry['language']['name'].lower() == 'en':
            return entry['flavor_text']    
    return ''

def _handle_effect(entries, effect_chance):
    for entry in reversed(entries):
        if entry['language']['name'].lower() == 'en':
            if '$effect_chance' in entry['effect']:
                return entry['effect'].replace('$effect_chance', str(effect_chance))
            return entry['effect']
    return ''

def save_each_move():
    dirpath = os.path.join(PARPATH, 'raw_data', 'moves')
    for file in os.listdir(dirpath):
        move = {}
        with open(os.path.join(dirpath, file)) as f:
            move_raw = json.load(f)

            for attr in ('id', 'name', 'power', 'accuracy', 'pp', 'priority'):
                move[attr] = move_raw[attr]
                
            for attr in ('type', 'damage_class'):
                move[attr] = move_raw[attr]['name']

            move['description'] = _handle_flavor_text(move_raw['flavor_text_entries'])
            move['effect'] = _handle_effect(move_raw['effect_entries'], move_raw['effect_chance'])
        
        print(f"{move['id']}: {move['name']}")
        filepath = os.path.join(PARPATH, 'data', 'moves', f"{move['id']}.json")
        with open(filepath, 'w') as f:
            json.dump(move, f, indent=4)

if __name__ == '__main__':
    save_each_move()