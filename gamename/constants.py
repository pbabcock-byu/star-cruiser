from game.shared.color import Color
import random

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

BROWN = Color(145, 20, 22)

BLUE = Color(5, 90, 255)
ORANGE = Color(255, 190, 0)
AQUA = Color(100, 255, 255)
PINK = Color(255, 150, 150)
BREEN = Color(245, 120, 22)


# Ship shields and damage
MAXSHIELDS = 40
STARTSHEILDS = 20
LOWSHIELDS = 5

# Sound
SHIPFIRE_SOUND = "gamename\game\sounds\sf_laser_15.mp3"
ASTEROIDSEXPLOSION_SOUND = ""
SHIPSEXPLOSION_SOUND = ""
LOWSHIELDSWARNING_SOUND = ""
GAMEOVER_SOUND = ""

# Ship Layout
SHIP_LAYOUT = [["+", 0, 0, 0], ["A", 0, 1, 0], ["H", 0, 2, 1], [
    "=", -1, 2, 0], ["=", 1, 2, 0], ["_", -2, 2, 0], ["_", 2, 2, 0], ['*', 0, 3, 2]]
SHIP_COLORS = [BLUE, WHITE, RED]

# ASTEROID ATTRIBUTES - - - - - - - - - - - - - - - -


def asteroid_color():
    return random.choice([BROWN, RED, ORANGE, BREEN])


ASTEROID_TYPES_LIST = [
    {
        "name": "SML",
        "text": "°",
        "damage": 1,
        "health": 1,
        "points": 1,
        "movewait": lambda: random.choice([2, 3, 4]),
        "color": asteroid_color()
    },
    {
        "name": "MED",
        "text": "*",
        "damage": 2,
        "health": 1,
        "points": 1,
        'movewait': lambda: random.choice([3, 4]),
        "color": asteroid_color()
    },
    {
        "name": "LRG",
        "text": "@",
        "damage": 2,
        "health": 2,
        "points": 2,
        'movewait': lambda: random.choice([4, 5]),
        "color": asteroid_color()
    },
    {
        "name": "SML-xmove",
        "text": "¤",
        "damage": 2,
        "health": 1,
        "points": 3,
        'movewait': lambda: random.choice([1, 2]),
        "color": asteroid_color()
    },
    {
        "name": "HUGE",
        "text": "@",
        "damage": 4,
        "health": 3,
        "points": 4,
        'movewait': lambda: random.choice([4, 5, 6]),
        "color": asteroid_color()
    },
    {
        "name": "GIANT",
        "text": "▣",
        "damage": 6,
        "health": 5,
        "points": 6,
        'movewait': lambda: random.choice([5, 6]),
        "color": asteroid_color()
    }]


hgtx = ASTEROID_TYPES_LIST[4]["text"]
HUGE_ASTEROID_LAYOUT = [[hgtx, 0, 0, 0], [hgtx, 1, 0, 0], [hgtx, -1, 0, 0], [hgtx, 0, 1, 0], [hgtx, 0, -1, 0],
                        [hgtx, -1, -1, 0], [hgtx, 1, -1, 0],
                        [hgtx, -1, 1, 0], [hgtx, 1, 1, 0],
                        [hgtx, -2, 0, 0], [hgtx, 0, -2, 0], [hgtx, 2, 0, 0], [hgtx, 0, 2, 0]]

gitx = ASTEROID_TYPES_LIST[5]["text"]
GIANT_ASTEROID_LAYOUT = [[gitx, 0, 0, 0], [gitx, 1, 0, 0], [gitx, -1, 0, 0], [gitx, 0, 1, 0], [gitx, 0, -1, 0],
                         [gitx, -1, -1, 0], [gitx, 1, -1, 0],
                         [gitx, -1, 1, 0], [gitx, 1, 1, 0],
                         [gitx, -2, 0, 0], [gitx, 0, -2, 0],
                         [gitx, 2, 0, 0], [gitx, 0, 2, 0],

                         [gitx, -2, -2, 0], [gitx, 2, -2, 0],
                         [gitx, -2, 2, 0], [gitx, 2, 2, 0],

                         [gitx, -2, -1, 0], [gitx, -2, 1, 0],
                         [gitx, 2, 1, 0], [gitx, 2, -1, 0],
                         [gitx, -1, 2, 0], [gitx, 1, 2, 0],
                         [gitx, 1, -2, 0], [gitx, -1, -2, 0],

                         [gitx, -3, -1, 0], [gitx, -3, 1, 0],
                         [gitx, 3, 1, 0], [gitx, 3, -1, 0],
                         [gitx, -1, 3, 0], [gitx, 1, 3, 0],
                         [gitx, 1, -3, 0], [gitx, -1, -3, 0],
                         [gitx, 0, 3, 0], [gitx, 0, -3, 0],
                         [gitx, -3, 0, 0], [gitx, 3, 0, 0]
                         ]
