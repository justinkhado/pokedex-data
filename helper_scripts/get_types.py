import requests
import json

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
    print(type)
    r = requests.get(f'https://pokeapi.co/api/v2/type/{type}')
    for pokemon in r.json()['pokemon']:
        types[type].append(pokemon['pokemon']['name'])

with open('types_list.json', 'w') as f:
    json.dump(types, f, indent=4)
