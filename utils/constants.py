SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TITLE = "Echoes Beyond the Moon"

# Scenes
SCENE_MENU = "menu"
SCENE_PROLOGUE = "prologue"
SCENE_LEVEL1 = "level1"
SCENE_LEVEL2 = "level2"
SCENE_HANDOFF = "handoff"
SCENE_GAMEOVER = "gameover"

# Player
MAX_LIVES = 3
MOVE_SPEED = 4
MAX_FALL_SPEED = 8
GRAVITY = 0.2
JUMP_FORCE = -14

# Oxygen
OXYGEN_MAX = 100
OXYGEN_DRAIN_RATE = 0.02       # per frame, idle/walk
OXYGEN_DRAIN_RUN = 0.03        # per frame, running
OXYGEN_DRAIN_JUMP = 0.05       # per frame, airborne
OXYGEN_WARN = 25.0
OXYGEN_VENT_REFILL = 100.0
OXYGEN_TANK_REFILL = 30.0
VENDING_GEM_COST = 25

# Meteors
METEOR_SPEED = 3.5
METEOR_SPAWN_FRAMES = 240      # frames between spawns (~4s at 60fps)
METEOR_TRACK_FRAMES = 90       # frames before lock-on (~1.5s)

# Colors
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
RED        = (220, 50,  50)
CYAN       = (80,  200, 220)
ORANGE     = (255, 140, 0)
WARN_COLOR = (255, 80,  0)
