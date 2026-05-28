"""Persistent settings — load/save JSON, single source of truth."""
from __future__ import annotations
import json
import os

_SAVE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "settings.json")

# Use raw integer key codes so this module needs no pygame import at load time.
# pygame.K_LEFT=1073741904, K_RIGHT=1073741903, K_SPACE=32
_DEFAULTS: dict = {
    "music_vol":  0.35,
    "sfx_vol":    0.6,
    "fullscreen": False,
    "key_left":   1073741904,
    "key_right":  1073741903,
    "key_jump":   32,
}

_current: dict = dict(_DEFAULTS)


def load() -> None:
    global _current
    _current = dict(_DEFAULTS)
    try:
        with open(_SAVE_PATH) as f:
            data = json.load(f)
        for k in _DEFAULTS:
            if k in data:
                _current[k] = data[k]
    except Exception:
        pass


def save() -> None:
    try:
        with open(_SAVE_PATH, "w") as f:
            json.dump(_current, f, indent=2)
    except Exception:
        pass


def get(key: str):
    return _current.get(key, _DEFAULTS[key])


def put(key: str, value) -> None:
    _current[key] = value
