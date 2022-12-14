import texticular.actions.verb_actions as va
from texticular.game_object import GameObject
from texticular.rooms.room import Room
from texticular.game_enums import Directions
from texticular.character import Player,NPC
from dataclasses import dataclass
from texticular.game_enums import GameStates
import textwrap

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
        self.response = []
        self.set_commands()
        self.tokens = self.Tokens("", "", None, "", None)
        self.gamestate = GameStates.EXPLORATION
        self.player = player


    def go(self):
        #https://patorjk.com/software/taag/#p=display&v=1&f=Standard&t=Texticular%3A%20Chapter%201%0AYou%20Gotta%20Go!
        #'Standard' Font
        intro_text = (
            """
  _____         _   _            _                 ____ _                 _              _ 
 |_   _|____  _| |_(_) ___ _   _| | __ _ _ __ _   / ___| |__   __ _ _ __ | |_ ___ _ __  / |
   | |/ _ \ \/ / __| |/ __| | | | |/ _` | '__(_) | |   | '_ \ / _` | '_ \| __/ _ \ '__| | |
   | |  __/>  <| |_| | (__| |_| | | (_| | |   _  | |___| | | | (_| | |_) | ||  __/ |    | |
   |_|\___/_/\_\\__|_|\___|\__,_|_| \__,_|_|  (_)  \____|_| |_|\__,_| .__/ \__\___|_|    |_|
 __   __             ____       _   _           ____       _       |_|                     
 \ \ / /__  _   _   / ___| ___ | |_| |_ __ _   / ___| ___ | |                              
  \ V / _ \| | | | | |  _ / _ \| __| __/ _` | | |  _ / _ \| |                              
   | | (_) | |_| | | |_| | (_) | |_| || (_| | | |_| | (_) |_|                              
   |_|\___/ \__,_|  \____|\___/ \__|\__\__,_|  \____|\___/(_)                              
                                                                                           
            """

        )

        print(intro_text)
        self.commands["look"](self)
        return self.render()
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
            target_object = self.tokens.indirect_object
            custom_action_method_exists = target_object.action_method_name
            if custom_action_method_exists:
                print("indirect object handler")
                if target_object.action(controller=self, target=target_object):
                    return True

        #If that doesn't work try giving the direct object a change to handle the input
        if direct_object:
            target_object = self.tokens.direct_object
            custom_action_method_exists = target_object.action_method_name
            if custom_action_method_exists:
                print("direct object handler")
                if target_object.action(controller=self, target=target_object):
                    return True

        # fall through to the most generic verb response
        print("generic verb handler")
        return self.commands[verb](controller=self)

    def get_game_object(self, key_value: str) -> GameObject:
        game_object = GameObject.objects_by_key.get(key_value)
        return game_object

    def get_input(self):
        self.response = []
    def parse(self) ->bool:
        return True
    def update(self):
        if self.parse():
            self.handle_input()
            self.clocker()
    def render(self):
        formatted_output = ''
        for line in self.response:
            if line.endswith("\n"):
                formatted_output += line
            else:
                formatted_output += "\n".join(
                    textwrap.wrap(
                        line,
                        width=150,
                        replace_whitespace=False,
                        break_long_words=False,
                        break_on_hyphens=False
                    )
                ) + "\n"

        formatted_output += f'\n\n{"-" * 150}'
        return formatted_output

    def clocker(self):
        pass
    def main_loop(self):
        pass

    def set_commands(self):
        self.commands["look"] = va.look
        self.commands["walk"] = va.walk
        self.commands["get"] = va.take
        self.commands["take"] = va.take
        self.commands["drop"] = va.drop
        self.commands["open"] = va.open
        self.commands["close"] = va.close
        self.commands["put"] = va.put
        self.commands["inventory"] = va.inventory


