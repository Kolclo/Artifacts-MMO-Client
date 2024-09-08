from main_menu import MainMenu
from character_selection import CharacterSelector
from data.character import Character
from data.map import Map
from mapper import Game
from api_actions import Get
from game_state import GameState
from data.options import Options
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
    get_request.server_status()

    # Loads user options
    settings: Options = Options()

    # Initiates main menu
    main_menu: MainMenu = MainMenu(settings)
    continue_game = main_menu.run()
    if not continue_game:
        sys.exit()

    # Initiates character selection menu
    character_selector: CharacterSelector = CharacterSelector(settings)
    selected_character: Character = character_selector.run()

    # Gets chosen character's current tile data
    map_data_request: Map = get_request.map(selected_character.x, selected_character.y)

    # Stores data
    game_data: GameState = GameState(selected_character, map_data_request)

    if selected_character:
        game: Game = Game(game_data, settings)
        game.run()

        sys.exit()

if __name__ == "__main__":
    main()