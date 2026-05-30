import os
import pygame

_BASE   = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "level1")

# Tile height — width derived from aspect ratio
_TILE_H = 50

_TILES: list[pygame.Surface] = []   # lazy-loaded on first use


def _ensure_tiles():
    """Load tile on first call — display must be initialized by then."""
    if _TILES:
        return
    src = pygame.image.load(os.path.join(_BASE, "new_platform1.png")).convert_alpha()
    w   = int(_TILE_H * src.get_width() / src.get_height())
    _TILES.append(pygame.transform.scale(src, (w, _TILE_H)))


def _tile_surface(total_w: int, tile_h: int) -> pygame.Surface:
    """Tile sprites side by side — surface rounds up to fit last full tile."""
    _ensure_tiles()
    tile_w  = _TILES[0].get_width()
    n       = -(-total_w // tile_w)      # ceiling division — last tile never cropped
    surf    = pygame.Surface((n * tile_w, tile_h), pygame.SRCALPHA)
    for i in range(n):
        surf.blit(_TILES[0], (i * tile_w, 0))
    return surf


class Platform(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, w: int, h: int, is_quicksand: bool = False):
        super().__init__()
        self.image = _tile_surface(w, _TILE_H)
        self.rect  = self.image.get_rect(topleft=(x, y))
