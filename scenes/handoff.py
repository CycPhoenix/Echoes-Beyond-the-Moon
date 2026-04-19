import pygame
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, SCENE_LEVEL2
from utils.game_state import GameState

# Beat: (name, duration_frames)
BEATS = [
    ("FADE_IN",   120),
    ("WALK",      180),
    ("SUIT_SPOT", 120),
    ("SUIT_VFX",  150),
    ("PAUSE",     90),
    ("ALARM",     120),
    ("FADE_OUT",  90),
]


class HandoffScene:
    def __init__(self, screen: pygame.Surface, state: GameState):
        self.screen     = screen
        self.state      = state
        self.beat_index = 0
        self.timer      = 0
        self.alpha      = 255
        self.font       = pygame.font.SysFont(None, 48)
        self.small_font = pygame.font.SysFont(None, 32)
        self.alarm_on   = False

    def update(self, dt) -> str | None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                if self._current_beat() == "SUIT_SPOT":
                    self._advance()

        self.timer += 1
        beat, duration = BEATS[self.beat_index]

        if beat == "FADE_IN":
            self.alpha = max(0, 255 - int(255 * self.timer / duration))
        elif beat == "ALARM":
            self.alarm_on = (self.timer // 8) % 2 == 0
        elif beat == "FADE_OUT":
            self.alpha = min(255, int(255 * self.timer / duration))
            if self.alpha >= 255:
                return SCENE_LEVEL2

        if self.timer >= duration:
            self._advance()

        return None

    def draw(self):
        self.screen.fill((10, 5, 20))
        beat = self._current_beat()

        # Base interior label
        label = self.small_font.render("Science Base — Interior", True, (120, 120, 160))
        self.screen.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, 100))

        if beat == "SUIT_SPOT":
            txt = self.font.render("Press E to equip the suit", True, (200, 200, 100))
            self.screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        elif beat == "SUIT_VFX":
            txt = self.font.render("Suit equipped!", True, (100, 220, 255))
            self.screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        elif beat in ("ALARM", "FADE_OUT"):
            if self.alarm_on:
                alarm_overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
                alarm_overlay.fill((180, 0, 0, 60))
                self.screen.blit(alarm_overlay, (0, 0))
            warn = self.font.render("UNAUTHORIZED LIFEFORM DETECTED", True, (255, 60, 60))
            self.screen.blit(warn, warn.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))

        # Fade overlay
        if self.alpha > 0:
            overlay = pygame.Surface(self.screen.get_size())
            overlay.fill(BLACK)
            overlay.set_alpha(self.alpha)
            self.screen.blit(overlay, (0, 0))

    def _current_beat(self) -> str:
        return BEATS[self.beat_index][0]

    def _advance(self):
        self.beat_index += 1
        self.timer = 0
        if self.beat_index >= len(BEATS):
            self.beat_index = len(BEATS) - 1
