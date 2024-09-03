from data.character import Character

class GameState:
    def __init__(self, character_data, tile_data = None):
        self.character_data = character_data
        self.tile_data = tile_data

    def set_character_data(self, character_data):
        self.character_data = character_data

    def get_character_data(self):
        return self.character_data
    
    def set_tile_data(self, tile_data):
        self.tile_data = tile_data
    
    def get_tile_data(self):
        return self.tile_data