import pygame
from controller import CharacterController
from game_state import GameState

class EventHandler:
    def __init__(self, game_state):
        self.controller: CharacterController = CharacterController(game_state)
        self.game_state: GameState = game_state
        # self.move_up: int = 0
        # self.move_down: int = 0
        # self.move_left: int = 0
        # self.move_right: int = 0
        # self.cooldown: int = 0

    def handle_events(self) -> bool:
        """Handles pygame events and updates the character's position accordingly.

        Updates the grid by calling draw_grid and then redraws the window with the updated grid.

        Returns:
            bool: True if the game should continue, False if the game should quit
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if self.game_state.character_data.is_cooldown_active() < 0:
                    if event.key == pygame.K_LEFT:
                        self.controller.move_left()
                    elif event.key == pygame.K_RIGHT:
                        self.controller.move_right()
                    elif event.key == pygame.K_UP:
                        self.controller.move_up()
                    elif event.key == pygame.K_DOWN:
                        self.controller.move_down()
                    elif event.key == pygame.K_SPACE:
                        self.controller.perform_action()
                    elif event.key == pygame.K_w:
                        self.controller.unequip("weapon")
                    
                    return "Update render"

                    pygame.display.flip()
                else:
                    print(f"Unable to perform action, character in cooldown for {self.game_state.character_data.is_cooldown_active()}s")

        return True