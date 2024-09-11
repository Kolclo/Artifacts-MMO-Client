import pygame
from pygame_util import PygameUtils
import pygame_gui
from options_menu import OptionsMenu
from data.options import Options
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

class MainMenu:
    def __init__(self, settings):
        self.pygame_utils: PygameUtils = PygameUtils()
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1024, 1024
        self.WHITE: tuple[int, int, int] = (255, 255, 255)
        self.BLACK: tuple[int, int, int] = (0, 0, 0)
        self.icon: pygame.Surface = pygame.image.load("Artifacts_MMO_Client/resources/window/icon1.png")
        self.window_name: str = "ArtifactsMMO - Main Menu"
        self.window = PygameUtils.pygame_init(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.window_name, self.icon)
        self.music: str = "Artifacts_MMO_Client/resources/music/main_menu1.wav"

        self.gui_styles = "Artifacts_MMO_Client/resources/window/mass_character_controller.json"
        self.gui_manager = pygame_gui.UIManager((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), self.gui_styles)

        self.menu_title: str = "Artifacts_MMO_Client/resources/window/menu_title.png"
        self.menu_title_surface: pygame.Surface = pygame.image.load(self.menu_title)

        self.background_image: str = "Artifacts_MMO_Client/resources/window/main_menu.jpeg"
        self.background_surface: pygame.Surface = pygame.image.load(self.background_image)

        self.button_sound: str = "Artifacts_MMO_Client/resources/music/button_press.wav"

        self.settings: Options = settings
        
    
    def center_ui_element(self, width, height, y_offset = 0, x_offset = 0):
        x = (self.WINDOW_WIDTH - width) // 2
        y = (self.WINDOW_HEIGHT - height) // 2
        return pygame.Rect((x - x_offset, y - y_offset), (width, height))

    def setup(self):
        button_width = 150
        button_height = 50
        characters = ['Kieran', 'Shabazz', 'longnametest', 'Pog', 'ChadusRexus']

        self.buttons = []
        self.toggled_buttons = [False] * len(characters)
        total_width = sum(button_width for _ in characters) + (len(characters) - 1) * 20
        x_offset = (self.WINDOW_WIDTH - total_width) // 2
        y_offset = 20

        for i, character in enumerate(characters):
            rect = pygame.Rect(x_offset + (i * (button_width + 20)), y_offset, button_width, button_height)
            button = pygame_gui.elements.UIButton(relative_rect=rect, text=character, manager=self.gui_manager)
            self.buttons.append(button)

        self.pygame_music = self.pygame_utils.play_music(self.music, self.settings.music_volume)

    def run(self):
        self.setup()
        clock = pygame.time.Clock()
        running = True

    def run(self):
        self.setup()
        clock = pygame.time.Clock()
        running = True

        while running:
            time_delta = clock.tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    self.pygame_utils.play_music(self.button_sound, self.settings.sound_volume, 0)
                    for i, button in enumerate(self.buttons):
                        if event.ui_element == button:
                            self.toggled_buttons[i] = not self.toggled_buttons[i]
                            characters = ['Kieran', 'Shabazz', 'longnametest', 'Pog', 'ChadusRexus']
                            character = characters[i]
                            if self.toggled_buttons[i]:
                                print(button)
                
                self.gui_manager.process_events(event)
                
            self.gui_manager.update(time_delta)
            
            self.window.blit(self.background_surface, (0, 0))
            self.gui_manager.draw_ui(self.window)

            pygame.display.update()
        return True

if __name__ == "__main__":
    settings: Options = Options()
    main = MainMenu(settings)
    main.run()