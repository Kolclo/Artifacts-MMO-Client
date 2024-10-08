import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Hides Pygame welcome message

import pygame
from api_actions import Get
from controller import CharacterController
from game_state import GameState
from pygame_util import PygameUtils
from event_handler import EventHandler
from data.options import Options
from data.map import Map
import pygame_gui

class CharacterSprite:
    def __init__(self, game_state, tile_size) -> None:
        self.game_state = game_state
        self.x: int = self.game_state.character_data.x + 5
        self.y: int = self.game_state.character_data.y + 5
        self.skin: str = self.game_state.character_data.skin
        self.sprite: pygame.surface.Surface = pygame.image.load(f"Artifacts_MMO_Client/resources/characters/{self.skin}.png")
        self.sprite = pygame.transform.scale(self.sprite, (30, 40))
        self.offset_x = (50 - self.sprite.get_width()) // 2
        self.offset_y = (50 - self.sprite.get_height()) // 2
        self.tile_size = tile_size

    def draw(self, surface: pygame.surface.Surface) -> None:
        """Draws the character sprite on the given window at the correct position.

        This function first calculates the offset needed to center the sprite on the tile.
        Then it draws the sprite at the correct position using the offset.
        """
        surface.blit(self.sprite, (self.x * self.tile_size + self.offset_x, self.y * self.tile_size + self.offset_y))

class Game:
    def __init__(self, game_state, settings):
        self.map_tile_length: int = 17
        self.map_tile_height: int = 21
        self.tile_size: int = 50
        self.window_width: int = self.map_tile_length * self.tile_size + 200 # 200px added for GUI sidebar
        self.window_height: int = self.map_tile_height * self.tile_size
        self.pygame_utils: PygameUtils = PygameUtils()
        self.game_state: GameState = game_state
        self.character_sprite: CharacterSprite = CharacterSprite(game_state, self.tile_size)
        self.character_name: str = self.game_state.character_data.name
        self.controller: CharacterController = CharacterController(game_state)
        self.get_request = Get()
        self.settings: Options = settings
        self.icon: pygame.Surface = pygame.image.load("Artifacts_MMO_Client/resources/window/icon1.png")
        self.music: str = "Artifacts_MMO_Client/resources/music/mapper1.wav"
        self.button_sound: str = "Artifacts_MMO_Client/resources/music/button_press.wav"

    def load_images(self, data: list[dict[str, str | int]]) -> dict:
        """Loads and scales each tiles resources

        Args:
            data (list[dict[str, str | int]]): A list of dictionaries describing each tile on the map

        Returns:
            images (dict): A dictionary with the skin of each tile as the key and the loaded and scaled image as the value
        """
        images = {}
        for tile in data:
            skin = tile["skin"]
            image_path = f"Artifacts_MMO_Client/resources/tiles/{skin}.png"

            try:
                images[skin] = pygame.image.load(image_path)
                images[skin] = pygame.transform.scale(images[skin], (self.tile_size, self.tile_size))
            except FileNotFoundError:
                print(f"Image file '{image_path}' not found. Skipping...")
        return images

    def create_grid(self, width: int, height: int) -> list:
        """Creates a 2D grid of size width x height, filled with None values.

        Args:
            width (int): The width of the grid
            height (int): The height of the grid

        Returns:
            list: A 2D grid of size width x height, filled with None values
        """
        return [[None for _ in range(width)] for _ in range(height)]

    def map_tiles_to_images(self, data: list[dict[str, str | int]], images: dict, grid: list) -> None:
        """Maps each tile to an image and stores in a grid

        Args:
            data (list): A list of dictionaries describing each tile on the map
            images (dict): A dictionary with the skin of each tile as the key and the loaded and scaled image as the value
            grid (list): A 2D grid of size width x height, filled with None values

        Returns:
            None
        """
        for tile in data:
            x = tile["x"]
            y = tile["y"]
            skin = tile["skin"]

            # Check if the image exists in the images dictionary
            if skin in images:
                image = images[skin]
                grid_x = x + 5
                grid_y = y + 5
                grid[grid_y][grid_x] = image
            else:
                print(f"Image not found for tile with skin '{skin}' at coordinates ({x}, {y})")

    def draw_grid(self, grid: list) -> None:
        """Clears window and draws the grid of tile images. Then draws the character on top of the grid.

        Args:
            grid (list): A 2D grid of size width x height, filled with None values
        """
        self.map_surface.fill((0, 0, 0))
        for y, row in enumerate(grid):
            for x, image in enumerate(row):
                if image:
                    self.map_surface.blit(image, (x * self.tile_size, y * self.tile_size))
        # Draws character on top of grid
        self.character_sprite.draw(self.map_surface)
    
    def load_gui(self):
        self.button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((-self.window_width, 0), (200, self.window_height)),
                            manager=self.gui_manager,
                            text="A Button",
                            container=None,
                            anchors={"right": "right", "top": "top"})

    def setup(self) -> None:
        """Main game loop.

        This method will load all maps from the API, create a grid of the correct size, load the images for each tile on the map, and map each tile to its corresponding image.

        The game loop will then run until the user closes the window, at which point the pygame window will be closed and the program will exit.
        """
        map_data: list[dict[str, str | int]] = self.get_request.all_maps()

        self.map_surface: pygame.surface.Surface = PygameUtils.pygame_init(self.window_width, self.window_height, "ArtifactsMMO - World", self.icon)
        self.gui_surface: pygame.surface.Surface = pygame.Surface((self.window_width, self.window_height))
        self.pygame_utils.play_music(self.music, self.settings.music_volume)

        self.gui_styles = "Artifacts_MMO_Client/resources/window/map_gui.json"
        self.gui_manager: pygame_gui.UIManager = pygame_gui.UIManager((self.window_width, self.window_height), self.gui_styles)
        self.event_handler: EventHandler = EventHandler(self.game_state, self.settings, self.gui_manager)

        self.images: dict = self.load_images(map_data)
        self.grid: list = self.create_grid(self.map_tile_length, self.map_tile_height)
        self.map_tiles_to_images(map_data, self.images, self.grid)

        self.load_gui()
    
    def update_render(self) -> None:
        self.character_sprite.x, self.character_sprite.y = self.game_state.character_data.x + 5, self.game_state.character_data.y + 5
        self.draw_grid(self.grid)
    
    def run(self) -> None:
        # Initial setup
        self.setup()

        # Initial map rendering
        self.update_render()

        # Gameplay loop
        clock = pygame.time.Clock()
        running: bool = True
        while running:
            time_delta = clock.tick(60)/1000.0
            
            # Checks for events
            event_handling = self.event_handler.handle_events()

            # Updates rendered map if an event has taken place
            if event_handling == "Update render":
                self.update_render()
            else:
                # Stops the loop and closes the window when event handler returns False
                running = event_handling
            
            self.gui_manager.update(time_delta)
            self.gui_manager.draw_ui(self.gui_surface)

            self.map_surface.blit(self.gui_surface, (self.window_width - 200, 0))

            pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    get_request: Get = Get()
    character_data = get_request.character("Kieran")
    settings: Options = Options()
    map_data_request: Map = get_request.map(character_data.x, character_data.y)
    game_data: GameState = GameState(character_data, map_data_request)
    game: Game = Game(game_data, settings)
    game.run()