import PySimpleGUI as sg
import requests
import argparse
import gen_pokemon_for_gui as gpfg
import pyperclip

##Create the game_state object
game_state = {}

##Parse Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--num", type=int)
parser.add_argument("--dex_num", type=int)
parser.add_argument("--gen", type=int)
parser.add_argument("--players", type=int)
args = parser.parse_args()
num_of_pokemon_to_generate = args.num
dex_num = args.dex_num
gen = args.gen
game_state["num_players"] = args.players

##Argument Validation
if game_state["num_players"] > 5 or game_state["num_players"] > num_of_pokemon_to_generate / 6:
    print("ERROR!  TOO MANY PLAYERS FOR THAT MANY POKEMON")
    exit(1)
if num_of_pokemon_to_generate > 30:
    print("ERROR!  CAN'T GENERATE MORE THAN 30 POKEMON")
    exit(1)

##Define the window icon
icon = requests.get(url="https://e1.pngegg.com/pngimages/429/296/png-clipart-poke-balls-generation-i-free-icons-great-ball-thumbnail.png").content
##Define the theme for the window
sg.theme('DarkBlue6')



##Define a library to store player's teams
game_state["players_teams"] = {}

##Generate the desired number of Pokemon
game_state["pokemon"] = gpfg.gen_x_random_pokemon(num_of_pokemon_to_generate, gen, inclusions = ["FE"], exclusions = ["legendaries", "shitmons"])

##Initialize the Draft Direction
game_state["draft_direction"] = "FORWARD"

##Initialize each Pokemon reaveled and chosen status
i = 0
while i < len(game_state["pokemon"]):
    game_state["pokemon"][i]["chosen"] = False
    game_state["pokemon"][i]["revealed"] = False
    i = i + 1

##Initialize the action log for undo's
game_state["action_log"] = []

##Choose the starting player
game_state["active_player"] = 1

##Initialize the players number of views
game_state["views_remaining"] = 3

##Create the layout for the window
layout = []
rows=[]
i = 0
while i < len(game_state["pokemon"]):
    j = 0
    row = []
    while j < 6 and i < len(game_state["pokemon"]):
        print(i)
        row.append(sg.Button("", key=str(i), image_source = game_state["pokemon"][i]["sprite"], image_size=(120,120)))
        row.append(sg.Text("", key=str(i)+"Set", size=(20,8)))
        i = i + 1
        j = j + 1
    layout.append(row)
    rows.append(row)
i = 0
while i < game_state["num_players"]:
    game_state["players_teams"][i+1] = []
    layout.append([sg.Text("Player " + str(i + 1) + "'s team: ", font = ("Arial", 20)), sg.Image(key="P"+str(i+1)+"P1", size=(60,60)), sg.Image(key="P"+str(i+1)+"P2", size=(60,60)), sg.Image(key="P"+str(i+1)+"P3", size=(60,60)), sg.Image(key="P"+str(i+1)+"P4", size=(60,60)), sg.Image(key="P"+str(i+1)+"P5", size=(60,60)), sg.Image(key="P"+str(i+1)+"P6", size=(60,60))])
    i = i + 1
layout.append([sg.Button("Undo", key="-UNDO-"), sg.Text("Player's Turn: 1", key="active_player"), sg.Text("Views Remaining: 3", key="views_remaining"), sg.Button("Get Showdown List to Clipboard", key="get-showdown-list")])
game_state["window"] = sg.Window('Pokemon Draft', layout, icon=icon)

##Define Functions

def get_showdown_list(game_state):
    showdown_strings = []
    for player_id in game_state["players_teams"].keys():
        for players_pokemon in game_state["players_teams"][player_id]:
            showdown_strings.append(gpfg.get_showdown_set(players_pokemon))
    showdown_string = gpfg.get_showdown_list(showdown_strings)
    pyperclip.copy(showdown_string)

def advance_draft(game_state):
    game_state["views_remaining"] = views_remaining = 3
    if game_state["draft_direction"] == "FORWARD":
        game_state["active_player"] = game_state["active_player"] + 1
        if game_state["active_player"] > game_state["num_players"]:
            game_state["active_player"] = game_state["active_player"] - 1
            game_state["draft_direction"] = "BACKWARD"
    elif game_state["draft_direction"] == "BACKWARD":
        game_state["active_player"] = game_state["active_player"] - 1
        if game_state["active_player"] == 0:
            game_state["active_player"] = game_state["active_player"] + 1
            game_state["draft_direction"] = "FORWARD"
    return game_state

