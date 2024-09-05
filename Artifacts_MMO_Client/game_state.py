from data.character import Character
from data.map import Map

class GameState:
    def __init__(self, character_data: Character, tile_data: Map = None):
        self.character_data = character_data
        self.tile_data = tile_data