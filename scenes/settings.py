from __future__ import annotations
import os
import pygame
import pygame_menu
import pygame_menu.widgets

from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCENE_MENU
import utils.settings_store as store

_ASSETS = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")


def _key_label(key_const: int) -> str:
    try:
        return pygame.key.name(key_const).upper()
    except Exception:
        return str(key_const)


class SettingsScene:
    def __init__(self, screen: pygame.Surface, state):
        self.screen = screen
        self.state  = state
        self._next  = None
        self._rebind_target:   str | None = None
        self._rebind_focus_id: str | None = None   # widget ID to refocus after rebuild

        try:
            raw     = pygame.image.load(os.path.join(_ASSETS, "menu", "mainmenu_final.png"))
            self.bg = pygame.transform.scale(raw, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except Exception:
            self.bg = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            self.bg.fill((5, 8, 25))

        self._rebind_font = pygame.font.SysFont(None, 52)
        self._build_menu()

    # ── Menu construction ─────────────────────────────────────────────────
    def _build_menu(self, focus_id: str | None = None) -> None:
        theme = pygame_menu.themes.THEME_DARK.copy()
        theme.background_color        = (8,  12, 35, 210)
        theme.title_background_color  = (5,   8, 25, 230)
        theme.title_bar_style         = pygame_menu.widgets.MENUBAR_STYLE_NONE
        theme.widget_font             = pygame_menu.font.FONT_OPEN_SANS_BOLD
        theme.widget_font_color       = (220, 240, 255)
        theme.widget_font_size        = 26
        theme.widget_padding          = (6, 30)
        theme.widget_margin           = (0, 6)
        theme.widget_alignment        = pygame_menu.locals.ALIGN_CENTER
        # Visible teal highlight on selected item
        theme.selection_color         = (0, 220, 200)
        theme.widget_selection_effect = pygame_menu.widgets.HighlightSelection(
            border_width=2, margin_x=18, margin_y=6
        )

        self.menu = pygame_menu.Menu(
            title='',
            width=560,
            height=520,
            theme=theme,
            center_content=False,
        )

        # Volume sliders (0-10 → 0.0-1.0)
        self.menu.add.range_slider(
            'Music Volume',
            int(store.get("music_vol") * 10),
            (0, 10), 1,
            onchange=self._on_music_vol,
            rangeslider_id='slider_music',
        )
        self.menu.add.range_slider(
            'SFX Volume',
            int(store.get("sfx_vol") * 10),
            (0, 10), 1,
            onchange=self._on_sfx_vol,
            rangeslider_id='slider_sfx',
        )

        # Fullscreen toggle
        fs_label = 'Fullscreen:  ON' if store.get('fullscreen') else 'Fullscreen:  OFF'
        self.menu.add.button(fs_label, self._toggle_fullscreen, button_id='btn_fullscreen')

        # Key bindings
        self.menu.add.label('─── Key Bindings ───', font_size=20, label_id='lbl_keys')
        self.menu.add.button(
            f'Move Left :  {_key_label(store.get("key_left"))}',
            lambda: self._start_rebind('key_left', 'btn_key_left'),
            button_id='btn_key_left',
        )
        self.menu.add.button(
            f'Move Right:  {_key_label(store.get("key_right"))}',
            lambda: self._start_rebind('key_right', 'btn_key_right'),
            button_id='btn_key_right',
        )
        self.menu.add.button(
            f'Jump      :  {_key_label(store.get("key_jump"))}',
            lambda: self._start_rebind('key_jump', 'btn_key_jump'),
            button_id='btn_key_jump',
        )

        self.menu.add.label('', label_id='lbl_spacer')
        self.menu.add.button('Back', self._back, button_id='btn_back')
        self.menu.set_relative_position(50, 55)

        # Restore focus to widget that triggered the rebuild
        if focus_id:
            try:
                self.menu.get_widget(focus_id).select(recursive=False)
            except Exception:
                pass

    # ── Callbacks ─────────────────────────────────────────────────────────
    def _on_music_vol(self, val) -> None:
        v = val / 10.0
        store.put('music_vol', v)
        pygame.mixer.music.set_volume(v)
        store.save()

    def _on_sfx_vol(self, val) -> None:
        store.put('sfx_vol', val / 10.0)
        store.save()

    def _toggle_fullscreen(self) -> None:
        fs = not store.get('fullscreen')
        store.put('fullscreen', fs)
        store.save()
        flags = pygame.FULLSCREEN if fs else 0
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
        self._build_menu(focus_id='btn_fullscreen')

    def _start_rebind(self, target: str, focus_id: str) -> None:
        self._rebind_target   = target
        self._rebind_focus_id = focus_id

    def _back(self) -> None:
        self._next = SCENE_MENU

    # ── Scene interface ───────────────────────────────────────────────────
    def update(self, dt) -> str | None:
        events = pygame.event.get()

        # Rebind mode — swallow all input until key pressed
        if self._rebind_target:
            for e in events:
                if e.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                if e.type == pygame.KEYDOWN:
                    if e.key != pygame.K_ESCAPE:
                        store.put(self._rebind_target, e.key)
                        store.save()
                    focus             = self._rebind_focus_id
                    self._rebind_target   = None
                    self._rebind_focus_id = None
                    self._build_menu(focus_id=focus)
            return None

        for e in events:
            if e.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE:
                return SCENE_MENU

        self.menu.update(events)
        result, self._next = self._next, None
        return result

    def draw(self) -> None:
        self.screen.blit(self.bg, (0, 0))
        self.menu.draw(self.screen)

        if self._rebind_target:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 190))
            self.screen.blit(overlay, (0, 0))
            name = self._rebind_target.replace('key_', '').upper()
            txt  = self._rebind_font.render(
                f'Press new key for  {name}  (ESC to cancel)', True, (0, 220, 200)
            )
            self.screen.blit(txt, txt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)))
