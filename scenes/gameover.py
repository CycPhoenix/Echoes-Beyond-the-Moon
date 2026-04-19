import pygame
from utils.constants import SCENE_LEVEL1, SCENE_MENU, SCREEN_WIDTH, SCREEN_HEIGHT
from utils.game_state import GameState


class GameOverScene:
    def __init__(self, screen: pygame.Surface, state: GameState):
        self.screen     = screen
        self.state      = state
        self.font_big   = pygame.font.SysFont(None, 80)
        self.font_small = pygame.font.SysFont(None, 40)

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
