from game.shared.color import Color


# Game grid sizes
COLUMNS = 40
ROWS = 60
CELL_SIZE = 15

# Screen size
MAX_X = 600  # COLUMNS * CELL_SIZE
MAX_Y = 705  # ROWS * CELL_SIZE

# Pyray window settings
FRAME_RATE = 15
FONT_SIZE = 15
CAPTION = "STAR CRUISER 5000 ✈"

# Colors
WHITE = Color(255, 255, 255)
BLACK = Color(0, 0, 0)
RED = Color(255, 0, 0)
YELLOW = Color(255, 255, 0)
GREEN = Color(0, 255, 0)
BROWN = Color(165, 42, 42)
BLUE = Color(5, 90, 255)
ORANGE = Color(255, 190, 0)
AQUA = Color(100, 255, 255)
PINK = Color(255, 150, 150)

# Ship shields and damage
STARTSHEILDS = 20
LOWSHIELDS = 5

# Sound
SHIPFIRE_SOUND = ""
ASTEROIDSEXPLOSION_SOUND = ""
SHIPSEXPLOSION_SOUND = ""
LOWSHIELDSWARNING_SOUND = ""
GAMEOVER_SOUND = ""

# Ship Layout
SHIP_LAYOUT = [["+", 0, 0, 0], ["A", 0, 1, 0], ["H", 0, 2, 1], [
    "=", -1, 2, 0], ["=", 1, 2, 0], ["_", -2, 2, 0], ["_", 2, 2, 0], ['*', 0, 3, 2]]
SHIP_COLORS = [BLUE, WHITE, RED]

# ASTEROID ATTRIBUTES - - - - - - - - - - - - - - - -

ASTEROID_TYPES_LIST = [
    {
        "name": "SML",
        "text": "`",
        "damage": 1,
        "health": 1,
        "points": 1
    },
    {
        "name": "MED",
        "text": "*",
        "damage": 2,
        "health": 1,
        "points": 1
    },
    {
        "name": "LRG",
        "text": "@",
        "damage": 2,
        "health": 2,
        "points": 2
    },
    {
        "name": "SML-xmove",
        "text": "°",
        "damage": 2,
        "health": 1,
        "points": 3
    },
    {
        "name": "HUGE",
        "text": "@",
        "damage": 4,
        "health": 3,
        "points": 4
    },
    {
        "name": "GIANT",
        "text": "▣",
        "damage": 6,
        "health": 5,
        "points": 6
    }]


HTX = "☐"
HUGE_ASTEROID_LAYOUT = [["@", 0, 0, 0], ["@", 1, 0, 0], ["@", -1, 0, 0], ["@", 0, 1, 0], ["@", 0, -1, 0],
                        ["@", -1, -1, 0], ["@", 1, -1, 0],
                        ["@", -1, 1, 0], ["@", 1, 1, 0],
                        ["@", -2, 0, 0], ["@", 0, -2, 0], ["@", 2, 0, 0], ["@", 0, 2, 0]]

GTX = "@"
GIANT_ASTEROID_LAYOUT = [[GTX, 0, 0, 0], [GTX, 1, 0, 0], [GTX, -1, 0, 0], [GTX, 0, 1, 0], [GTX, 0, -1, 0],
                         [GTX, -1, -1, 0], [GTX, 1, -1, 0],
                         [GTX, -1, 1, 0], [GTX, 1, 1, 0],
                         [GTX, -2, 0, 0], [GTX, 0, -2, 0],
                         [GTX, 2, 0, 0], [GTX, 0, 2, 0],

                         [GTX, -2, -2, 0], [GTX, 2, -2, 0],
                         [GTX, -2, 2, 0], [GTX, 2, 2, 0],

                         [GTX, -2, -1, 0], [GTX, -2, 1, 0],
                         [GTX, 2, 1, 0], [GTX, 2, -1, 0],
                         [GTX, -1, 2, 0], [GTX, 1, 2, 0],
                         [GTX, 1, -2, 0], [GTX, -1, -2, 0],

                         [GTX, -3, -1, 0], [GTX, -3, 1, 0],
                         [GTX, 3, 1, 0], [GTX, 3, -1, 0],
                         [GTX, -1, 3, 0], [GTX, 1, 3, 0],
                         [GTX, 1, -3, 0], [GTX, -1, -3, 0],
                         [GTX, 0, 3, 0], [GTX, 0, -3, 0],
                         [GTX, -3, 0, 0], [GTX, 3, 0, 0]
                         ]
