from __future__ import annotations
from typing import TYPE_CHECKING
from texticular.game_enums import *

if TYPE_CHECKING:
    from texticular.game_controller import Controller
    from texticular.game_object import GameObject


def action_nightstand(controller: Controller, target: GameObject) -> bool:
    target.action_method_name = "action_nightstand"
    if controller.tokens.action == "open":
        # Redirect from the prop to the actual container then call the stock open method
        drawer = controller.get_game_object("room201-nightStand-drawer")
        controller.tokens.direct_object = drawer
        controller.tokens.direct_object = drawer.key_value
        controller.commands["open"](controller)
    return False

def action_couch(controller: Controller, target: GameObject) -> bool:
    target.action_method_name = "action_couch"
    tokens = controller.tokens
    couch = target
    if tokens.verb == "sit":
        couch.current_description = couch.descriptions["Sitting"]
        controller.response.append("You sit on the couch.")
        controller.response.extend(controller.player.go_to(couch.key_value))
        return True
    elif tokens.verb in ["stand", "get off", "get up"]:
        couch.current_description = couch.descriptions["Main"]
        controller.response.append("You get off the couch.")
        controller.response.extend(controller.player.go_to(couch.location_key))
        return True
    return False
