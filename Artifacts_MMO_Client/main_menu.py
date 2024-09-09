import pygame
from pygame_util import PygameUtils
import pygame_gui
from options_menu import OptionsMenu
from data.options import Options

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

        self.gui_styles = "Artifacts_MMO_Client/resources/window/main_menu.json"
        self.gui_manager = pygame_gui.UIManager((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), self.gui_styles)

        self.menu_title: str = "Artifacts_MMO_Client/resources/window/menu_title.png"
        self.menu_title_surface: pygame.Surface = pygame.image.load(self.menu_title)

        self.background_image: str = "Artifacts_MMO_Client/resources/window/main_menu.jpeg"
        self.background_surface: pygame.Surface = pygame.image.load(self.background_image)

        self.button_sound: str = "Artifacts_MMO_Client/resources/music/button_press.wav"

        self.settings: Options = settings
        
    
    def center_ui_element(self, width, height, y_offset = 0):
        x = (self.WINDOW_WIDTH - width) // 2
        y = (self.WINDOW_HEIGHT - height) // 2
        return pygame.Rect((x, y - y_offset), (width, height))

    def setup(self):
        self.game_title = pygame_gui.elements.UIImage(relative_rect=self.center_ui_element(800, 150, 300), image_surface=self.menu_title_surface, manager=self.gui_manager)
        self.play_button = pygame_gui.elements.UIButton(relative_rect=self.center_ui_element(400, 100, 50), text='Play', manager=self.gui_manager)
        self.options_button = pygame_gui.elements.UIButton(relative_rect=self.center_ui_element(400, 100, -125), text='Options', manager=self.gui_manager)
        self.exit_button = pygame_gui.elements.UIButton(relative_rect=self.center_ui_element(400, 100, -300), text='Exit', manager=self.gui_manager)
        self.pygame_music = self.pygame_utils.play_music(self.music, self.settings.music_volume)

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
                    if event.ui_element == self.play_button:
                        pygame.time.wait(500)
                        running = False
                    if event.ui_element == self.options_button:
                        self.options_menu: OptionsMenu = OptionsMenu(self.window, self.settings)
                        self.options_menu.run()
                        self.pygame_music.set_volume(self.settings.music_volume)
                    if event.ui_element == self.exit_button:
                        pygame.time.wait(500)
                        return False
                
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