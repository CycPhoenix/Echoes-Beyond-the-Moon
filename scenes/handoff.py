from __future__ import annotations
import os
import pygame
from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, BLACK, SCENE_LEVEL2
from utils.game_state import GameState


class HandoffScene:
    def __init__(self, screen: pygame.Surface, state: GameState):
        self.screen = screen
        self.state = state
        self.timer = 0
        self.frame_index = 0
        self.sound_played = False

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.frames = []
        for i in range(1, 5):
            path = os.path.join(
                base_dir, "assets", "base", "transition", f"transition_{i}.png"
            )
            img = pygame.image.load(path).convert()
            img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
            self.frames.append(img)

        try:
            self.teleport_sound = pygame.mixer.Sound(
                os.path.join(base_dir, "assets", "base", "sounds", "teleporting.mp3")
            )
            self.teleport_sound.set_volume(0.8)
        except Exception as e:
            print("[audio] teleport sound failed:", e)
            self.teleport_sound = None

    def update(self, dt) -> str | None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

        if not self.sound_played:
            if self.teleport_sound:
                self.teleport_sound.play()
            self.sound_played = True

        self.timer += 1

        # Change image every 18 frames
        self.frame_index = self.timer // 18

        if self.frame_index >= len(self.frames):
            return SCENE_LEVEL2

        return None

    def draw(self):
        self.screen.fill(BLACK)

        if self.frame_index < len(self.frames):
            self.screen.blit(self.frames[self.frame_index], (0, 0))