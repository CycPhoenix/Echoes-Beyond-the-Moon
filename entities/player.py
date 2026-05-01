import os
import pygame
from utils.constants import (GRAVITY, JUMP_FORCE, MOVE_SPEED, MAX_FALL_SPEED,
                              MAX_LIVES, SCREEN_HEIGHT)

_BASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "character", "char_split")


def _load_frames(folder: str, size: tuple[int, int]) -> list[pygame.Surface]:
    path = os.path.join(_BASE, folder)
    files = sorted(f for f in os.listdir(path) if f.endswith(".png"))
    return [pygame.transform.scale(
        pygame.image.load(os.path.join(path, f)).convert_alpha(), size
    ) for f in files]


def _load_single(rel: str, size: tuple[int, int]) -> pygame.Surface:
    return pygame.transform.scale(
        pygame.image.load(os.path.join(_BASE, rel)).convert_alpha(), size
    )


_SIZE = (48, 96)   # ~0.5:1 ratio — matches natural proportions of sprites


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()

        # Load all animation frames
        self._anims = {
            "IDLE_R":  [_load_single("char_idle_new.png", _SIZE)],
            "IDLE_L":  [pygame.transform.flip(_load_single("char_idle_new.png", _SIZE), True, False)],
            "WALK_R":  _load_frames("character_walk_right_new", _SIZE),
            "WALK_L":  _load_frames("character_walk_left_new",  _SIZE),
            "JUMP_R":  _load_frames("character_small_jump_right_new", _SIZE),
            "JUMP_L":  _load_frames("character_small_jump_left_new",  _SIZE),
            "RUN_R":   _load_frames("run_right", _SIZE),
            "RUN_L":   _load_frames("run_left",  _SIZE),
        }
        self._anim_key  = "IDLE_R"
        self._frame_idx = 0
        self._frame_timer = 0
        self._frame_speed = 6   # frames between animation advances

        self.image = self._anims["IDLE_R"][0]
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
        self._animate()
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

    def _animate(self):
        if self.state == "DEATH":
            return

        # Pick anim key
        if self.state in ("IDLE", "PANIC"):
            key = "IDLE_R" if self.facing_right else "IDLE_L"
        elif self.state == "WALK":
            key = "WALK_R" if self.facing_right else "WALK_L"
        elif self.state == "JUMP":
            key = "JUMP_R" if self.facing_right else "JUMP_L"
        else:
            key = "IDLE_R" if self.facing_right else "IDLE_L"

        if key != self._anim_key:
            self._anim_key  = key
            self._frame_idx = 0
            self._frame_timer = 0

        frames = self._anims[self._anim_key]
        self._frame_timer += 1
        if self._frame_timer >= self._frame_speed:
            self._frame_timer = 0
            self._frame_idx = (self._frame_idx + 1) % len(frames)

        self.image = frames[self._frame_idx]

    def take_damage(self):
        if self.invincible > 0:
            return
        self.lives -= 1
        self.invincible = 120
        self.state = "HURT"
        if self.lives <= 0:
            self.die()

    def die(self):
        self.state = "DEATH"
