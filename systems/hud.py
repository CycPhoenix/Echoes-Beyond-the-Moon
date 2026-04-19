import pygame
from utils.constants import (SCREEN_WIDTH, RED, CYAN, WHITE, WARN_COLOR,
                              OXYGEN_MAX, OXYGEN_WARN)


class HUD:
    def __init__(self, o2, player):
        self.o2     = o2
        self.player = player
        self.warn_timer = 0
        self.font   = pygame.font.SysFont(None, 28)
        self.big_font = pygame.font.SysFont(None, 48)

    def update(self):
        if self.o2.is_critical:
            self.warn_timer += 1
        else:
            self.warn_timer = 0

    def draw(self, screen: pygame.Surface):
        self._draw_o2_bar(screen)
        self._draw_lives(screen)
        self._draw_gems(screen)
        if self.o2.is_critical:
            self._draw_low_oxygen(screen)

    def _draw_o2_bar(self, screen):
        bx, by, bw, bh = 20, 20, 200, 20
        fill  = int(bw * self.o2.fraction)
        color = RED if self.o2.is_critical else CYAN
        pygame.draw.rect(screen, (40, 40, 40), (bx, by, bw, bh))
        pygame.draw.rect(screen, color,        (bx, by, fill, bh))
        pygame.draw.rect(screen, WHITE,        (bx, by, bw, bh), 2)
        label = self.font.render("O2", True, WHITE)
        screen.blit(label, (bx + bw + 6, by))

    def _draw_lives(self, screen):
        label = self.font.render(f"Lives: {self.player.lives}", True, WHITE)
        screen.blit(label, (20, 48))

    def _draw_gems(self, screen):
        label = self.font.render(f"Gems: {self.player.gems}", True, WHITE)
        screen.blit(label, (SCREEN_WIDTH - 140, 20))

    def _draw_low_oxygen(self, screen):
        alpha = int(abs(pygame.math.Vector2(1, 0).rotate(self.warn_timer * 5).x) * 180)
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((255, 0, 0, max(0, min(60, alpha))))
        screen.blit(overlay, (0, 0))
        pulse = abs(pygame.math.Vector2(1, 0).rotate(self.warn_timer * 5).x)
        if pulse > 0.5:
            warn = self.big_font.render("LOW OXYGEN", True, WARN_COLOR)
            screen.blit(warn, warn.get_rect(center=(SCREEN_WIDTH // 2, 80)))
