# https://adamj.eu/tech/2021/05/13/python-type-hints-how-to-fix-circular-imports/
# https://stackoverflow.com/questions/39740632/python-type-hinting-without-cyclic-imports
from __future__ import annotations
from typing import TYPE_CHECKING
from texticular.game_enums import *
from collections import namedtuple

if TYPE_CHECKING:
    from texticular.game_controller import Controller


def look(controller:Controller):
    pass

def walk(controller:Controller):
    walk_direction = controller.tokens.direct_object_key
    controller.response += controller.player.do_walk(walk_direction)
    return True

def take(controller: Controller):
    direct_object = controller.tokens.direct_object
    #TODO
    # Check if the item is visible
    # Check if the item is in the same location as the player (or in a container in that location)

    inventory = controller.player.inventory

    if Flags.TAKEBIT in direct_object.flags:
        item = controller.tokens.direct_object
        item_taken = inventory.add_item(item)
        if item_taken:
            item.move(inventory.location_key)
            item.current_description = "Main"
            controller.response += "Taken."
            return True
        else:
            controller.response += (f"The  {direct_object.name} won't fit in your {inventory.name}! "
                                    f"Try dropping something if you really want it.")
    else:
        controller.response += (f"The {direct_object.name} won't budge." )

    return False

def drop(controller):
    pass

def inventory(controller: Controller):
    controller.response += controller.player.inventory.describe()
    return True

def talke(controller):
    pass
