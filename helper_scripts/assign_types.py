import json

pokemons = {'pokemons': []}

with open('pokemon_list.json') as p, open('types_list.json') as t:
    pokemon_list = json.load(p)
    types = json.load(t)

    for type in types:
        for pokemon in types[type]:
            try:
                pokemon_list[pokemon]['type'].append(type)
            except KeyError as err:
                pass

for pokemon in pokemon_list:
    pokemons['pokemons'].append(pokemon_list[pokemon])

with open('pokemons.json', 'w') as f:
    json.dump(pokemons, f, indent=4)