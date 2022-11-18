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

