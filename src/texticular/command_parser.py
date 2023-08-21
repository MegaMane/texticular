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

    def expand_adjectives(self, adjective_list):
        """
        Generate all possible combinations of adjectives given a list of adjectives containig 0-3 elements.

        Args:
            adjective_list (list): A list of adjectives to be combined max len = 3.

        Returns:
            list: A list containing individual adjectives and all possible combinations
                  of adjectives from the input list.

        Example:
            >>> input_array = ["Tiny", "Sour", "Yellow"]
            >>> result = expand_adjectives(input_array)
            >>> print(result)
            ['Sour', 'Sour Tiny', 'Sour Tiny Yellow', 'Sour Yellow', 'Sour Yellow Tiny', 'Tiny', 'Tiny Sour',
            'Tiny Sour Yellow', 'Tiny Yellow', 'Tiny Yellow Sour', 'Yellow', 'Yellow Sour',
            'Yellow Sour Tiny', 'Yellow Tiny', 'Yellow Tiny Sour']
        """
        combinations = []

        for i in range(len(adjective_list)):
            # Add individual adjective
            combinations.append(adjective_list[i])

            for j in range(i + 1, len(adjective_list)):
                # Combine with the next adjective
                combinations.append(f"{adjective_list[i]} {adjective_list[j]}")
                combinations.append(f"{adjective_list[j]} {adjective_list[i]}")

                for k in range(j + 1, len(adjective_list)):
                    # Combine with the next adjective again
                    combinations.append(f"{adjective_list[i]} {adjective_list[j]} {adjective_list[k]}")
                    combinations.append(f"{adjective_list[i]} {adjective_list[k]} {adjective_list[j]}")
                    combinations.append(f"{adjective_list[j]} {adjective_list[i]} {adjective_list[k]}")
                    combinations.append(f"{adjective_list[j]} {adjective_list[k]} {adjective_list[i]}")
                    combinations.append(f"{adjective_list[k]} {adjective_list[i]} {adjective_list[j]}")
                    combinations.append(f"{adjective_list[k]} {adjective_list[j]} {adjective_list[i]}")

        return sorted(combinations)

    def get_possible_matches(self, synonyms, adjectives):
        """
        Generate all possible combinations of synonyms and adjectives.

        Args:
            synonyms (list): A list of synonyms.
            adjectives (list): A list of adjectives.

        Returns:
            list: A list containing all possible combinations of adjectives and synonyms.

        Example:s
            >>> synonyms = ["Ear Plugs"]
            >>> adjectives = ["Crusty", "Yellow"]
            >>> matches = self.get_possible_matches(synonyms, adjectives)
            >>> print(matches)
            ['Crusty Ear Plugs', 'Crusty Yellow Ear Plugs', 'Yellow Ear Plugs', 'Yellow Crusty Ear Plugs']
        """
        expanded_adjectives = self.expand_adjectives(adjectives)
        matches = [f'{adj} {syn}' for adj in expanded_adjectives for syn in synonyms]
        return matches


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


