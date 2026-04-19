import pygame
from utils.constants import (GRAVITY, JUMP_FORCE, MOVE_SPEED, MAX_FALL_SPEED,
                              MAX_LIVES, SCREEN_HEIGHT)


class Player(pygame.sprite.Sprite):
    ROW_IDLE  = 0
    ROW_WALK  = 1
    ROW_JUMP  = 2
    ROW_HURT  = 3
    ROW_PANIC = 4

    def __init__(self, x: int, y: int):
        super().__init__()
        self.image = pygame.Surface((32, 48), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (180, 140, 200), (0, 0, 32, 48))
        self.rect  = self.image.get_rect(topleft=(x, y))

        self.vel          = pygame.math.Vector2(0, 0)
        self.pos          = pygame.math.Vector2(x, y)
        self.on_ground    = False
        self.facing_right = True
        self.lives        = MAX_LIVES
        self.gems         = 0
        self.invincible   = 0
        self.state        = "IDLE"

    def update(self, keys, platforms, o2):
        self._handle_input(keys)
        self._apply_physics()
        self._collide(platforms, o2)
        self._update_state(o2)
        if self.invincible > 0:
            self.invincible -= 1

    def _handle_input(self, keys):
        moving = False
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vel.x = -MOVE_SPEED
            self.facing_right = False
            moving = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vel.x = MOVE_SPEED
            self.facing_right = True
            moving = True
        else:
            self.vel.x *= 0.75

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel.y = JUMP_FORCE
            self.on_ground = False

        if self.on_ground:
            self.state = "WALK" if moving else "IDLE"
        else:
            self.state = "JUMP"

    def _apply_physics(self):
        self.vel.y = min(self.vel.y + GRAVITY, MAX_FALL_SPEED)
        self.pos  += self.vel
        self.rect.topleft = (int(self.pos.x), int(self.pos.y))

    def _collide(self, platforms, o2):
        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat.rect):
                if self.vel.y > 0 and self.rect.bottom - self.vel.y <= plat.rect.top + 10:
                    self.rect.bottom = plat.rect.top
                    self.pos.y = float(self.rect.y)
                    self.vel.y = 0
                    self.on_ground = True
                    if hasattr(plat, "is_quicksand") and plat.is_quicksand:
                        o2.level = max(0.0, o2.level - 0.05)

        if self.pos.y > SCREEN_HEIGHT + 100:
            self.die()

    def _update_state(self, o2):
        if o2.is_critical and self.state in ("IDLE", "WALK"):
            self.state = "PANIC"
        if o2.is_empty:
            self.die()

    def take_damage(self):
        if self.invincible > 0:
            return
        self.lives  -= 1
        self.invincible = 120
        self.state  = "HURT"
        if self.lives <= 0:
            self.die()

    def die(self):
        self.state = "DEATH"
