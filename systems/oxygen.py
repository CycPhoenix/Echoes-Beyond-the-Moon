from utils.constants import (OXYGEN_MAX, OXYGEN_DRAIN_RATE, OXYGEN_DRAIN_RUN,
                              OXYGEN_DRAIN_JUMP, OXYGEN_WARN)


class OxygenSystem:
    def __init__(self):
        self.level    = float(OXYGEN_MAX)
        self.draining = True

    def update(self, player_state: str):
        if not self.draining:
            return
        if player_state == "JUMP":
            rate = OXYGEN_DRAIN_JUMP
        elif player_state == "WALK":
            rate = OXYGEN_DRAIN_RUN
        else:
            rate = OXYGEN_DRAIN_RATE
        self.level = max(0.0, self.level - rate)

    def refill(self, amount: float):
        self.level = min(float(OXYGEN_MAX), self.level + amount)

    @property
    def is_critical(self) -> bool:
        return self.level <= OXYGEN_WARN

    @property
    def is_empty(self) -> bool:
        return self.level <= 0.0

    @property
    def fraction(self) -> float:
        return self.level / OXYGEN_MAX
