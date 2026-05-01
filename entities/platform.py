import os
import pygame

_BASE    = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "level1")
_PLT_IMG = os.path.join(_BASE, "platform.png")
_QS_IMG  = os.path.join(_BASE, "moonsurface_horizontal_.png")


class Platform(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, w: int, h: int, is_quicksand: bool = False):
        super().__init__()
        src = pygame.image.load(_QS_IMG if is_quicksand else _PLT_IMG).convert_alpha()
        self.image = pygame.transform.scale(src, (w, h))
        self.rect  = self.image.get_rect(topleft=(x, y))
        self.is_quicksand = is_quicksand
