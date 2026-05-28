import math
import pygame
import pygame_menu
import pygame_menu.widgets
import sys

from utils.constants import (SCREEN_WIDTH, SCREEN_HEIGHT,
                              SCENE_PROLOGUE, SCENE_LEVEL1, SCENE_LEVEL2, SCENE_SETTINGS)

_GLOW_COLOR = (120, 190, 255)   # light blue glow


class MainMenuScene:
    def __init__(self, screen, state):
        self.screen = screen
        self.state  = state
        self._next  = None

        # ── Background (lab3 technique: load + scale to screen) ──
        raw = pygame.image.load("assets/menu/mainmenu_final.png")
        self.bg = pygame.transform.scale(raw, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # ── pygame_menu custom theme ──────────────────────────────────────
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.background_color        = (8,  12, 35, 210)
        theme.title_background_color  = (5,   8, 25, 230)
        theme.title_bar_style         = pygame_menu.widgets.MENUBAR_STYLE_NONE
        theme.widget_font             = pygame_menu.font.FONT_OPEN_SANS_BOLD
        theme.widget_font_color       = (220, 240, 255)
        theme.widget_font_size        = 28
        theme.widget_padding          = (8, 40)
        theme.scrollarea_outer_margin = (0, 0)
        theme.widget_margin           = (0, 10)
        theme.widget_alignment        = pygame_menu.locals.ALIGN_CENTER
        # Disable built-in flat highlight — we use our own glow instead
        theme.widget_selection_effect = pygame_menu.widgets.NoneSelection()

        menu_w, menu_h = 420, 340
        self.menu = pygame_menu.Menu(
            title='',
            width=menu_w,
            height=menu_h,
            theme=theme,
            center_content=False,
        )
        self.menu.add.button('Start Game', self._start)
        self.menu.add.button('Level 1',    self._level1)
        self.menu.add.button('Level 2',    self._level2)
        self.menu.add.button('Settings',   self._settings)
        self.menu.add.button('Quit',       self._quit)

        self.menu.set_relative_position(50, 85)

        # ── Audio ─────────────────────────────────────────────────────────
        pygame.mixer.music.load("assets/audio/backgroundmusic/intro.mp3")
        pygame.mixer.music.set_volume(0.35)
        pygame.mixer.music.play(-1)   # loop forever

        self._sfx_select  = pygame.mixer.Sound("assets/audio/soundeffects/menu_select.wav")
        self._sfx_select.set_volume(0.6)
        self._last_selected = None    # track selection changes

    # ── Glow helper ───────────────────────────────────────────────────────
    def _draw_glow(self, rect):
        """Draw pulsing concentric border rings around rect to simulate glow."""
        t     = pygame.time.get_ticks() / 1000.0
        pulse = 0.5 + 0.5 * math.sin(t * 3)   # 0.0 → 1.0, cycles ~3×/sec
        r, g, b = _GLOW_COLOR
        for i in range(1, 8):
            alpha   = int(pulse * 95 * (8 - i) / 7)
            expand  = i * 3
            gr      = rect.inflate(expand * 2, expand * 2)
            surf    = pygame.Surface(gr.size, pygame.SRCALPHA)
            pygame.draw.rect(surf, (r, g, b, alpha),
                             surf.get_rect(), width=2, border_radius=6)
            self.screen.blit(surf, gr.topleft)

    # ── Button callbacks ──────────────────────────────────────────────────
    def _start(self):
        self._next = SCENE_PROLOGUE

    def _level1(self):
        self._next = SCENE_LEVEL1

    def _level2(self):
        self._next = SCENE_LEVEL2

    def _settings(self):
        self._next = SCENE_SETTINGS

    def _quit(self):
        pygame.quit()
        sys.exit()

    # ── Scene interface ───────────────────────────────────────────────────
    def update(self, dt):
        events = pygame.event.get()
        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self.menu.update(events)

        # Play select sound when highlighted button changes
        sel = self.menu.get_selected_widget()
        if sel is not None and sel is not self._last_selected:
            self._sfx_select.play()
            self._last_selected = sel

        result, self._next = self._next, None
        return result

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        self.menu.draw(self.screen)

        # Draw glow on top of the menu, around whichever button is selected
        sel = self.menu.get_selected_widget()
        if sel:
            self._draw_glow(sel.get_rect(to_real_position=True))
