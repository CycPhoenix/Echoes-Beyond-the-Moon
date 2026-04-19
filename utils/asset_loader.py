import os
import pygame

_cache = {}
_BASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")


def load(path: str, alpha: bool = True) -> pygame.Surface:
    if path not in _cache:
        full = os.path.join(_BASE, path)
        img = pygame.image.load(full)
        _cache[path] = img.convert_alpha() if alpha else img.convert()
    return _cache[path]


def load_sound(path: str) -> pygame.mixer.Sound:
    if path not in _cache:
        full = os.path.join(_BASE, path)
        _cache[path] = pygame.mixer.Sound(full)
    return _cache[path]


def clear():
    _cache.clear()
