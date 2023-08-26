from __future__ import annotations
from typing import TYPE_CHECKING
from texticular.game_enums import *
from texticular.globals import *

if TYPE_CHECKING:
    from texticular.game_controller import Controller
    from texticular.game_object import GameObject


def action_room201(context: str = "M-ENTER") -> bool:
    CONTROLLER.response.extend(["Room action for Room 201 called!"])
    CONTROLLER.response.extend([f"visited the bathroom {CONTROLLER.player.location.times_visited} times"])
    return False

def action_bathroom_room201(context: str = "M-ENTER") -> bool:
    CONTROLLER.response.extend(["Room action for Bathroom Room 201 called!"])
    CONTROLLER.response.extend([f"visited the bathroom {CONTROLLER.player.location.times_visited} times"])
    return False

