import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Hides Pygame welcome message

import pygame
from pygame_util import PygameUtils
import sys
from api_actions import Get
from data.character import Character

class CharacterSelector:
    def __init__(self):
        self.pygame_utils: PygameUtils = PygameUtils()
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1024, 1024
        self.WHITE: tuple[int, int, int] = (255, 255, 255)
        self.BLACK: tuple[int, int, int] = (0, 0, 0)
        self.FONT_SIZE: int = 48
        self.FONT_MACONDO_LOCATION: str = "Artifacts_MMO_Client/resources/window/Macondo-Regular.ttf"
        self.icon: pygame.Surface = pygame.image.load("Artifacts_MMO_Client/resources/window/icon1.png")
        self.window_name: str = "ArtifactsMMO - Character Selection"
        self.window = PygameUtils.pygame_init(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.window_name, self.icon)
        self.font: pygame.font.Font = pygame.font.Font(self.FONT_MACONDO_LOCATION, self.FONT_SIZE)
        self.music: str = "Artifacts_MMO_Client/resources/music/character_selection2.wav"

        self.background_image: str = "Artifacts_MMO_Client/resources/window/character_selection.png"
        self.background_x: int = 0
        self.background_y: int = 0

        self.get_request: Get = Get()

        self.characters: list[Character] = self.get_request.characters()

        self.num_buttons: int = len(self.characters)
        self.button_height: int = 40
        self.spacing: int = (self.WINDOW_HEIGHT - (self.num_buttons * (self.button_height + 50))) // (self.num_buttons + 1)
    
    def load_background_image(self):
        try:
            self.background_image: pygame.Surface = pygame.image.load(self.background_image)
            self.background_image: pygame.Surface = pygame.transform.scale(self.background_image, (self.WINDOW_WIDTH * 1.5, self.WINDOW_HEIGHT * 1.5))
        except pygame.error as e:
            print(f"Error loading background image: {e}")
            pygame.quit()
            sys.exit()
    
    def button_setup(self):
        self.buttons: list[pygame.Rect] = []
        self.images: list[pygame.Surface] = []
        self.image_rects: list[pygame.Rect] = []
        self.scales: list[float] = []
        self.velocities: list[float] = []
        for i, character in enumerate(self.characters):
            y: int = self.spacing + (i * (self.button_height + 50 + self.spacing))
            button: pygame.Rect = pygame.Rect(self.WINDOW_WIDTH // 2 - 100, y + 50, 200, self.button_height)
            self.buttons.append(button)

            # Load the character image
            try:
                image_name: str = character.skin
                image: pygame.Surface = pygame.image.load(f"Artifacts_MMO_Client/resources/characters/{image_name}.png")
                image: pygame.Surface = pygame.transform.scale(image, (100, 121))
            except pygame.error as e:
                print(f"Error loading character image {image_name}: {e}")
                pygame.quit()
                sys.exit()
            self.images.append(image)

            # Create a rect for the image
            image_rect: pygame.Rect = image.get_rect(center=(button.centerx, button.top - 50))
            self.image_rects.append(image_rect)

            # Initialize the scale to 1.0 (no scaling) and velocity to 0.0
            self.scales.append(1.0)
            self.velocities.append(0.01) 
    
    def run(self):
        """Displays a character selection screen with a scrolling background, character images with names, and hover effects using Pygame.

        Returns:
            Character: The selected character
        """
        self.load_background_image()
        self.button_setup()

        clock: pygame.time.Clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for i, (button, image_rect) in enumerate(zip(self.buttons, self.image_rects)):
                        if button.collidepoint(event.pos) or image_rect.collidepoint(event.pos):
                            # User clicked on a character button or image
                            self.pygame_utils.stop_music()
                            selected_character: Character = self.characters[i]
                            return selected_character

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

            # Draw the character buttons
            for i, (button, image, image_rect, scale, velocity) in enumerate(zip(self.buttons, self.images, self.image_rects, self.scales, self.velocities)):
                # Create a surface with a transparent background
                circle_surface: pygame.Surface = pygame.Surface((200, 200), pygame.SRCALPHA)
                circle_surface.fill((0, 0, 0, 0))

                # Draw a circle on the surface
                pygame.draw.circle(circle_surface, (255, 255, 255, 128), (100, 100), 100)

                # Blit the circle surface onto the screen
                self.window.blit(circle_surface, (button.centerx - 100, button.centery - 150))

                text: pygame.Surface = self.font.render(self.characters[i].name, True, self.BLACK)
                text_rect: pygame.Rect = text.get_rect(center=button.center)
                self.window.blit(text, text_rect)

                # Update the scale based on hover state
                if image_rect.collidepoint(pygame.mouse.get_pos()):
                    # Update the scale based on velocity
                    self.scales[i] += self.velocities[i]
                    if self.scales[i] > 1.2:
                        self.velocities[i] = -self.velocities[i]
                    elif self.scales[i] < 1.0:
                        self.velocities[i] = -self.velocities[i]
                else:
                    # Reset the scale and velocity when not hovered
                    self.scales[i] = 1.0
                    self.velocities[i] = 0.01

                # Draw the character image with the updated scale
                scaled_image: pygame.Surface = pygame.transform.scale(image, (int(100 * scale), int(121 * scale)))
                scaled_image_rect: pygame.Rect = scaled_image.get_rect(center=image_rect.center)
                self.window.blit(scaled_image, scaled_image_rect)

            # Update the display
            pygame.display.flip()
            clock.tick(60)