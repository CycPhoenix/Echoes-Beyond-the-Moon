import pygame
from utils.constants import SCENE_LEVEL2, SCREEN_WIDTH, SCREEN_HEIGHT

# PARTNER'S PART — Level 1: Stranded on the Moon
class Level1Scene:
    def __init__(self, screen, state):
        self.screen = screen
        self.state = state
        self.font = pygame.font.SysFont(None, 48)

    def update(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return SCENE_LEVEL2
        return None

    def draw(self):
        self.screen.fill((10, 10, 30))
        text = self.font.render("Level 1 — Work in Progress", True, (255, 255, 255))
        self.screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
