import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Hides Pygame welcome message

import pygame
import sys
from api_actions import Get
from data.character import Character

def character_selection() -> Character:
    """Displays a character selection screen with a scrolling background, character images with names, and hover effects using Pygame.

    Returns:
        Character: The selected character
    """
    pygame.init()

    # Set up constants
    SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 1200
    WHITE: tuple[int, int, int] = (255, 255, 255)
    BLACK: tuple[int, int, int] = (0, 0, 0)
    FONT_SIZE: int = 48
    FONT_MACONDO_LOCATION: str = "Artifacts_MMO_Client/resources/Macondo-Regular.ttf"

    # Set up the display
    screen: pygame.Surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("ArtifactsMMO - Character Selection")
    icon: pygame.Surface = pygame.image.load("Artifacts_MMO_Client/resources/icon1.png")
    pygame.display.set_icon(icon)

    # Load the background image
    try:
        background_image: pygame.Surface = pygame.image.load("Artifacts_MMO_Client/resources/character_selection.png")
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        pygame.quit()
        sys.exit()
    background_image: pygame.Surface = pygame.transform.scale(background_image, (SCREEN_WIDTH * 1.5, SCREEN_HEIGHT * 1.5))

    # Set the initial position of the background image
    background_x: int = 0
    background_y: int = 0

    # Get the list of characters from the API
    get_request: Get = Get()
    characters: list[Character] = get_request.characters()

    # Set up the font
    font: pygame.font.Font = pygame.font.Font(FONT_MACONDO_LOCATION, FONT_SIZE)

    # Calculate the spacing between buttons
    num_buttons: int = len(characters)
    button_height: int = 40
    spacing: int = (SCREEN_HEIGHT - (num_buttons * (button_height + 50))) // (num_buttons + 1)

    # Set up the character buttons
    buttons: list[pygame.Rect] = []
    images: list[pygame.Surface] = []
    image_rects: list[pygame.Rect] = []
    scales: list[float] = []
    velocities: list[float] = []
    for i, character in enumerate(characters):
        y: int = spacing + (i * (button_height + 50 + spacing))
        button: pygame.Rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, y + 50, 200, button_height)
        buttons.append(button)

        # Load the character image
        try:
            image_name: str = character.skin
            image: pygame.Surface = pygame.image.load(f"Artifacts_MMO_Client/resources/{image_name}.png")
            image: pygame.Surface = pygame.transform.scale(image, (100, 121))
        except pygame.error as e:
            print(f"Error loading character image {image_name}: {e}")
            pygame.quit()
            sys.exit()
        images.append(image)

        # Create a rect for the image
        image_rect: pygame.Rect = image.get_rect(center=(button.centerx, button.top - 50))
        image_rects.append(image_rect)

        # Initialize the scale to 1.0 (no scaling) and velocity to 0.0
        scales.append(1.0)
        velocities.append(0.01) 

    # Load and play the background music
    pygame.mixer.init()
    try:
        background_music: pygame.mixer.Sound = pygame.mixer.Sound("Artifacts_MMO_Client/resources/music/character_selection1.wav")
        background_music.set_volume(0.5)  # Set the volume to 50%
        background_music.play(-1)  # Play the music in a loop
    except pygame.error as e:
        print(f"Error loading background music: {e}")

    # Main loop
    clock: pygame.time.Clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, (button, image_rect) in enumerate(zip(buttons, image_rects)):
                    if button.collidepoint(event.pos) or image_rect.collidepoint(event.pos):
                        # User clicked on a character button or image
                        selected_character: Character = characters[i]
                        return selected_character

        # Create a larger background surface
        background_surface: pygame.Surface = pygame.Surface((SCREEN_WIDTH * 2, SCREEN_HEIGHT * 4))

        # Draw the background image onto the surface
        for i in range(2):
            for j in range(4):
                background_surface.blit(background_image, (background_x + (i * SCREEN_WIDTH * 1.5), background_y + (j * SCREEN_HEIGHT * 1.5)))

        # Draw the background surface onto the screen
        screen.blit(background_surface, (0, 0))

        # Update the position of the background image
        background_x -= 1.5
        background_y -= 1

        # Check if the background has scrolled two screens
        if background_y < -SCREEN_HEIGHT * 2:
            background_y = -600  # Reset y-position
        if background_x < -SCREEN_WIDTH * 2:
            background_x = -600  # Reset x-position

        # Draw the character buttons
        for i, (button, image, image_rect, scale, velocity) in enumerate(zip(buttons, images, image_rects, scales, velocities)):
            # Create a surface with a transparent background
            circle_surface: pygame.Surface = pygame.Surface((200, 200), pygame.SRCALPHA)
            circle_surface.fill((0, 0, 0, 0))

            # Draw a circle on the surface
            pygame.draw.circle(circle_surface, (255, 255, 255, 128), (100, 100), 100)

            # Blit the circle surface onto the screen
            screen.blit(circle_surface, (button.centerx - 100, button.centery - 150))

            text: pygame.Surface = font.render(characters[i].name, True, BLACK)
            text_rect: pygame.Rect = text.get_rect(center=button.center)
            screen.blit(text, text_rect)

            # Update the scale based on hover state
            if image_rect.collidepoint(pygame.mouse.get_pos()):
                # Update the scale based on velocity
                scales[i] += velocities[i]
                if scales[i] > 1.2:
                    velocities[i] = -velocities[i]
                elif scales[i] < 1.0:
                    velocities[i] = -velocities[i]
            else:
                # Reset the scale and velocity when not hovered
                scales[i] = 1.0
                velocities[i] = 0.01

            # Draw the character image with the updated scale
            scaled_image: pygame.Surface = pygame.transform.scale(image, (int(100 * scale), int(121 * scale)))
            scaled_image_rect: pygame.Rect = scaled_image.get_rect(center=image_rect.center)
            screen.blit(scaled_image, scaled_image_rect)

        # Update the display
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    character_name = character_selection()