import pygame
import sys
from requester import APIRequester

def character_selection():
    """
    Displays a character selection menu using Pygame.
    """
    pygame.init()

    # Set up some constants
    WIDTH, HEIGHT = 800, 800
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    FONT_SIZE = 24

    # Set up the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Character Selection")

    # Load the background image
    background_image = pygame.image.load("Artifacts_MMO_Client/resources/forest_village3.png")
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    # Set the initial position of the background image
    background_x = 0
    
    pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    # Get the list of characters from the API
    api_requester = APIRequester()
    response = api_requester.get("/my/characters")
    characters = response["data"]

    # Since 'data' is a list of characters, we need to iterate over it
    character_list = []
    for character_data in characters:
        character_list.append(character_data)

    # Set up the font
    font = pygame.font.SysFont("Arial", FONT_SIZE)

    # Calculate the spacing between buttons
    num_buttons = len(character_list)
    button_height = 40
    spacing = (HEIGHT - (num_buttons * (button_height + 50))) // (num_buttons + 1)

    # Set up the character buttons
    buttons = []
    images = []
    image_rects = []
    scales = []  # New list to store the current scale of each image
    velocities = []  # New list to store the velocity of each image's scale
    for i, character in enumerate(character_list):
        y = spacing + (i * (button_height + 50 + spacing))
        button = pygame.Rect(WIDTH // 2 - 100, y + 50, 200, button_height)
        buttons.append(button)

        # Load the character image
        image_name = character["skin"]
        image = pygame.image.load(f"Artifacts_MMO_Client/resources/{image_name}.png")
        image = pygame.transform.scale(image, (100, 100))
        images.append(image)

        # Create a rect for the image
        image_rect = image.get_rect(center=(button.centerx, button.top - 50))
        image_rects.append(image_rect)

        # Initialize the scale to 1.0 (no scaling) and velocity to 0.0
        scales.append(1.0)
        velocities.append(0.01)  # Reduce the initial velocity to slow down the bouncing effect

    # Load and play the background music
    pygame.mixer.init()
    background_music = pygame.mixer.Sound("Artifacts_MMO_Client/resources/character_selection.wav")
    background_music.set_volume(0.5)  # Set the volume to 50%
    background_music.play(-1)  # Play the music in a loop

    # Main loop
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                for i, (button, image_rect) in enumerate(zip(buttons, image_rects)):
                    if button.collidepoint(event.pos) or image_rect.collidepoint(event.pos):
                        # User clicked on a character button or image
                        selected_character = character_list[i]
                        return selected_character

        # Draw the background
        screen.blit(background_image, (background_x, 0))
        screen.blit(background_image, (background_x + WIDTH, 0))  # Draw the background image again, offset by the width of the screen

        # Update the position of the background image
        background_x -= 1
        if background_x < -WIDTH:
            background_x = 0

        # Draw the character buttons
        for i, (button, image, image_rect, scale, velocity) in enumerate(zip(buttons, images, image_rects, scales, velocities)):
            pygame.draw.rect(screen, BLACK, button)
            text = font.render(character_list[i]["name"], True, WHITE)
            text_rect = text.get_rect(center=button.center)
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
                velocities[i] = 0.01  # Reset the velocity to the initial value

            # Draw the character image with the updated scale
            scaled_image = pygame.transform.scale(image, (int(100 * scale), int(100 * scale)))
            scaled_image_rect = scaled_image.get_rect(center=image_rect.center)
            screen.blit(scaled_image, scaled_image_rect)

        # Update the display
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    character_name = character_selection()