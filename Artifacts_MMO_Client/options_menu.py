import pygame
from pygame_util import PygameUtils
import pygame_gui
from data.options import Options

class OptionsMenu:
    def __init__(self, window, settings):
        self.pygame_utils: PygameUtils = PygameUtils()
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1024, 1024
        self.WHITE: tuple[int, int, int] = (255, 255, 255)
        self.BLACK: tuple[int, int, int] = (0, 0, 0)
        self.window = window
        self.gui_styles = "Artifacts_MMO_Client/resources/window/main_menu.json"
        self.gui_manager = pygame_gui.UIManager((self.WINDOW_WIDTH, self.WINDOW_HEIGHT), self.gui_styles)
        self.music: str = "Artifacts_MMO_Client/resources/music/main_menu1.wav"

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
    
    def write_settings(self):
        with open("Artifacts_MMO_Client/saved_user_options.py", "w") as file:
            file.write(f"music_volume = {self.settings.music_volume}\n")
            file.write(f"sound_volume = {self.settings.sound_volume}\n")

    def setup(self):
        self.game_title = pygame_gui.elements.UIImage(relative_rect=self.center_ui_element(800, 150, 300), image_surface=self.menu_title_surface, manager=self.gui_manager)

        self.music_volume_text = pygame_gui.elements.UILabel(relative_rect=self.center_ui_element(400, 50, 100), text='Music Volume', manager=self.gui_manager)
        self.music_volume_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=self.center_ui_element(400, 50, 50), start_value=self.settings.music_volume, value_range=[0, 1], manager=self.gui_manager)

        self.sound_volume_text = pygame_gui.elements.UILabel(relative_rect=self.center_ui_element(400, 50, -50), text='Sound Volume', manager=self.gui_manager)
        self.sound_volume_slider = pygame_gui.elements.UIHorizontalSlider(relative_rect=self.center_ui_element(400, 50, -100), start_value=self.settings.sound_volume, value_range=[0, 1], manager=self.gui_manager)

        self.back_button = pygame_gui.elements.UIButton(relative_rect=self.center_ui_element(400, 100, -300), text='Back', manager=self.gui_manager)

    def run(self):
        self.setup()
        clock = pygame.time.Clock()
        running = True

        while running:
            time_delta = clock.tick(60)/1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
                    if event.ui_element == self.sound_volume_slider:
                        self.settings.sound_volume = round(self.sound_volume_slider.get_current_value(), 1)
                    
                    if event.ui_element == self.music_volume_slider:
                        self.settings.music_volume = round(self.music_volume_slider.get_current_value(), 1)

                if event.type == pygame_gui.UI_BUTTON_PRESSED:
                    self.pygame_utils.play_music(self.button_sound, self.settings.sound_volume, 0)
                    if event.ui_element == self.back_button:
                        self.write_settings()
                        pygame.time.wait(500)
                        return False
                                        
                self.gui_manager.process_events(event)
            
            self.gui_manager.update(time_delta)
            
            self.window.blit(self.background_surface, (0, 0))
            self.gui_manager.draw_ui(self.window)

            pygame.display.update()

if __name__ == "__main__":
    main = OptionsMenu()
    main.run()