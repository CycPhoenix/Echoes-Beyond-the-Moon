import pygame
import sys

from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCENE_PROLOGUE

BLINK_EVENT  = pygame.USEREVENT + 1
CROP_LEFT    = 90
CROP_TOP     = 80
CROP_RIGHT   = 20
CROP_BOTTOM  = 50


class MainMenuScene:
    def __init__(self, screen, state):
        self.screen    = screen
        self.state     = state
        self.show_hint = True

        # ── Load + crop border + scale to screen (lab3 technique) ──
        raw = pygame.image.load("assets/intro/begining/mainmenu_start.png")
        w, h = raw.get_width(), raw.get_height()

        # subsurface trims the transparent checkerboard border (lab5 technique)
        cropped = raw.subsurface(pygame.Rect(
            CROP_LEFT, CROP_TOP,
            w - CROP_LEFT - CROP_RIGHT,
            h - CROP_TOP  - CROP_BOTTOM
        ))
        self.background = pygame.transform.scale(cropped, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Font for blinking prompt
        self.font = pygame.font.Font(None, 42)

        # Blink every 600ms (lab3: USEREVENT + set_timer)
        pygame.time.set_timer(BLINK_EVENT, 600)

    def update(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == BLINK_EVENT:
                self.show_hint = not self.show_hint

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.time.set_timer(BLINK_EVENT, 0)
                    return SCENE_PROLOGUE
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        return None

    def draw(self):
        self.screen.blit(self.background, (0, 0))

        if self.show_hint:
            hint = self.font.render("Press ENTER to Begin Your Adventure", True, (180, 240, 255))
            rect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 45))
            self.screen.blit(hint, rect)
