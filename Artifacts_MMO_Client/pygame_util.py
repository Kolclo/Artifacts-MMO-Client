import pygame

class PygameUtils:
    def pygame_init(window_width, window_height, title, icon):
        """Initializes the pygame window with the correct size and title.

        window_width and window_height are used to set the size of the window.
        The window is given the provided title.
        """

        pygame.init()
        window: pygame.surface.Surface = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption(title)
        pygame.display.set_icon(icon)

        return window

    def play_music(self, music_location: str, volume: int = 0.5, loops: int = -1):
        pygame.mixer.init()
        try:
            music: pygame.mixer.Sound = pygame.mixer.Sound(music_location)
            music.set_volume(volume)
            music.play(loops)
            return music
        except pygame.error as e:
            print(f"Error loading background music: {e}")
    
    def stop_music(self):
        """Stops the currently playing music"""
        pygame.mixer.quit()
