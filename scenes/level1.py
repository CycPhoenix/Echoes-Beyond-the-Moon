from __future__ import annotations
import random
import pygame

from utils.constants import (SCREEN_WIDTH, SCREEN_HEIGHT, BLACK,
                              SCENE_HANDOFF, SCENE_GAMEOVER,
                              METEOR_SPAWN_FRAMES, OXYGEN_VENT_REFILL,
                              VENDING_GEM_COST, OXYGEN_MAX)
from utils.game_state import GameState
from entities.player   import Player
from entities.meteor   import EyeMeteor
from entities.platform import Platform
from entities.pickup   import Pickup
from systems.oxygen    import OxygenSystem
from systems.hud       import HUD
from systems.camera    import Camera
from systems.particles import ParticleSystem

# Max reachable gap given JUMP_FORCE=-14, GRAVITY=0.2, MOVE_SPEED=4
_MAX_GAP_X = 320
_MAX_GAP_Y = 200


def _generate_level():
    rng = random.Random()   # new seed every run
    platforms, gems, o2_tanks, vents, vending = [], [], [], [], []

    # Starting ground
    platforms.append((0, 650, 700, 20, False))
    gems.append((200, 620))
    gems.append((500, 620))
    o2_tanks.append((350, 620))

    x, y = 700, 650

    for i in range(20):
        gap_x = rng.randint(60, _MAX_GAP_X)
        gap_y = rng.randint(-_MAX_GAP_Y, _MAX_GAP_Y)
        w     = rng.randint(140, 320)
        new_y = max(200, min(650, y + gap_y))
        is_qs = rng.random() < 0.12

        px = x + gap_x
        platforms.append((px, new_y, w, 20, is_qs))

        # Gems on top of platform
        for gx in range(px + 20, px + w - 20, 60):
            if rng.random() < 0.5:
                gems.append((gx, new_y - 24))

        # O2 tank every ~4 platforms
        if i % 4 == 2:
            o2_tanks.append((px + w // 2 - 10, new_y - 24))

        # Vent every ~5 platforms
        if i % 5 == 3:
            vents.append((px + 10, new_y - 28))

        # Vending machine every ~7 platforms
        if i % 7 == 5:
            vending.append((px + w // 2 - 16, new_y - 52))

        x = px + w
        y = new_y

    # Airlock platform at end
    airlock_x = x + 120
    platforms.append((airlock_x, y, 500, 20, False))

    return platforms, gems, o2_tanks, vents, vending, airlock_x + 480


class VendingMachine(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((32, 48))
        self.image.fill((100, 100, 200))
        self.rect  = self.image.get_rect(topleft=(x, y))
        self.interaction_rect = self.rect.inflate(40, 0)


class OxygenVent(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((24, 24))
        self.image.fill((80, 200, 220))
        self.rect  = self.image.get_rect(topleft=(x, y))


class Level1Scene:
    def __init__(self, screen: pygame.Surface, state: GameState):
        self.screen = screen
        self.state  = state

        self.camera    = Camera()
        self.o2        = OxygenSystem()
        self.player    = Player(100, 580)
        self.particles = ParticleSystem()
        self.hud       = HUD(self.o2, self.player)

        self.platforms = pygame.sprite.Group()
        self.meteors   = pygame.sprite.Group()
        self.pickups   = pygame.sprite.Group()
        self.vents     = pygame.sprite.Group()
        self.vending   = pygame.sprite.Group()

        self._build_level()

        self.meteor_timer = 0
        self.bg_color     = (10, 5, 25)
        self.font         = pygame.font.SysFont(None, 36)
        self.death_timer  = 0
        self.next_scene   = None

    def _build_level(self):
        plats, gems, o2s, vents, vending, airlock_x = _generate_level()
        self.airlock_x = airlock_x
        for x, y, w, h, qs in plats:
            self.platforms.add(Platform(x, y, w, h, is_quicksand=qs))
        for x, y in gems:
            self.pickups.add(Pickup(x, y, "gem"))
        for x, y in o2s:
            self.pickups.add(Pickup(x, y, "o2"))
        for x, y in vents:
            self.vents.add(OxygenVent(x, y))
        for x, y in vending:
            self.vending.add(VendingMachine(x, y))

    def update(self, dt) -> str | None:
        if self.next_scene:
            return self.next_scene

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                self._try_vend()

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

        self._check_vents()
        self._check_pickups()
        self._spawn_meteors()
        self.meteors.update(self.platforms)
        self._check_meteor_hits()

        self.camera.update(self.player)
        self.hud.update()
        self.particles.update()

        if self._at_airlock():
            self.state.lives = self.player.lives
            self.state.gems  = self.player.gems
            return SCENE_HANDOFF

        return None

    def draw(self):
        self.screen.fill(self.bg_color)
        self._draw_stars()
        for sprite in list(self.platforms) + list(self.vents) + list(self.vending) + list(self.pickups) + list(self.meteors):
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        self.screen.blit(self.player.image, self.camera.apply(self.player))
        self.particles.draw(self.screen, self.camera)
        self.hud.draw(self.screen)

        if self.player.state == "DEATH":
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, min(255, self.death_timer * 2)))
            self.screen.blit(overlay, (0, 0))
            if self.death_timer > 60:
                txt = self.font.render("LOST IN THE VOID", True, (200, 80, 80))
                self.screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

    def _draw_stars(self):
        # Simple static stars — seed for consistency
        rng = random.Random(42)
        for _ in range(120):
            x = rng.randint(0, SCREEN_WIDTH)
            y = rng.randint(0, SCREEN_HEIGHT // 2)
            pygame.draw.circle(self.screen, (255, 255, 255), (x, y), 1)

    def _check_vents(self):
        for vent in self.vents:
            if self.player.rect.colliderect(vent.rect):
                self.o2.refill(OXYGEN_VENT_REFILL)
                self.particles.spawn_o2_mist(vent.rect.centerx, vent.rect.top)

    def _check_pickups(self):
        hits = pygame.sprite.spritecollide(self.player, self.pickups, True)
        for item in hits:
            if item.kind == "gem":
                self.player.gems += item.value
                self.particles.spawn_shard_pickup(item.rect.centerx, item.rect.centery)
            elif item.kind == "o2":
                self.o2.refill(item.value)

    def _spawn_meteors(self):
        self.meteor_timer += 1
        if self.meteor_timer >= METEOR_SPAWN_FRAMES:
            self.meteor_timer = 0
            spawn_x = self.camera.offset_x + random.randint(100, SCREEN_WIDTH - 100)
            self.meteors.add(EyeMeteor(spawn_x, self.player))

    def _check_meteor_hits(self):
        hits = pygame.sprite.spritecollide(self.player, self.meteors, True)
        for _ in hits:
            self.player.take_damage()
            self.particles.spawn_explosion(self.player.pos)

    def _try_vend(self):
        for vm in self.vending:
            if self.player.rect.colliderect(vm.interaction_rect):
                if self.player.gems >= VENDING_GEM_COST:
                    self.player.gems -= VENDING_GEM_COST
                    self.o2.refill(float(OXYGEN_MAX))

    def _at_airlock(self) -> bool:
        return self.player.pos.x >= self.airlock_x
