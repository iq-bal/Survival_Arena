# Game Constants and Configuration

# Window Settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
GRID_SIZE = 20
CELL_SIZE = 40  # pixels per cell
FPS = 10

# Game Limits
MAX_HEALTH = 100
MAX_RESOURCES = 12
MAX_ENEMIES = 4
MAX_OBSTACLES = 30
MAX_HEALTH_PACKS = 6
MAX_COINS = 6

# Game Rules
HEALTH_PACK_RESTORE = 25
COIN_VALUE = 50
RESOURCE_SPAWN_CHANCE = 0.15
WIN_SCORE = 500
MAX_TURNS = 50
ENEMY_DAMAGE = 20
PLAYER_COLLISION_DAMAGE = 10

# Color Scheme
COLORS = {
    'background': (40, 40, 40),
    'grid_lines': (60, 60, 60),
    'empty': (50, 50, 50),
    'obstacle': (80, 80, 80),

    # Players
    'player1': (50, 120, 255),      # Blue
    'player2': (255, 50, 50),       # Red

    # Allies
    'ally1': (100, 170, 255),       # Light blue
    'ally2': (255, 100, 100),       # Light red

    # Enemies
    'enemy': (200, 50, 200),        # Purple

    # Resources
    'health': (50, 255, 50),        # Green
    'coin': (255, 215, 0),          # Gold

    # UI
    'text': (255, 255, 255),
    'health_bar_bg': (100, 100, 100),
    'health_bar': (50, 255, 50),
    'ui_panel': (30, 30, 30),
}

# AI Parameters
MINIMAX_DEPTH = 3
FUZZY_HEALTH_LOW = 35
FUZZY_HEALTH_MEDIUM_LOW = 30
FUZZY_HEALTH_MEDIUM_HIGH = 70
FUZZY_HEALTH_HIGH = 65
FUZZY_DISTANCE_NEAR = 3
FUZZY_DISTANCE_MEDIUM = 7

# Actions for Fuzzy Logic
ACTIONS = {
    'COLLECT_RESOURCES': 'COLLECT_RESOURCES',
    'FLEE_ENEMY': 'FLEE_ENEMY',
    'AGGRESSIVE_PLAY': 'AGGRESSIVE_PLAY',
    'DEFENSIVE_PLAY': 'DEFENSIVE_PLAY',
    'SEEK_HEALTH': 'SEEK_HEALTH',
    'COLLECT_COINS': 'COLLECT_COINS',
}
