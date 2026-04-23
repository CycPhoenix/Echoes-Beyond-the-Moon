import pygame
import sys

from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCENE_LEVEL1


class PrologueScene:
    def __init__(self, screen, state):
        self.screen = screen
        self.state = state

        # load background image (same way as lab3)
        background_img = pygame.image.load("assets/intro/begining/afterparty.png")
        self.background = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # load each dialogue box image one by one (student style)
        img1 = pygame.image.load("assets/character/char_dialogue/character_dialogue_happy_claphand.png")
        img2 = pygame.image.load("assets/character/char_dialogue/character_dialogue_smile.png")
        img3 = pygame.image.load("assets/character/char_dialogue/character_dialogue_normal.png")
        img4 = pygame.image.load("assets/character/char_dialogue/character_dialogue_smile2.png")
        img5 = pygame.image.load("assets/character/char_dialogue/character_dialogue_wink2.png")

        # --- image 1: happy_claphand --- adjust size and position here
        img1_W = 800
        img1_H = 330
        img1_X = 200
        img1_Y = 380
        self.img1 = pygame.transform.scale(img1, (img1_W, img1_H))
        self.img1_pos = (img1_X, img1_Y)

        # --- image 2: smile --- adjust size and position here
        img2_W = 800
        img2_H = 290
        img2_X = 200
        img2_Y = 420
        self.img2 = pygame.transform.scale(img2, (img2_W, img2_H))
        self.img2_pos = (img2_X, img2_Y)

        # --- image 3: normal --- adjust size and position here
        img3_W = 800
        img3_H = 280
        img3_X = 200
        img3_Y = 430
        self.img3 = pygame.transform.scale(img3, (img3_W, img3_H))
        self.img3_pos = (img3_X, img3_Y)

        # --- image 4: smile2 --- adjust size and position here
        img4_W = 800
        img4_H = 280
        img4_X = 200
        img4_Y = 430
        self.img4 = pygame.transform.scale(img4, (img4_W, img4_H))
        self.img4_pos = (img4_X, img4_Y)

        # --- image 5: wink2 --- adjust size and position here
        img5_W = 800
        img5_H = 300
        img5_X = 200
        img5_Y = 415
        self.img5 = pygame.transform.scale(img5, (img5_W, img5_H))
        self.img5_pos = (img5_X, img5_Y)

        # font for dialogue text — reduced 5% from 30
        self.font = pygame.font.Font(None, 31)
        self.hintFont = pygame.font.Font(None, 26)

        # text position inside the dialogue box
        self.textX = 500
        self.textY = 630

        # dialogue lines (same list style as lab3)
        self.dialogue = [
            "That was such an amazing party, Isabelle!",
            "It's getting late. I should head home now.",
            "Oh, don't worry about me walking alone...",
            "I know a shortcut through the woods.",
            "I walk that path all the time. Don't worry!",
            "Alright, good night! See you tomorrow!",
        ]

        # same variable names as lab3
        self.currLine = 0
        self.diaTime = 0
        self.diaInterval = 4000

        self.clock = pygame.time.Clock()

    def update(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.currLine += 1
                    self.diaTime = 0

        # auto advance dialogue (same as lab3)
        self.diaTime += dt
        if self.diaTime >= self.diaInterval:
            self.currLine += 1
            self.diaTime = 0

        # move to next scene when all lines are done
        if self.currLine >= len(self.dialogue):
            return SCENE_LEVEL1

        return None

    def draw(self):
        # draw background
        self.screen.blit(self.background, (0, 0))

        # draw the correct dialogue box image based on current line (student if/elif style)
        if self.currLine == 0:
            self.screen.blit(self.img1, self.img1_pos)
        elif self.currLine == 1:
            self.screen.blit(self.img2, self.img2_pos)
        elif self.currLine == 2:
            self.screen.blit(self.img3, self.img3_pos)
        elif self.currLine == 3:
            self.screen.blit(self.img4, self.img4_pos)
        elif self.currLine == 4:
            self.screen.blit(self.img3, self.img3_pos)
        elif self.currLine == 5:
            self.screen.blit(self.img5, self.img5_pos)

        # draw the dialogue text inside the box (same as lab3 renderDialogue)
        if self.currLine < len(self.dialogue):
            textSurface = self.font.render(self.dialogue[self.currLine], True, (80, 50, 20))
            textRect = textSurface.get_rect(center=(self.textX, self.textY))
            self.screen.blit(textSurface, textRect)

        # small hint at the bottom
        hint = self.hintFont.render("Press ENTER to continue", True, (200, 200, 200))
        hintRect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 15))
        self.screen.blit(hint, hintRect)
