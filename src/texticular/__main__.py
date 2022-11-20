from game_controller import  Controller
import textwrap
#These imports should go away after testing
from texticular.game_loader import load_game_map, load_game_objects, load_player
from texticular.game_enums import Directions
from texticular.game_object import GameObject

gamemap = load_game_map("./../../data/initialGameMap.json")
storyitems = load_game_objects(gamemap, "./../../data/items.json")
player = load_player()

controller = Controller(gamemap, player)


def input_generator(input_commands):
    """Generate perfectly parsed input for testing"""
    for command in input_commands:
        yield command

def parse(input_generator):
    """Generate perfectly parsed input for testing"""
    return next(input_generator)

def display(output):
    print("\n".join(textwrap.wrap(output, width=150, replace_whitespace=False)))
    print("-" * 150)

display(controller.go())

walk_commands = [
    {
        "action": "walk",
        "direct_object_key": Directions.WEST,
        "direct_object": "WEST",
        "indirect_object_key": None,
        "indirect_object": None,
        "user_input": "User Input: Go West"
    },
    {
        "action": "walk",
        "direct_object_key": Directions.EAST,
        "direct_object": "EAST",
        "indirect_object_key": None,
        "indirect_object": None,
        "user_input": "User Input: Go East"
    },
    {
        "action": "take",
        "direct_object_key": "intro-note",
        "direct_object": GameObject.objects_by_key.get("intro-note"),
        "indirect_object_key": None,
        "indirect_object": None,
        "user_input": "User Input: Take note"
    },
    {
        "action": "inventory",
        "direct_object_key": None,
        "direct_object": None,
        "indirect_object_key": None,
        "indirect_object": None,
        "user_input": "User Input: Inventory"
    }

]

test_walk = input_generator(walk_commands)

while controller.gamestate.name != "GAMEOVER":
    controller.get_input()
    try:
        tokens = parse(test_walk)
        controller.tokens.action = tokens["action"]
        controller.tokens.direct_object = tokens["direct_object"]
        controller.tokens.direct_object_key = tokens["direct_object_key"]
        controller.tokens.indirect_object = tokens["indirect_object"]
        controller.tokens.indirect_object_key = tokens["indirect_object_key"]
        controller.update()
        display(tokens["user_input"])
        display(controller.render())
    except StopIteration:
        print("Reached End of Command Sequence")
        break





