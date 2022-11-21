from texticular.game_object import GameObject
from texticular.game_enums import Flags
class StoryItem(GameObject):
    def __init__(self, key_value: str, name: str, descriptions: dict, synonyms: list,
                 adjectives: list = None, size: int = 1, location_key: str = None, flags: list = None):
        self.synonyms = synonyms
        self.adjectives = adjectives
        self.size = size

        if adjectives is None:
            self.adjectives = []

        super().__init__(key_value, name, descriptions, location_key, flags)

    def encode_tojson(self, o):
        """Serialize Story Item to Json

        """

        return {
            "type": self.__class__.__name__,
            "keyValue": self.key_value,
            "locationKey": self.location_key,
            "name": self.name,
            "synonyms": self.synonyms,
            "adjectives": self.adjectives,
            "currentDescription": self._current_description,
            "examineDescription": self._examine_description,
            "descriptions": self.descriptions,
            "size": self.size,
            "flags": [flag.name for flag in self.flags],
            "actionMethod": self.action_method_name
        }

    def is_present(self, room) -> bool:
        """Check if the item is present in the provided location or
         any open containers in the provided location and visible

        Parameters
        ----------
        room: Room
            The room to search for the item
        """
        return (self.location_key == room.key_value and Flags.INVISIBLE not in self.flags )

class Container(StoryItem):
    def __init__(self, key_value: str, name: str, descriptions: dict, synonyms: list, adjectives: list = None,
                 slots: int = 10, location_key: str = None, key_object=None, flags: list = [Flags.CONTAINERBIT]):
        super().__init__(key_value, name, descriptions, synonyms, adjectives, size=99,
                         location_key=location_key, flags=flags)
        self.slots = slots
        self.slots_occupied = 0
        self.key_object = key_object
        self.items = []

    def add_item(self, item: StoryItem) -> bool:
        if item.size + self.slots_occupied <= self.slots:
            self.slots_occupied += item.size
            self.items.append(item)
            item.location_key = self.key_value
            return True
        return False

    def remove_item(self, item: StoryItem) -> bool:
        if item in self.items:
            self.slots_occupied -= item.size
            self.items.remove(item)
            item.location_key = None
            return True
        return False

    def open(self, key_object=None):
        if Flags.LOCKEDBIT in self.flags and key_object.key_value != self.key_object:
            return False
        else:
            self.add_flag(Flags.OPENBIT)
            return  True

    def close(self):
        self.remove_flag(Flags.OPENBIT)
        return True

    def look_inside(self) -> str:
        response = []
        response.append(f"You look inside the {self.name} and see...")
        response.append("\n" + ("-" * len(response[0])) + "\n\n")
        for item in self.items:
            response.append(f"{item.name}: {item.describe()}")

        return response

class Inventory(Container):
    def __init__(self, key_value: str, name: str, descriptions: dict, synonyms: list, adjectives: list = None,
                 slots: int = 10, location_key: str = None, flags: list = [Flags.CONTAINERBIT, Flags.OPENBIT]):
        super().__init__(key_value, name, descriptions, synonyms, adjectives,
                         slots, location_key, key_object=None, flags=flags)

    def look_inside(self) -> str:
        response = []
        response.append(f"{self.name}: {super().describe()}")
        response.append("\n" + ("-" * (len(self.name) + len(super().describe()) + 2)) + "\n\n")
        for item in self.items:
            response.append(f"{item.name}: {item.describe()}")

        return response

if __name__ == "__main__":
    import json
    masterKey = StoryItem(
        key_value="masterKey",
        name="Master Key",
        location_key="nowhereLand",
        descriptions={"Main": "The key that opens every door"},
        synonyms=["Bad Mother Fuckin' Key"],
        flags=[Flags.KLUDGEBIT]

    )

    print(json.dumps(masterKey, indent=4, default=masterKey.encode_tojson))

