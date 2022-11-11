import json
import os
import json

with open("../../data/rooms.json") as json_file:
    config = json.load(json_file)

print(json.dumps(config, indent=4))
class GameLoader:
    def load_json(json_file_path):
        with open(json_file_path) as json_file:
            config = json.load(json_file)
        return config

    def readFromFile(self, filePath):
        if not os.path.exists(filePath):
            raise FileNotFoundError

        infile = open(filePath, "r")
        line = infile.readline()
        infile.close()
        return line
