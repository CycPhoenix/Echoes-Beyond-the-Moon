import pygame


class Platform(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, w: int, h: int,
                 color=(80, 80, 100), is_quicksand: bool = False):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill((180, 140, 80) if is_quicksand else color)
        self.rect  = self.image.get_rect(topleft=(x, y))
        self.is_quicksand = is_quicksand
