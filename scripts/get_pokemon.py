import os
import json
import time
import requests

TOTAL_POKEMON = 898

def get_raw_data(parpath):
    for i in range(740, TOTAL_POKEMON + 1):
        r = requests.get(f'https://pokeapi.co/api/v2/pokemon/{i}')

        pokemon = r.json()
        print(f'{pokemon["id"]}: {pokemon["name"]}')
        filepath = os.path.join(parpath, 'raw_data', f'{pokemon["id"]}.json')
        with open(filepath, 'w') as f:
            json.dump(pokemon, f, indent=4)

        time.sleep(3)
        if i % 100 == 0:
            time.sleep(60)

def save_each_pokemon(parpath):
    for i in range(1, TOTAL_POKEMON + 1):
        pokemon = {}
        filepath = os.path.join(parpath, 'raw_data', f'{i}.json')
        with open(filepath) as f:
            pokemon_raw = json.load(f)            
            for attr in ('name', 'id', 'types', 'abilities', 'moves', 'stats', 'height', 'weight'):
                pokemon[attr] = pokemon_raw[attr]
        
        filepath = os.path.join(parpath, 'pokemon', f'{i}.json')
        with open(filepath, 'w') as f:
            json.dump(pokemon, f, indent=4)

def save_pokemons(parpath):
    pokemons = {'pokemons': []}
    for i in range(1, TOTAL_POKEMON + 1):
        pokemon = {}
        filepath = os.path.join(parpath, 'pokemon', f'{i}.json')
        with open(filepath) as f:
            pokemon_untrimmed = json.load(f)
            pokemon['name'] = pokemon_untrimmed['name']
            pokemon['id'] = pokemon_untrimmed['id']
            pokemon['types'] = []
            for type in pokemon_untrimmed['types']:
                pokemon['types'].append(type['type']['name'])
            if pokemon['id'] <= 151:
                pokemon['gen'] = 1
            elif pokemon['id'] <= 251:
                pokemon['gen'] = 2
            elif pokemon['id'] <= 386:
                pokemon['gen'] = 3
            elif pokemon['id'] <= 493:
                pokemon['gen'] = 4
            elif pokemon['id'] <= 649:
                pokemon['gen'] = 5
            elif pokemon['id'] <= 721:
                pokemon['gen'] = 6
            elif pokemon['id'] <= 809:
                pokemon['gen'] = 7
            elif pokemon['id'] <= 898:
                pokemon['gen'] = 8
            
            pokemons['pokemons'].append(pokemon)
            
    filepath = os.path.join(parpath, 'pokemons.json')    
    with open(filepath, 'w') as f:
        json.dump(pokemons, f, indent=4)

if __name__ == '__main__':
    curpath = os.path.dirname(__file__)
    parpath = os.path.abspath(os.path.join(curpath, os.pardir))

    #raw_pokemons = get_raw_data(parpath)

    #save_each_pokemon(parpath)

    save_pokemons(parpath)

