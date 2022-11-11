from itertools import count
from texticular.game_enums import Flags


class GameObject:
    """A Base Class representing a generic game object

    Provides some basic functionality for commands that can be used on all objects (i.e. Look and Examine).
    As well as a class level dictionary that keeps track of all game objects that are instantiated.

    Attributes
    -----------
    attribute1: list
        a list of dictionaries in the form of {col: val} for each successfully parsed item

    Methods
    ---------
    __init__()
        The constructor for the GameObject Class

    """

    _objectid = count(1)
    objects_by_key = {}

    @classmethod
    def lookup_by_key(cls, key_value:str):
        return cls.objects_by_key .get(key_value)


    def __init__(self, key_value: str, name: str, descriptions: dict, location_key=None, flags=[]):
        self.id = next(GameObject._objectid)
        self.name = name
        self.descriptions = descriptions
        self.location_key = location_key
        self.flags = set()
        for flag in flags:
            self.add_flag(flag)

        if descriptions.get("Main"):
            self._current_description = descriptions["Main"]
        else:
            self._current_description = self.name
        if descriptions.get("Examine"):
            self._examine_description = descriptions["Examine"]
        else:
            self._examine_description = "..."

        duplicate_object = GameObject.lookup_by_key(key_value)
        if duplicate_object:
            raise ValueError(f"Each game object must have a unique key value. {key_value} already exists on "
                             f"Object: {duplicate_object.name}:"
                             f" {duplicate_object.key_value}")
        else:
            self.key_value = key_value
            GameObject.objects_by_key[key_value] = self

    def __str__(self):
        return self.name

    @property
    def current_description(self):
        return self._current_description
    @current_description.setter
    def current_description(self, descript_key):
        self._current_description = self.descriptions[descript_key]

    @property
    def examine_description(self):
        return self._examine_description
    @examine_description.setter
    def examine_description(self, descript_key):
        self._examine_description = self.descriptions[descript_key]

    def describe(self) -> str:
        """Return the current description of the game object

        Returns
        -------
        str
            the current description of the game object
        """
        return self._current_description

    def examine(self) -> str:
        """Return the more detailed description of the game object

        Returns
        -------
        str
            A more detailed description of the game object if one is available
        """
        return self._examine_description

    def move(self, location_key:str):
        """Puts object1 into object2.
         Example:
             bread.move("toaster")
         """
        if GameObject.lookup_by_key(location_key):
            self.location_key = location_key
        else:
            raise ValueError(f"Invalid location Key provided {location_key}")

    def remove(self):
        """Remove the object from the game setting its location to None

         Examples
         ----------
         >>> skeleton_key.remove()
         >>> print(skeleton_key.location_key)
         None

         """
        self.location_key = None

    def add_flag(self, flag:str):
        """Attempt to add a flag attribute to a game object if it is a valid member of the Flags Enum.

        Parameters
        ----------
        flag:str
            The flag to be added to the game object
        """
        flags = [member.name for member in Flags]
        if flag in flags:
            self.flags.add(flag)
        else:
            raise ValueError(f"Flag {flag} does not exist in game_enums.Flags.")

    def remove_flag(self, flag) -> bool:
        """Remove a flag enum attribute from the game object if it is found in the flags set else return false

        Parameters
        ----------
        flag:str
            The flag to be removed from the game object

        """
        try:
            self.flags.remove(flag)
            return True
        except KeyError:
            return False


    def action(self, func):
        def wrapper_action(*args, **kwargs):
            func( *args, **kwargs)
        return wrapper_action

