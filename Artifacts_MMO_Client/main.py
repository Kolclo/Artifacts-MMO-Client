from character_selection import character_selection
from controller import CharacterController
from mapper import Game
from api_actions import Get
import sys

def main():
    # Sets up requests for later use
    get_request = Get()

    # Checks whether server is online
    server_status = get_request.server_status()
    if not server_status["status"] == "online":
        print("Server is offline. Please try again later.")
        sys.exit()
    print("Server is online! Continuing game initialisation.")

    # Initiates character selection menu
    selected_character = character_selection()

    # Gets chosen character's data
    character_data = get_request.character(selected_character.name)

    if selected_character:
        game = Game(character_data)
        game.run()

        # Create a new CharacterController instance with the selected character's name
        controller = CharacterController(selected_character.name)
        controller.run()
        print("Closing controller")
        
        sys.exit()

if __name__ == "__main__":
    main()