from texticular.game_object import GameObject
from texticular.items.story_item import StoryItem
from texticular.rooms.room import Room
from texticular.game_enums import Flags, Directions


class Inventory(GameObject):
    def __init__(self, key_value: str, name: str, descriptions: dict,
                 slots: int = 10, location_key: str = None, flags: list = None):
        super().__init__(key_value, name, descriptions, location_key, flags)
        self.slots = slots
        self.slots_occupied = 0
        self.items = []

    def add_item(self, item: StoryItem) -> bool:
        if item.size + self.slots_occupied <= self.slots:
            self.slots_occupied += item.size
            self.items.append(item)
            return True
        return False

    def remove_item(self, item: StoryItem) -> bool:
        if item in self.items:
            self.slots_occupied -= item.size
            self.items.remove(item)
            return True
        return False

    def describe(self) -> str:
        response = ""
        response += f"{self.name}: {self.current_description}"
        response += "\n" + ("-" * (len(self.name) + len(self.current_description) + 2)) + "\n\n"
        for item in self.items:
            response += f"{item}: {item.current_description}\n\n"

        return response




class Character(GameObject):
    def __init__(self, key_value: str, name: str, descriptions: dict, sex: str = "?", hp: int = 100,
                 inventory: Inventory = None, location_key: str = None, flags: list = None):
        super().__init__(key_value, name, descriptions, location_key, flags)
        self.hp = hp
        self.sex = sex
        self.inventory = inventory


class Player(Character):
    def __init__(self, key_value: str, name: str, descriptions: dict, sex: str = "?", hp: int = 100, hpoo: int = 80,
                 inventory: Inventory = None, location_key: str = None, flags: list = None):
        self.hpoo = hpoo
        super().__init__(key_value, name, descriptions, sex, hp, inventory, location_key, flags)

    def go_to(self, location_key: str):
        """sends the player to that room, and does all the appropriate things such as...

        call the room's action routine with M-ENTER, and call the describers. V-WALK, the
        routine which normally handles all movement, calls GOTO; however, there are
        many instances when you will want to call it yourself, such as when the player
        pushes the button in the teleportation booth. Some games allow GOTO to work
        with a vehicle as well as a room.

        Parameters
        ----------
        location_key

        Returns
        -------

        """
        target_location = GameObject.objects_by_key.get(location_key)
        if target_location:
            # player location changed
            # call rooms action routine
            # call describers
            self.location_key = location_key
            return target_location.describe()
        else:
            raise ValueError("Invalid Location Key")

    def do_walk(self, direction):
        """The game will now attempt to walk the player in that direction.

        Notice the
        difference between GOTO and DO-WALK. DO-WALK is just an attempt, and the
        response might be something like "The door to the west is locked." GOTO
        overrides all that, however, and positively sends the player to the given room.

        Parameters
        ----------
        direction: Direction Enum

        Returns
        -------
        str: response

        """
        # print("do walk called")
        obj = GameObject.objects_by_key[self.location_key]
        if isinstance(obj, Room):
            room = obj
            exit = room.exits.get(direction)
            # print(exit.name)
            if exit:
                if Flags.LOCKEDBIT not in exit.flags:
                    #Everything is good move the player
                    return self.go_to(exit.connection)
                else:
                    key = GameObject.objects_by_key.get(exit.key_object)
                    key_name = (" ".join(key.adjectives) + " " + key.name).strip()
                    for item in self.inventory.items:
                        if item == exit.key_object:
                            exit.remove_flag("LOCKEDBIT")
                            exit.add_flag("OPENBIT")
                            self.inventory.remove(item, exit.key_value)

                            return f"The {exit.name} opens with the {key_name}." + self.go_to(exit.connection)

                    return f"The {exit.name} is locked and you don't have the {key_name}."
            else:
                return "There isn't an exit in that direction!"
        else:
            return f"You can't do that from the {obj.name}!"




class NPC(Character):
    pass
