import requests
import random
import json
import string
import pyperclip
import inclusions_exclusions

pokemon_inclusions = inclusions_exclusions.inclusions
pokemon_exclusions = inclusions_exclusions.exclusions
    

gen_num_to_rn_lib = {3: "generation-iii"
,4: "generation-iv"
,5: "generation-v"
,6: "generation-vi"
,7: "generation-vii"
,8: "generation-viii"
,9: "generation-ix"}

gen_lib = {"generation-iii": "firered-leafgreen"
,"generation-iv": "heartgold-soulsilver"
,"generation-v": "black-2-white-2"
,"generation-vi": "omega-ruby-alpha-sapphire"
,"generation-vii": "ultra-sun-ultra-moon"}

dex_cutoff = {3: 386
,4: 493
,5: 649
,6: 721
,7: 807
,8: 905}

pokemon_info_url = "https://pokeapi.co/api/v2/pokemon/"
item_list_url = "https://pokeapi.co/api/v2/item-category/"
valid_item_categories = [12,13]

possible_natures = [
    "Hardy"
    ,"Lonely"
    ,"Brave"
    ,"Adamant"
    ,"Naughty"
    ,"Bold"
    ,"Docile"
    ,"Relaxed"
    ,"Impish"
    ,"Lax"
    ,"Timid"
    ,"Hasty"
    ,"Serious"
    ,"Jolly"
    ,"Naive"
    ,"Modest"
    ,"Mild"
    ,"Quiet"
    ,"Bashful"
    ,"Rash"
    ,"Calm"
    ,"Gentle"
    ,"Sassy"
    ,"Careful"
    ,"Quirky"
    ]

def clean_string(x):
    return string.capwords(x.replace("-", " "))

def get_pokemon_json(nat_dex_number):
    x = requests.get(pokemon_info_url + str(nat_dex_number))
    return json.loads(x.text)

def get_pokemon_name(pokemon_info, gen):
    exceptions = {"Mime Jr": "Mime Jr."
        , "Wormadam Plant": "Wormadam"
        , "Farfetchd": "Farfetch'd"
        , "Nidoran M": "Nidoran-M"
        , "Nidoran F": "Nidoran-F"
        , "Giratina Altered": "Giratina"
        , "Mr Mime": "Mr. Mime"
        , "Deoxys Normal": "Deoxys"
        , "Deoxys Attack": "Deoxys-Attack"
        , "Deoxys Defense": "Deoxys-Defense"
        , "Deoxys Speed": "Deoxys-Speed"
        , "Shaymin Land": "Shaymin"
        , "Sirfetchd": "Sirfetch'd"
        , "Mr Rime": "Mr. Rime"
        , "Ho Oh": "Ho-Oh"
        , "Porygon Z": "Porygon-Z"
        , "Jangmo O": "Jangmo-o"
        , "Hakamo O": "Hakamo-o"
        , "Kommo O": "Kommo-o"
        , "Wo Chien": "Wo-Chien"
        , "Chien Pao": "Chien-Pao"
        , "Ting Lu": "Ting-Lu"
        , "Chi Yu": "Chi-Yu"
        , "Wishiwashi Solo": "Wishiwashi"
        , "Oricorio Baile": "Oricorio"
        , "Thundurus Incarnate": "Thundurus"
        , "Zygarde 50": "Zygarde"
        , "Type Null": "Type: Null"
        , "Lycanroc Midday": "Lycanroc"
        , "Basculin Red Striped": "Basculin"
        , "Gourgeist Average": "Gourgeist"
        , "Mimikyu Disguised": "Mimikyu"
        , "Darmanitan Standard": "Darmanitan"
        , "Tornadus Incarnate": "Tornadus"
        , "Meowstic Male": "Meowstic"
        , "Meloetta Aria": "Meloetta"
        , "Minior Red Meteor": "Minior"
        , "Landorus Incarnate": "Landorus"
        , "Aegislash Shield": "Aegislash"
        , "Keldeo Ordinary": "Keldeo"
        , "Pumpkaboo Average": "Pumpkaboo"}
    if clean_string(pokemon_info["name"]) in exceptions.keys():
        return exceptions[clean_string(pokemon_info["name"])]
    return clean_string(pokemon_info["name"])

def get_pokemon_sprite(pokemon_info, gen):
    return requests.get(pokemon_info["sprites"]["versions"][gen_num_to_rn_lib[gen]][gen_lib[gen_num_to_rn_lib[gen]]]["front_default"]).content

