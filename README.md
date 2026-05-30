# Echoes Beyond the Moon

A 2D side-scrolling platformer built with Python and Pygame. Play as Luna, an astronaut stranded on the moon, navigating hostile terrain, dodging meteor showers, and managing a dwindling oxygen supply to reach safety.

---

## Requirements

- Python 3.10+
- Dependencies listed in `requirements.txt`

```bash
pip install -r requirements.txt
```

---

## How to Run

```bash
python main.py
```

---

## Controls

| Action | Default Key |
|--------|-------------|
| Move Left | ← Arrow |
| Move Right | → Arrow |
| Jump | Space |
| Interact (vending machine) | E |
| Pause | ESC |

> Controls are fully rebindable via **Settings** in the main menu.

---

## Gameplay

### Objective
Survive the moon's surface and reach the science base at the end of each level. Manage your oxygen — running out means death.

### Oxygen System
- Oxygen drains continuously — faster while airborne or running
- Refill sources:
  - **O2 Tank pickups** — scattered across platforms (+30)
  - **Oxygen Vents** — walk over them for full refill
  - **Vending Machines** — spend 25 gems for a full refill (press **E** nearby)
- HUD bar turns orange/red when oxygen is critical

### Gems
- Collect blue crystals scattered on platforms
- Used to purchase O2 refills from vending machines
- Carried across levels

### Meteors
- Eye meteors rain from above on a diagonal trajectory
- Land and destroy on contact with platforms
- Hitting the player costs a life (3 lives total)

### Lives
- 3 lives per run
- Losing all lives → Game Over screen
- Lives and gems carry into the handoff between levels

---

## Scenes / Flow

```
Main Menu
  └─ Start Game → Prologue → Level 1 → Handoff → Level 2
  └─ Level 1 (direct)
  └─ Level 2 (direct)
  └─ Settings
```

---

## Settings

Accessible from the main menu. Persisted to `settings.json`.

| Setting | Description |
|---------|-------------|
| Music Volume | Background music volume (0–100%) |
| SFX Volume | Sound effect volume (0–100%) |
| Fullscreen | Toggle windowed / fullscreen |
| Key Bindings | Rebind Move Left, Move Right, Jump |

---

## Project Structure

```
Echoes-Beyond-the-Moon/
├── main.py                  # Entry point, scene manager
├── settings.json            # Saved player settings
├── requirements.txt
│
├── entities/
│   ├── player.py            # Luna — movement, animation, collision, lives
│   ├── meteor.py            # Eye meteor — ballistic diagonal physics
│   ├── platform.py          # Tiled rock platforms
│   └── pickup.py            # Gem and O2 tank collectibles
│
├── scenes/
│   ├── main_menu.py         # Main menu with pygame_menu
│   ├── prologue.py          # Intro cutscene / story
│   ├── level1.py            # Moon surface level — procedural platforms
│   ├── handoff.py           # Transition scene between levels
│   ├── level2.py            # Level 2
│   ├── gameover.py          # Game over screen
│   └── settings.py          # Settings scene
│
├── systems/
│   ├── oxygen.py            # Oxygen drain / refill logic
│   ├── hud.py               # On-screen HUD (O2 bar, gems, lives)
│   ├── camera.py            # Horizontal scrolling camera
│   ├── particles.py         # Visual particle effects
│   └── animation.py         # Sprite frame animation helper
│
└── utils/
    ├── constants.py         # Game-wide constants
    ├── game_state.py        # Shared state passed between scenes
    ├── settings_store.py    # Load/save settings.json
    └── asset_loader.py      # Asset loading helpers
```

---

## Dependencies

| Package | Purpose |
|---------|---------|
| `pygame >= 2.5.0` | Game engine — rendering, input, audio, sprites |
| `pygame-menu >= 4.4.0` | Menu UI (main menu, settings) |

---

## Audio Credits

- Background music: *Iwan Gabovitch — Dark Ambience Loop* (CC0)
- Level 1 music: `lvl1_audio.mp3`
- Sound effects: `collect.wav`, `jump.wav`
