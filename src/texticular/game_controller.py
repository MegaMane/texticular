import texticular.actions.verb_actions as va
from texticular.game_object import  GameObject
from texticular.rooms.room import Room
from texticular.game_enums import Directions
from texticular.character import Player,NPC
from dataclasses import dataclass
from texticular.game_enums import GameStates

class Controller:
    # def __new__(cls, gamemap: dict, player: Player):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super(Controller, cls).__new__(cls, gamemap, player)
    #     return cls.instance
    @dataclass
    class Tokens:
        action: str
        direct_object_key: str
        direct_object: GameObject
        indirect_object_key: str
        indirect_object: GameObject

    def __init__(self, gamemap: dict[str, Room], player: Player):
        self.gamemap = gamemap
        self.commands = {}
        self.globals = {}
        self.response = ""
        self.set_commands()
        self.tokens = self.Tokens("", "", None, "", None)
        self.gamestate = GameStates.EXPLORATION
        self.player = player
        self.player_location = GameObject.objects_by_key.get(self.player.location_key)


    def go(self):
        return self.player_location.describe()
    def handle_input(self) ->bool:
        tokens = self.tokens
        # print("handle input called")
        # print(vars(tokens))
        verb = tokens.action
        direct_object= tokens.direct_object_key
        indirect_object = tokens.indirect_object

        if isinstance(tokens.direct_object_key, Directions):
            # print("is instance of direction")
            return self.commands[verb](controller=self)


        #Try letting the indirect object handle the input first
        if indirect_object:
            target_object = self.game_objects[indirect_object]
            action = target_object.commands.get("Action")
            if action:
                print("indirect object handler")
                if action(self, target=target_object):
                    return True

        #If that doesn't work try giving the direct object a change to handle the input
        if direct_object:
            target_object = self.game_objects[direct_object]
            action = target_object.commands.get("Action")
            if action:
                print("direct object handler")
                if action(self, target=target_object):
                    return True

        # fall through to the most generic verb response
        print("generic verb handler")
        return self.commands[verb](controller=self)

    def get_input(self):
        pass
    def parse(self) ->bool:
        return True
    def update(self):
        if self.parse():
            self.handle_input()
            self.clocker()
    def render(self):
        return self.response + "\n--------------------------------------------------------"

    def clocker(self):
        pass
    def main_loop(self):
        pass

    def set_commands(self):
        self.commands["take"] = va.take
        self.commands["walk"] = va.walk

