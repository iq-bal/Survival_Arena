# Game Constants and Configuration

# Window Settings
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
GRID_SIZE = 20
CELL_SIZE = 35  # pixels per cell
FPS = 5  # Slower speed for better AI watching

# Layout Settings
GRID_WIDTH = 700  # Width of the game grid area
GRID_HEIGHT = 700  # Height of the game grid area
GRID_OFFSET_X = 20
GRID_OFFSET_Y = 180
SIDEBAR_X = 750  # X position where sidebar starts
SIDEBAR_WIDTH = 630

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

# Color Scheme (Modern UI)
COLORS = {
    # Main background
    'background': (240, 242, 248),  # Light gray-blue
    'border': (100, 110, 200),      # Purple-blue border

    # Grid
    'grid_bg': (220, 225, 235),     # Light grid background
    'grid_lines': (200, 205, 215),  # Subtle grid lines
    'empty': (235, 238, 245),       # Empty cell

    # Entities
    'obstacle': (60, 65, 75),       # Dark gray walls
    'player1': (50, 120, 255),      # Blue (Blue Team)
    'player2': (255, 70, 70),       # Red (Red Team)
    'ally1': (100, 170, 255),       # Light blue (Blue Team allies)
    'ally2': (255, 120, 120),       # Light red (Red Team allies)
    'enemy': (180, 60, 180),        # Purple enemy
    'health': (80, 220, 130),       # Green health
    'coin': (255, 215, 70),         # Gold coin

    # UI Cards
    'card_purple': (110, 100, 220),     # Purple stat cards
    'card_red': (240, 100, 110),        # Red enemy card
    'card_yellow': (255, 235, 170),     # Yellow AI decision card
    'card_info': (220, 240, 255),       # Light blue info card
    'card_green': (60, 200, 180),       # Green restart button

    # Text colors
    'text_white': (255, 255, 255),
    'text_dark': (40, 45, 60),
    'text_red': (220, 60, 80),
    'text_blue': (80, 110, 220),

    # Title
    'title_blue': (80, 110, 220),
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
