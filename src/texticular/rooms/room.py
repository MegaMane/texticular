from texticular.game_object import  GameObject
from texticular.game_enums import Flags, Directions

class Room(GameObject):
    room_count = 0

    def __init__(self, key_value: str, name: str, descriptions: dict, location_key="Map", flags=[]):
        self.times_visited = 0
        self.items = []
        self.exits = {}
        self.npcs = []
        super().__init(key_value, name, descriptions,location_key, flags)
        Room.room_count += 1

