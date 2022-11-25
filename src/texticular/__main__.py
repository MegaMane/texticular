from game_controller import Controller
import textwrap
#These imports should go away after testing
from texticular.game_loader import load_player, load_game_map, wire_item_action_funcs
from texticular.game_enums import Directions
from texticular.game_object import GameObject


gamemap = load_game_map("./../../data/newGameManifest.json")
player = load_player()
wire_item_action_funcs()

controller = Controller(gamemap, player)


def input_generator(input_commands):
    """Generate perfectly parsed input for testing"""
    for command in input_commands:
        yield command

def parse(input_generator):
    """Generate perfectly parsed input for testing"""
    return next(input_generator)


walk_commands = [
    {
        "action": "look",
        "direct_object_key": "room201-nightStand",
        "direct_object": GameObject.objects_by_key.get("room201-nightStand"),
        "indirect_object_key": None,
        "indirect_object": None,
        "user_input": "User Input: Look Night Stand",
        "notes": "Look at the Night Stand instead of the whole room"
    },
    {
        "action": "take",
        "direct_object_key": "crustyEarPlugs",
        "direct_object": GameObject.objects_by_key.get("crustyEarPlugs"),
        "indirect_object_key": None,
        "indirect_object": None,
        "user_input": "User Input: Take Ear Plugs",
        "notes": "Try to take an item from a closed container"
    },
    {
        "action": "open",
        "direct_object_key": "room201-nightStand",
        "direct_object": GameObject.objects_by_key.get("room201-nightStand"),
        "indirect_object_key": None,
        "indirect_object": None,
        "user_input": "User Input: Open Night Stand",
        "notes": "Open the night stand drawer to see what is inside"
    },
    {
        "action": "take",
        "direct_object_key": "crustyEarPlugs",
        "direct_object": GameObject.objects_by_key.get("crustyEarPlugs"),
        "indirect_object_key": None,
        "indirect_object": None,
        "user_input": "User Input: Take Ear Plugs",
        "notes": "Try to take an item from an open container"
    },
    {
        "action": "open",
        "direct_object_key": "room201-nightStand-drawer",
        "direct_object": GameObject.objects_by_key.get("room201-nightStand-drawer"),
        "indirect_object_key": None,
        "indirect_object": None,
        "user_input": "User Input: Look Little Wooden Drawer",
        "notes": "Open the Drawer and there is nothing inside"
    },
    {
        "action": "walk",
        "direct_object_key": Directions.WEST,
        "direct_object": "WEST",
        "indirect_object_key": None,
        "indirect_object": None,
        "user_input": "User Input: Go West",
        "notes": "Try to use the Bathroom and discover the Great Dane."
    },
    {
        "action": "walk",
        "direct_object_key": Directions.EAST,
        "direct_object": "EAST",
        "indirect_object_key": None,
        "indirect_object": None,
        "user_input": "User Input: Go East",
        "notes": "retreat back to the bedroom"
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
    },
    {
        "action": "walk",
        "direct_object_key": Directions.EAST,
        "direct_object": "EAST",
        "indirect_object_key": None,
        "indirect_object": None,
        "user_input": "User Input: Go East",
        "notes": "Go to the west hallway"
    },
    {
        "action": "drop",
        "direct_object_key": "intro-note",
        "direct_object": GameObject.objects_by_key.get("intro-note"),
        "indirect_object_key": None,
        "indirect_object": None,
        "user_input": "User Input: Drop Note",
        "notes": "Try Dropping the note"
    },
    {
        "action": "look",
        "direct_object_key": None,
        "direct_object": None,
        "indirect_object_key": None,
        "indirect_object": None,
        "user_input": "User Input: Look",
        "notes": "Look at surroundings and verify note is now in west hallway"
    }


]

test_walk = input_generator(walk_commands)

print(controller.go())
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
        print(tokens["user_input"])
        print('-' * 150)
        print(controller.render())
        #print(controller.render())
    except StopIteration:
        print("Reached End of Command Sequence")
        break





