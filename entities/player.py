import os
import pygame
from utils.constants import (GRAVITY, JUMP_FORCE, MOVE_SPEED, MAX_FALL_SPEED,
                              MAX_LIVES, SCREEN_HEIGHT)
import utils.settings_store as store

_BASE      = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "character", "char_split")
_SFX_BASE  = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "audio", "soundeffects")

_ANIM_FOLDERS = {
    "idle": "luna-idle/images",
    "walk": "Luna-run/images",
    "jump": "Luna-jump/images",
    "run":  "Luna-run/images",
}

# Target heights per animation; width is computed from the crop's natural aspect ratio
# so characters are never squeezed.
_TARGET_HEIGHT = 112
_HEIGHT_OVERRIDES = {
    "idle": 100,   # 10% smaller than default
    "jump": 123,   # 10% larger than default
}


def _anim_crop_rect(folder_path: str) -> pygame.Rect:
    """Per-animation bbox so each animation's character fills the frame fully."""
    from PIL import Image as _PIL
    union = None
    for f in sorted(os.listdir(folder_path)):
        if not f.lower().endswith(".png"):
            continue
        bbox = _PIL.open(os.path.join(folder_path, f)).convert("RGBA").getbbox()
        if bbox:
            if union is None:
                union = list(bbox)
            else:
                union[0] = min(union[0], bbox[0])
                union[1] = min(union[1], bbox[1])
                union[2] = max(union[2], bbox[2])
                union[3] = max(union[3], bbox[3])
    if union is None:
        return pygame.Rect(0, 0, 256, 256)
    l, t, r, b = union
    return pygame.Rect(l, t, r - l, b - t)


def _load_all_anims() -> dict:
    result = {}
    for key, folder in _ANIM_FOLDERS.items():
        path  = os.path.join(_BASE, folder)
        crop  = _anim_crop_rect(path)
        h     = _HEIGHT_OVERRIDES.get(key, _TARGET_HEIGHT)
        w     = max(1, round(crop.width * h / crop.height))  # preserve natural aspect ratio
        files = sorted(f for f in os.listdir(path) if f.lower().endswith(".png"))
        surfs = []
        for f in files:
            raw     = pygame.image.load(os.path.join(path, f)).convert_alpha()
            cropped = raw.subsurface(crop).copy()
            scaled  = pygame.transform.scale(cropped, (w, h))
            surfs.append(scaled)
        result[key] = surfs
    return result


class Player(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int):
        super().__init__()

        _a = _load_all_anims()
        self._anims = {
            "IDLE_R":  _a["idle"],
            "IDLE_L":  [pygame.transform.flip(f, True, False) for f in _a["idle"]],
            "WALK_R":  _a["walk"],
            "WALK_L":  [pygame.transform.flip(f, True, False) for f in _a["walk"]],
            "JUMP_R":  _a["jump"],
            "JUMP_L":  [pygame.transform.flip(f, True, False) for f in _a["jump"]],
            "RUN_R":   _a["run"],
            "RUN_L":   [pygame.transform.flip(f, True, False) for f in _a["run"]],
        }
        self._anim_key    = "IDLE_R"
        self._frame_idx   = 0
        self._frame_timer = 0
        self._frame_speed = 4   # advance one frame every 4 game ticks (~15 fps)

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

        self._sfx_jump = None
        try:
            self._sfx_jump = pygame.mixer.Sound(os.path.join(_SFX_BASE, "jump.wav"))
            self._sfx_jump.set_volume(0.5)
        except Exception:
            pass

    def update(self, keys, platforms, o2):
        self._handle_input(keys)
        self._apply_physics()
        self._collide(platforms, o2)
        self._update_state(o2)
        self._animate()
        if self.invincible > 0:
            self.invincible -= 1

    def _handle_input(self, keys):
        k_left  = store.get('key_left')
        k_right = store.get('key_right')
        k_jump  = store.get('key_jump')

        moving = False
        if keys[k_left] or keys[pygame.K_a]:
            self.vel.x = -MOVE_SPEED
            self.facing_right = False
            moving = True
        elif keys[k_right] or keys[pygame.K_d]:
            self.vel.x = MOVE_SPEED
            self.facing_right = True
            moving = True
        else:
            self.vel.x *= 0.75

        if (keys[k_jump] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.vel.y = JUMP_FORCE
            self.on_ground = False
            if self._sfx_jump:
                self._sfx_jump.stop()
                self._sfx_jump.play()

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
                    self.rect.bottom = plat.rect.top + 1  # 1px overlap keeps colliderect reliable
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

        if self.state in ("IDLE", "PANIC"):
            key = "IDLE_R" if self.facing_right else "IDLE_L"
        elif self.state == "WALK":
            key = "WALK_R" if self.facing_right else "WALK_L"
        elif self.state == "JUMP":
            key = "JUMP_R" if self.facing_right else "JUMP_L"
        else:
            key = "IDLE_R" if self.facing_right else "IDLE_L"

        if key != self._anim_key:
            self._anim_key    = key
            self._frame_idx   = 0
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
