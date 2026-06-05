from __future__ import annotations
import os
import random
import pygame

from utils.constants import (SCREEN_WIDTH, SCREEN_HEIGHT, BLACK,
                              SCENE_MENU, SCENE_LEVEL1, SCENE_HANDOFF, SCENE_GAMEOVER,
                              METEOR_SPAWN_FRAMES)
from utils.game_state import GameState
from entities.player   import Player
from entities.meteor   import EyeMeteor
from entities.platform import Platform
from entities.pickup   import Pickup
from systems.oxygen     import OxygenSystem
from systems.hud        import HUD
from systems.camera     import Camera
from systems.particles  import ParticleSystem
from systems.animation  import FrameAnimation

# Gaps tuned for JUMP_FORCE=-10, GRAVITY=0.25, MOVE_SPEED=4
# Max height ~200px, max horiz ~240px — keep gaps well under that
_MAX_GAP_X = 160
_MAX_GAP_Y = 80
_GROUND_Y  = 650


def _generate_level():
    rng = random.Random()
    platforms, gems, o2_tanks = [], [], []

    # Long starting ground
    platforms.append((0, _GROUND_Y, 800, 20, False))
    gems.append((200, _GROUND_Y - 30))
    gems.append((500, _GROUND_Y - 30))
    o2_tanks.append((350, _GROUND_Y - 30))

    x, y = 800, _GROUND_Y

    for i in range(18):
        gap_x = rng.randint(40, _MAX_GAP_X)
        gap_y = rng.randint(-_MAX_GAP_Y, _MAX_GAP_Y)
        w     = rng.randint(180, 340)
        new_y = max(300, min(_GROUND_Y, y + gap_y))

        px = x + gap_x
        platforms.append((px, new_y, w, 20, False))

        # Gems along platform
        for gx in range(px + 20, px + w - 20, 55):
            if rng.random() < 0.45:
                gems.append((gx, new_y - 28))

        # O2 tank every ~4 platforms
        if i % 4 == 2:
            o2_tanks.append((px + w // 2 - 10, new_y - 28))

        x = px + w
        y = new_y

    # Final flat ground leading into the base
    base_ground_x = x + 60
    base_ground_y = _GROUND_Y
    platforms.append((base_ground_x, base_ground_y, 900, 20, False))

    airlock_trigger = base_ground_x + 750

    return platforms, gems, o2_tanks, base_ground_x, base_ground_y, airlock_trigger



_BASE_IMG_W = 600
_BASE_IMG_H = int(_BASE_IMG_W * 1215 / 2160)   # ~338px, preserves aspect ratio


class ScienceBase:
    """Drawn at the end of level 1 — sciencelab_dooropen.png sprite."""
    def __init__(self, x: int, ground_y: int):
        self.x        = x
        self.ground_y = ground_y

        src = pygame.image.load(os.path.join(_ASSETS, "level1", "sciencelab_dooropen.png")).convert_alpha()
        self.image = pygame.transform.scale(src, (_BASE_IMG_W, _BASE_IMG_H))

        # Door collision rect — roughly centre-bottom of building
        door_w, door_h = 80, 100
        self.door_rect = pygame.Rect(
            x + _BASE_IMG_W // 2 - door_w // 2,
            ground_y - door_h,
            door_w, door_h
        )

    def update(self):
        pass   # no animation needed

    def draw(self, screen: pygame.Surface, camera):
        gx = self.x - camera.offset_x
        gy = self.ground_y - _BASE_IMG_H   # bottom of image sits on ground
        screen.blit(self.image, (gx, gy))



_ASSETS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")


def _load_bg(name: str) -> pygame.Surface:
    return pygame.transform.scale(
        pygame.image.load(os.path.join(_ASSETS, name)).convert(),
        (SCREEN_WIDTH, SCREEN_HEIGHT)
    )


class Level1Scene:
    def __init__(self, screen: pygame.Surface, state: GameState):
        self.screen = screen
        self.state  = state

        pygame.mixer.music.stop()
        try:
            pygame.mixer.music.load(os.path.join(_ASSETS, "audio", "backgroundmusic", "lvl1_audio.mp3"))
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)
        except Exception:
            pass

        # Background
        self.bg_far  = _load_bg("level1/lv1_background.png")

        self.camera    = Camera()
        self.o2        = OxygenSystem()
        self.player    = Player(100, 490)   
        self.particles = ParticleSystem()
        self.hud       = HUD(self.o2, self.player)

        self.platforms = pygame.sprite.Group()
        self.meteors   = pygame.sprite.Group()
        self.pickups   = pygame.sprite.Group()

        self._build_level()

        self.meteor_timer = 0
        self.font         = pygame.font.SysFont(None, 36)

        _sfx = os.path.join(_ASSETS, "audio", "soundeffects")
        self._sfx_collect = None
        self._sfx_energy  = None
        self._sfx_door    = None
        self._door_played = False
        try:
            self._sfx_collect = pygame.mixer.Sound(os.path.join(_sfx, "collect.wav"))
            self._sfx_collect.set_volume(0.6)
        except Exception as e:
            print(f"[audio] collect sfx failed: {e}")
        try:
            self._sfx_energy = pygame.mixer.Sound(os.path.join(_sfx, "energy.mp3"))
            self._sfx_energy.set_volume(0.6)
        except Exception as e:
            print(f"[audio] energy sfx failed: {e}")
        try:
            self._sfx_door = pygame.mixer.Sound(os.path.join(_sfx, "door_unlock.mp3"))
            self._sfx_door.set_volume(0.8)
        except Exception as e:
            print(f"[audio] door_unlock sfx failed: {e}")
        self.death_timer  = 0
        self.next_scene   = None
        self.paused       = False
        self._pause_font  = pygame.font.SysFont(None, 64)
        self._pause_small = pygame.font.SysFont(None, 38)

    def _build_level(self):
        plats, gems, o2s, base_x, base_y, airlock_x = _generate_level()
        self.airlock_x = airlock_x
        self.base      = ScienceBase(base_x + 200, base_y)
        for x, y, w, h, qs in plats:
            self.platforms.add(Platform(x, y, w, h))
        for x, y in gems:
            self.pickups.add(Pickup(x, y, "gem"))
        for x, y in o2s:
            self.pickups.add(Pickup(x, y, "o2"))

    def update(self, dt) -> str | None:
        if self.next_scene:
            return self.next_scene

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.paused = not self.paused
                if self.paused:
                    if event.key == pygame.K_r:
                        return SCENE_LEVEL1
                    if event.key == pygame.K_m:
                        return SCENE_MENU

        if self.paused:
            return None

        if self.player.state == "DEATH":
            self.death_timer += 1
            if self.death_timer > 120:
                self.state.lives = self.player.lives
                self.state.gems  = self.player.gems
                return SCENE_GAMEOVER
            return None

        keys = pygame.key.get_pressed()
        self.player.update(keys, self.platforms, self.o2)
        self.o2.update(self.player.state)

        self._check_pickups()
        self._spawn_meteors()
        self.meteors.update(self.platforms)
        self._check_meteor_hits()

        self.camera.update(self.player)
        self.hud.update()
        self.particles.update()
        self.base.update()

        if self._at_airlock():
            if not self._door_played:
                self._door_played = True
                if self._sfx_door:
                    self._sfx_door.play()
            self.state.lives = self.player.lives
            self.state.gems  = self.player.gems
            pygame.mixer.music.stop()
            return SCENE_HANDOFF

        return None

    def draw(self):
        self._draw_parallax()
        self.base.draw(self.screen, self.camera)
        for sprite in list(self.platforms) + list(self.pickups) + list(self.meteors):
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.screen.blit(self.player.image, self.camera.apply(self.player))
        self.particles.draw(self.screen, self.camera)
        self.hud.draw(self.screen)

        # "Enter base" prompt when near door
        if self.player.rect.inflate(60, 0).colliderect(self.base.door_rect):
            hint = self.font.render("Touch door to enter base", True, (0, 240, 210))
            hint_rect = hint.get_rect(center=(SCREEN_WIDTH // 2, 80))
            self.screen.blit(hint, hint_rect)

        if self.player.state == "DEATH":
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, min(255, self.death_timer * 2)))
            self.screen.blit(overlay, (0, 0))
            if self.death_timer > 60:
                txt = self.font.render("LOST IN THE VOID", True, (200, 80, 80))
                self.screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        if self.paused:
            self._draw_pause()

    def _draw_pause(self):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        cx, cy = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
        box = pygame.Rect(0, 0, 420, 280)
        box.center = (cx, cy)
        pygame.draw.rect(self.screen, (15, 15, 30), box, border_radius=14)
        pygame.draw.rect(self.screen, (0, 200, 180), box, 2, border_radius=14)
        title = self._pause_font.render("PAUSED", True, (0, 220, 200))
        self.screen.blit(title, title.get_rect(center=(cx, cy - 90)))
        for i, text in enumerate(["ESC  —  Resume", "R     —  Restart", "M    —  Main Menu"]):
            surf = self._pause_small.render(text, True, (200, 200, 200))
            self.screen.blit(surf, surf.get_rect(center=(cx, cy - 20 + i * 50)))

    def _draw_parallax(self):
        # Single layer, very slow scroll — only 1 seam, moves slowly enough to be unnoticeable
        scroll = int(self.camera.offset_x * 0.05) % SCREEN_WIDTH
        self.screen.blit(self.bg_far, (-scroll, 0))
        self.screen.blit(self.bg_far, (-scroll + SCREEN_WIDTH, 0))

    def _check_pickups(self):
        hits = pygame.sprite.spritecollide(self.player, self.pickups, True)
        for item in hits:
            if item.kind == "gem":
                self.player.gems += item.value
                self.particles.spawn_shard_pickup(item.rect.centerx, item.rect.centery)
                if self._sfx_collect:
                    self._sfx_collect.play()
            elif item.kind == "o2":
                self.o2.refill(item.value)
                self.particles.spawn_o2_mist(item.rect.centerx, item.rect.centery)
                if self._sfx_collect:
                    self._sfx_collect.stop()
                    self._sfx_collect.play()

    def _spawn_meteors(self):
        self.meteor_timer += 1
        if self.meteor_timer >= METEOR_SPAWN_FRAMES:
            self.meteor_timer = 0
            spawn_x = self.camera.offset_x + random.randint(100, SCREEN_WIDTH - 100)
            self.meteors.add(EyeMeteor(spawn_x))

    def _check_meteor_hits(self):
        hits = pygame.sprite.spritecollide(self.player, self.meteors, True)
        for _ in hits:
            self.player.take_damage()
            self.particles.spawn_explosion(self.player.pos)

    def _at_airlock(self) -> bool:
        return self.player.rect.colliderect(self.base.door_rect)
