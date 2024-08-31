import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide" # Hides Pygame welcome message

import pygame
import requester
import sys

class CharacterController:
    def __init__(self, character_name):
        self.character_name = character_name
        self.endpoint = f"my/{character_name}/action/move"
        self.pygame_window = pygame.display.set_mode((800, 600))
        pygame.font.init()
        self.clock = pygame.time.Clock()
        self.character_location = None
        self.requester = requester.SendRequest()

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
        # print("moving character")
        data = {"x": x, "y": y}
        response = self.requester.post(self.endpoint, data)
        if "error" not in response:
            new_location = response["data"]["destination"]
            self.character_location = new_location
            print(f"Character moved to ({new_location['x']}, {new_location['y']})")
            return new_location
        else:
            print(f"Error moving character: {response['error']}")
            return None

    def get_character_location(self):
        # print("getting location")
        endpoint = f"characters/{self.character_name}"
        response = self.requester.get(endpoint)
        if "error" not in response:
            print("no error")
            self.character_location = {"x": response["data"]["x"], 
                                       "y": response["data"]["y"]}
            return self.character_location
        else:
            print(f"Error getting character location: {response['error']}")
            return None

    def run(self):
        self.character_location = self.get_character_location()
        if self.character_location is None:
            # print("Failed to get character location")
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