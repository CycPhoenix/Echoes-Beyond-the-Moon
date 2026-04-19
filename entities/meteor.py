import pygame
from utils.constants import (METEOR_SPEED, METEOR_TRACK_FRAMES,
                              SCREEN_HEIGHT, ORANGE)


class EyeMeteor(pygame.sprite.Sprite):
    def __init__(self, x: int, target):
        super().__init__()
        self.image = pygame.Surface((24, 24), pygame.SRCALPHA)
        pygame.draw.circle(self.image, ORANGE, (12, 12), 12)
        pygame.draw.circle(self.image, (255, 255, 80), (12, 12), 5)
        self.rect   = self.image.get_rect(topleft=(x, -40))

        self.pos    = pygame.math.Vector2(x, -40)
        self.vel    = pygame.math.Vector2(0, 1.5)
        self.target = target
        self.phase  = "DRIFT"
        self.timer  = 0
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
