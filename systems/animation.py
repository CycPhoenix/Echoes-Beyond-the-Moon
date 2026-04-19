import pygame


class AnimationController:
    def __init__(self, sheet: pygame.Surface, frame_w: int, frame_h: int,
                 fps: int = 8, loop: bool = True, row: int = 0):
        self.frames = []
        cols = sheet.get_width() // frame_w
        for col in range(cols):
            rect = pygame.Rect(col * frame_w, row * frame_h, frame_w, frame_h)
            self.frames.append(sheet.subsurface(rect).copy())

        self.fps   = fps
        self.loop  = loop
        self.timer = 0
        self.index = 0
        self.done  = False

    def update(self):
        if self.done:
            return
        self.timer += 1
        if self.timer >= 60 // self.fps:
            self.timer = 0
            self.index += 1
            if self.index >= len(self.frames):
                if self.loop:
                    self.index = 0
                else:
                    self.index = len(self.frames) - 1
                    self.done = True

    def get_frame(self) -> pygame.Surface:
        return self.frames[self.index]

    def reset(self):
        self.index = 0
        self.timer = 0
        self.done  = False
