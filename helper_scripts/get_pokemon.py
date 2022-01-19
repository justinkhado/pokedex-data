import requests
import json

r = requests.get('https://pokeapi.co/api/v2/pokemon?limit=898') #898

pokemons = {}
for pokemon in r.json()['results']:
    pokemons[pokemon['name']] = {
        **pokemon,
        'dexNumber': pokemon['url'].split('/')[-2],
        'type': []
    }

with open('pokemon_list.json', 'w') as f:
    json.dump(pokemons, f, indent=4)