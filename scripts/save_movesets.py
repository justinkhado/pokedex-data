import os
import json

from settings import PARPATH, TOTAL_POKEMON

def _get_moves_list(id):
    pokemon_raw_path = os.path.join(PARPATH, 'raw_data', 'pokemon', f"{id}.json")
    with open(pokemon_raw_path) as f:
        pokemon_raw = json.load(f)
        return pokemon_raw['moves']


def _sort_moveset(moveset):
    moveset_copy = dict(moveset)
    for version in moveset_copy:
        for method in moveset_copy[version]:
            if method == 'level-up':
                moveset[version][method] = sorted(moveset[version][method], key = lambda x: x['level'])
            elif method == 'machine':
                moveset[version][method] = sorted(moveset[version][method], key = lambda x: x['machine'])            

def _get_moveset(moves_list):
    versions = ('yellow', 'crystal', 'emerald', 'platinum', 'black-2-white-2', 'x-y', 'ultra-sun-ultra-moon', 'sword-shield')
    moves = {version: {'level-up': [], 'egg': [], 'tutor': [], 'machine': []} for version in versions}    
    for move_raw in moves_list:
        for version_group_detail in move_raw['version_group_details']:
            version = version_group_detail['version_group']['name']
            if version in versions:
                id = move_raw['move']['url'].split('/')[-2]
                filepath = os.path.join(PARPATH, 'data', 'moves', f"{id}.json")
                with open(filepath) as f:
                    move_details = json.load(f)
                    move_details_without_machines = {key: move_details[key] for key in move_details if key != 'machines'}
                    method = version_group_detail['move_learn_method']['name']
                    if method == 'level-up':
                        moves[version][method].append({
                            **move_details_without_machines,
                            'level': version_group_detail['level_learned_at']
                        })
                    elif method in ('egg', 'tutor'):
                        moves[version][method].append(move_details_without_machines)
                    elif method == 'machine':
                        moves[version][method].append({
                            **move_details_without_machines,
                            'machine': move_details['machines'][version]
                        })
    
    return moves
                
def save_each_moveset():
    dirpath = os.path.join(PARPATH, 'data', 'movesets')
    for pokemon_id in range(1, TOTAL_POKEMON + 1):
        moves_list = _get_moves_list(pokemon_id)
        moveset = _get_moveset(moves_list)
        _sort_moveset(moveset)

        print(f"{pokemon_id}")
        filepath = os.path.join(dirpath, f"{pokemon_id}.json")
        with open(filepath, 'w') as f:
            json.dump(moveset, f, indent=4)

if __name__ == '__main__':
    save_each_moveset()