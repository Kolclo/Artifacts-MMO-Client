from data.character import Character
from data.monster import Monster
import pygame
from pygame_util import PygameUtils

class BattleSimulator:
    def __init__(self, player_character: Character, enemy_monster: Monster, pygame_data) -> None:
        self.pygame_utils = pygame_data
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 800, 800
        self.WHITE: tuple[int, int, int] = (255, 255, 255)
        self.BLACK: tuple[int, int, int] = (0, 0, 0)
        self.FONT_SIZE: int = 48
        self.icon: pygame.Surface = pygame.image.load("Artifacts_MMO_Client/resources/window/icon1.png")
        self.window_name: str = "ArtifactsMMO - Monster Battle"
        self.window = self.pygame_utils.pygame_init(self.WINDOW_WIDTH, self.WINDOW_HEIGHT, self.window_name, self.icon)
        self.clock = pygame.time.Clock()
        self.player_character = player_character
        self.enemy_monster = enemy_monster
        self.player_character_sprite = pygame.image.load(f"Artifacts_MMO_Client/resources/characters/{player_character.skin}.png")
        self.player_character_sprite = pygame.transform.scale(self.player_character_sprite, (100, 100))
        self.enemy_monster_sprite = pygame.image.load(f"Artifacts_MMO_Client/resources/monsters/{enemy_monster.code}.png")
        self.enemy_monster_sprite = pygame.transform.scale(self.enemy_monster_sprite, (100, 100))
        self.battle_entrance_music = pygame.mixer.Sound("Artifacts_MMO_Client/resources/music/battle1.mp3")
        self.battle_entrance_music.play()

    def run(self) -> None:
        player_character_x = 100
        player_character_y = 200
        enemy_monster_x = 600
        enemy_monster_y = 200
        player_character_move_speed = 1
        enemy_monster_move_speed = 1
        battle_in_progress = True
        while battle_in_progress:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    battle_in_progress = False

            self.window.fill((0, 0, 0))
            self.window.blit(self.player_character_sprite, (player_character_x, player_character_y))
            self.window.blit(self.enemy_monster_sprite, (enemy_monster_x, enemy_monster_y))
            pygame.display.flip()
            player_character_x += player_character_move_speed
            enemy_monster_x -= enemy_monster_move_speed
            if player_character_x >= 600:
                player_character_move_speed *= -1
            if enemy_monster_x <= 100:
                enemy_monster_move_speed *= -1
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    from api_actions import Get
    get_request = Get()
    characters = get_request.characters()
    player_character = characters[0]
    monster = get_request.monster("red_slime")
    battle_simulator = BattleSimulator(player_character, monster)
    battle_simulator.run()
