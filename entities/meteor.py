import os
import pygame
from utils.constants import (METEOR_SPEED, METEOR_TRACK_FRAMES, SCREEN_HEIGHT, ORANGE)

_BASE     = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "level1")
_MTR_SIZE = (48, 48)


class EyeMeteor(pygame.sprite.Sprite):
    def __init__(self, x: int, target):
        super().__init__()
        src = pygame.image.load(os.path.join(_BASE, "Meteors.png")).convert_alpha()
        self.image  = pygame.transform.scale(src, _MTR_SIZE)
        self.rect   = self.image.get_rect(topleft=(x, -60))

        self.pos      = pygame.math.Vector2(x, -60)
        self.vel      = pygame.math.Vector2(0, 1.5)
        self.target   = target
        self.phase    = "DRIFT"
        self.timer    = 0
        self.locked_x = 0.0

    def update(self, platforms):
        self.timer += 1

        if self.phase == "DRIFT":
            self.pos += self.vel
            if self.timer >= METEOR_TRACK_FRAMES:
                self.locked_x = self.target.pos.x
                self.phase = "LOCK"

        elif self.phase == "LOCK":
            dx = self.locked_x - self.pos.x
            self.vel.x += 0.15 * (1 if dx > 0 else -1)
            self.vel.x  = max(-METEOR_SPEED, min(METEOR_SPEED, self.vel.x))
            self.vel.y  = METEOR_SPEED
            self.pos   += self.vel

        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                self.kill()
                return

        if self.pos.y > SCREEN_HEIGHT + 50:
            self.kill()
