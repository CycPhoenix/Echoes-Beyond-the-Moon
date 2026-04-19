from utils.constants import MAX_LIVES, OXYGEN_MAX

class GameState:
    """Shared state passed between scenes."""
    def __init__(self):
        self.lives = MAX_LIVES
        self.gems = 0
        self.oxygen = OXYGEN_MAX
        self.current_scene = None