def choose_random_held_item(valid_items, gen):
    num_of_items_chosen = 0
    while num_of_items_chosen < 1:
        item = random.choice(valid_items)
        num_of_items_chosen = num_of_items_chosen + 1
    return item

def choose_random_ability(pokemon_info, gen):
    num_of_abilities_chosen = 0
    exceptions = {
    "tapu-bulu": "Grassy Surge"
    ,"tapu-fini": "Misty Surge"
    ,"tapu-lele": "Pyschic Surge"
    ,"tapu-koko": "Electric Surge"
    ,"silvally": "RKS System"
    ,"heatran": "Flash Fire"}
    if (pokemon_info["name"] in exceptions):
        ability = exceptions[pokemon_info["name"]]
    else:
        while num_of_abilities_chosen < 1:
            ability = random.choice(pokemon_info["abilities"])
            if not ability["is_hidden"] or gen_num_to_rn_lib[gen] not in ["generation-iii", "generation-iv"]:
                ability = ability["ability"]["name"]
                num_of_abilities_chosen = num_of_abilities_chosen + 1
    return ability

def choose_four_random_moves(pokemon_info, gen):
    num_moves_chosen = 0
    moves = []
    move_special_cases = {"Mud Slap": "Mud-Slap"
        , "X Scissor": "X-Scissor"
        , "Double Edge": "Double-Edge"
        , "Self Destruct": "Self-Destruct"
        , "Lock On": "Lock-On"
        , "Will O Wisp": "Will-O-Wisp"
        , "Wake Up Slap": "Wake-Up Slap"
        , "U Turn": "U-Turn"
        , "V Create": "V-Create"
        , "Trick Or Treat": "Trick-or-Treat"
        , "Freeze Dry": "Freeze-Dry"
        , "Topsy Turvy": "Topsy-Turvy"
        , "Baby Doll Eyes": "Baby-Doll Eyes"
        , "All Out Pummeling": "All-Out Pummeling"
        , "Savage Spin Out": "Savage Spin-Out"
        , "Never Ending Nightmare": "Never-Ending Nightmare"
        , "Soul Stealing 7 Star Strike": "Soul-Stealing 7-Star Strike"
        , "Multi Attack": "Multi-Attack"}
    possible_moves = []
    for move in pokemon_info["moves"]:
        for version_group_detail in move["version_group_details"]:
            if version_group_detail["version_group"]["name"] == gen_lib[gen_num_to_rn_lib[gen]]:
                if clean_string(move["move"]["name"]) not in move_special_cases.keys() and clean_string(move["move"]["name"]) not in possible_moves:
                    possible_moves.append(clean_string(move["move"]["name"]))
                elif clean_string(move["move"]["name"]) in move_special_cases.keys():
                    if move_special_cases[clean_string(move["move"]["name"])] not in possible_moves:
                        possible_moves.append(move_special_cases[clean_string(move["move"]["name"])])
    target_num_of_moves = 4
    if len(possible_moves) < 4:
        moves = possible_moves
    else:
        while num_moves_chosen < target_num_of_moves:
            chosen_move = random.choice(possible_moves)
            if chosen_move not in moves:
                num_moves_chosen = num_moves_chosen + 1
                moves.append(chosen_move)
    return moves

def choose_random_IVS():
    IVS = {}
    IVS["HP"] = 31
    IVS["ATK"] = 31
    IVS["DEF"] = 31
    IVS["SPA"] = 31
    IVS["SPD"] = 31
    IVS["SPE"] = 31
    return IVS

def choose_random_EVS():
    EVS = {"HP": 0, "ATK": 0, "DEF": 0, "SPA": 0, "SPD": 0, "SPE": 0}
    EVS_arr = [0,0,0,0,0,0]
    EVS_spent = 0
    while EVS_spent < 510:
        EV_choice = random.randrange(0, 6, 1)
        if EVS_arr[EV_choice] < 252 and EVS_spent < 504:
            EVS_arr[EV_choice] = EVS_arr[EV_choice] + 252
            EVS_spent = EVS_spent + 252
        elif EVS_arr[EV_choice] == 0 and EVS_spent == 504:
            EVS_arr[EV_choice] = EVS_arr[EV_choice] + 6
            EVS_spent = EVS_spent + 6
    EVS["HP"] = EVS_arr[0]
    EVS["ATK"] = EVS_arr[1]
    EVS["DEF"] = EVS_arr[2]
    EVS["SPA"] = EVS_arr[3]
    EVS["SPD"] = EVS_arr[4]
    EVS["SPE"] = EVS_arr[5]
    return EVS

