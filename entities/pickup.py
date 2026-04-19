import pygame
from utils.constants import CYAN, OXYGEN_TANK_REFILL


class Pickup(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, kind: str):
        super().__init__()
        self.kind = kind  # "gem" or "o2"
        size = 20
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        color = CYAN if kind == "o2" else (255, 220, 50)
        pygame.draw.circle(self.image, color, (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect(topleft=(x, y))

    @property
    def value(self):
        return OXYGEN_TANK_REFILL if self.kind == "o2" else 1
