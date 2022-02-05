import os
import json

from settings import PARPATH

def _handle_special_evolutions(evolution_chain, id):
    special_evolution_details = [
        '462',      # magneton -> magnezone     chain-id: 34 
        '105',      # cubone -> marowak         chain-id: 46
        '470',      # eevee -> leafeon          chain-id: 67
        '471',      # eevee -> glaceon          chain-id: 67
        '292',      # nincada -> shedinja       chain-id: 144
        '476',      # nosepass -> probopass     chain-id: 147
        '350',      # feebas -> milotic         chain-id: 178
        '678',      # espurr -> meowstic        chain-id: 348
        '738',      # charjabug -> vikavolt     chain-id: 379
        '745',      # rockruff -> lycanroc      chain-id: 383
    ]

    thunder_stone = {
        'item': {
            'name': 'thunder-stone',
            'url': 'https://pokeapi.co/api/v2/item/83/'
        },
        'trigger': {
            'name': 'use-item',
            'url': 'https://pokeapi.co/api/v2/evolution-trigger/3/'
        }
    }

    magnetic_field = {
        'location': {
            'name': 'level up in areas with a special magnetic field',
            'url': ''
        },
        'trigger': {
            'name': 'level-up',
            'url': 'https://pokeapi.co/api/v2/evolution-trigger/1/'
        }
    }

    if id == '462':
        evolution_chain['evolution_details'].clear()
        evolution_chain['evolution_details'].append(magnetic_field)
        evolution_chain['evolution_details'].append(thunder_stone)
    elif id == '105':
        evolution_chain['evolution_details'].pop()
    elif id in ['470', '471']:
        del evolution_chain['evolution_details'][:-1]
    elif id == '292':
        evolution_chain['evolution_details'][0]['trigger']['name'] = 'have 1+ pokeballs and 1+ spaces in party while evolving Nincada to Ninjask'
    elif id == '476':
        evolution_chain['evolution_details'].clear()
        evolution_chain['evolution_details'].append(magnetic_field)
    elif id == '350':
        evolution_chain['evolution_details'].pop(0)
    elif id == '678':
        evolution_chain['evolution_details'].pop()
    elif id == '738':
        evolution_chain['evolution_details'].clear()
        evolution_chain['evolution_details'].append(magnetic_field)
        evolution_chain['evolution_details'].append(thunder_stone)
    elif id == '745':
        evolution_chain['evolution_details'].pop()

def _clean_evolution_chain(evolution_chain, id):
    evolution_chain['id'] = id
    evolution_chain['name'] = evolution_chain['species']['name']
    evolution_chain.pop('species')
    evolution_chain.pop('is_baby')
    if len(evolution_chain['evolves_to']) == 0:
        evolution_chain.pop('evolves_to')
    
    _handle_special_evolutions(evolution_chain, id)

    # remove falsy evolution details
    for evolution_detail in evolution_chain['evolution_details']:
        for key, value in list(evolution_detail.items()):
            if not value:
                 evolution_detail.pop(key)

    # remove urls
    for evolution_detail in evolution_chain['evolution_details']:
        evolution_detail['trigger'] = evolution_detail['trigger']['name']


def save_each_evolution_chain():
    dirpath = os.path.join(PARPATH, 'raw_data', 'evolution_chains')
    for file in os.listdir(dirpath):
        evolution_chain = {}
        file_names = []
        with open(os.path.join(dirpath, file)) as f:
            chain_object = json.load(f)
            evolution_chain = dict(chain_object['chain'])
            print(f"{chain_object['id']}: ", end='')
            
            pokemon_id = str(evolution_chain['species']['url'].split('/')[-2])
            file_names.append(pokemon_id)
            _clean_evolution_chain(evolution_chain, pokemon_id)
            evolution_chain.pop('evolution_details')

            if 'evolves_to' in evolution_chain:
                for evo1 in evolution_chain['evolves_to']:
                    pokemon_id = str(evo1['species']['url'].split('/')[-2])
                    file_names.append(pokemon_id)
                    _clean_evolution_chain(evo1, pokemon_id)

                    if 'evolves_to' in evo1:
                        for evo2 in evo1['evolves_to']:
                            pokemon_id = str(evo2['species']['url'].split('/')[-2])
                            file_names.append(pokemon_id)
                            _clean_evolution_chain(evo2, pokemon_id)

        print(file_names)
        for file_name in file_names:
            filepath = os.path.join(PARPATH, 'data', 'evolution_chains', f'{file_name}.json')
            with open(filepath, 'w') as f:
                json.dump(evolution_chain, f, indent=4)

if __name__ == '__main__':
    save_each_evolution_chain()