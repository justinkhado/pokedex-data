import os
import json

from download_data import TOTAL_POKEMON, PARPATH

def _clean_pokemon_raw(pokemon_raw):
    pokemon = {}
    for attr in ('name', 'id', 'abilities', 'moves'):
        pokemon[attr] = pokemon_raw[attr]
    
    pokemon['types'] = []
    for _type in pokemon_raw['types']:
        pokemon['types'].append(_type['type']['name'])

    pokemon['stats'] = {}
    for stat in pokemon_raw['stats']:
        stat_name = stat['stat']['name']
        if 'special-' in stat_name:
            stat_name = stat_name.replace('special-', 'sp. ')
        pokemon['stats'][stat_name] = stat['base_stat']

    # convert decimeter to ft and inches
    pokemon['height'] = f"{int(pokemon_raw['height'] * 3.937 // 12)}\'{round(pokemon_raw['height'] * 3.937 % 12)}\""

    # convert hectogram to lbs
    pokemon['weight'] = f"{round(pokemon_raw['weight'] / 4.536, 1)} lbs"

    return pokemon

def save_each_pokemon():
    for i in range(1, 2):
        filepath = os.path.join(PARPATH, 'raw_data', 'pokemon', f'{i}.json')
        with open(filepath) as f:
            pokemon_raw = json.load(f)            
            pokemon = _clean_pokemon_raw(pokemon_raw)
        
        filepath = os.path.join(PARPATH, 'pokemon', f'{i}.json')
        with open(filepath, 'w') as f:
            json.dump(pokemon, f, indent=4)

def save_pokemons():
    pokemons = {'pokemons': []}
    for i in range(1, TOTAL_POKEMON + 1):
        pokemon = {}
        filepath = os.path.join(PARPATH, 'pokemon', f'{i}.json')
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
            
    filepath = os.path.join(PARPATH, 'pokemons.json')    
    with open(filepath, 'w') as f:
        json.dump(pokemons, f, indent=4)

def save_each_evolution_chain():
    dir_path = os.path.join(PARPATH, 'raw_data', 'evolution_chains')
    for file in os.listdir(dir_path):
        evolution_chain = {}
        file_name = ''
        with open(os.path.join(dir_path, file)) as f:
            chain_object = json.load(f)
            evolution_chain = dict(chain_object['chain'])
            print(f"{chain_object['id']}: ", end='')
            
            pokemon_id = str(evolution_chain['species']['url'].split('/')[-2])
            file_name += pokemon_id
            evolution_chain['id'] = pokemon_id
            evolution_chain['name'] = evolution_chain['species']['name']
            evolution_chain.pop('species')
            evolution_chain.pop('is_baby')
            evolution_chain.pop('evolution_details')

            for evo1 in evolution_chain['evolves_to']:
                pokemon_id = str(evo1['species']['url'].split('/')[-2])
                file_name += '_' + pokemon_id
                evo1['id'] = pokemon_id
                evo1['name'] = evo1['species']['name']
                evo1.pop('species')
                evo1.pop('is_baby')

                for evo2 in evo1['evolves_to']:
                    pokemon_id = str(evo2['species']['url'].split('/')[-2])
                    file_name += '_' + pokemon_id
                    evo2['id'] = pokemon_id
                    evo2['name'] = evo2['species']['name']
                    evo2.pop('species')
                    evo2.pop('is_baby')
                    evo2.pop('evolves_to')

        print(file_name)
        filepath = os.path.join(PARPATH, 'evolution_chains', f'{file_name}.json')
        with open(filepath, 'w') as f:
            json.dump(evolution_chain, f, indent=4)

if __name__ == '__main__':
    # save_pokemons()
    # save_each_pokemon()
    save_each_evolution_chain()