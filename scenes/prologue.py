import array
import math
import os
import pygame
import sys

from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCENE_LEVEL1

_BASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")


def _load(rel: str) -> pygame.Surface:
    return pygame.image.load(os.path.join(_BASE, rel))


def _scale_bg(rel: str) -> pygame.Surface:
    return pygame.transform.scale(_load(rel), (SCREEN_WIDTH, SCREEN_HEIGHT))


def _scale_bg_blur(rel: str, radius: int = 8) -> pygame.Surface:
    """Scale background to screen size, apply Gaussian blur (ref: lab9_2 gaussionBlur)."""
    from PIL import Image, ImageFilter
    path = os.path.join(_BASE, rel)
    pil_img = Image.open(path).convert("RGBA")
    pil_img = pil_img.resize((SCREEN_WIDTH, SCREEN_HEIGHT), Image.LANCZOS)
    blurred = pil_img.filter(ImageFilter.GaussianBlur(radius=radius))
    return pygame.image.frombuffer(blurred.tobytes(), blurred.size, "RGBA")


def _scale_dlg(rel: str, target_w: int = 820, max_h: int = 320) -> tuple[pygame.Surface, tuple[int, int]]:
    """Scale dialogue image to target_w, cap height at max_h, bottom-anchor at screen bottom."""
    src = _load(rel)
    h = int(target_w * src.get_height() / src.get_width())
    if h > max_h:
        h = max_h
        target_w = int(h * src.get_width() / src.get_height())
    surf = pygame.transform.scale(src, (target_w, h))
    x = (SCREEN_WIDTH - target_w) // 2
    y = SCREEN_HEIGHT - h
    return surf, (x, y)


def _make_piano_note(freq: float, sample_rate: int = 44100,
                     duration: float = 0.5, volume: float = 0.28) -> pygame.mixer.Sound:
    """Synthesise a piano-like note: sine + octave harmonic, ADSR envelope."""
    n = int(sample_rate * duration)
    attack  = int(sample_rate * 0.008)   # 8 ms
    decay   = int(sample_rate * 0.12)    # 120 ms
    sustain = 0.55
    release = int(sample_rate * 0.08)    # 80 ms

    buf = array.array('h')
    for i in range(n):
        # ADSR
        if i < attack:
            env = i / attack
        elif i < attack + decay:
            env = 1.0 - (i - attack) / decay * (1.0 - sustain)
        elif i < n - release:
            env = sustain
        else:
            env = sustain * (1.0 - (i - (n - release)) / release)

        # Fundamental + 2nd harmonic for body
        t = i / sample_rate
        s = (0.7 * math.sin(2 * math.pi * freq * t) +
             0.3 * math.sin(2 * math.pi * freq * 2 * t))
        sample = int(32767 * volume * env * s)
        buf.append(sample)   # left
        buf.append(sample)   # right (stereo)

    return pygame.mixer.Sound(buffer=buf)


# ── Piano key definitions ─────────────────────────────────────────────────────
_PIANO_KEYS = [
    (pygame.K_a, 'A', 'C', 261.63),
    (pygame.K_s, 'S', 'D', 293.66),
    (pygame.K_d, 'D', 'E', 329.63),
    (pygame.K_f, 'F', 'F', 349.23),
    (pygame.K_g, 'G', 'G', 392.00),
    (pygame.K_h, 'H', 'A', 440.00),
    (pygame.K_j, 'J', 'B', 493.88),
]
_KEY_W   = 82
_KEY_H   = 130
_KEYS_X0 = (SCREEN_WIDTH - len(_PIANO_KEYS) * _KEY_W) // 2
_KEYS_Y  = SCREEN_HEIGHT - _KEY_H - 28

# Twinkle Twinkle Little Star — first two phrases (C C G G A A G  F F E E D D C)
_TWINKLE_SEQ = [
    pygame.K_a, pygame.K_a,   # C C  — Twinkle twinkle
    pygame.K_g, pygame.K_g,   # G G  — little star
    pygame.K_h, pygame.K_h,   # A A  — How I
    pygame.K_g,               # G    — wonder
    pygame.K_f, pygame.K_f,   # F F  — what you
    pygame.K_d, pygame.K_d,   # E E  — are up
    pygame.K_s, pygame.K_s,   # D D  — above the
    pygame.K_a,               # C    — world
]

