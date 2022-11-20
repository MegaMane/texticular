"""responsible for loading and saving game objects to and from json"""

import json
from texticular.game_enums import Flags, Directions
from texticular.items.story_item import StoryItem
from texticular.rooms.room import Room
from texticular.rooms.exit import  RoomExit
from texticular.character import Player, Inventory, NPC




def load_json(json_file_path):
    with open(json_file_path) as json_file:
        config = json.load(json_file)
    return config

def generate_game_object_flags(flag_list=None):
    if flag_list is None:
        return []
    else:
        return [Flags[flag] for flag in flag_list]

def decode_room_fromjson(dct):
    constructed_room = Room(
        key_value=dct["keyValue"],
        name=dct["name"],
        descriptions=dct["descriptions"],
        location_key="Map",
        flags=generate_game_object_flags(dct["flags"]),
    )

    constructed_room.current_description = dct["currentDescription"]
    constructed_room.examine_description = dct["examineDescription"]
    constructed_room.action_method_name = dct["actionMethod"]
    constructed_room.times_visited = dct["timesVisited"]
    constructed_room.exits = decode_room_exits_fromjson(dct["exits"])

    return constructed_room

def decode_room_exits_fromjson(dct):
    exits = {}
    for direction in dct.keys():
        constructed_exit = RoomExit(
            key_value=dct[direction]["keyValue"],
            name=dct[direction]["name"],
            descriptions=dct[direction]["descriptions"],
            location_key=dct[direction]["locationKey"],
            connection=dct[direction]["connection"],
            key_object=dct[direction]["keyObject"],
            flags=generate_game_object_flags(dct[direction]["flags"]),
        )

        constructed_exit.current_description = dct[direction]["currentDescription"]
        constructed_exit.examine_description = dct[direction]["examineDescription"]
        constructed_exit.action_method_name = dct[direction]["actionMethod"]

        exits[Directions[direction]] = constructed_exit

    return exits

def decode_story_item_fromjson(dct):
    constructed_item = StoryItem(
        key_value=dct["keyValue"],
        location_key=dct["locationKey"],
        name=dct["name"],
        synonyms=dct["synonyms"],
        adjectives=dct["adjectives"],
        descriptions=dct["descriptions"],
        size=dct["size"],
        flags=generate_game_object_flags(dct["flags"])
    )

    constructed_item .current_description = dct["currentDescription"]
    constructed_item .examine_description = dct["examineDescription"]
    constructed_item .action_method_name = dct["actionMethod"]

    return constructed_item

def encode_rooms_tojson(gamemap, save_file_path):
    rooms = []
    root_element = {}
    for gameroom in gamemap.keys():
        rooms.append(gamemap[gameroom].encode_tojson(gamemap[gameroom]))
    root_element["rooms"] = rooms
    with open(save_file_path, "w") as jsonfile:
        json.dump(root_element, jsonfile, indent=4)

def encode_story_items_tojson(storyitems, save_file_path):
    items = []
    root_element = {}
    for item in storyitems.keys():
        items.append(storyitems[item].encode_tojson(storyitems[item]))
        root_element["items"] = items
    with open(save_file_path, "w") as jsonfile:
        json.dump(root_element, jsonfile, indent=4)




def load_game_map(config_file_path):
    config = load_json(config_file_path)
    gamemap = {}
    for room in config["rooms"]:
        #print(json.dumps(room, indent=4))
        decoded_room = decode_room_fromjson(room)
        gamemap[decoded_room.key_value] = decoded_room
    return gamemap

def load_game_objects(gamemap, config_file_path):
    config = load_json(config_file_path)
    storyitems = {}
    for item in config["items"]:
        #print(json.dumps(item, indent=4))
        decoded_item = decode_story_item_fromjson(item)
        add_item_reference_to_room(gamemap, decoded_item)
        storyitems[decoded_item.key_value] = decoded_item
    return storyitems

def add_item_reference_to_room(gamemap, decoded_item):
    item_location = gamemap.get(decoded_item.location_key)
    if item_location:
        item_location.items.append(decoded_item.key_value)
        return True
    return False

def load_player():
    inventory = Inventory(
        key_value="player-inventory",
        name="Backpack",
        descriptions={"Main": "Your trusty black backpack."},
        location_key="player"

    )
    player = Player(
        key_value="player",
        name="Jon",
        descriptions= {"Main": "An Angry nerd with delusions of grandeur."},
        sex = "Male",
        location_key=("room201"),
        flags=[Flags.PLAYERBIT],
        inventory=inventory
    )

    return player







if __name__ ==  "__main__":
    gamemap = load_game_map("./../../data/initialGameMap.json")
    storyitems = load_game_objects(gamemap,"./../../data/items.json")
    #print(json.dumps(config, indent=4))


        #print(json.dumps(decoded_room, indent=4, default=decoded_room.encode_tojson))
    print(gamemap.keys())
    print(gamemap["room201"].items)
    encode_rooms_tojson(gamemap, save_file_path="../../data/initialGameMap.json")
    encode_story_items_tojson(storyitems, save_file_path="../../data/items.json")
