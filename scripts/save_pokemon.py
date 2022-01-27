import os
import json

from settings import TOTAL_POKEMON, PARPATH

def _clean_pokemon_raw(pokemon_raw):
    pokemon = {}
    for attr in ('name', 'id'):
        pokemon[attr] = pokemon_raw[attr]
    
    # convert decimeter to ft and inches
    pokemon['height'] = f"{int(pokemon_raw['height'] * 3.937 // 12)}\'{round(pokemon_raw['height'] * 3.937 % 12)}\""

    # convert hectogram to lbs
    pokemon['weight'] = f"{round(pokemon_raw['weight'] / 4.536, 1)} lbs"

    pokemon['types'] = []
    for _type in pokemon_raw['types']:
        pokemon['types'].append(_type['type']['name'])

    pokemon['stats'] = {}
    for stat in pokemon_raw['stats']:
        stat_name = stat['stat']['name']
        if 'special-' in stat_name:
            stat_name = stat_name.replace('special-', 'sp. ')
        pokemon['stats'][stat_name] = stat['base_stat']

    return pokemon

def _get_generation(id):
    if id <= 151:
        return 1
    elif id <= 251:
        return 2
    elif id <= 386:
        return 3
    elif id <= 493:
        return 4
    elif id <= 649:
        return 5
    elif id <= 721:
        return 6
    elif id <= 809:
        return 7
    elif id <= 898:
        return 8

def _get_abilities(abilities_raw):
    dirpath = os.path.join(PARPATH, 'data', 'abilities')
    abilities = []
    for ability_raw in abilities_raw:
        id = ability_raw['ability']['url'].split('/')[-2]
        filepath = os.path.join(dirpath, f"{id}.json")
        with open(filepath) as f:
            ability = json.load(f)
            ability.pop('id')
            ability['hidden'] = ability_raw['is_hidden']
            abilities.append(ability)
    
    return abilities


def save_pokemons():
    pokemons = {'pokemons': []}
    for i in range(1, TOTAL_POKEMON + 1):
        pokemon = {}
        filepath = os.path.join(PARPATH, 'data', 'pokemon', f'{i}.json')
        with open(filepath) as f:
            pokemon_untrimmed = json.load(f)
            pokemon['name'] = pokemon_untrimmed['name']
            pokemon['id'] = pokemon_untrimmed['id']
            pokemon['gen'] = _get_generation(pokemon['id'])
            pokemon['types'] = []
            for type in pokemon_untrimmed['types']:
                pokemon['types'].append(type['type']['name'])            
            
            pokemons['pokemons'].append(pokemon)
            
    filepath = os.path.join(PARPATH, 'data', 'pokemons.json')    
    with open(filepath, 'w') as f:
        json.dump(pokemons, f, indent=4)

def save_each_pokemon():
    for i in range(1, 4):
        print(i)
        pokemon = {}

        filepath = os.path.join(PARPATH, 'raw_data', 'pokemon', f'{i}.json')
        with open(filepath) as f:
            pokemon_raw = json.load(f)            
            pokemon = _clean_pokemon_raw(pokemon_raw)
            pokemon['abilities'] = _get_abilities(pokemon_raw['abilities'])
            # pokemon['moves'] = _get_moves()
        
        filepath = os.path.join(PARPATH, 'data', 'pokemon', f'{i}.json')
        with open(filepath, 'w') as f:
            json.dump(pokemon, f, indent=4)

if __name__ == '__main__':
    save_each_pokemon()