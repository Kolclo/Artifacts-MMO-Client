import pygame
from requester import APIRequester

class Game:
    def __init__(self):
        self.map_tile_length = 17
        self.map_tile_height = 21
        self.tile_size = 65
        self.window_width = self.map_tile_length * self.tile_size
        self.window_height = self.map_tile_height * self.tile_size
        self.pygame_init()

    def pygame_init(self):
        pygame.init()
        self.window = pygame.display.set_mode((self.window_width, self.window_height))

    def load_images(self, data):
        images = {}
        for tile in data:
            skin = tile["skin"]
            image_path = f"Artifacts_MMO_Client/resources/{skin}.png"
            print(image_path)
            images[skin] = pygame.image.load(image_path)
            images[skin] = pygame.transform.scale(images[skin], (self.tile_size, self.tile_size))
        return images

    def create_grid(self, width, height):
        return [[None for _ in range(width)] for _ in range(height)]

    def map_tiles_to_images(self, data, images, grid):
        for tile in data:
            x = tile["x"]
            y = tile["y"]
            skin = tile["skin"]
            image = images[skin]

            print(f"Tile coordinates: ({x}, {y})")

            grid_x = x + 5
            grid_y = y + 5
            print(f"Grid coordinates: ({grid_x}, {grid_y})")

            grid[grid_y][grid_x] = image
            print(f"Placing image {skin} at grid coordinates ({grid_x}, {grid_y})")

    def draw_grid(self, grid):
        self.window.fill((0, 0, 0))  # Clear the window
        for y, row in enumerate(grid):
            for x, image in enumerate(row):
                if image:
                    self.window.blit(image, (x * self.tile_size, y * self.tile_size))

    def run(self):
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.draw_grid(grid)
            pygame.display.flip()
            pygame.time.Clock().tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()