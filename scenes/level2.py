import pygame
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT

# OTHER TEAM'S PART — Level 2: The Lunar Base Siege
class Level2Scene:
    def __init__(self, screen, state):
        self.screen = screen
        self.state = state
        self.font = pygame.font.SysFont(None, 48)

    def update(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
        return None

    def draw(self):
        self.screen.fill((10, 10, 30))
        text = self.font.render("Level 2 — Work in Progress", True, (255, 255, 255))
        self.screen.blit(text, text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
