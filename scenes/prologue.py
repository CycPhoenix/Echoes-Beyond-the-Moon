import pygame
from utils.constants import SCENE_LEVEL1, SCREEN_WIDTH, SCREEN_HEIGHT

LINES = [
    "Luna, a curious girl, wanders into a mysterious forest...",
    "She finds an abandoned cabin with a glowing grand piano.",
    "She presses a key. The air shimmers. A portal opens.",
    "Luna is pulled in — and wakes up on the Moon.",
    "",
    "Press ENTER to continue...",
]


class PrologueScene:
    def __init__(self, screen, state):
        self.screen = screen
        self.state  = state
        self.font   = pygame.font.SysFont(None, 38)

    def update(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                return SCENE_LEVEL1
        return None

    def draw(self):
        self.screen.fill((5, 5, 20))
        y = SCREEN_HEIGHT // 2 - (len(LINES) * 44) // 2
        for line in LINES:
            surf = self.font.render(line, True, (210, 210, 240))
            self.screen.blit(surf, surf.get_rect(center=(SCREEN_WIDTH // 2, y)))
            y += 44
