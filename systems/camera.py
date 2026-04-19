import pygame
from utils.constants import SCREEN_WIDTH


class Camera:
    def __init__(self):
        self.offset_x = 0

    def update(self, target: pygame.sprite.Sprite):
        self.offset_x = target.rect.centerx - int(SCREEN_WIDTH * 0.35)
        self.offset_x = max(0, self.offset_x)

    def apply(self, sprite: pygame.sprite.Sprite) -> pygame.Rect:
        return sprite.rect.move(-self.offset_x, 0)

    def apply_rect(self, rect: pygame.Rect) -> pygame.Rect:
        return rect.move(-self.offset_x, 0)
