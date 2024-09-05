import pygame

class PygameUtils:
    def pygame_init(window_width, window_height, title):
        """Initializes the pygame window with the correct size and title.

        window_width and window_height are used to set the size of the window.
        The window is given the provided title.
        """

        pygame.init()
        window: pygame.surface.Surface = pygame.display.set_mode((window_width, window_height))
        pygame.display.set_caption(title)

        return window