def build_possible_held_item_list(gen):
    possible_items = []
    valid_items = []
    exceptions = {"Kings Rock": "King's Rock"}
    disclude = ["Pass Orb", "Misty Seed"]
    for valid_item_category in valid_item_categories:
        item_list = get_item_list_json_by_category(valid_item_category)
        possible_items = possible_items + item_list
    for item in possible_items:
        item_details = get_item_details(item["url"])
        for game_indicy in item_details["game_indices"]:
            if game_indicy["generation"]["name"] == gen_num_to_rn_lib[gen]:
                if clean_string(item["name"]) in exceptions.keys():
                    valid_items.append(exceptions[clean_string(item["name"])])
                else:
                    if clean_string(item["name"]) not in disclude:
                        valid_items.append(clean_string(item["name"]))
    return valid_items

def get_item_list_json_by_category(item_category):
    x = requests.get(item_list_url + str(item_category))
    return json.loads(x.text)["items"]

def get_item_details(item_url):
    x = requests.get(item_url)
    return json.loads(x.text)

def build_random_pokemon(pokemon_info, gen, possible_items):
    random_pokemon = {}
    
    random_pokemon["sprite"] = get_pokemon_sprite(pokemon_info, gen)
    random_pokemon["name"] = get_pokemon_name(pokemon_info, gen)
    print(random_pokemon["name"])
    random_pokemon["held_item"] = clean_string(choose_random_held_item(possible_items, gen))
    random_pokemon["ability"] = clean_string(choose_random_ability(pokemon_info, gen))
    random_pokemon["EVS"] = choose_random_EVS()
    random_pokemon["nature"] = clean_string(random.choice(possible_natures))
    random_pokemon["moves"] = choose_four_random_moves(pokemon_info, gen)
    random_pokemon["IVS"] = choose_random_IVS()
    return random_pokemon

def get_showdown_set(pokemon):
    return_str = pokemon["name"] + """ @ """ + pokemon["held_item"] + """
Ability: """ + pokemon['ability'] + """
EVs: """ + str(pokemon["EVS"]["HP"]) + """ HP / """ + str(pokemon["EVS"]["ATK"]) + """ Atk / """ + str(pokemon["EVS"]["DEF"]) + """ Def / """ + str(pokemon["EVS"]["SPA"]) + """ SpA / """ + str(pokemon["EVS"]["SPD"]) + """ SpD / """ + str(pokemon["EVS"]["SPE"]) + """ Spe
""" + pokemon["nature"] + """ Nature"""
    i = 0
    while i < len(pokemon["moves"]):
        return_str = return_str + """
- """ + pokemon["moves"][i]
        i = i + 1
    return return_str.replace("0 HP / ", "").replace("0 Atk / ", "").replace("0 Def / ", "").replace("0 SpA / ", "").replace("0 SpD / ", "").replace("/ 0 Spe", "")

def get_showdown_list(showdown_pokemon_strings):
    output = ""
    for showdown_pokemon_string in showdown_pokemon_strings:
        output = output + "\n\n" + showdown_pokemon_string
    return output

def gen_x_random_pokemon(num_of_pokemon_to_generate, gen, inclusions = [], exclusions = []):
    possible_items = build_possible_held_item_list(gen)
    inclusion_list = []
    for inclusion in inclusions:
        inclusion_list = inclusion_list + pokemon_inclusions[inclusion]
    exclusion_list = []
    for exclusion in exclusions:
        exclusion_list = exclusion_list + pokemon_exclusions[exclusion]
    i = 0
    pokemon = []
    while i < num_of_pokemon_to_generate:
        print("Generating Pokemon " + str(i + 1))
        chosen_dex_num = 0
        while (chosen_dex_num == 0 or chosen_dex_num in exclusion_list or (chosen_dex_num not in inclusion_list or len(inclusion_list) == 0)):
            chosen_dex_num = random.randrange(1, dex_cutoff[gen], 1)
        pokemon.append(build_random_pokemon(get_pokemon_json(chosen_dex_num), gen, possible_items))
        i = i + 1
    return pokemon