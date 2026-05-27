import os
import random
import pygame
from utils.constants import (METEOR_SPEED, SCREEN_HEIGHT)

_BASE     = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "level1")
_MTR_SIZE = (48, 48)


class EyeMeteor(pygame.sprite.Sprite):
    def __init__(self, x: int):
        super().__init__()
        src  = pygame.image.load(os.path.join(_BASE, "Meteors.png")).convert_alpha()
        base = pygame.transform.scale(src, _MTR_SIZE)

        self.pos = pygame.math.Vector2(x, -60)
        # Diagonal streak — strong sideways component, random left or right
        direction = random.choice((-1, 1))
        self.vel  = pygame.math.Vector2(
            direction * random.uniform(2.5, METEOR_SPEED),
            random.uniform(2.5, METEOR_SPEED * 0.8),
        )

        # Flip horizontally when going right so streak faces travel direction
        self.image = pygame.transform.flip(base, direction > 0, False)
        self.rect  = self.image.get_rect(topleft=(x, -60))

    def update(self, platforms):
        # Gravity accelerates fall, no tracking
        self.vel.y = min(self.vel.y + 0.08, METEOR_SPEED * 1.5)
        self.pos  += self.vel
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                self.kill()
                return

        if self.pos.y > SCREEN_HEIGHT + 50:
            self.kill()
