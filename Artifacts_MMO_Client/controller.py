import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Hides Pygame welcome message

import pygame
import sys
from api_actions import Get, Post

class CharacterController:
    def __init__(self, character_name):
        self.character_name = character_name
        self.endpoint = f"my/{character_name}/action/move"
        self.pygame_window = pygame.display.set_mode((800, 600))
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.character_location = None
        self.get_request = Get()
        self.post_request = Post()

    def handle_pygame_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw_pygame_window(self):
        # print("draw pygame window")
        self.pygame_window.fill((0, 0, 0))
        # Draw WASD key layout - temp
        font = pygame.font.SysFont("Arial", 38)
        w_key = font.render("W", True, (255, 255, 255))
        a_key = font.render("A", True, (255, 255, 255))
        s_key = font.render("S", True, (255, 255, 255))
        d_key = font.render("D", True, (255, 255, 255))
        self.pygame_window.blit(w_key, (375, 275))
        self.pygame_window.blit(a_key, (325, 325))
        self.pygame_window.blit(s_key, (375, 325))
        self.pygame_window.blit(d_key, (425, 325))
        # Draw other game elements here
        pygame.display.flip()

    def move_character(self, x, y):
        response = self.post_request.move_character(self.character_name, x, y)
        new_location = {"x": response.x, "y": response.y}
        self.character_location = new_location
        print(f"Character moved to ({new_location['x']}, {new_location['y']})")
        return new_location

    def get_character_location(self):
        response = self.get_request.character(self.character_name)
        self.character_location = {"x": response.x, "y": response.y}
        return self.character_location

    def run(self):
        self.character_location = self.get_character_location()
        if self.character_location is None:
            return

        while True:
            self.handle_pygame_events()
            self.draw_pygame_window()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                new_location = self.move_character(self.character_location["x"], self.character_location["y"] - 1)
                if new_location:
                    self.character_location = new_location
            elif keys[pygame.K_s]:
                new_location = self.move_character(self.character_location["x"], self.character_location["y"] + 1)
                if new_location:
                    self.character_location = new_location
            elif keys[pygame.K_a]:
                new_location = self.move_character(self.character_location["x"] - 1, self.character_location["y"])
                if new_location:
                    self.character_location = new_location
            elif keys[pygame.K_d]:
                new_location = self.move_character(self.character_location["x"] + 1, self.character_location["y"])
                if new_location:
                    self.character_location = new_location
            self.clock.tick(60)

if __name__ == "__main__":
    character_name = "Kieran"
    controller = CharacterController(character_name)
    controller.run()