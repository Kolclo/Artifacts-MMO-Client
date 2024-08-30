import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Hides Pygame welcome message

import pygame
from requester import APIRequester

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.sprite = pygame.image.load("Artifacts_MMO_Client/resources/men2.png")
        self.sprite = pygame.transform.scale(self.sprite, (40, 50))

    def draw(self, window):
        # Calculate the offset to center the sprite on the tile
        offset_x = (65 - self.sprite.get_width()) // 2
        offset_y = (65 - self.sprite.get_height()) // 2
        # Draw the sprite
        window.blit(self.sprite, (self.x * 65 + offset_x, self.y * 65 + offset_y))

class Game:
    def __init__(self):
        self.map_tile_length = 17
        self.map_tile_height = 21
        self.tile_size = 65
        self.window_width = self.map_tile_length * self.tile_size
        self.window_height = self.map_tile_height * self.tile_size
        self.pygame_init()
        self.character = Character(5, 5)  # Character's starting position

    def pygame_init(self):
        # Starts Pygame
        pygame.init()
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

    def load_images(self, data):
        # Loads and scales each tiles resources
        images = {}
        for tile in data:
            skin = tile["skin"]
            image_path = f"Artifacts_MMO_Client/resources/{skin}.png"
            # print(image_path)
            images[skin] = pygame.image.load(image_path)
            images[skin] = pygame.transform.scale(images[skin], (self.tile_size, self.tile_size))
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
            image = images[skin]

            # print(f"Tile coordinates: ({x}, {y})")

            grid_x = x + 5
            grid_y = y + 5
            # print(f"Grid coordinates: ({grid_x}, {grid_y})")

            grid[grid_y][grid_x] = image
            # print(f"Placing image {skin} at grid coordinates ({grid_x}, {grid_y})")

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
                elif event.key == pygame.K_RIGHT:
                    self.character.x += 1
                elif event.key == pygame.K_UP:
                    self.character.y -= 1
                elif event.key == pygame.K_DOWN:
                    self.character.y += 1

                # Stops character from leaving the map
                self.character.x = max(0, min(self.character.x, self.map_tile_length - 1))
                self.character.y = max(0, min(self.character.y, self.map_tile_height - 1))
        return True

    def run(self):
        # Main Pygame loop
        requester = APIRequester()
        data = []
        page = 1
        while True:
            response = requester.get("maps", params={"size": 100, "page": page})
            if not response["data"]:
                break
            data.extend(response["data"])
            page += 1

        images = self.load_images(data)
        grid = self.create_grid(self.map_tile_length, self.map_tile_height)
        self.map_tiles_to_images(data, images, grid)

        running = True
        while running:
            running = self.handle_events()
            self.draw_grid(grid)
            pygame.display.flip()
            pygame.time.Clock().tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()