from texticular.game_loader import load_game_map

def test_can_load_game_map():
    gamemap = load_game_map("../data/initialGameMap.json")
    print()
    print(gamemap.keys())

