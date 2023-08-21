import re
from texticular.game_loader import load_player, load_game_map, wire_item_action_funcs
from texticular.game_enums import Directions
from texticular.game_object import GameObject

class Parser:
    """A class responsible for attempting to parse player input into a known verb and optionally direct object & indirect object

     The parser splits player input on spaces or certain punctuation into words it then attempts to search the grammar
     for a known verb, remove articles and prepositions and then search the list of game objects for a direct and indirect
     object in the form:

     VERB_PHRASE DIRECT_OBJECT_PHRASE? INDIRECT_OBJECT_PHRASE?

    Attributes
    ----------
    known_commands: list
        the list of known verbs passed in to the parser at initialization
    prepositions: list
        hard coded list of prepositions to be used in identifying indirect objects
        Example: Get the lamp on the table
        ('the' is an article, 'on' is a preposition. Once the articles are removed,
        the indirect object appears directly after the preposition)


     Methods
     ---------

     tokenize(self, user_input: str, game_objects: dict):
        attempt to parse the player input and return a ParseTree object that contains the resulting parsed tokens
        or at the very least a ParseTree object that contains a response explaining why the input could not be parsed
    """
    def __init__(self, known_verbs):
        self.actions = known_verbs
        self.prepositions = ["in", "on", "at", "from"]
        # through, inside, up, under, over, beside, below, down ...{the apple}

    def tokenize(self, user_input: str):
        parse_tree = ParseTree()
        parse_tree.unparsed_input = user_input
        # To split a string with multiple delimiters in Python, use the re.split() method.
        # The re.split() function splits the string by each occurrence of the pattern
        delimiters = "[\s,!\.\?]"
        parse_tree.tokens = re.split(delimiters, parse_tree.unparsed_input.lower())
        # split on the delimiters and remove any empty entries
        parse_tree.tokens  = [token.strip() for token in parse_tree.tokens if token]
        return parse_tree


    def get_verb(self, parse_tree):
        # Search for the Verb
        offset = -1

        for index, part in enumerate(parse_tree.tokens):
            command_name = " ".join(parse_tree.tokens[0:index + 1])
            if command_name in self.actions:
                parse_tree.action = command_name
                offset = index + 1
        return offset


    def parse_input(self, user_input):
        parse_tree = self.tokenize(user_input)
        if len(parse_tree.tokens) == 0:
            parse_tree.response = "Command is Empty"
            return parse_tree

        verb_offset = self.get_verb(parse_tree)
        if verb_offset == -1:
            # exit early command did not start with a known verb
            parse_tree.response = f'''Command: "{parse_tree.unparsed_input}" does not start with a known verb.'''
            return parse_tree

        # The rest of the input after the verb has been extracted
        # Remove articles
        remaining_input = [token for token in parse_tree.tokens[verb_offset:] if token not in ["a", "an", "the"]]

        return parse_tree



class ParseTree:
    def __init__(self):
        self.unparsed_input = None
        self.tokens = []
        self.action = None
        self.direct_object_key = None
        self.indirect_object_key = None
        self.input_parsed = False
        self.response = None

    def __repr__(self):
        return f"""
        Parse Tree
        -----------
        unparsed_input: {self.unparsed_input}
        tokens: {str(self.tokens)}
        action: {self.action}
        direct_object_key: {self.direct_object_key}
        indirect_object_key:  {self.indirect_object_key}
        input_parsed: {str(self.input_parsed)}
        response = {self.response}
        """


if __name__ == "__main__":
    gamemap = load_game_map("./../../data/GameConfigManifest.json")
    print(GameObject.objects_by_key)
    parser = Parser(["walk", "look", "turn off", "pick up", "drop"])
    parse_tree = parser.parse_input("Walk East")
    print(parse_tree)
    parse_tree = parser.parse_input("Turn off the light!")
    print(parse_tree)
    parse_tree = parser.parse_input("Hey, Drop that candlestick!")
    print(parse_tree)


