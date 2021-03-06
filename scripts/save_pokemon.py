import os
import json

from settings import TOTAL_POKEMON, PARPATH

def get_pokemon_name(pokemon_name):
    dashed_names = ('deoxys', 'wormadam', 'giratina', 'shaymin', 'basculin', 'darmanitan', 'tornadus', 'thundurus', 'landorus', 'keldeo', 'meloetta', 'meowstic', 'aegislash', 'pumpkaboo', 'gourgeist', 'oricorio', 'lycanroc', 'wishiwashi', 'minior', 'mimikyu')
    for name in dashed_names:
        if name in pokemon_name:
            return pokemon_name.split('-')[0]

    if pokemon_name == 'mr-mime':
        return 'mr. mime'
    elif pokemon_name == 'mime-jr':
        return 'mime jr.'

    return pokemon_name
    

def _clean_pokemon_raw(pokemon_raw):
    pokemon = {}

    pokemon['id'] = pokemon_raw['id']
    pokemon['name'] = get_pokemon_name(pokemon_raw['name'])
    
    # convert decimeter to ft and inches
    pokemon['height'] = f"{int(pokemon_raw['height'] * 3.937 // 12)}\'{round(pokemon_raw['height'] * 3.937 % 12)}\""

    # convert hectogram to lbs
    pokemon['weight'] = f"{round(pokemon_raw['weight'] / 4.536, 1)} lbs"

    pokemon['types'] = []
    for _type in pokemon_raw['types']:
        pokemon['types'].append(_type['type']['name'])

    pokemon['stats'] = {'total': 0}
    for stat in pokemon_raw['stats']:
        stat_name = stat['stat']['name']
        if 'special-' in stat_name:
            stat_name = stat_name.replace('special-', 'sp. ')
        pokemon['stats'][stat_name] = stat['base_stat']
        pokemon['stats']['total'] += stat['base_stat']

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
    else:
        return None

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

def _get_type_chart(types_raw):
    dirpath = os.path.join(PARPATH, 'data', 'types')
    types = []
    for type_ in types_raw:
        filepath = os.path.join(dirpath, f"{type_['type']['name']}.json")
        with open(filepath) as f:
            types.append(json.load(f))
    
    if len(types) == 1:
        return {**types[0], '4': [], '1/4': []}

    type_chart = {}
    type_chart['4'] = list(set(types[0]['2']).intersection(set(types[1]['2'])))
    type_chart['2'] = list(set(types[0]['2']).intersection(set(types[1]['1'])))
    type_chart['2'] += list(set(types[0]['1']).intersection(set(types[1]['2'])))
    type_chart['1'] = list(set(types[0]['1']).intersection(set(types[1]['1'])))
    type_chart['1'] += list(set(types[0]['1/2']).intersection(set(types[1]['2'])))
    type_chart['1'] += list(set(types[0]['2']).intersection(set(types[1]['1/2'])))
    type_chart['1/2'] = list(set(types[0]['1/2']).intersection(set(types[1]['1'])))
    type_chart['1/2'] += list(set(types[0]['1']).intersection(set(types[1]['1/2'])))
    type_chart['1/4'] = list(set(types[0]['1/2']).intersection(set(types[1]['1/2'])))
    type_chart['0'] = list(set(types[0]['0']).intersection(set(types[1]['0'])))

    return type_chart

def save_pokemons():
    pokemons = {'pokemons': []}
    for i in range(1, 808):
        pokemon = {}
        filepath = os.path.join(PARPATH, 'data', 'pokemon', f'{i}.json')
        with open(filepath) as f:
            pokemon_untrimmed = json.load(f)
            pokemon['name'] = get_pokemon_name(pokemon_untrimmed['name'])
            for attr in ('id', 'types'):
                pokemon[attr] = pokemon_untrimmed[attr]
            pokemon['gen'] = _get_generation(pokemon['id'])
            
            pokemons['pokemons'].append(pokemon)
            
    filepath = os.path.join(PARPATH, 'data', 'pokemons.json')    
    with open(filepath, 'w') as f:
        json.dump(pokemons, f, indent=4)

def save_each_pokemon():
    for i in range(1, TOTAL_POKEMON + 1):
        print(i)
        pokemon = {}

        filepath = os.path.join(PARPATH, 'raw_data', 'pokemon', f'{i}.json')
        with open(filepath) as f:
            pokemon_raw = json.load(f)            
            pokemon = _clean_pokemon_raw(pokemon_raw)
            pokemon['abilities'] = _get_abilities(pokemon_raw['abilities'])
            pokemon['type_chart'] = _get_type_chart(pokemon_raw['types'])
        
        filepath = os.path.join(PARPATH, 'data', 'pokemon', f'{i}.json')
        with open(filepath, 'w') as f:
            json.dump(pokemon, f, indent=4)

if __name__ == '__main__':
    save_pokemons()