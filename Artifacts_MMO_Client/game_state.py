from data.character import Character
from data.map import Map

class GameState:
    def __init__(self, character_data: Character, tile_data: Map = None):
        """
        Initialises the game state with the given character and tile data.

        Args:
            character_data (Character): The character object to be stored in the game state
            tile_data (Map, optional): The tile data object to be stored in the game state. Defaults to None.
        """
        self.character_data = character_data
        self.tile_data = tile_data