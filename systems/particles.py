import random
import math
import pygame
from utils.constants import CYAN


class Particle:
    def __init__(self, x, y, vx, vy, color, life, radius):
        self.pos    = pygame.math.Vector2(x, y)
        self.vel    = pygame.math.Vector2(vx, vy)
        self.color  = color
        self.life   = life
        self.max_life = life
        self.radius = radius

    def update(self):
        self.vel.y += 0.05
        self.pos   += self.vel
        self.vel   *= 0.97
        self.life  -= 1

    @property
    def alpha(self) -> int:
        return int(255 * max(0, self.life / self.max_life))

    @property
    def alive(self) -> bool:
        return self.life > 0


class ParticleSystem:
    def __init__(self):
        self.particles: list[Particle] = []

    def spawn_dust(self, x: int, y: int, count: int = 8):
        for _ in range(count):
            self.particles.append(Particle(
                x, y,
                vx=random.uniform(-2, 2),
                vy=random.uniform(-3, -1),
                color=(200, 200, 170),
                life=random.randint(24, 48),
                radius=random.randint(2, 4),
            ))

    def spawn_explosion(self, pos: pygame.math.Vector2, count: int = 20):
        for _ in range(count):
            angle = random.uniform(0, 360)
            speed = random.uniform(2, 6)
            self.particles.append(Particle(
                pos.x, pos.y,
                vx=math.cos(math.radians(angle)) * speed,
                vy=math.sin(math.radians(angle)) * speed,
                color=(random.randint(200, 255), random.randint(80, 160), 0),
                life=random.randint(30, 60),
                radius=random.randint(2, 5),
            ))

    def spawn_shard_pickup(self, x: int, y: int):
        for _ in range(6):
            self.particles.append(Particle(
                x, y,
                vx=random.uniform(-1, 1),
                vy=random.uniform(-3, -1),
                color=CYAN,
                life=random.randint(18, 36),
                radius=random.randint(1, 3),
            ))

    def spawn_o2_mist(self, x: int, y: int, count: int = 5):
        for _ in range(count):
            self.particles.append(Particle(
                x + random.randint(-10, 10), y,
                vx=random.uniform(-0.5, 0.5),
                vy=random.uniform(-2, -0.5),
                color=(100, 200, 255),
                life=random.randint(30, 50),
                radius=random.randint(2, 4),
            ))

    def update(self):
        self.particles = [p for p in self.particles if p.alive]
        for p in self.particles:
            p.update()

    def draw(self, screen: pygame.Surface, camera):
        for p in self.particles:
            surf = pygame.Surface((p.radius * 2, p.radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (*p.color, p.alpha), (p.radius, p.radius), p.radius)
            pos = camera.apply_rect(pygame.Rect(p.pos.x, p.pos.y, 0, 0))
            screen.blit(surf, (pos.x - p.radius, pos.y - p.radius))
