import os
import json
import time
import requests

from settings import TOTAL_POKEMON, PARPATH, BASE_URL

def get_pokemon():
    for i in range(740, TOTAL_POKEMON + 1):
        r = requests.get(f'{BASE_URL}/pokemon/{i}')

        pokemon = r.json()
        print(f'{pokemon["id"]}: {pokemon["name"]}')
        filepath = os.path.join(PARPATH, 'raw_data', 'pokemon', f'{pokemon["id"]}.json')
        with open(filepath, 'w') as f:
            json.dump(pokemon, f, indent=4)

        time.sleep(3)
        if i % 100 == 0:
            time.sleep(60)


def get_evolution_chains():
    num_chains = 467
    r = requests.get(f'{BASE_URL}/evolution-chain?limit={num_chains}')
    chain_list = r.json()['results']
    
    for chain_url in chain_list:
        r = requests.get(chain_url['url'])
        chain = r.json()
        print(chain['id'])
        filepath = os.path.join(PARPATH, 'raw_data', 'evolution_chains', f'{chain["id"]}.json')
        with open(filepath, 'w') as f:
            json.dump(chain, f, indent=4)
        
        time.sleep(5)
