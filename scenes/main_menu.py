import pygame
from utils.constants import SCENE_PROLOGUE, SCREEN_WIDTH, SCREEN_HEIGHT


class MainMenuScene:
    def __init__(self, screen, state):
        self.screen = screen
        self.state  = state
        self.font_title = pygame.font.SysFont(None, 80)
        self.font_btn   = pygame.font.SysFont(None, 48)

    def update(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return SCENE_PROLOGUE
        return None

    def draw(self):
        self.screen.fill((5, 5, 20))
        title = self.font_title.render("Echoes Beyond the Moon", True, (200, 200, 255))
        prompt = self.font_btn.render("Press ENTER to Start", True, (150, 150, 200))
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60)))
        self.screen.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)))
