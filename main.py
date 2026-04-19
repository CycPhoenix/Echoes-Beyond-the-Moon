
import pygame
from utils.constants import (SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE,
                              SCENE_MENU, SCENE_PROLOGUE, SCENE_LEVEL1,
                              SCENE_LEVEL2, SCENE_HANDOFF)
from utils.game_state  import GameState
from scenes.main_menu  import MainMenuScene
from scenes.prologue   import PrologueScene
from scenes.level1     import Level1Scene
from scenes.handoff    import HandoffScene
from scenes.level2     import Level2Scene


def main():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()

    state = GameState()

    scenes = {
        SCENE_MENU:     MainMenuScene,
        SCENE_PROLOGUE: PrologueScene,
        SCENE_LEVEL1:   Level1Scene,
        SCENE_HANDOFF:  HandoffScene,
        SCENE_LEVEL2:   Level2Scene,
    }

    current_scene = MainMenuScene(screen, state)

    while True:
        dt = clock.tick(FPS)
        next_scene_key = current_scene.update(dt)
        current_scene.draw()
        pygame.display.flip()

        if next_scene_key and next_scene_key in scenes:
            current_scene = scenes[next_scene_key](screen, state)


if __name__ == "__main__":
    main()
