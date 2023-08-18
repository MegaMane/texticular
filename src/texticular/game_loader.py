"""responsible for loading and saving game objects to and from json"""

import json
import texticular.actions.item_actions as item_actions
from texticular.game_object import GameObject
from texticular.game_enums import Flags, Directions
from texticular.items.story_item import StoryItem, Inventory, Container
from texticular.rooms.room import Room
from texticular.rooms.exit import  RoomExit
from texticular.character import Player, NPC
import inspect


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


def load_json(json_file_path):
    with open(json_file_path) as json_file:
        config = json.load(json_file)
    return config

def generate_game_object_flags(flag_list=None):
    if flag_list is None:
        return []
    else:
        return [Flags[flag] for flag in flag_list]

def decode_container_fromjson(dct):
    constructed_container = Container(
        key_value=dct["keyValue"],
        location_key=dct["locationKey"],
        name=dct["name"],
        synonyms=dct["synonyms"],
        adjectives=dct["adjectives"],
        descriptions=dct["descriptions"],
        slots=dct["slots"],
        key_object=dct["keyObject"],
        flags=generate_game_object_flags(dct["flags"])
    )

    constructed_container.current_description = dct["currentDescription"]
    constructed_container.examine_description = dct["examineDescription"]
    constructed_container.action_method_name = dct["actionMethod"]

    #Add the items to the container
    for keyval in dct["itemKeyValues"]:
        constructed_container.add_item(GameObject.objects_by_key.get(keyval))

    return constructed_container


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

    constructed_item.current_description = dct["currentDescription"]
    constructed_item.examine_description = dct["examineDescription"]
    constructed_item.action_method_name = dct["actionMethod"]

    return constructed_item


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

    # Add the items to the room
    for keyval in dct["itemKeyValues"]:
        constructed_room.items.append(GameObject.objects_by_key.get(keyval))


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


def load_story_items(config_file_path):
    config = load_json(config_file_path)
    items = [item for item in config["items"] if item["type"] == "StoryItem"]
    storyitems = {}
    for item in items:
        #print(json.dumps(item, indent=4))
        decoded_item = decode_story_item_fromjson(item)
        storyitems[decoded_item.key_value] = decoded_item
    return storyitems

def load_containers(config_file_path):
    config = load_json(config_file_path)
    storage_containers = [item for item in config["items"] if item["type"] == "Container"]
    containers = {}
    for container in storage_containers:
        #print(json.dumps(item, indent=4))
        decoded_container = decode_container_fromjson(container)
        #add_item_reference_to_room(gamemap, decoded_item)
        containers[decoded_container.key_value] = decoded_container
    return containers

def load_player():
    inventory = Inventory(
        key_value="player-inventory",
        name="Backpack",
        descriptions={"Main": "Your trusty black backpack."},
        location_key="player",
        synonyms=["Bag", "Inventory"]

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


def load_game_rooms(config_file_path):
    config = load_json(config_file_path)
    rooms = {}
    for room in config["rooms"]:
        decoded_room = decode_room_fromjson(room)
        rooms[decoded_room.key_value] = decoded_room
    return rooms


def load_game_map(game_manifest, manifest_key="newGame"):
    manifest = load_json(game_manifest)
    room_config = manifest[manifest_key]["roomConfig"]
    item_config = manifest[manifest_key]["itemConfig"]
    relative_path = "./../../data/"
    gamemap = {}
    gamemap["items"] = load_story_items(f"{relative_path}{item_config}")
    gamemap["containers"] = load_containers(f"{relative_path}{item_config}")
    gamemap["rooms"] = load_game_rooms(f"{relative_path}{room_config}")
    return gamemap

def wire_item_action_funcs():
    """Use the inspect module to return all of the functions in the item_actions module

    function names are identical to the key value of the object they belong to with two exceptions

    1. an 'action_' prefix is added on to the beginning of the function
    2. dashes from the key value are replaced with underscores because they are not allowed in function names

    example: The function action_room201_nightStand maps to the item with a key value of room201-nightStand

    Once the key_value: function mapping is built we loop through the dictionary keys and try to get any
    corresponding game items that match and then use eval to assign that function to the objects action method
    as well as write a reference to its name that will be saved when the object is serialized

    This seems like it might be some bad hacky shit, but it seems to work and it's pretty cool


    """
    func_names = [item[0] for item in inspect.getmembers(item_actions,predicate=inspect.isfunction)]
    key_values = [func_name.strip("action_").replace("_","-") for func_name in func_names]
    action_functions = dict(zip(key_values, func_names))

    for item in action_functions:
        item_to_wire = GameObject.objects_by_key.get(item)
        if item_to_wire:
            func_name = action_functions[item]
            custom_action = eval(f"item_actions.{func_name }")
            item_to_wire.action = item_to_wire.action(custom_action)
            item_to_wire.action_method_name = func_name







if __name__ ==  "__main__":
    gamemap = load_game_map("./../../data/GameConfigManifest.json")
    load_player()
    wire_item_action_funcs()

    #print(gamemap["containers"])

    save_state = True

    if save_state:
        encode_rooms_tojson(gamemap["rooms"], save_file_path="../../data/newGameMap.json")
        encode_story_items_tojson({**gamemap["items"], **gamemap["containers"]}, save_file_path="../../data/newGameItems.json")
