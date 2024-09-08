import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Hides Pygame welcome message

import pygame
from pygame_util import PygameUtils
import sys
from api_actions import Get
from data.character import Character
import pygame_gui
from data.options import Options

class CharacterSelector:
    def __init__(self, settings):
        self.pygame_utils: PygameUtils = PygameUtils()
        self.get_request: Get = Get()
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1024, 1024
        self.WHITE: tuple[int, int, int] = (255, 255, 255)
        self.BLACK: tuple[int, int, int] = (0, 0, 0)
        self.icon: pygame.Surface = pygame.image.load("Artifacts_MMO_Client/resources/window/icon1.png")
        self.window_name: str = "ArtifactsMMO - Character Selection"
        self.window = PygameUtils.pygame_init(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.window_name, self.icon)

        self.background_image: str = "Artifacts_MMO_Client/resources/window/character_selection.png"
        self.background_x: int = 0
        self.background_y: int = 0

        self.gui_styles = "Artifacts_MMO_Client/resources/window/character_selection.json"
        self.gui_manager = pygame_gui.UIManager((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), self.gui_styles)

        self.button_sound: str = "Artifacts_MMO_Client/resources/music/button_press.wav"

        self.characters: list[Character] = self.get_request.characters()

        self.settings: Options = settings
        
    
    def load_background_image(self):
        try:
            self.background_image: pygame.Surface = pygame.image.load(self.background_image)
            self.background_image: pygame.Surface = pygame.transform.scale(self.background_image, (self.WINDOW_WIDTH * 1.5, self.WINDOW_HEIGHT * 1.5))
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            pygame.quit()
            sys.exit()
    
    def update_background_location(self):
        # Create a larger background surface
        background_surface: pygame.Surface = pygame.Surface((self.WINDOW_WIDTH * 2, self.WINDOW_HEIGHT * 4))

        # Draw the background image onto the surface
        for i in range(2):
            for j in range(4):
                background_surface.blit(self.background_image, (self.background_x + (i * self.WINDOW_WIDTH * 1.5), self.background_y + (j * self.WINDOW_HEIGHT * 1.5)))

        # Draw the background surface onto the screen
        self.window.blit(background_surface, (0, 0))

        # Update the position of the background image
        self.background_x -= 1.5
        self.background_y -= 1

        # Check if the background has scrolled two screens
        if self.background_y < -self.WINDOW_HEIGHT * 2:
            self.background_y = -self.WINDOW_HEIGHT/2  # Reset y-position
        if self.background_x < -self.WINDOW_WIDTH * 2:
            self.background_x = -self.WINDOW_WIDTH/2  # Reset x-position
    
    def center_ui_element(self, width, height, y_offset = 0, x_offset = 0):
        x = (self.WINDOW_WIDTH - width) // 2
        y = (self.WINDOW_HEIGHT - height) // 2
        return pygame.Rect((x - x_offset, y - y_offset), (width, height))
    
    def create_character_buttons(self) -> list[pygame_gui.elements.UIPanel]:
        """Creates a list of character buttons with images and names.

        Returns:
            list[pygame_gui.elements.UIPanel]: List of UI Panels for the character buttons
        """
        button_width: int = 400
        button_height: int = 150
        x_gap: int = 20
        y_gap: int = 60
        y_offset: int = 150

        images: list[pygame.Surface] = [pygame.image.load(f"Artifacts_MMO_Client/resources/characters/{character.skin}.png").convert_alpha() for character in self.characters]

        button_list: list[pygame_gui.elements.UIPanel] = []
        self.character_buttons_dict = {}  # Dictionary to store buttons and their corresponding characters

        # Calculate the x position of the leftmost button
        x_offset: int = (900 - (button_width * 2 + x_gap)) // 2

        for i in range(len(self.characters)):
            x: int = x_offset + (i % 2) * (button_width + x_gap)
            y: int = (900 - button_height) // 2 + (i // 2) * (button_height + y_gap) - y_offset

            # Create a panel for the button and image
            panel: pygame_gui.elements.UIPanel = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((x, y), (button_width, button_height)), manager=self.gui_manager, container=self.button_background)

            # Create the image element and add it to the panel
            pygame_gui.elements.UIImage(relative_rect=pygame.Rect((10, (button_height - 100) // 2), (80, 100)), image_surface=images[i], manager=self.gui_manager, container=panel)

            # Create the button element and add it to the panel
            button: pygame_gui.elements.UIButton = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((100, 10), (button_width - 110, button_height - 20)), text=self.characters[i].name, manager=self.gui_manager, container=panel)
            self.character_buttons_dict[button] = self.characters[i]  # Store the button and its corresponding character
            button_list.append(panel)

        return button_list


    def setup(self):
        self.load_background_image()
        self.button_background = pygame_gui.elements.UIWindow(rect=self.center_ui_element(900, 900), manager=self.gui_manager, draggable=False)
        self.character_buttons = self.create_character_buttons()
        title_rect = pygame.Rect(((900 - 800) // 2 - 0, (900 - 150) // 2 - 325), (800, 150))
        self.title_text = pygame_gui.elements.UITextBox("<u>Choose Your Character</u>", relative_rect=title_rect, container=self.button_background, manager=self.gui_manager)

    def run(self):
        clock = pygame.time.Clock()
        self.setup()
        running = True

        while running:
            time_delta = clock.tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    self.pygame_utils.play_music(self.button_sound, self.settings.sound_volume, 0)
                    if event.ui_element in self.character_buttons_dict:
                        pygame.time.wait(500)
                        self.pygame_utils.stop_music()
                        selected_character = self.character_buttons_dict[event.ui_element]
                        return selected_character
                        
                self.gui_manager.process_events(event)
            
            self.gui_manager.update(time_delta)
            self.update_background_location()

            self.gui_manager.draw_ui(self.window)

            pygame.display.update()
        return True

if __name__ == "__main__":
    settings: Options = Options()
    character_selection = CharacterSelector(settings)
    character_selection.run()