from data.character import Character
from data.map import Map

class GameState:
    def __init__(self, character_data: Character, tile_data: Map = None):
        self.character_data = character_data
        self.tile_data = tile_data

    def set_character_data(self, character_data: Character):
        self.character_data = character_data

    def get_character_data(self):
        return self.character_data
    
    def set_tile_data(self, tile_data: Map):
        self.tile_data = tile_data
    
    def get_tile_data(self):
        return self.tile_data