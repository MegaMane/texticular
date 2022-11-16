import json
import texticular.globals
from texticular.game_enums import Flags,Directions
from texticular.game_object import GameObject
from texticular.rooms.room import Room
from texticular.rooms.exit import  RoomExit




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
    #constructed_room.action_method_name = dct["actionMethod"]
    #constructed_room.times_visited = dct["timesVisited"]
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
        #constructed_exit.action_method_name = dct[direction]["actionMethod"]

        exits[Directions[direction]] = constructed_exit

    return exits

def encode_rooms_toJson(gamemap, save_file_path):
    rooms = []
    root_element = {}
    for gameroom in gamemap.keys():
        rooms.append(gamemap[gameroom].encode_tojson(gamemap[gameroom]))
    root_element["rooms"] = rooms
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



if __name__ ==  "__main__":
    gamemap = load_game_map("./../../data/initialGameMap.json")
    #print(json.dumps(config, indent=4))


        #print(json.dumps(decoded_room, indent=4, default=decoded_room.encode_tojson))
    print(gamemap.keys())
    encode_rooms_toJson(gamemap, save_file_path="../../data/initialGameMap.json")