_WRONG_NOTE_TEXTS = [
    "Oops, wrong note~\nIt's okay, let me try again!",
    "Aw, not quite!\nFrom the top, I've got this!",
    "Hmm, that didn't sound right...\nLet me start over, no worries!",
]

_PIANO_VICTORY_TEXT = "Twinkle twinkle, I'm a star!\nI played it all — and here we are!"

_PIANO_ERR_DLG_IDX     = 7    # new_char_dialogue_sad_depress.png
_PIANO_VICTORY_DLG_IDX = 18   # new_char_dialogue_victory.png


# ── Dialogue image filenames ──────────────────────────────────────────────────
_DLG = "character/char_dialogue_new/"
_DLG_FILES = [
    _DLG + "new_char_dialogue_happy_claphand.png",   # 0  img1
    _DLG + "new_char_dialogue_smile2.png",            # 1  img2
    _DLG + "new_char_dialogue_normal.png",            # 2  img3
    _DLG + "new_char_dialogue_smile2.png",            # 3  img4
    _DLG + "new_char_dialogue_wink2.png",             # 4  img5
    _DLG + "new_char_dialogue_shock.png",             # 5  img6
    _DLG + "new_char_dialogue_excited.png",           # 6  img7
    _DLG + "new_char_dialogue_sad_depress.png",       # 7  img8
    _DLG + "new_char_dialogue_plain_smile.png",       # 8  img9
    _DLG + "new_char_dialogue_cry.png",               # 9  img10
    _DLG + "new_char_dialogue_lightsmile.png",        # 10 img11
    _DLG + "new_char_dialogue_terrified.png",         # 11 img12
    _DLG + "new_char_dialogue_afraid_panic.png",      # 12 img13
    _DLG + "new_char_dialogue_suddenrealization.png", # 13 img14
    _DLG + "new_char_dialogue_curiosity.png",         # 14 img15
    _DLG + "new_char_dialogue_judge.png",             # 15 img16
    _DLG + "new_char_dialogue_doubt.png",             # 16 img17
    _DLG + "new_char_dialogue_stareyes.png",          # 17 img18
    _DLG + "new_char_dialogue_victory.png",            # 18 img19
    _DLG + "new_char_dialogue_frustrated.png",        # 19 img20
    _DLG + "new_char_dialogue_smirking2.png",         # 20 img21
    _DLG + "new_char_dialogue_suspecious.png",        # 21 img22
    _DLG + "new_char_dialogue_spiraleyes.png",        # 22 img23
    _DLG + "new_char_dialogue_pouting.png",           # 23 img24
]

# line → _DLG_FILES index  (None = cinematic / piano — no dialogue box)
_LINE_TO_DLG = [
    0,    # 0  happy_claphand
    13,   # 1  suddenrealization
    4,    # 2  wink2
    8,    # 3  plain_smile
    20,   # 4  smirking
    21,   # 5  suspicious
    11,   # 6  terrified
    22,   # 7  spiraleyes
    12,   # 8  afraid_panic
    14,   # 9  curiosity
    13,   # 10 suddenrealization
    11,   # 11 terrified
    15,   # 12 raiseeyebrow_judge
    17,   # 13 stareyes
    8,    # 14 plain_smile
    23,   # 15 pouting
    10,   # 16 lightsmile
    14,   # 17 curiosity
    6,    # 18 excited
    15,   # 19 raiseeyebrow_judge
    17,   # 20 stareyes
    None, # 21 piano minigame
    13,   # 22 suddenrealization — door is glowing
    None, # 23 cinematic — room door luna
]


