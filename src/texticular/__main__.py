import json
with open("../../data/rooms.json") as json_file:
    config = json.load(json_file)

print(json.dumps(config, indent=4))