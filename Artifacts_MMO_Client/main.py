from character_chooser import character_selection
from controller import CharacterController
from mapper import Game
import pygame
import sys

def main():
    selected_character = None
    while True:
        if selected_character is None:
            selected_character = character_selection()
            print(f"Selected character: {selected_character['name']}")
        if selected_character is not None:
            game = Game()
            game.run()

            # Create a new CharacterController instance with the selected character's name
            controller = CharacterController(selected_character['name'])
            controller.run()
            print("Closing controller")
            
            sys.exit()

if __name__ == "__main__":
    main()