class PrologueScene:
    def __init__(self, screen, state):
        self.screen = screen
        self.state  = state

        # ── Backgrounds ───────────────────────────────────────────────────────
        self.backgrounds = [
            _scale_bg("intro/begining/afterparty.png"),                        # lines 0-2
            _scale_bg("intro/begining/walkalone.png"),                         # lines 3-5
            _scale_bg("intro/begining/turn_into_fog.png"),                     # lines 6-8
            _scale_bg("intro/begining/forest with house.png"),                 # lines 9-11
            _scale_bg("intro/begining/woodenhouse_overview.png"),              # lines 12-14
            _scale_bg("intro/begining/room_inside_piano.png"),                 # lines 15-17
            _scale_bg("intro/begining/piano_overview.png"),                    # lines 18-20 (discover piano)
            _scale_bg_blur("intro/begining/piano_overview.png", radius=8),     # line 21 (piano interactive, blurred)
            _scale_bg("intro/begining/room_door.png"),                         # line 22
            _scale_bg("intro/begining/room_door_luna.png"),                    # line 23
        ]

        # Music sheet at 70% of screen width, centered, positioned above piano keys
        ms_src = _load("intro/begining/musicsheet_new.png")
        ms_w = int(SCREEN_WIDTH * 0.7)
        ms_h = int(ms_w * ms_src.get_height() / ms_src.get_width())
        self.musicsheet_surf = pygame.transform.scale(ms_src, (ms_w, ms_h))
        self.musicsheet_x = (SCREEN_WIDTH - ms_w) // 2
        self.musicsheet_y = _KEYS_Y - ms_h - 30

        # ── Dialogue box images ────────────────────────────────────────────────
        # Index 0 (happy_claphand) is a full-body portrait — needs its own scale
        self.dlg_surfs = []
        self.dlg_poses = []
        for i, rel in enumerate(_DLG_FILES):
            if i == 0:
                surf, pos = _scale_dlg(rel, target_w=950, max_h=450)
                pos = (270, 350)
            else:
                surf, pos = _scale_dlg(rel)
            self.dlg_surfs.append(surf)
            self.dlg_poses.append(pos)

        # ── Fonts ────────────────────────────────────────────────────────────
        self.font        = pygame.font.Font(None, 31)
        self.hint_font   = pygame.font.Font(None, 26)
        self.piano_font  = pygame.font.Font(None, 28)
        self.label_font  = pygame.font.Font(None, 22)

        self.textX = 530
        self.textY = 640

        # ── Skip button ───────────────────────────────────────────────────────
        skip_W, skip_H   = 180, 84
        self.skipBtn     = pygame.transform.scale(_load("menu/extra_14.png"), (skip_W, skip_H))
        self.skipBtn_pos = (SCREEN_WIDTH - skip_W - 15, SCREEN_HEIGHT - skip_H - 15)

        # ── Dialogue lines ────────────────────────────────────────────────────
        self.dialogue = [
            # Scene 1: afterparty (0-2)
            "Best party ever, Isabelle!",
            "Wait, past nine?\nMum's going to kill me. Gotta go.",
            "I know a shortcut through the woods.\nDon't worry!",
            # Scene 2: walkalone (3-5)
            "Almost home.\nJust a little further through the woods...",
            "Better be quick",
            "Hmmm, wait a second.\nSomething's weird.",
            # Scene 3: fog (6-8)
            "Oh my, the fog's getting thicker.",
            "I can't see the path clearly.",
            "Where am I?!",
            # Scene 4: forest with house (9-11)
            "Huh, is that a house?",
            "Wait. There is no house in these woods.\nI know this path.",
            "And some sound is coming from inside...",
            # Scene 5: wooden house (12-14)
            "My instincts say run. But...",
            "Maybe I can ask for help?",
            "Just... a little closer.",
            # Scene 6: room inside (15-17)
            "Urgh... spiderwebs everywhere.",
            "No one's been here in years,\nI guess.",
            "A piano.\nIs that where the sound is coming from?",
            # Scene 7: piano overview (18-20)
            "This piano looks like\nit's been well taken care of.",
            "Oh, a note: 'Play me.'\nHmm, should I?",
            "Somehow...\nmy fingers already know what to do.",
            # Scene 8: piano interactive (21) — handled separately
            "",
            # Scene 9-10: cinematic door shots (22-23)
            "W-wait... the door?!\nWhy is there light coming from it?!",
            "",
        ]

        self.currLine = 0

        # ── Piano mini-game state ─────────────────────────────────────────────
        self._piano_flash     = {}    # pygame_key → frames left to flash
        self.piano_step       = 0     # how far through _TWINKLE_SEQ the player is
        self.piano_can_advance = False
        self.piano_err_timer  = 0     # frames remaining to show error dialogue
        self.piano_err_count  = 0     # how many mistakes made (cycles error messages)

        # Pre-generate note sounds
        self._piano_sounds = {}
        mixer_init = pygame.mixer.get_init()
        sr = mixer_init[0] if mixer_init else 44100
        for key, _, _, freq in _PIANO_KEYS:
            self._piano_sounds[key] = _make_piano_note(freq, sample_rate=sr)

    # ─────────────────────────────────────────────────────────────────────────
    def _bg_index(self) -> int:
        thresholds = [3, 6, 9, 12, 15, 18, 21, 22, 23]
        for i, t in enumerate(thresholds):
            if self.currLine < t:
                return i
        return len(self.backgrounds) - 1

    # ─────────────────────────────────────────────────────────────────────────
    def update(self, dt) -> str | None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Piano note keys (only active on line 21)
                if self.currLine == 21 and event.key in self._piano_sounds:
                    # Ignore input while showing error or after completion
                    if self.piano_err_timer == 0 and not self.piano_can_advance:
                        self._piano_sounds[event.key].play()
                        self._piano_flash[event.key] = 18
                        if event.key == _TWINKLE_SEQ[self.piano_step]:
                            self.piano_step += 1
                            if self.piano_step >= len(_TWINKLE_SEQ):
                                self.piano_can_advance = True
                        else:
                            # Wrong note — reset sequence and show error dialogue
                            self.piano_step = 0
                            self.piano_err_count += 1
                            self.piano_err_timer = 150   # ~2.5 s at 60 fps

                # Advance key
                elif event.key in (pygame.K_e, pygame.K_SPACE, pygame.K_RETURN):
                    if self.currLine == 21:
                        if self.piano_can_advance:
                            self.currLine += 1
                    else:
                        self.currLine += 1

                # Skip entire prologue
                elif event.key == pygame.K_x:
                    return SCENE_LEVEL1

        # Tick timers
        for k in list(self._piano_flash.keys()):
            self._piano_flash[k] -= 1
            if self._piano_flash[k] <= 0:
                del self._piano_flash[k]
        if self.piano_err_timer > 0:
            self.piano_err_timer -= 1

        if self.currLine >= len(self.dialogue):
            return SCENE_LEVEL1

        return None

    # ─────────────────────────────────────────────────────────────────────────
    def draw(self):
        line = self.currLine

        # ── Piano mini-game (line 21) ─────────────────────────────────────────
        if line == 21:
            self.screen.blit(self.backgrounds[7], (0, 0))
            self.screen.blit(self.musicsheet_surf, (self.musicsheet_x, self.musicsheet_y))

            # Piano keys
            self._draw_piano_keys()

            # Top instruction / completion prompt
            cx = SCREEN_WIDTH // 2
            if self.piano_can_advance:
                msg = "Press E / SPACE to continue"
                color = (140, 255, 200)
                msg_surf = self.piano_font.render(msg, True, color)
                shadow  = self.piano_font.render(msg, True, (20, 20, 20))
                self.screen.blit(shadow,   shadow.get_rect(center=(cx + 2, 22)))
                self.screen.blit(msg_surf, msg_surf.get_rect(center=(cx, 20)))
                # Victory dialogue box
                v_surf = self.dlg_surfs[_PIANO_VICTORY_DLG_IDX]
                v_pos  = self.dlg_poses[_PIANO_VICTORY_DLG_IDX]
                self.screen.blit(v_surf, v_pos)
                parts = _PIANO_VICTORY_TEXT.split("\n")
                s1 = self.font.render(parts[0].strip(), True, (80, 50, 20))
                s2 = self.font.render(parts[1].strip(), True, (80, 50, 20))
                self.screen.blit(s1, s1.get_rect(center=(self.textX, self.textY - 15)))
                self.screen.blit(s2, s2.get_rect(center=(self.textX, self.textY + 15)))
            elif self.piano_err_timer == 0:
                # Show note progress  (e.g. "Note 3 / 14")
                msg = f"Note {self.piano_step + 1} / {len(_TWINKLE_SEQ)}"
                color = (220, 200, 140)
                msg_surf = self.piano_font.render(msg, True, color)
                shadow  = self.piano_font.render(msg, True, (20, 20, 20))
                self.screen.blit(shadow,   shadow.get_rect(center=(cx + 2, 22)))
                self.screen.blit(msg_surf, msg_surf.get_rect(center=(cx, 20)))

            # Error dialogue overlay (wrong note)
            if self.piano_err_timer > 0:
                err_surf = self.dlg_surfs[_PIANO_ERR_DLG_IDX]
                err_pos  = self.dlg_poses[_PIANO_ERR_DLG_IDX]
                self.screen.blit(err_surf, err_pos)
                err_text = _WRONG_NOTE_TEXTS[self.piano_err_count % len(_WRONG_NOTE_TEXTS)]
                if "\n" in err_text:
                    parts = err_text.split("\n")
                    s1 = self.font.render(parts[0].strip(), True, (80, 50, 20))
                    s2 = self.font.render(parts[1].strip(), True, (80, 50, 20))
                    self.screen.blit(s1, s1.get_rect(center=(self.textX, self.textY - 15)))
                    self.screen.blit(s2, s2.get_rect(center=(self.textX, self.textY + 15)))
                else:
                    ts = self.font.render(err_text, True, (80, 50, 20))
                    self.screen.blit(ts, ts.get_rect(center=(self.textX, self.textY)))

            self.screen.blit(self.skipBtn, self.skipBtn_pos)
            return

        # ── Normal dialogue lines ─────────────────────────────────────────────
        self.screen.blit(self.backgrounds[self._bg_index()], (0, 0))

        dlg_idx = _LINE_TO_DLG[line] if line < len(_LINE_TO_DLG) else None

        if dlg_idx is not None:
            self.screen.blit(self.dlg_surfs[dlg_idx], self.dlg_poses[dlg_idx])
            text = self.dialogue[line]
            if text:
                if "\n" in text:
                    p = text.split("\n")
                    s1 = self.font.render(p[0].strip(), True, (80, 50, 20))
                    s2 = self.font.render(p[1].strip(), True, (80, 50, 20))
                    self.screen.blit(s1, s1.get_rect(center=(self.textX, self.textY - 15)))
                    self.screen.blit(s2, s2.get_rect(center=(self.textX, self.textY + 15)))
                else:
                    ts = self.font.render(text, True, (80, 50, 20))
                    self.screen.blit(ts, ts.get_rect(center=(self.textX, self.textY)))

        self.screen.blit(self.skipBtn, self.skipBtn_pos)

        hint = self.hint_font.render("Press E / SPACE to continue  |  X to skip",
                                     True, (200, 200, 200))
        self.screen.blit(hint, hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 15)))

    # ─────────────────────────────────────────────────────────────────────────
    def _draw_piano_keys(self):
        font_note = self.label_font
        font_key  = self.label_font

        for i, (key, kb_label, note_label, _) in enumerate(_PIANO_KEYS):
            x = _KEYS_X0 + i * _KEY_W
            y = _KEYS_Y
            w = _KEY_W - 4

            # Key colour
            if key in self._piano_flash:
                frac  = self._piano_flash[key] / 18
                r = int(255 * frac + 220 * (1 - frac))
                g = int(230 * frac + 220 * (1 - frac))
                b = int(80  * frac + 220 * (1 - frac))
                color = (r, g, b)
            else:
                color = (235, 230, 215)

            # Shadow / depth
            pygame.draw.rect(self.screen, (80, 60, 40),
                             (x + 3, y + 3, w, _KEY_H), border_radius=6)
            pygame.draw.rect(self.screen, color,
                             (x, y, w, _KEY_H), border_radius=6)
            pygame.draw.rect(self.screen, (100, 80, 55),
                             (x, y, w, _KEY_H), 2, border_radius=6)

            # Note label (top of key)
            ns = font_note.render(note_label, True, (60, 40, 20))
            self.screen.blit(ns, ns.get_rect(center=(x + w // 2, y + 18)))

            # Keyboard shortcut (bottom of key)
            ks = font_key.render(kb_label, True, (100, 70, 40))
            self.screen.blit(ks, ks.get_rect(center=(x + w // 2, y + _KEY_H - 16)))
