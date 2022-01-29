import os
import json

from settings import PARPATH

def _handle_flavor_text(flavors):
    for flavor in reversed(flavors):
        if flavor['language']['name'].lower() == 'en':
            return flavor['flavor_text']    
    return ''

def _handle_effect(effects, effect_chance):
    for effect in reversed(effects):
        if effect['language']['name'].lower() == 'en':
            if '$effect_chance' in effect['effect']:
                return effect['effect'].replace('$effect_chance', str(effect_chance))
            return effect['effect']
    return ''

def _handle_machines(machines_list):
    machine_path = os.path.join(PARPATH, 'raw_data', 'machines')
    versions = ('yellow', 'crystal', 'emerald', 'platinum', 'black-2-white-2', 'x-y', 'ultra-sun-ultra-moon', 'sword-shield')
    machines = {}
    for machine in machines_list:
        if machine['version_group']['name'] in versions:
            machine_id = machine['machine']['url'].split('/')[-2]
            filepath = os.path.join(machine_path, f"{machine_id}.json")
            with open(filepath) as f:
                machine_raw = json.load(f)
                machines[machine['version_group']['name']] = machine_raw['item']['name']
    
    return machines

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
            move['machines'] = _handle_machines(move_raw['machines'])
        
        print(f"{move['id']}: {move['name']}")
        filepath = os.path.join(PARPATH, 'data', 'moves', f"{move['id']}.json")
        with open(filepath, 'w') as f:
            json.dump(move, f, indent=4)

if __name__ == '__main__':
    save_each_move()