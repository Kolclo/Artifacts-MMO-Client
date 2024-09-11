from api_actions import Get, Post
from data.character import Character
from data.map import Map
from game_state import GameState
from controller import CharacterController
import time
import sys

class Automation:
    def __init__(self, excluded_characters: list[str] = []):
        self.get_request: Get = Get()
        self.characters: list[Character] = self.get_request.characters()
        self.excluded_characters: list[str] = excluded_characters
        self.controllers = []

        for character in self.characters:
            if character.name not in self.excluded_characters:
                character_data = self.get_request.character(character.name)
                map_data_request: Map = self.get_request.map(character_data.x, character_data.y)
                game_data: GameState = GameState(character_data, map_data_request)
                post_request: Post = Post(game_data)
                controller: CharacterController = CharacterController(game_data)
                self.controllers.append(controller)

    def run(self):
        loops = 0
        x = 0

        if loops == 0:
            loops = 9999999999999999999999999999999999999999999999999999999999999999999999999999999

        while x < loops:
            for controller in self.controllers:
                controller.perform_action()
                # controller.move_up()
            x =+ 1
            if loops == x:
                sys.exit()
            time.sleep(30)

if __name__ == "__main__":
    excluded_characters = []
    # excluded_characters.append("Kieran")
    # excluded_characters.append("Shabazz")
    # excluded_characters.append("longnametest")
    # excluded_characters.append("Pog")
    # excluded_characters.append("ChadusRexus")
    automation = Automation(excluded_characters)
    automation.run()