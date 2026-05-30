class Level2Scene:
    def __init__(self, screen, state):
        self.screen = screen
        self.state  = state
        self.started = False
        self._result = None

    def update(self, dt):
        if not self.started:
            self.started = True
            self._result = run_level2(self.state)
        return self._result

    def draw(self):
        pass








import pygame
import sys
import os
import random
from utils.constants import SCENE_MENU

def run_level2(state):
    pygame.mixer.init()

    def load_sound(path, trim_seconds=None):
        """Returns a (Sound, trim_ms) tuple. trim_ms is None if no trimming needed."""
        snd = pygame.mixer.Sound(path)
        trim_ms = int(trim_seconds * 1000) if trim_seconds is not None else None
        return (snd, trim_ms)

    def play_sound(snd_tuple):
        if snd_tuple is None:
            return
        snd, trim_ms = snd_tuple
        if trim_ms is not None:
            snd.play(maxtime=trim_ms)
        else:
            snd.play()

    WIDTH, HEIGHT = 1000, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Level 2 - Lunar Base Siege")

    clock = pygame.time.Clock()
    FPS = 60

    BLACK = (10, 10, 15)
    RED = (220, 40, 40)
    GREEN = (40, 220, 80)
    WHITE = (255, 255, 255)
    YELLOW = (240, 220, 80)
    PURPLE = (130, 70, 180)
    CYAN = (0, 200, 255)

    font = pygame.font.SysFont("bahnschrift", 24)
    small_font = pygame.font.SysFont("bahnschrift", 17)

    # ---------------- BASE DIR ----------------
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    try:
        pygame.mixer.music.load(os.path.join(BASE_DIR, r"assets\base\sounds\dungeon_ambient_1.ogg"))
        pygame.mixer.music.set_volume(0.35)
        pygame.mixer.music.play(-1)
    except Exception as e:
        print("[audio] dungeon ambient failed:", e)

    try:
        alarm_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, r"assets\base\sounds\alarm.ogg"))
        alarm_sound.set_volume(0.55)
    except Exception as e:
        print("[audio] alarm failed:", e)
        alarm_sound = None

    try:
        purchase_sound = pygame.mixer.Sound(os.path.join(BASE_DIR, r"assets\base\sounds\snd_purchase.wav"))
        purchase_sound.set_volume(0.70)
    except Exception as e:
        print("[audio] purchase sound failed:", e)
        purchase_sound = None

    alarm_playing = False

    try:
        scan_sound = pygame.mixer.Sound(
            os.path.join(BASE_DIR, r"assets\base\sounds\scanning.mp3")
        )
        scan_sound.set_volume(0.7)
    except:
        scan_sound = None


    def load_image(path, size=None):
        image = pygame.image.load(path).convert_alpha()
        rect = image.get_bounding_rect()
        image = image.subsurface(rect).copy()
        if size:
            image = pygame.transform.scale(image, size)
        return image


    def load_animation(folder_path, size=None):
        frames = []
        if not os.path.exists(folder_path):
            print("Folder not found:", folder_path)
            return frames
        for file_name in sorted(os.listdir(folder_path)):
            if file_name.lower().endswith(".png"):
                frames.append(load_image(os.path.join(folder_path, file_name), size))
        print(folder_path, "loaded", len(frames), "frames")
        return frames


    def draw_center_text(text, y, color=YELLOW, font_used=small_font):
        img = font_used.render(text, True, color)
        x = WIDTH // 2 - img.get_width() // 2
        screen.blit(img, (x, y))


    # ---------------- ASSETS ----------------

    bg1_img = load_image(os.path.join(BASE_DIR, r"assets\base\background\background.png"), (500, 420))
    bg2_img = load_image(os.path.join(BASE_DIR, r"assets\base\background\background 2.png"), (500, 420))

    yellow_floor_img = load_image(os.path.join(BASE_DIR, r"assets\base\floor\yellow tile.png"), (500, 120))

    spawn_door_img = load_image(os.path.join(BASE_DIR, r"assets\base\doors\spawn door.png"), (230, 230))
    exit_door_closed_img  = load_image(os.path.join(BASE_DIR, r"assets\base\extra\base_door (1).png"), (230, 230))
    exit_door_opening_img = load_image(os.path.join(BASE_DIR, r"assets\base\extra\base_door (2).png"), (230, 230))
    exit_door_img = exit_door_closed_img  # starts closed

    suit_blue_img = load_image(os.path.join(BASE_DIR, r"assets\base\chamber\images\chamber_blue.png"), (170, 220))
    suit_red_img = load_image(os.path.join(BASE_DIR, r"assets\base\chamber\images\red_chamber.png"), (170, 220))
    suit_equipping_img = load_image(os.path.join(BASE_DIR, r"assets\base\chamber\images\luna_suit_chamber.png"), (170, 220))

    vending_welcome_frames = [
        load_image(os.path.join(BASE_DIR, r"assets\base\effects\5.png"), (190, 220)),
        load_image(os.path.join(BASE_DIR, r"assets\base\effects\6.png"), (190, 220)),
        load_image(os.path.join(BASE_DIR, r"assets\base\effects\7.png"), (190, 220)),
        load_image(os.path.join(BASE_DIR, r"assets\base\effects\8.png"), (190, 220))
    ]

    vending_shop_frames = [
        load_image(os.path.join(BASE_DIR, r"assets\base\effects\1.png"), (190, 220)),
        load_image(os.path.join(BASE_DIR, r"assets\base\effects\2.png"), (190, 220)),
        load_image(os.path.join(BASE_DIR, r"assets\base\effects\3.png"), (190, 220)),
        load_image(os.path.join(BASE_DIR, r"assets\base\effects\4.png"), (190, 220))
    ]

    panel_blue_img = load_image(os.path.join(BASE_DIR, r"assets\base\panels\panel blue.png"), (100, 100))
    panel_green_img = load_image(os.path.join(BASE_DIR, r"assets\base\panels\Panel green.png"), (100, 100))
    panel_red_img = load_image(os.path.join(BASE_DIR, r"assets\base\panels\panel red.png"), (100, 100))

    torch_frames = [
        load_image(os.path.join(BASE_DIR, r"assets\base\sparks\1.png"), (80, 120)),
        load_image(os.path.join(BASE_DIR, r"assets\base\sparks\2.png"), (80, 120)),
        load_image(os.path.join(BASE_DIR, r"assets\base\sparks\3.png"), (80, 120)),
        load_image(os.path.join(BASE_DIR, r"assets\base\sparks\4.png"), (80, 120))
    ]

    # ---------------- ENDING IMAGES ----------------
    ending_img1 = load_image(os.path.join(BASE_DIR, "assets", "base", "ending", "end 1.png"), (WIDTH, HEIGHT))
    ending_img2 = load_image(os.path.join(BASE_DIR, "assets", "base", "ending", "end 2.png"), (WIDTH, HEIGHT))
    ending_img3 = load_image(os.path.join(BASE_DIR, "assets", "base", "ending", "end 3.png"), (WIDTH, HEIGHT))

    idle_frames   = load_animation(os.path.join(BASE_DIR, r"assets\player\luna-idle\images"), (80, 100))
    luna_die_frames = load_animation(os.path.join(BASE_DIR, r"assets\player\luna-die"), (80, 100))
    run_frames = load_animation(os.path.join(BASE_DIR, r"assets\player\Luna-run\images"), (80, 100))
    jump_frames = load_animation(os.path.join(BASE_DIR, r"assets\player\Luna-jump\images"), (80, 100))

    suit_idle_frames = load_animation(os.path.join(BASE_DIR, r"assets\player\Luna_suit_idle\images"), (80, 100))
    suit_run_frames = load_animation(os.path.join(BASE_DIR, r"assets\player\Luna_suit_run\images"), (80, 100))
    suit_jump_frames = load_animation(os.path.join(BASE_DIR, r"assets\player\Luna_suit_jump\images"), (80, 100))

    # Gun: separate folders for idle (1-2) and fire (3-14)
    gun_idle_frames = load_animation(os.path.join(BASE_DIR, r"assets\player\luna-gun-idle"), (80, 100))
    gun_run_frames  = load_animation(os.path.join(BASE_DIR, r"assets\player\luna-gun-run"),  (80, 100))
    gun_fire_frames = load_animation(os.path.join(BASE_DIR, r"assets\player\luna-gun-fire"), (80, 100))

    # Bomb: separate folders for idle, run, and throw
    bomb_idle_frames      = load_animation(os.path.join(BASE_DIR, r"assets\player\luna-bomb-idle"),      (80, 100))
    bomb_run_frames       = load_animation(os.path.join(BASE_DIR, r"assets\player\luna-bomb-run"),       (80, 100))
    bomb_throw_frames     = load_animation(os.path.join(BASE_DIR, r"assets\player\luna-bomb-throw"),     (80, 100))
    bomb_explosion_frames = load_animation(os.path.join(BASE_DIR, r"assets\player\bomb-explosion"),      (90, 90))

    # Keep these for backward compat checks
    gun_frames  = gun_idle_frames + gun_run_frames + gun_fire_frames
    bomb_frames = bomb_idle_frames + bomb_run_frames + bomb_throw_frames

    # ---------------- SOUNDS ----------------
    snd_alien_dying    = load_sound(os.path.join(BASE_DIR, r"assets\base\sounds\alien dying.mpeg"),    trim_seconds=3)
    snd_alien_kills    = load_sound(os.path.join(BASE_DIR, r"assets\base\sounds\alien kills her.mpeg"), trim_seconds=3)
    snd_bomb_explodes  = load_sound(os.path.join(BASE_DIR, r"assets\base\sounds\bomb explodes.mpeg"))
    snd_bomb_thrown    = load_sound(os.path.join(BASE_DIR, r"assets\base\sounds\bomb thrown.mpeg"))
    snd_gun_equipped   = load_sound(os.path.join(BASE_DIR, r"assets\base\sounds\gun equipped.mpeg"))
    snd_gun_shooting   = load_sound(os.path.join(BASE_DIR, r"assets\base\sounds\gun shooting.mpeg"))
    snd_door_opening   = load_sound(os.path.join(BASE_DIR, r"assets\base\sounds\base door opening.mp3"),  trim_seconds=2)
    snd_teleporting    = load_sound(os.path.join(BASE_DIR, r"assets\base\sounds\teleporting.mp3"))
    snd_scared_breath  = load_sound(os.path.join(BASE_DIR, r"assets\base\sounds\scared breathing.mp3"),    trim_seconds=3)
    snd_eery_ending    = load_sound(os.path.join(BASE_DIR, r"assets\base\sounds\eery ending.mp3"))
    snd_button_press   = load_sound(os.path.join(BASE_DIR, r"assets\base\sounds\button press.mp3"))

    # ---------------- ALIEN ANIMATIONS ----------------

    alien_idle_frames   = load_animation(os.path.join(BASE_DIR, r"assets\base\alien\idle"),   (55, 65))
    alien_walk_frames   = load_animation(os.path.join(BASE_DIR, r"assets\base\alien\walk"),   (55, 65))
    alien_hurt_frames   = load_animation(os.path.join(BASE_DIR, r"assets\base\alien\hurt"),   (55, 65))
    alien_death_frames  = load_animation(os.path.join(BASE_DIR, r"assets\base\alien\death"),  (55, 65))
    alien_attack_frames = load_animation(os.path.join(BASE_DIR, r"assets\base\alien\attack"), (55, 65))

    # Global alien animation timer (shared cycle for walking/idle)
    alien_anim_index = 0
    alien_anim_timer = 0

    animation_index = 0
    animation_timer = 0
    player_facing_right = True

    torch_frame_index = 0
    torch_anim_timer = 0

    vending_frame_index = 0
    vending_anim_timer = 0

    # ---------------- PLAYER ----------------

    player = pygame.Rect(100, 390, 45, 100)
    player_speed = 4
    player_vel_y = 0
    gravity = 0.8
    on_ground = False

    player_dead = False
    player_death_timer = 0   # counts down after death before GAME OVER screen
    luna_die_index = 0        # current frame of luna die animation
    luna_die_timer = 0        # animation frame timer
    luna_die_done  = False    # True once all die frames have played
    door_stand_timer = 0      # counts up while Luna stands in front of door (need 120 = 2s)

    # ---------------- WORLD ----------------

    camera_x = 0
    floor_y = 500
    world_width = 4500

    has_suit = False
    equipping_suit = False
    equip_timer = 0

    spawn_delay_timer = 120
    spawn_dialogue_timer = 300

    alarm_triggered = False
    dialogue_timer = 0
    heartbeat_timer = 0
    screen_flicker = False
    flicker_timer = 0

    shards = state.gems
    weapon_bought = None
    weapon_equipped = False
    alien_spawned = False

    died_without_shards = False


    # "idle" = holding weapon before aliens appear
    # "active" = aiming/shooting (gun) or throwing (bomb)
    weapon_anim_state = "idle"
    weapon_active_delay = 0   # frames to show idle pose before switching to active
    is_firing = False  # True while firing/throwing animation plays
    gun_idle_timer = 0  # counts up when no key pressed; show idle after 2s (120 frames)
    firing_timer = 0   # counts down to end the firing animation

    # bomb: hit aliens one by one with a delay between each
    bomb_hit_index = 0
    bomb_hit_timer = 0
    explosions = []  # list of {x, y, anim_index, timer} drawn at alien positions

    vending_state = "welcome"
    vending_dialogue_timer = 0
    no_shards_timer = 0

    suit_chamber = pygame.Rect(900, 280, 170, 220)
    vending_machine = pygame.Rect(1900, 280, 190, 220)

    spawn_door = pygame.Rect(40, 270, 230, 230)
    exit_door = pygame.Rect(3800, 270, 230, 230)

    torch_positions = [
        (520, 215),
        (1450, 200),
        (2350, 220),
        (3300, 205)
    ]

    # Each alien is now a dict so we can track per-alien state
    # {
    #   "rect": pygame.Rect,
    #   "state": "walk" | "attack" | "hurt" | "death",
    #   "anim_index": int,
    #   "anim_timer": int,
    #   "death_timer": int,   # countdown after death anim finishes before removal
    #   "attack_timer": int,  # countdown between attack hits
    # }
    aliens = []
    bullets = []

    # Attack timing — one alien attacks Luna at a time
    # We use a global cooldown so attacks come one by one
    attack_cooldown = 0   # frames between successive alien attacks on Luna


    def make_alien(x, y):
        return {
            "rect": pygame.Rect(x, y, 55, 65),
            "state": "walk",
            "anim_index": 0,
            "anim_timer": 0,
            "death_timer": 0,
            "attack_timer": 0,
        }


    def draw_text(text, x, y, color=WHITE, font_used=font):
        img = font_used.render(text, True, color)
        screen.blit(img, (x, y))


    def draw_dialogue(text):
        box_width = 680
        box_height = 72
        box_x = WIDTH // 2 - box_width // 2
        box_y = 505
        box = pygame.Rect(box_x, box_y, box_width, box_height)

        panel = pygame.Surface((box_width, box_height), pygame.SRCALPHA)
        panel.fill((5, 10, 20, 235))
        screen.blit(panel, (box_x, box_y))

        pygame.draw.rect(screen, (0, 70, 110), pygame.Rect(box_x - 3, box_y - 3, box_width + 6, box_height + 6), 2)
        pygame.draw.rect(screen, (0, 200, 255), box, 2)
        pygame.draw.rect(screen, (120, 230, 255), pygame.Rect(box_x + 4, box_y + 4, box_width - 8, box_height - 8), 1)

        corner = 20
        pygame.draw.line(screen, CYAN, (box_x, box_y + corner), (box_x, box_y), 2)
        pygame.draw.line(screen, CYAN, (box_x, box_y), (box_x + corner, box_y), 2)
        pygame.draw.line(screen, CYAN, (box_x + box_width - corner, box_y), (box_x + box_width, box_y), 2)
        pygame.draw.line(screen, CYAN, (box_x + box_width, box_y), (box_x + box_width, box_y + corner), 2)
        pygame.draw.line(screen, CYAN, (box_x, box_y + box_height - corner), (box_x, box_y + box_height), 2)
        pygame.draw.line(screen, CYAN, (box_x, box_y + box_height), (box_x + corner, box_y + box_height), 2)
        pygame.draw.line(screen, CYAN, (box_x + box_width - corner, box_y + box_height), (box_x + box_width, box_y + box_height), 2)
        pygame.draw.line(screen, CYAN, (box_x + box_width, box_y + box_height - corner), (box_x + box_width, box_y + box_height), 2)

        for i in range(4):
            pygame.draw.circle(screen, CYAN, (box_x + 14, box_y + 18 + i * 10), 2)

        words = text.split(" ")
        lines = []
        current_line = ""
        for word in words:
            test_line = current_line + word + " "
            if small_font.size(test_line)[0] < box_width - 70:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)

        for i, line in enumerate(lines[:2]):
            shadow = small_font.render(line, True, (45, 95, 130))
            screen.blit(shadow, (box_x + 44, box_y + 20 + i * 22))
            txt = small_font.render(line, True, (235, 245, 255))
            screen.blit(txt, (box_x + 42, box_y + 18 + i * 22))

        pygame.draw.polygon(screen, CYAN, [
            (box_x + box_width - 34, box_y + box_height - 22),
            (box_x + box_width - 18, box_y + box_height - 22),
            (box_x + box_width - 26, box_y + box_height - 10)
        ])


    def draw_torch(world_x, y, camera_x, shake_x, shake_y):
        screen_x = world_x - camera_x * 0.6 + shake_x
        screen_y = y + shake_y
        screen.blit(torch_frames[torch_frame_index], (screen_x, screen_y))


    def draw_vending_machine(vend_screen, shake_x, shake_y):
        if vending_state == "welcome":
            current_vending = vending_welcome_frames[vending_frame_index % len(vending_welcome_frames)]
            draw_text(f"Current Gems: {shards}", vend_screen.x - 10, vend_screen.y - 30, CYAN, small_font)
        else:
            current_vending = vending_shop_frames[vending_frame_index % len(vending_shop_frames)]
        screen.blit(current_vending, (vend_screen.x + shake_x, vend_screen.y + shake_y))


    def draw_chamber_effects(chamber_screen, shake_x, shake_y, equip_timer):
        scan_y = chamber_screen.y + ((180 - equip_timer) % chamber_screen.height)
        pygame.draw.line(screen, (255, 80, 80),
            (chamber_screen.x + 20 + shake_x, scan_y + shake_y),
            (chamber_screen.x + chamber_screen.width - 20 + shake_x, scan_y + shake_y), 3)
        pygame.draw.line(screen, (255, 180, 180),
            (chamber_screen.x + 25 + shake_x, scan_y - 5 + shake_y),
            (chamber_screen.x + chamber_screen.width - 25 + shake_x, scan_y - 5 + shake_y), 1)
        if equip_timer % 8 == 0:
            for _ in range(5):
                spark_x = random.randint(chamber_screen.x + 25, chamber_screen.x + chamber_screen.width - 25)
                spark_y = random.randint(chamber_screen.y + 25, chamber_screen.y + chamber_screen.height - 25)
                pygame.draw.circle(screen, (255, 190, 80), (spark_x + shake_x, spark_y + shake_y), 2)


    def spawn_aliens():
        nonlocal alien_spawned
        if not alien_spawned:
            start_x = exit_door.x + 120
            for i in range(8):
                aliens.append(make_alien(start_x + i * 180, 435))
            alien_spawned = True


    def get_alien_frame(alien, frames):
        """Return the correct frame for this alien's anim state, flipped to face left."""
        if not frames:
            return None
        frame = frames[alien["anim_index"] % len(frames)]
        return pygame.transform.flip(frame, True, False)


    running = True
    moving = False   # initialise before first frame so weapon idle timer never NameErrors
    paused = False
    return_scene = None

    # Pause font surfaces (created once, reused every frame)
    _pause_font_big = pygame.font.SysFont("bahnschrift", 52)
    _pause_font_sm  = pygame.font.SysFont("bahnschrift", 26)

    while running:

        clock.tick(FPS)

        # ---------------- TIMERS ----------------

        torch_anim_timer += 1
        if torch_anim_timer >= 14:
            torch_anim_timer = 0
            torch_frame_index = (torch_frame_index + 1) % len(torch_frames)

        vending_anim_timer += 1
        if vending_anim_timer >= 12:
            vending_anim_timer = 0
            vending_frame_index += 1

        if attack_cooldown > 0:
            attack_cooldown -= 1

        # gun idle timer — counts up when no movement/firing; resets on any input
        if weapon_equipped and weapon_bought == "gun":
            if not moving and not is_firing:
                gun_idle_timer += 1
            # moving/firing resets handled inside animation block

        # count down firing timer so full animation plays through
        if is_firing:
            firing_timer -= 1
            if firing_timer <= 0:
                is_firing = False
                firing_timer = 0

        # count down idle delay, then switch to active once aliens exist
        if weapon_equipped and weapon_anim_state == "idle":
            if weapon_active_delay > 0:
                weapon_active_delay -= 1
            elif len(aliens) > 0:
                weapon_anim_state = "active" 

        # bomb one-by-one hit sequence
        if bomb_hit_timer > 0:
            bomb_hit_timer -= 1
            if bomb_hit_timer == 0:
                # find the bomb_hit_index-th alive alien and hurt it
                alive = [a for a in aliens if a["state"] not in ("hurt", "death")]
                if bomb_hit_index < len(alive):
                    a = alive[bomb_hit_index]
                    a["state"] = "hurt"
                    a["anim_index"] = 0
                    play_sound(snd_alien_dying)
                    # spawn explosion at this alien's screen position
                    play_sound(snd_bomb_explodes)
                    explosions.append({
                        "x": a["rect"].x,  # world x — will convert to screen when drawing
                        "y": a["rect"].y - 20,
                        "anim_index": 0,
                        "anim_timer": 0,
                        "done": False
                    })
                    bomb_hit_index += 1
                    bomb_hit_timer = 40  # delay before hitting next alien (~0.7s)
                else:
                    # this throw sequence done — stay equipped, reset for next throw
                    is_firing = False
                    firing_timer = 0
                    bomb_hit_index = 0

        # ---------------- EVENTS ----------------

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    paused = not paused

                if paused:
                    if event.key == pygame.K_m:
                        return_scene = SCENE_MENU
                        running = False
                    if event.key == pygame.K_r:
                        # Full restart — same as retry button
                        player.x, player.y = 100, 390
                        player_vel_y = 0
                        on_ground    = False
                        player_dead  = False
                        player_death_timer = 0
                        luna_die_index = 0
                        luna_die_timer = 0
                        luna_die_done  = False
                        door_stand_timer = 0
                        camera_x     = 0
                        has_suit     = False
                        equipping_suit = False
                        spawn_delay_timer = 120
                        alarm_triggered   = False
                        dialogue_timer    = 0
                        heartbeat_timer   = 0
                        screen_flicker    = False
                        flicker_timer     = 0
                        shards = state.gems
                        weapon_bought     = None
                        weapon_equipped   = False
                        alien_spawned     = False
                        weapon_anim_state = "idle"
                        weapon_active_delay = 0
                        is_firing         = False
                        gun_idle_timer    = 0
                        firing_timer      = 0
                        bomb_hit_index    = 0
                        bomb_hit_timer    = 0
                        explosions.clear()
                        aliens.clear()
                        bullets.clear()
                        vending_state          = "welcome"
                        vending_dialogue_timer = 0
                        no_shards_timer = 0
                        spawn_dialogue_timer   = 300
                        exit_door_img          = exit_door_closed_img
                        paused = False
                    continue  # swallow all other input while paused

                if player_dead:
                    continue  # ignore all input while dead

                if event.key == pygame.K_e:

                    chamber_screen = pygame.Rect(
                        suit_chamber.x - camera_x, suit_chamber.y,
                        suit_chamber.width, suit_chamber.height)

                    if player.colliderect(chamber_screen) and not has_suit and not equipping_suit:
                        equipping_suit = True
                        equip_timer = 180

                        if scan_sound:
                            scan_sound.play()

                    vend_screen = pygame.Rect(
                        vending_machine.x - camera_x, vending_machine.y,
                        vending_machine.width, vending_machine.height)

                    if player.colliderect(vend_screen) and vending_state == "welcome":
                       if shards <= 0:
                            no_shards_timer = 240
                            died_without_shards = True
                            spawn_aliens()
                       else:
                           
                            vending_state = "shop"
                            vending_frame_index = 0
                            vending_anim_timer = 0
                            vending_dialogue_timer = 300

                if event.key == pygame.K_1:
                    vend_screen = pygame.Rect(
                        vending_machine.x - camera_x, vending_machine.y,
                        vending_machine.width, vending_machine.height)
                    if player.colliderect(vend_screen) and vending_state == "shop":
                        if shards >= 5:
                            shards -= 5
                            weapon_bought = "gun"
                            weapon_equipped = False

                            if purchase_sound:
                               purchase_sound.play()

                if event.key == pygame.K_2:
                    vend_screen = pygame.Rect(
                        vending_machine.x - camera_x, vending_machine.y,
                        vending_machine.width, vending_machine.height)
                    if player.colliderect(vend_screen) and vending_state == "shop":
                        if shards >= 10:
                            shards -= 10
                            weapon_bought = "bomb"
                            weapon_equipped = False

                            if purchase_sound:
                                purchase_sound.play()

                if event.key == pygame.K_z:
                    if weapon_bought:
                        weapon_equipped = True
                        weapon_anim_state = "idle"   # always start idle when equipping
                        weapon_active_delay = 120    # show idle for 2 seconds before going active
                        animation_index = 0
                        if weapon_bought == "gun":
                            play_sound(snd_gun_equipped)
                        if alarm_triggered:
                            spawn_aliens()

                if event.key == pygame.K_SPACE:
                    if weapon_equipped and weapon_bought == "gun":
                        bullets.append(pygame.Rect(player.x + 55, player.y + 45, 18, 6))
                        is_firing = True
                        firing_timer = max(len(gun_fire_frames), 1) * 8
                        play_sound(snd_gun_shooting)
                    elif weapon_equipped and weapon_bought == "bomb":
                        is_firing = True
                        firing_timer = max(len(bomb_throw_frames), 1) * 8
                        bomb_hit_index = 0
                        bomb_hit_timer = firing_timer + 5
                        play_sound(snd_bomb_thrown)

        if paused:
            # Draw pause overlay on top of current frame then skip game logic
            ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            ov.fill((0, 0, 0, 160))
            screen.blit(ov, (0, 0))
            cx, cy = WIDTH // 2, HEIGHT // 2
            box = pygame.Rect(0, 0, 380, 240)
            box.center = (cx, cy)
            pygame.draw.rect(screen, (15, 15, 30), box, border_radius=12)
            pygame.draw.rect(screen, (0, 200, 180), box, 2, border_radius=12)
            title = _pause_font_big.render("PAUSED", True, (0, 220, 200))
            screen.blit(title, title.get_rect(center=(cx, cy - 70)))
            for i, line in enumerate(["ESC  —  Resume", "R     —  Restart", "M    —  Main Menu"]):
                surf = _pause_font_sm.render(line, True, (200, 200, 200))
                screen.blit(surf, surf.get_rect(center=(cx, cy - 10 + i * 40)))
            pygame.display.update()
            clock.tick(FPS)
            continue

        # ---------------- PLAYER MOVEMENT ----------------

        if not player_dead:

            keys = pygame.key.get_pressed()

            if not equipping_suit:  # lock movement while suit-up animation plays
                if keys[pygame.K_LEFT]:
                    if camera_x > 0:
                        camera_x -= player_speed
                    player_facing_right = False

                if keys[pygame.K_RIGHT]:
                    if camera_x < exit_door.x - 200:
                        camera_x += player_speed
                    else:
                        # camera has hit its limit — let player walk right on screen toward door
                        if player.x < WIDTH - 80:
                            player.x += player_speed
                    player_facing_right = True

                if keys[pygame.K_UP] and on_ground:
                    player_vel_y = -15
                    on_ground = False

            player.y += player_vel_y
            player_vel_y += gravity

            if player.bottom >= floor_y:
                player.bottom = floor_y
                player_vel_y = 0
                on_ground = True

        else:
            keys = pygame.key.get_pressed()  # still need keys for animation check

        # ---------------- SUIT TIMER ----------------

        if equipping_suit:
            equip_timer -= 1
            if equip_timer <= 0:
                if scan_sound:
                    scan_sound.stop()

                equipping_suit = False
                has_suit = True
                alarm_triggered = True
                dialogue_timer = 240
                heartbeat_timer = 300
                screen_flicker = True
                flicker_timer = 600
                if alarm_sound and not alarm_playing:
                    alarm_sound.play(-1)
                    alarm_playing = True

        # ---------------- PLAYER DEATH TIMER ----------------

        if player_dead:
            player_death_timer -= 1
            # advance die animation frame counter (sprite drawn after world below)
            if luna_die_frames and not luna_die_done:
                luna_die_timer += 1
                if luna_die_timer >= 8:
                    luna_die_timer = 0
                    luna_die_index += 1
                    if luna_die_index >= len(luna_die_frames):
                        luna_die_index = len(luna_die_frames) - 1
                        luna_die_done = True

            if player_death_timer <= 0:
                # ── GAME OVER SCREEN WITH RETRY ──────────────────
                go_font  = pygame.font.SysFont("bahnschrift", 64)
                go_sub   = pygame.font.SysFont("bahnschrift", 24)
                btn_font = pygame.font.SysFont("bahnschrift", 28)
                go_img   = go_font.render("GAME OVER", True, RED)

                if died_without_shards:
                    sub_img = go_sub.render("You died without any gems... The aliens got you quickly.", True, WHITE)
                else:
                   sub_img  = go_sub.render("The aliens got Luna...", True, WHITE)

                btn_rect = pygame.Rect(WIDTH // 2 - 90, HEIGHT // 2 + 70, 180, 48)

                waiting = True
                while waiting:
                    mx, my = pygame.mouse.get_pos()
                    hovered = btn_rect.collidepoint(mx, my)

                    screen.fill(BLACK)
                    screen.blit(go_img,  (WIDTH // 2 - go_img.get_width()  // 2, HEIGHT // 2 - 80))
                    screen.blit(sub_img, (WIDTH // 2 - sub_img.get_width() // 2, HEIGHT // 2 - 10))

                    # Retry button
                    btn_color = (180, 30, 30) if hovered else (120, 20, 20)
                    pygame.draw.rect(screen, btn_color, btn_rect, border_radius=10)
                    pygame.draw.rect(screen, RED, btn_rect, 2, border_radius=10)
                    btn_txt = btn_font.render("RETRY", True, WHITE)
                    screen.blit(btn_txt, (btn_rect.centerx - btn_txt.get_width() // 2,
                                        btn_rect.centery - btn_txt.get_height() // 2))

                    pygame.display.update()
                    clock.tick(FPS)

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if event.type == pygame.MOUSEBUTTONDOWN and hovered:
                            play_sound(snd_button_press)
                            pygame.time.delay(300)  # brief pause so sound is heard
                            # ── RESET ALL GAME STATE ──────────────
                            player.x, player.y = 100, 390
                            player_vel_y = 0
                            on_ground    = False
                            player_dead  = False
                            player_death_timer = 0
                            luna_die_index = 0
                            luna_die_timer = 0
                            luna_die_done  = False
                            door_stand_timer = 0
                            camera_x     = 0
                            has_suit     = False
                            equipping_suit = False
                            spawn_delay_timer = 120
                            alarm_triggered   = False
                            dialogue_timer    = 0
                            heartbeat_timer   = 0
                            screen_flicker    = False
                            flicker_timer     = 0
                            shards = state.gems
                            weapon_bought     = None
                            weapon_equipped   = False
                            alien_spawned     = False
                            weapon_anim_state = "idle"
                            weapon_active_delay = 0
                            is_firing         = False
                            gun_idle_timer    = 0
                            firing_timer      = 0
                            bomb_hit_index    = 0
                            bomb_hit_timer    = 0
                            explosions.clear()
                            aliens.clear()
                            bullets.clear()
                            vending_state          = "welcome"
                            vending_dialogue_timer = 0
                            no_shards_timer = 0
                            
                            spawn_dialogue_timer   = 0
                            exit_door_img          = exit_door_closed_img
                            waiting = False

        # ---------------- CAMERA SHAKE ----------------

        shake_x = 0
        shake_y = 0
        if screen_flicker:
            shake_x = random.randint(-3, 3)
            shake_y = random.randint(-3, 3)

        # ---------------- DRAW WORLD ----------------

        screen.fill((5, 5, 8))

        backgrounds = [bg1_img, bg2_img]
        for i in range(10):
            bg = backgrounds[i % 2]
            screen.blit(bg, (i * 500 - camera_x * 0.6 + shake_x, 100 + shake_y))

        for torch_x, torch_y in torch_positions:
            draw_torch(torch_x, torch_y, camera_x, shake_x, shake_y)

        floor_tile_width = yellow_floor_img.get_width()
        floor_overlap = 17
        floor_step = floor_tile_width - floor_overlap
        for i in range(-2, world_width // floor_step + 5):
            screen.blit(yellow_floor_img, (i * floor_step - camera_x + shake_x, 470 + shake_y))

        screen.blit(spawn_door_img, (spawn_door.x - camera_x + shake_x, spawn_door.y + shake_y))

        # ---------------- CHAMBER ----------------

        chamber_screen = pygame.Rect(
            suit_chamber.x - camera_x, suit_chamber.y,
            suit_chamber.width, suit_chamber.height)

        if equipping_suit:
            screen.blit(suit_equipping_img, (chamber_screen.x + shake_x, chamber_screen.y + shake_y))
            draw_chamber_effects(chamber_screen, shake_x, shake_y, equip_timer)
        elif has_suit:
            screen.blit(suit_red_img, (chamber_screen.x + shake_x, chamber_screen.y + shake_y))
        else:
            screen.blit(suit_blue_img, (chamber_screen.x + shake_x, chamber_screen.y + shake_y))

        # ---------------- VENDING ----------------

        vend_screen = pygame.Rect(
            vending_machine.x - camera_x, vending_machine.y,
            vending_machine.width, vending_machine.height)
        draw_vending_machine(vend_screen, shake_x, shake_y)

        screen.blit(panel_blue_img,  (620  - camera_x + shake_x, 400 + shake_y))
        screen.blit(panel_green_img, (1200 - camera_x + shake_x, 400 + shake_y))
        screen.blit(panel_red_img,   (2500 - camera_x + shake_x, 400 + shake_y))

        # ---------------- EXIT ----------------

        exit_screen = pygame.Rect(
            exit_door.x - camera_x, exit_door.y,
            exit_door.width, exit_door.height)
        # Door only appears after all aliens have been killed
        door_visible = (not alarm_triggered) or (alien_spawned and len(aliens) == 0)
        if door_visible:
            screen.blit(exit_door_img, (exit_screen.x + shake_x, exit_screen.y + shake_y))

        # ---------------- BULLETS ----------------

        for bullet in bullets[:]:
            bullet.x += 10
            pygame.draw.rect(screen, YELLOW, bullet)
            if bullet.x > WIDTH:
                bullets.remove(bullet)

        # ---------------- ALIENS ----------------

        player_world_x = camera_x + player.x

        for alien in aliens[:]:

            a_rect = alien["rect"]
            a_state = alien["state"]

            alien_screen = pygame.Rect(
                a_rect.x - camera_x, a_rect.y,
                a_rect.width, a_rect.height)

            # --- advance this alien's animation ---
            alien["anim_timer"] += 1
            if alien["anim_timer"] >= 8:
                alien["anim_timer"] = 0
                alien["anim_index"] += 1

            # --- state machine ---

            if a_state == "death":
                # play death anim then remove
                frames = alien_death_frames
                if frames:
                    clamped = min(alien["anim_index"], len(frames) - 1)
                    frame = pygame.transform.flip(frames[clamped], True, False)
                    screen.blit(frame, (alien_screen.x, alien_screen.y))
                alien["death_timer"] -= 1
                if alien["death_timer"] <= 0:
                    aliens.remove(alien)
                continue  # skip movement & collision while dying

            if a_state == "hurt":
                frames = alien_hurt_frames
                if frames:
                    clamped = min(alien["anim_index"], len(frames) - 1)
                    frame = pygame.transform.flip(frames[clamped], True, False)
                    screen.blit(frame, (alien_screen.x, alien_screen.y))
                # after hurt anim finishes → death
                if alien["anim_index"] >= len(frames if frames else [1]):
                    alien["state"] = "death"
                    alien["anim_index"] = 0
                    alien["death_timer"] = max(len(alien_death_frames), 1) * 8 + 20
                continue  # stay in place while hurt

            if a_state == "attack":
                frames = alien_attack_frames
                if frames:
                    clamped = min(alien["anim_index"], len(frames) - 1)
                    frame = pygame.transform.flip(frames[clamped], True, False)
                    screen.blit(frame, (alien_screen.x, alien_screen.y))

                # deal damage to Luna once per attack cycle
                alien["attack_timer"] -= 1
                if alien["attack_timer"] <= 0 and not player_dead:
                    # stagger attacks: only attack if global cooldown is clear
                    if attack_cooldown == 0:
                        player_dead = True
                        player_death_timer = 180  # ~3 seconds before GAME OVER
                        play_sound(snd_alien_kills)

                # if alien drifts away from player, go back to walk
                if a_rect.x > player_world_x + 80:
                    alien["state"] = "walk"
                    alien["anim_index"] = 0

            elif a_state == "walk":
                frames = alien_walk_frames
                if frames:
                    frame = pygame.transform.flip(
                        frames[alien["anim_index"] % len(frames)], True, False)
                    screen.blit(frame, (alien_screen.x, alien_screen.y))

                # move toward player
                if a_rect.x > player_world_x + 60:
                    a_rect.x -= 1
                else:
                    # reached player — switch to attack
                    alien["state"] = "attack"
                    alien["anim_index"] = 0
                    alien["attack_timer"] = 90   # ~1.5s before first hit
                    attack_cooldown = 60         # global stagger between aliens

            # --- bullet collision (only for walk/attack states) ---
            for bullet in bullets[:]:
                if bullet.colliderect(alien_screen):
                    bullets.remove(bullet)
                    alien["state"] = "hurt"
                    alien["anim_index"] = 0
                    play_sound(snd_alien_dying)
                    break

        # ---------------- EXPLOSIONS ----------------

        for exp in explosions[:]:
            exp["anim_timer"] += 1
            if exp["anim_timer"] >= 6:
                exp["anim_timer"] = 0
                exp["anim_index"] += 1
            if bomb_explosion_frames and exp["anim_index"] < len(bomb_explosion_frames):
                frame = bomb_explosion_frames[exp["anim_index"]]
                screen.blit(frame, (exp["x"] - camera_x, exp["y"]))
            else:
                explosions.remove(exp)  # animation finished — remove it

        # ---------------- PLAYER ANIMATION ----------------

        if not player_dead:
            moving = keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]

            if weapon_equipped and weapon_bought == "gun":
                if is_firing:
                    # SPACE pressed — full attack animation
                    current_frames = gun_fire_frames if gun_fire_frames else gun_idle_frames
                    gun_idle_timer = 0  # reset idle countdown while attacking
                elif moving:
                    # arrow key held — run animation
                    current_frames = gun_run_frames if gun_run_frames else gun_idle_frames
                    gun_idle_timer = 0  # reset idle countdown while running
                elif gun_idle_timer >= 120:
                    # no input for 2+ seconds — idle
                    current_frames = gun_idle_frames if gun_idle_frames else gun_run_frames
                else:
                    # just stopped — keep showing run frames briefly
                    current_frames = gun_run_frames if gun_run_frames else gun_idle_frames

            elif weapon_equipped and weapon_bought == "bomb":
                if is_firing and bomb_throw_frames:
                    # SPACE pressed — throwing animation
                    current_frames = bomb_throw_frames
                elif moving and bomb_run_frames:
                    # moving — running with bomb
                    current_frames = bomb_run_frames
                else:
                    # standing — idle holding bomb
                    current_frames = bomb_idle_frames if bomb_idle_frames else bomb_run_frames

            elif has_suit:
                if not on_ground:
                    current_frames = suit_jump_frames
                elif moving:
                    current_frames = suit_run_frames
                else:
                    current_frames = suit_idle_frames

            else:
                if not on_ground:
                    current_frames = jump_frames
                elif moving:
                    current_frames = run_frames
                else:
                    current_frames = idle_frames

            if len(current_frames) > 0:
                # clamp so switching to a shorter set never goes out of range
                if animation_index >= len(current_frames):
                    animation_index = 0

                animation_timer += 1
                if animation_timer >= 8:
                    animation_timer = 0
                    animation_index = (animation_index + 1) % len(current_frames)

                player_img = current_frames[animation_index]
                if not player_facing_right:
                    player_img = pygame.transform.flip(player_img, True, False)

                if not equipping_suit:
                    screen.blit(player_img, (player.x - 18 + shake_x, player.y - 8 + shake_y))

        # ---------------- LUNA DIE ANIMATION (drawn on top of world) ----------------

        if player_dead and luna_die_frames:
            die_img = luna_die_frames[luna_die_index]
            screen.blit(die_img, (player.x - 18 + shake_x, player.y - 8 + shake_y))

        # ---------------- UI ----------------

        draw_text(f"Gems: {shards}", 20, 20, WHITE, small_font)
        draw_text(f"Suit: {'YES' if has_suit else 'NO'}", 20, 45, WHITE, small_font)
        draw_text(f"Weapon: {weapon_bought if weapon_bought else 'None'}", 20, 70, WHITE, small_font)
        if weapon_equipped:
            draw_text("Weapon Equipped", 20, 95, GREEN, small_font)

        # ---------------- DIALOGUES ----------------

        if player.colliderect(chamber_screen) and not has_suit and not equipping_suit:
            draw_center_text("Press E to equip suit", 30, YELLOW, small_font)
            draw_dialogue("A lunar protection suit...? Why would this base need something like that?")

        elif equipping_suit:
            draw_center_text("Equipping lunar suit...", 30, CYAN, small_font)

        
        
        elif no_shards_timer > 0:
            draw_dialogue("I don't have any gems... I need to complete the lunar surface mission and collect gems first!")
            no_shards_timer -= 1
        elif player.colliderect(vend_screen) and vending_state == "welcome":
            draw_center_text("Press E to open vending machine", 30, YELLOW, small_font)
            draw_dialogue("A supply terminal... maybe these shards still work here. This is my chance to break free!")

        elif vending_dialogue_timer > 0:
            draw_dialogue("It says choose 1 for gun and choose 2 for bomb, then press Z to equip.")
            vending_dialogue_timer -= 1

        elif dialogue_timer > 0:
            draw_dialogue("That noise... something's inside this base. I need to get out of here now!")
            dialogue_timer -= 1

        elif spawn_delay_timer > 0:
            spawn_delay_timer -= 1

        elif spawn_dialogue_timer > 0:
            draw_dialogue("Lab... silent. No people. No signals. Something happened here...")
            spawn_dialogue_timer -= 1

        # ---------------- ALARM ----------------

        if heartbeat_timer > 0:
            if heartbeat_timer % 30 < 15:
                pygame.draw.rect(screen, RED, (0, 0, WIDTH, HEIGHT), 5)
            heartbeat_timer -= 1

        if screen_flicker and flicker_timer > 0:
            if flicker_timer % 20 < 10:
                red_overlay = pygame.Surface((WIDTH, HEIGHT))
                red_overlay.set_alpha(75)
                red_overlay.fill(RED)
                screen.blit(red_overlay, (shake_x, shake_y))
                draw_text("WARNING: BASE SECURITY BREACH", 330, 120, RED, small_font)
           
            flicker_timer -= 1
            if flicker_timer <= 0:
               screen_flicker = False

               if alarm_sound:
                alarm_sound.stop()

                alarm_playing = False

        # ---------------- DOOR STAND PROGRESS BAR ----------------

        if door_stand_timer > 0 and door_visible:
            bar_w = 120
            bar_h = 10
            bar_x = exit_screen.x + (exit_door.width - bar_w) // 2
            bar_y = exit_screen.y - 20
            progress = min(door_stand_timer / 120, 1.0)
            pygame.draw.rect(screen, (60, 60, 60), (bar_x, bar_y, bar_w, bar_h))
            pygame.draw.rect(screen, CYAN, (bar_x, bar_y, int(bar_w * progress), bar_h))
            pygame.draw.rect(screen, WHITE, (bar_x, bar_y, bar_w, bar_h), 1)

        # ---------------- LEVEL COMPLETE ----------------

        if not player_dead:
            player_world_rect = pygame.Rect(
                camera_x + player.x, player.y,
                player.width, player.height)

            if player_world_rect.colliderect(exit_door) and door_visible:
                door_stand_timer += 1
            else:
                door_stand_timer = 0  # reset if she walks away

            if door_stand_timer >= 120:  # 2 seconds at 60 FPS

                # ── ENDING SEQUENCE ──────────────────────────────

                def fade_in_image(img):
                    overlay = pygame.Surface((WIDTH, HEIGHT))
                    overlay.fill(BLACK)
                    for alpha in range(255, -1, -3):
                        screen.blit(img, (0, 0))
                        overlay.set_alpha(alpha)
                        screen.blit(overlay, (0, 0))
                        pygame.display.update()
                        clock.tick(FPS)
                        for e in pygame.event.get():
                            if e.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()

                def fade_out():
                    overlay = pygame.Surface((WIDTH, HEIGHT))
                    overlay.fill(BLACK)
                    for alpha in range(0, 256, 4):
                        overlay.set_alpha(alpha)
                        screen.blit(overlay, (0, 0))
                        pygame.display.update()
                        clock.tick(FPS)

                # Step 1 — door swings open
                play_sound(snd_door_opening)
                exit_door_img = exit_door_opening_img
                screen.blit(exit_door_opening_img, (exit_screen.x, exit_screen.y))
                pygame.display.update()
                pygame.time.delay(2000)  # hold open image for 2s (matches audio trim)

                # Step 2 — teleport flash + sound
                play_sound(snd_teleporting)
                for _ in range(4):
                    screen.fill((200, 240, 255))  # pale cyan flash
                    pygame.display.update()
                    pygame.time.delay(70)
                    screen.fill(BLACK)
                    pygame.display.update()
                    pygame.time.delay(70)
                fade_out()

                # Scene 1
                fade_in_image(ending_img1)
                pygame.time.delay(3000)
                fade_out()

                # Scene 2 — scared breathing audio (first 3s)
                play_sound(snd_scared_breath)
                fade_in_image(ending_img2)
                pygame.time.delay(3000)
                fade_out()

                # Scene 3 — eery ending music plays through to end of credits
                play_sound(snd_eery_ending)
                fade_in_image(ending_img3)
                pygame.time.delay(3000)
                fade_out()

                # "To be Continued" text
                screen.fill(BLACK)
                tbc_font = pygame.font.SysFont("bahnschrift", 48)
                tbc_img = tbc_font.render("To be Continued...", True, WHITE)
                screen.blit(tbc_img, (WIDTH // 2 - tbc_img.get_width() // 2, HEIGHT // 2 - 30))
                pygame.display.update()
                pygame.time.delay(3000)
                fade_out()

                # ── CREDITS ──────────────────────────────────────

                credits_lines = [
                    ("MOON RACE", 40, CYAN),
                    ("Echoes Beyond The Moon", 26, WHITE),
                    ("", 20, WHITE),
                    ("", 20, WHITE),
                    ("DEVELOPED BY", 22, YELLOW),
                    ("", 16, WHITE),
                    ("Ban Cong Yin Brosnan", 30, WHITE),
                    ("Yong Zi Wen", 30, WHITE),
                    ("Bavatarani A/P Kalai Selvan", 30, WHITE),
                    ("Safa Eliash", 30, WHITE),
                    ("", 20, WHITE),
                    ("", 20, WHITE),
                    ("Thank you for playing!", 28, CYAN),
                    ("", 60, WHITE),
                ]

                rendered = []
                total_h = 0
                for text, size, color in credits_lines:
                    f = pygame.font.SysFont("bahnschrift", size)
                    surf = f.render(text, True, color) if text else None
                    h = size + 10 if not surf else surf.get_height() + 10
                    rendered.append((surf, h, color))
                    total_h += h

                scroll_y = HEIGHT
                scroll_speed = 1.2
                credits_running = True

                while credits_running:
                    clock.tick(FPS)
                    screen.fill(BLACK)
                    y = scroll_y
                    for surf, h, _ in rendered:
                        if surf and 0 < y < HEIGHT:
                            screen.blit(surf, (WIDTH // 2 - surf.get_width() // 2, int(y)))
                        y += h
                    scroll_y -= scroll_speed
                    if scroll_y + total_h < 0:
                        credits_running = False
                    for e in pygame.event.get():
                        if e.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                        if e.type == pygame.KEYDOWN:
                            credits_running = False
                    pygame.display.update()

                
                state.gems = shards
                return_scene = SCENE_MENU
                running = False

        pygame.display.update()

    pygame.mixer.music.stop()
    # Restore main game resolution after level 2's custom window size
    pygame.display.set_mode((1280, 720))
    return return_scene