def undo(game_state, action):
    game_state["active_player"] = action["active_player"]
    game_state["views_remaining"] = action["views_remaining"]
    game_state["draft_direction"] = action["draft_direction"]
    return game_state

def update_indicators(game_state):
    i = 0
    while i < game_state["num_players"]:
        j = 0
        while j < 6:
            if j < len(game_state["players_teams"][i+1]):
                game_state["window"]["P" + str(i+1) + "P" + str(j+1)].update(source = game_state["players_teams"][i+1][j]["sprite"])
            else:
                game_state["window"]["P" + str(i+1) + "P" + str(j+1)].update(source = None)
            j = j + 1
        i = i + 1
    game_state["window"]["active_player"].update("Player's Turn: " + str(game_state["active_player"]))
    game_state["window"]["views_remaining"].update("Views Remaining: " + str(game_state["views_remaining"]))
    return game_state

while True:
    event, values = game_state["window"].read()
    if event == 'Exit' or event == sg.WIN_CLOSED:
        break
    elif event == "-UNDO-":
        if len(game_state["action_log"]) > 0:
            action = game_state["action_log"].pop()
            if action["type"] == "reveal":
                game_state["pokemon"][action["choice"]]["revealed"] = False
                game_state["window"][str(action["choice"])+"Set"].update("")
                game_state = undo(game_state, action)
            if action["type"] == "reveal-and-take":
                game_state["pokemon"][action["choice"]]["revealed"] = False
                game_state["window"][str(action["choice"])+"Set"].update("")
                game_state["pokemon"][action["choice"]]["revealed"] = False
                game_state["pokemon"][action["choice"]]["chosen"] = False
                game_state["window"][str(action["choice"])+"Set"].update("")
                game_state["window"][str(action["choice"])].update(disabled=False)
                game_state["players_teams"][action["active_player"]].pop()
                game_state = undo(game_state, action)
            if action["type"] == "take":
                game_state["pokemon"][action["choice"]]["chosen"] = False
                game_state["window"][str(action["choice"])].update(disabled=False)
                game_state["players_teams"][action["active_player"]].pop()
                game_state = undo(game_state, action)
        game_state = update_indicators(game_state)
    elif event == "get-showdown-list":
        get_showdown_list(game_state)
    elif len(game_state["players_teams"][game_state["active_player"]]) < 6:
        if not game_state["pokemon"][int(event)]["chosen"]:
            if not game_state["pokemon"][int(event)]["revealed"] and game_state["views_remaining"] > 0:
                action = {"type": "reveal", "active_player": game_state["active_player"], "choice": int(event), "views_remaining": game_state["views_remaining"],  "draft_direction": game_state["draft_direction"]}
                game_state["action_log"].append(action)
                game_state["window"][event+"Set"].update(gpfg.get_showdown_set(game_state["pokemon"][int(event)]).replace("EVs: ", ""))
                game_state["pokemon"][int(event)]["revealed"] = True
                game_state["views_remaining"] = game_state["views_remaining"] - 1
            elif not game_state["pokemon"][int(event)]["revealed"] and game_state["views_remaining"] == 0:
                action = {"type": "reveal-and-take", "active_player": game_state["active_player"], "choice": int(event), "views_remaining": game_state["views_remaining"], "draft_direction": game_state["draft_direction"]}
                game_state["action_log"].append(action)
                game_state["window"][event].update(disabled=True)
                game_state["window"][event+"Set"].update(gpfg.get_showdown_set(game_state["pokemon"][int(event)]).replace("EVs: ", ""))
                game_state["pokemon"][int(event)]["revealed"] = True
                game_state["pokemon"][int(event)]["chosen"] = True
                game_state["players_teams"][game_state["active_player"]].append(game_state["pokemon"][int(event)])
                game_state = advance_draft(game_state)
            elif game_state["pokemon"][int(event)]["revealed"]:
                action = {"type": "take", "active_player": game_state["active_player"], "choice": int(event), "views_remaining": game_state["views_remaining"], "draft_direction": game_state["draft_direction"]}
                game_state["action_log"].append(action)
                game_state["window"][event].update(disabled=True)
                game_state["pokemon"][int(event)]["chosen"] = True
                game_state["players_teams"][game_state["active_player"]].append(game_state["pokemon"][int(event)])
                game_state = advance_draft(game_state)
        game_state = update_indicators(game_state)
game_state["window"].close()