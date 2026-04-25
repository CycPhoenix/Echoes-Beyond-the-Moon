import pygame
import sys

from utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCENE_LEVEL1


class PrologueScene:
    def __init__(self, screen, state):
        self.screen = screen
        self.state = state

        # load background images
        background_img = pygame.image.load("assets/intro/begining/afterparty.png")
        self.background = pygame.transform.scale(background_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        walkalone_img = pygame.image.load("assets/intro/begining/walkalone.png")
        self.background2 = pygame.transform.scale(walkalone_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        fog_img = pygame.image.load("assets/intro/begining/turn_into_fog.png")
        self.background3 = pygame.transform.scale(fog_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        forest_img = pygame.image.load("assets/intro/begining/forest with house.png")
        self.background4 = pygame.transform.scale(forest_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        woodenhouse_img = pygame.image.load("assets/intro/begining/woodenhouse_overview.png")
        self.background5 = pygame.transform.scale(woodenhouse_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        roominside_img = pygame.image.load("assets/intro/begining/room_inside_piano.png")
        self.background6 = pygame.transform.scale(roominside_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        piano_img = pygame.image.load("assets/intro/begining/piano_overview.png")
        self.background7 = pygame.transform.scale(piano_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        piano1_img = pygame.image.load("assets/intro/begining/piano (1).png")
        self.background8 = pygame.transform.scale(piano1_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        roomdoor_img = pygame.image.load("assets/intro/begining/room_door.png")
        self.background9 = pygame.transform.scale(roomdoor_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        roomdoor_luna_img = pygame.image.load("assets/intro/begining/room_door_luna.png")
        self.background10 = pygame.transform.scale(roomdoor_luna_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # load each dialogue box image
        img1  = pygame.image.load("assets/character/char_dialogue/character_dialogue_happy_claphand.png")
        img2  = pygame.image.load("assets/character/char_dialogue/character_dialogue_smile.png")
        img3  = pygame.image.load("assets/character/char_dialogue/character_dialogue_normal.png")
        img4  = pygame.image.load("assets/character/char_dialogue/character_dialogue_smile2.png")
        img5  = pygame.image.load("assets/character/char_dialogue/character_dialogue_wink2.png")
        img6  = pygame.image.load("assets/character/char_dialogue/character_dialogue_shock.png")
        img7  = pygame.image.load("assets/character/char_dialogue/character_dialogue_excited.png")
        img8  = pygame.image.load("assets/character/char_dialogue/character_dialogue_sadface.png")
        img9  = pygame.image.load("assets/character/char_dialogue/character_dialogue_plain_smile.png")
        img10 = pygame.image.load("assets/character/char_dialogue/character_dialogue_cry.png")
        img11 = pygame.image.load("assets/character/char_dialogue/char_dialogue_ lightsmile.png")
        img12 = pygame.image.load("assets/character/char_dialogue/char_dialogue_ terrified.png")
        img13 = pygame.image.load("assets/character/char_dialogue/char_dialogue_ afraid_panic.png")
        img14 = pygame.image.load("assets/character/char_dialogue/char_dialogue_suddenrealization.png")
        img15 = pygame.image.load("assets/character/char_dialogue/char_dialogue_curiosity.png")
        img16 = pygame.image.load("assets/character/char_dialogue/char_dialogue_raiseeyebrow_judge.png")
        img17 = pygame.image.load("assets/character/char_dialogue/char_dialogue_doubt.png")
        img18 = pygame.image.load("assets/character/char_dialogue/char_dialogue_stareyes.png")
        img19 = pygame.image.load("assets/character/char_dialogue/character_dialogue_happy_excited.png")
        img20 = pygame.image.load("assets/character/char_dialogue/char_dialogue_frustrated.png")
        img21 = pygame.image.load("assets/character/char_dialogue/char_dialogue_ smirking.png")
        img22 = pygame.image.load("assets/character/char_dialogue/char_dialogue_ suspecious.png")
        img23 = pygame.image.load("assets/character/char_dialogue/char_dialogue_ spiraleyes.png")
        img24 = pygame.image.load("assets/character/char_dialogue/char_dialogue_pouting.png")

        # --- image 1: happy_claphand (size and position)
        img1_W = 800
        img1_H = 330
        img1_X = 200
        img1_Y = 380
        self.img1 = pygame.transform.scale(img1, (img1_W, img1_H))
        self.img1_pos = (img1_X, img1_Y)

        # --- image 2: smile 
        img2_W = 800
        img2_H = 290
        img2_X = 200
        img2_Y = 420
        self.img2 = pygame.transform.scale(img2, (img2_W, img2_H))
        self.img2_pos = (img2_X, img2_Y)

        # --- image 3: normal 
        img3_W = 800
        img3_H = 280
        img3_X = 200
        img3_Y = 430
        self.img3 = pygame.transform.scale(img3, (img3_W, img3_H))
        self.img3_pos = (img3_X, img3_Y)

        # --- image 4: smile2 
        img4_W = 800
        img4_H = 280
        img4_X = 200
        img4_Y = 430
        self.img4 = pygame.transform.scale(img4, (img4_W, img4_H))
        self.img4_pos = (img4_X, img4_Y)

        # --- image 5: 
        img5_W = 800
        img5_H = 300
        img5_X = 200
        img5_Y = 415
        self.img5 = pygame.transform.scale(img5, (img5_W, img5_H))
        self.img5_pos = (img5_X, img5_Y)

        # --- image 6: shock 
        img6_W = 800
        img6_H = 300
        img6_X = 200
        img6_Y = 415
        self.img6 = pygame.transform.scale(img6, (img6_W, img6_H))
        self.img6_pos = (img6_X, img6_Y)

        # --- image 7: excited 
        img7_W = 800
        img7_H = 300
        img7_X = 200
        img7_Y = 415
        self.img7 = pygame.transform.scale(img7, (img7_W, img7_H))
        self.img7_pos = (img7_X, img7_Y)

        # --- image 8: sadface 
        img8_W = 800
        img8_H = 300
        img8_X = 200
        img8_Y = 415
        self.img8 = pygame.transform.scale(img8, (img8_W, img8_H))
        self.img8_pos = (img8_X, img8_Y)

        # --- image 9: plain_smile 
        img9_W = 800
        img9_H = 300
        img9_X = 200
        img9_Y = 415
        self.img9 = pygame.transform.scale(img9, (img9_W, img9_H))
        self.img9_pos = (img9_X, img9_Y)

        # --- image 10: cry 
        img10_W = 800
        img10_H = 300
        img10_X = 200
        img10_Y = 415
        self.img10 = pygame.transform.scale(img10, (img10_W, img10_H))
        self.img10_pos = (img10_X, img10_Y)

        # --- image 11: lightsmile 
        img11_W = 800
        img11_H = 300
        img11_X = 200
        img11_Y = 415
        self.img11 = pygame.transform.scale(img11, (img11_W, img11_H))
        self.img11_pos = (img11_X, img11_Y)

        # --- image 12: terrified 
        img12_W = 800
        img12_H = 300
        img12_X = 200
        img12_Y = 415
        self.img12 = pygame.transform.scale(img12, (img12_W, img12_H))
        self.img12_pos = (img12_X, img12_Y)

        # --- image 13: afraid_panic 
        img13_W = 800
        img13_H = 300
        img13_X = 200
        img13_Y = 415
        self.img13 = pygame.transform.scale(img13, (img13_W, img13_H))
        self.img13_pos = (img13_X, img13_Y)

        # --- image 14: suddenrealization 
        img14_W = 800
        img14_H = 300
        img14_X = 200
        img14_Y = 415
        self.img14 = pygame.transform.scale(img14, (img14_W, img14_H))
        self.img14_pos = (img14_X, img14_Y)

        # --- image 15: curiosity 
        img15_W = 800
        img15_H = 300
        img15_X = 200
        img15_Y = 415
        self.img15 = pygame.transform.scale(img15, (img15_W, img15_H))
        self.img15_pos = (img15_X, img15_Y)

        # --- image 16: raiseeyebrow_judge 
        img16_W = 800
        img16_H = 300
        img16_X = 200
        img16_Y = 415
        self.img16 = pygame.transform.scale(img16, (img16_W, img16_H))
        self.img16_pos = (img16_X, img16_Y)

        # --- image 17: doubt 
        img17_W = 800
        img17_H = 300
        img17_X = 200
        img17_Y = 415
        self.img17 = pygame.transform.scale(img17, (img17_W, img17_H))
        self.img17_pos = (img17_X, img17_Y)

        # --- image 18: stareyes 
        img18_W = 800
        img18_H = 300
        img18_X = 200
        img18_Y = 415
        self.img18 = pygame.transform.scale(img18, (img18_W, img18_H))
        self.img18_pos = (img18_X, img18_Y)

        # --- image 19: happy_excited 
        img19_W = 800
        img19_H = 300
        img19_X = 200
        img19_Y = 415
        self.img19 = pygame.transform.scale(img19, (img19_W, img19_H))
        self.img19_pos = (img19_X, img19_Y)

        # --- image 20: frustrated 
        img20_W = 800
        img20_H = 300
        img20_X = 200
        img20_Y = 415
        self.img20 = pygame.transform.scale(img20, (img20_W, img20_H))
        self.img20_pos = (img20_X, img20_Y)

        # --- image 21: smirking 
        img21_W = 800
        img21_H = 300
        img21_X = 200
        img21_Y = 415
        self.img21 = pygame.transform.scale(img21, (img21_W, img21_H))
        self.img21_pos = (img21_X, img21_Y)

        # --- image 22: suspicious 
        img22_W = 800
        img22_H = 300
        img22_X = 200
        img22_Y = 415
        self.img22 = pygame.transform.scale(img22, (img22_W, img22_H))
        self.img22_pos = (img22_X, img22_Y)

        # --- image 23: spiral eyes 
        img23_W = 800
        img23_H = 300
        img23_X = 200
        img23_Y = 415
        self.img23 = pygame.transform.scale(img23, (img23_W, img23_H))
        self.img23_pos = (img23_X, img23_Y)

        # --- image 24: pouting
        img24_W = 800
        img24_H = 300
        img24_X = 200
        img24_Y = 415
        self.img24 = pygame.transform.scale(img24, (img24_W, img24_H))
        self.img24_pos = (img24_X, img24_Y)

        # font for dialogue text
        self.font = pygame.font.Font(None, 31)
        self.hintFont = pygame.font.Font(None, 26)
        self.narrativeFont = pygame.font.Font(None, 38)

        # text position inside the dialogue box
        self.textX = 500
        self.textY = 635

        # narrative text position 
        self.narrativeTextX = 640
        self.narrativeTextY = 360

        # skip button (bottom right) — shown from start until Luna enters the house
        skip_img = pygame.image.load("assets/menu/extra_14.png")
        skip_W = 180
        skip_H = 84
        self.skipBtn = pygame.transform.scale(skip_img, (skip_W, skip_H))
        self.skipBtn_pos = (SCREEN_WIDTH - skip_W - 15, SCREEN_HEIGHT - skip_H - 15)

        # dialogue lines 
        self.dialogue = [
            # --- Scene 1: afterparty (lines 0-2) ---
            "Best party ever, Isabelle!",
            "Wait, past nine?\nMum's going to kill me. Gotta go.",
            "I know a shortcut through the woods.\nDon't worry!",
            # --- Scene 2: walkalone (lines 3-5) ---
            "Almost home. \nJust a little further through the woods...",
            "Better be quick",
            "Hmmm, wait a second. \nSomething's weird.",
            # --- Scene 3: Wrong path (lines 6-8) ---
            "Oh my, the fog's getting thicker.",
            "I can't see the path clearly.",
            "Where am I ?!!",
            # --- Scene 4: forest with house (lines 9-11) ---
            "Huh, is that a house?",
            "Wait. There is no house in these woods.\n I know this path.",
            "And some sound is coming from inside...",
            # --- Scene 5: wooden house overview (lines 12-14) ---
            "My instincts say run. But..",
            "Maybe i can ask for help?",
            "Just... a little closer.",
            # --- Scene 6: room inside (lines 15-17) ---
            "Urgh...spiderwebs everywhere.",
            "No one's been here in years,\n I guess.",
            "A piano. \nIs that where the sound is coming from?",
            # --- Scene 7: piano overview (lines 18-20) ---
            "This piano looks like \nit's been well taken care of.",
            "Oh, a note: 'Play me.' \n Hmm, should I?",
            "Somehow... \nmy fingers already know what to do.",
            # --- Scene 8: piano (1) (line 21) ---
            "...",
            # --- Scene 9: room door (line 22) ---
            "...",
            # --- Scene 10: room door luna (line 23) ---
            "...",
        ]
         
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
                if event.key == pygame.K_x:
                    return SCENE_LEVEL1

        # auto advance dialogue 
        self.diaTime += dt
        if self.diaTime >= self.diaInterval:
            self.currLine += 1
            self.diaTime = 0

        # move to next scene when all lines are done
        if self.currLine >= len(self.dialogue):
            return SCENE_LEVEL1

        return None

    def draw(self):
        # draw background based on current scene section
        if self.currLine < 3:
            self.screen.blit(self.background, (0, 0))
        elif self.currLine < 6:
            self.screen.blit(self.background2, (0, 0))
        elif self.currLine < 9:
            self.screen.blit(self.background3, (0, 0))
        elif self.currLine < 12:
            self.screen.blit(self.background4, (0, 0))
        elif self.currLine < 15:
            self.screen.blit(self.background5, (0, 0))
        elif self.currLine < 18:
            self.screen.blit(self.background6, (0, 0))
        elif self.currLine < 21:
            self.screen.blit(self.background7, (0, 0))
        elif self.currLine == 21:
            self.screen.blit(self.background8, (0, 0))
        elif self.currLine == 22:
            self.screen.blit(self.background9, (0, 0))
        else:
            self.screen.blit(self.background10, (0, 0))

        
        # draw the correct dialogue box image based on current line
        if self.currLine == 0:
            self.screen.blit(self.img1, self.img1_pos)
        elif self.currLine == 1:
            self.screen.blit(self.img14, self.img14_pos)
        elif self.currLine == 2:
            self.screen.blit(self.img5, self.img5_pos)
        elif self.currLine == 3:
            self.screen.blit(self.img9, self.img9_pos)
        elif self.currLine == 4:
            self.screen.blit(self.img21, self.img21_pos)
        elif self.currLine == 5:
            self.screen.blit(self.img22, self.img22_pos)
        elif self.currLine == 6:
            self.screen.blit(self.img12, self.img12_pos)
        elif self.currLine == 7:
            self.screen.blit(self.img23, self.img23_pos)
        elif self.currLine == 8:
            self.screen.blit(self.img13, self.img13_pos)
        elif self.currLine == 9:
            self.screen.blit(self.img15, self.img15_pos)
        elif self.currLine == 10:
            self.screen.blit(self.img14, self.img14_pos)
        elif self.currLine == 11:
            self.screen.blit(self.img12, self.img12_pos)
        elif self.currLine == 12:
            self.screen.blit(self.img16, self.img16_pos)
        elif self.currLine == 13:
            self.screen.blit(self.img18, self.img18_pos)
        elif self.currLine == 14:
            self.screen.blit(self.img9, self.img9_pos)
        elif self.currLine == 15:
            self.screen.blit(self.img24, self.img24_pos)
        elif self.currLine == 16:
            self.screen.blit(self.img11, self.img11_pos)
        elif self.currLine == 17:
            self.screen.blit(self.img15, self.img15_pos)
        elif self.currLine == 18:
            self.screen.blit(self.img7, self.img7_pos)
        elif self.currLine == 19:
            self.screen.blit(self.img16, self.img16_pos)
        elif self.currLine == 20:
            self.screen.blit(self.img18, self.img18_pos)
        elif self.currLine == 21:
            self.screen.blit(self.img3, self.img3_pos)
        elif self.currLine == 22:
            self.screen.blit(self.img3, self.img3_pos)
        elif self.currLine == 23:
            self.screen.blit(self.img3, self.img3_pos)

        # draw the dialogue text inside the box
        if self.currLine < len(self.dialogue):
            line = self.dialogue[self.currLine]
            if "\n" in line:
                parts = line.split("\n")
                surf1 = self.font.render(parts[0], True, (80, 50, 20))
                surf2 = self.font.render(parts[1], True, (80, 50, 20))
                self.screen.blit(surf1, surf1.get_rect(center=(self.textX, self.textY - 15)))
                self.screen.blit(surf2, surf2.get_rect(center=(self.textX, self.textY + 15)))
            else:
                textSurface = self.font.render(line, True, (80, 50, 20))
                self.screen.blit(textSurface, textSurface.get_rect(center=(self.textX, self.textY)))

        # skip button — visible throughout entire prologue
        self.screen.blit(self.skipBtn, self.skipBtn_pos)

        # small hint at the bottom
        hint = self.hintFont.render("Press ENTER to continue", True, (200, 200, 200))
        hintRect = hint.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 15))
        self.screen.blit(hint, hintRect)
