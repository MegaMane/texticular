from game_controller import  Controller
from texticular.game_loader import load_game_map, load_game_objects, load_player
from texticular.game_enums import Directions
import textwrap

gamemap = load_game_map("./../../data/initialGameMap.json")
storyitems = load_game_objects("./../../data/items.json")
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

display(controller.go())

walk_commands = [
    {
        "action": "walk",
        "direct_object_key": Directions.WEST,
        "direct_object": "WEST",
        "indirect_object_key": None,
        "indirect_object": None
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
        display(controller.render())
    except StopIteration:
        print("Reached End of Command Sequence")
        break





