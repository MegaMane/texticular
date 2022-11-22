# https://adamj.eu/tech/2021/05/13/python-type-hints-how-to-fix-circular-imports/
# https://stackoverflow.com/questions/39740632/python-type-hinting-without-cyclic-imports
from __future__ import annotations
from typing import TYPE_CHECKING
from texticular.game_enums import *
from collections import namedtuple

if TYPE_CHECKING:
    from texticular.game_controller import Controller


def look(controller: Controller):
    controller.response.extend(controller.player.location.describe())
    return True


def walk(controller: Controller):
    walk_direction = controller.tokens.direct_object_key
    controller.response.extend(controller.player.do_walk(walk_direction))
    return True


def take(controller: Controller):
    item = controller.tokens.direct_object
    inventory = controller.player.inventory

    if item.is_present(controller.player.location):
        # TODO
        # Change item.is_present to check if the item is present in any open containers in the players current location

        if Flags.TAKEBIT in item.flags:

            item_taken = inventory.add_item(item)
            if item_taken:
                controller.player.location.items.remove(item)
                item.move(inventory.location_key)
                item.current_description = "Main"
                controller.response.append("Taken.")
                return True
            else:
                controller.response.append((f"The  {item.name} won't fit in your {inventory.name}! "
                                            f"Try dropping something if you really want it."))
        else:
            controller.response.append(f"The {item.name} won't budge.")

        return False
    else:
        controller.response.append(f"You don't see a {item.name} here!")
        return False


def drop(controller: Controller):
    item = controller.tokens.direct_object
    inventory = controller.player.inventory
    if inventory.remove_item(item):
        item.move(controller.player.location_key)
        controller.player.location.items.append(item)
        item.current_description = "Dropped" if item.descriptions.get("Dropped") else "Main"
        controller.response.append("Dropped it like it's hot.")
        return True
    else:
        controller.response.append(f"You don't have a {item.name} to drop.")
        return False


def inventory(controller: Controller):
    controller.response.extend(controller.player.inventory.look_inside())
    return True


def talk(controller):
    pass
