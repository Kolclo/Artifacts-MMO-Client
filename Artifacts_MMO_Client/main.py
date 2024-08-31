from character_chooser import character_selection
from controller import CharacterController
from mapper import Game
from api_actions import get
import sys

def main():
    # Sets up requests for later use
    get_request = get()

    # Checks whether server is online
    server_status = get_request.server_status()
    if not server_status["status"] == "online":
        print("Server is offline. Please try again later.")
        sys.exit()
    print("Server is online! Continuing game initialisation.")

    # Initiates character selection menu
    selected_character = character_selection()
    # print(f"Selected character: {selected_character['name']}")

    if selected_character:
        game = Game()
        game.run()

        # Create a new CharacterController instance with the selected character's name
        controller = CharacterController(selected_character.name)
        controller.run()
        print("Closing controller")
        
        sys.exit()

if __name__ == "__main__":
    main()