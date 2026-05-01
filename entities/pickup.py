import os
import pygame
from utils.constants import OXYGEN_TANK_REFILL

_BASE   = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "level1")
_SIZE   = (32, 32)


class Pickup(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, kind: str):
        super().__init__()
        self.kind = kind  # "gem" or "o2"
        fname = "O^2.png" if kind == "o2" else "Crystal.png"
        src   = pygame.image.load(os.path.join(_BASE, fname)).convert_alpha()
        self.image = pygame.transform.scale(src, _SIZE)
        self.rect  = self.image.get_rect(topleft=(x, y))

    @property
    def value(self):
        return OXYGEN_TANK_REFILL if self.kind == "o2" else 1
