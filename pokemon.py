from bs4 import BeautifulSoup
import requests

def type_combine(types):
    return f"{types[0].text}/{types[1].text}"

def get_dex_info(name):
    name = name.replace("é", "e")
    print(name.lower())
    dex_url = f'https://pokemondb.net/pokedex/{name.lower()}#dex-flavor'
    print(requests.get(dex_url))
    dex_data = requests.get(dex_url).text
    soup_dex = BeautifulSoup(dex_data, 'lxml')
    info = soup_dex.find_all('td', class_='cell-med-text')
    return info[0].text

poke_data = requests.get('https://pokemondb.net/pokedex/national').text
soup = BeautifulSoup(poke_data, 'lxml')
gens = soup.find_all('div', class_='infocard-list infocard-list-pkmn-lg')
chosen_gen = int(input("Choose a generation number (1-9): "))
gen_choice = gens[chosen_gen-1]

pkmn = gen_choice.find_all('div', class_='infocard')

with open(f"gen{chosen_gen}.txt", "w") as f:
    for i in range(50):
        pkmn_info = pkmn[i].find('span', class_='infocard-lg-data text-muted')
        if pkmn_info.a.text == "Nidoran♀": # special case for special characters (gen 1)
            dex_info = get_dex_info("nidoran-f")
        elif pkmn_info.a.text == "Nidoran♂":
            dex_info = get_dex_info("nidoran-m")
        else:
            dex_info = get_dex_info(pkmn_info.a.text)
        f.write(f"{pkmn_info.a.text} - ")
        pkmn_types = pkmn_info.find_all('small')
        a_tags = pkmn_types[1].find_all('a')
        type_string = ""
        if len(a_tags) > 1:
            type_string = type_combine(a_tags)
        else:
            type_string += a_tags[0].text
        f.write(f"{type_string} - ")
        f.write(dex_info + "\n")