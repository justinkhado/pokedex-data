import os
import json
from platform import machine
import time
import requests

from settings import TOTAL_POKEMON, PARPATH, BASE_URL

def _download_resource(resource_name, resource):
    print(f"{resource['id']}")
    filepath = os.path.join(PARPATH, 'raw_data', resource_name, f"{resource['id']}.json")
    with open(filepath, 'w') as f:
        json.dump(resource, f, indent=4)

def download_pokemon():
    for i in range(740, TOTAL_POKEMON + 1):
        r = requests.get(f'{BASE_URL}/pokemon/{i}')
        pokemon = r.json()
        _download_resource('pokemon', pokemon)

        time.sleep(3)
        if i % 100 == 0:
            time.sleep(60)


def download_evolution_chains():
    r = requests.get(f'{BASE_URL}/evolution-chain?limit=1000')
    chain_list = r.json()['results']
    
    for chain_url in chain_list:
        r = requests.get(chain_url['url'])
        chain = r.json()
        _download_resource('evolution_chains', chain)
        
        time.sleep(5)

def download_abilties():
    r = requests.get(f"{BASE_URL}/ability?limit=1000")
    ability_list = r.json()['results']

    for ability_url in ability_list:
        r = requests.get(ability_url['url'])
        ability = r.json()
        _download_resource('abilities', ability)

        time.sleep(5)

def download_moves():
    r = requests.get(f"{BASE_URL}/move?limit=1000")
    move_list = r.json()['results']

    for i, move_url in enumerate(move_list):
        r = requests.get(move_url['url'])
        move = r.json()
        _download_resource('moves', move)
        
        time.sleep(2)
        if (i + 1) % 100 == 0:
            time.sleep(60)

def download_machines():
    r = requests.get(f"{BASE_URL}/machine")
    count = r.json()['count']
    r = requests.get(f"{BASE_URL}/machine?limit={count}")
    machine_list = r.json()['results']

    for i, machine_url in enumerate(machine_list):
        r = requests.get(machine_url['url'])
        machine = r.json()
        _download_resource('machines', machine)

        if (i + 1) % 100 == 0:
            time.sleep(60)

def download_type_relations():
    r = requests.get(f"{BASE_URL}/type")
    filepath = os.path.join(PARPATH, 'raw_data', 'types', 'types.json')
    with open(filepath, 'w') as f:
        json.dump(r.json(), f, indent=4)

    type_list = r.json()['results']
    for type_url in type_list:
        r = requests.get(type_url['url'])
        type_ = r.json()
        _download_resource('types', type_)

if __name__ == '__main__':
    download_type_relations()
