from character_selection import character_selection
from controller import CharacterController
from mapper import Game
from api_actions import Get
from game_state import GameState
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

    # Gets chosen character's data and current tile data
    character_data_request = get_request.character(selected_character.name)
    map_data_request = get_request.map(character_data_request.x, character_data_request.y)
    print(map_data_request)
    print(map_data_request.content.type)

    # Get data about characters current location
    game_data = GameState(character_data_request, map_data_request)


    if selected_character:
        game = Game(game_data)
        game.run()

        sys.exit()

if __name__ == "__main__":
    main()