import os
import json

from settings import PARPATH

def save_each_ability():
    dirpath = os.path.join(PARPATH, 'raw_data', 'abilities')
    for file in os.listdir(dirpath):
        ability = {}
        with open(os.path.join(dirpath, file)) as f:
            ability_raw = json.load(f)
            ability['id'] = ability_raw['id']
            ability['name'] = ability_raw['name']
            for entry in ability_raw['effect_entries']:
                if entry['language']['name'].lower() == 'en':
                    ability['effect'] = entry['short_effect']
                    break
            
        print(f"{ability['id']}: {ability['name']}")
        filepath = os.path.join(PARPATH, 'data', 'abilities', f"{ability['id']}.json")
        with open(filepath, 'w') as f:
            json.dump(ability, f, indent=4)

if __name__ == '__main__':
    save_each_ability()
