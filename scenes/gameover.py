import os
import pygame
from utils.constants import SCENE_LEVEL1, SCENE_MENU, SCREEN_WIDTH, SCREEN_HEIGHT
from utils.game_state import GameState

_ASSETS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")


class GameOverScene:
    def __init__(self, screen: pygame.Surface, state: GameState):
        self.screen     = screen
        self.state      = state
        self.font_big   = pygame.font.SysFont(None, 80)
        self.font_small = pygame.font.SysFont(None, 40)

        pygame.mixer.music.stop()
        try:
            pygame.mixer.music.load(os.path.join(_ASSETS, "audio", "backgroundmusic", "gameover.mp3"))
            pygame.mixer.music.set_volume(0.6)
            pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"[audio] gameover music failed: {e}")

    def update(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.state.__init__()   # reset state
                    return SCENE_LEVEL1
                if event.key == pygame.K_ESCAPE:
                    self.state.__init__()
                    return SCENE_MENU
        return None

    def draw(self):
        self.screen.fill((5, 0, 10))
        title  = self.font_big.render("LOST IN THE VOID", True, (200, 60, 60))
        retry  = self.font_small.render("R — Retry", True, (180, 180, 180))
        menu   = self.font_small.render("ESC — Main Menu", True, (180, 180, 180))
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)))
        self.screen.blit(retry, retry.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)))
        self.screen.blit(menu,  menu.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 65)))
