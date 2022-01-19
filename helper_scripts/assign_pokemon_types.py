import requests
import json

BASE_URL = 'https://pokeapi.co/api/v2'

def get_pokemon():
    # 898 pokemon total
    r = requests.get(f'{BASE_URL}/pokemon?limit=898')

    pokemons = {}
    for pokemon in r.json()['results']:
        pokemons[pokemon['name']] = {
            **pokemon,
            'dexNumber': pokemon['url'].split('/')[-2],
            'type': []
        }

    return pokemons

def get_types():
    types = {
    'normal': [],
    'fighting': [],
    'flying': [],
    'poison': [],
    'ground': [],
    'rock': [],
    'bug': [],
    'ghost': [],
    'steel': [],
    'fire': [],
    'water': [],
    'grass': [],
    'electric': [],
    'psychic': [],
    'ice': [],
    'dragon': [],
    'dark': [],
    'fairy': []
    }

    for type in types:
        r = requests.get(f'{BASE_URL}/type/{type}')
        for pokemon in r.json()['pokemon']:
            types[type].append(pokemon['pokemon']['name'])

    return types

def assign_types(pokemon_list, types):
    for type in types:
        for pokemon in types[type]:
            try:
                pokemon_list[pokemon]['type'].append(type)
            except KeyError as err:
                pass
    
    pokemons = {'pokemons': []}
    for pokemon in pokemon_list:
        pokemons['pokemons'].append(pokemon_list[pokemon])

    return pokemons

if __name__ == '__main__':
    pokemon_list = get_pokemon()
    types = get_types()
    pokemons = assign_types(pokemon_list, types)

    with open('pokemons.json', 'w') as f:
        json.dump(pokemons, f, indent=4)