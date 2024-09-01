import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Hides Pygame welcome message

import pygame
from api_actions import Get
from controller import CharacterController

class Character:
    def __init__(self, x, y, skin):
        self.x = x
        self.y = y
        self.sprite = pygame.image.load(f"Artifacts_MMO_Client/resources/{skin}.png")
        self.sprite = pygame.transform.scale(self.sprite, (40, 50))

    def draw(self, window):
        # Calculate the offset to center the sprite on the tile
        offset_x = (65 - self.sprite.get_width()) // 2
        offset_y = (65 - self.sprite.get_height()) // 2
        # Draw the sprite
        window.blit(self.sprite, (self.x * 65 + offset_x, self.y * 65 + offset_y))

class Game:
    def __init__(self, character_data):
        self.map_tile_length = 17
        self.map_tile_height = 21
        self.tile_size = 65
        self.window_width = self.map_tile_length * self.tile_size
        self.window_height = self.map_tile_height * self.tile_size
        self.pygame_init()
        self.character = Character((character_data.x + 5), (character_data.y + 5), character_data.skin)  # Character's starting position
        self.controller = CharacterController(character_data.name)

    def pygame_init(self):
        # Starts Pygame
        pygame.init()
        self.window = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("ArtifactsMMO - World")

    # Take a look at event lizard!!
    #IMPORTANT
    def load_images(self, data):
        # Loads and scales each tiles resources
        images = {}
        for tile in data:
            skin = tile["skin"]
            image_path = f"Artifacts_MMO_Client/resources/{skin}.png"

            try:
                images[skin] = pygame.image.load(image_path)
                images[skin] = pygame.transform.scale(images[skin], (self.tile_size, self.tile_size))
            except FileNotFoundError:
                print(f"Image file '{image_path}' not found. Skipping...")
        return images

    def create_grid(self, width, height):
        # Creates 2D grid
        return [[None for _ in range(width)] for _ in range(height)]

    def map_tiles_to_images(self, data, images, grid):
        # Maps each tile to an image and stores in a grid
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

    def draw_grid(self, grid):
        # Clears window and draws the grid of tile images
        self.window.fill((0, 0, 0))
        for y, row in enumerate(grid):
            for x, image in enumerate(row):
                if image:
                    self.window.blit(image, (x * self.tile_size, y * self.tile_size))
        # Draws character on top of grid
        self.character.draw(self.window)
    
    # Temporary until other API's and controls are coded in, handles button presses

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.character.x -= 1
                    self.controller.move_left()
                elif event.key == pygame.K_RIGHT:
                    self.character.x += 1
                    self.controller.move_right()
                elif event.key == pygame.K_UP:
                    self.character.y -= 1
                    self.controller.move_up()
                elif event.key == pygame.K_DOWN:
                    self.character.y += 1
                    self.controller.move_down()

                # Stops character from leaving the map
                self.character.x = max(0, min(self.character.x, self.map_tile_length - 1))
                self.character.y = max(0, min(self.character.y, self.map_tile_height - 1))
        return True

    def run(self):
        # Main Pygame loop
        get_request = Get()
        map_data = get_request.all_maps()

        images = self.load_images(map_data)
        grid = self.create_grid(self.map_tile_length, self.map_tile_height)
        self.map_tiles_to_images(map_data, images, grid)

        running = True
        while running:
            running = self.handle_events()
            self.draw_grid(grid)
            pygame.display.flip()
            pygame.time.Clock().tick(60)

        pygame.quit()

if __name__ == "__main__":
    get_request = Get()
    character_data = get_request.character("Kieran")
    game = Game(character_data)
    game.run()