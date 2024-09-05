from character_selection import CharacterSelector
from data.character import Character
from data.map import Map
from mapper import Game
from api_actions import Get
from game_state import GameState
import sys

def main() -> None:
    """Main entry point for the game.

    Performs initial setup of requests, checks if the server is online, and then
    initiates the character selection menu. After the character has been selected,
    the game data is retrieved and used to create a Game object, which is then
    run until the game loop is exited.
    """
    # Sets up requests
    get_request: Get = Get()

    # Checks whether server is online
    server_status = get_request.server_status()
    if not server_status["status"] == "online":
        print("Server is offline. Please try again later.")
        sys.exit()
    print("Server is online! Continuing game initialisation.")

    # Initiates character selection menu
    character_selector: CharacterSelector = CharacterSelector()
    selected_character: Character = character_selector.run()

    # Gets chosen character's current tile data
    map_data_request: Map = get_request.map(selected_character.x, selected_character.y)

    # Get data about characters current location
    game_data: GameState = GameState(selected_character, map_data_request)

    if selected_character:
        game: Game = Game(game_data)
        game.run()

        sys.exit()

if __name__ == "__main__":
    main()