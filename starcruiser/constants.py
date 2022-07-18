from game.shared.color import Color
import random

# Game name
GAME_TITLE = "STAR CRUISER 5000"

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
PURPLE = Color(255, 0, 150)
BREEN = Color(245, 120, 22)

# Ship shields and damage
MAXSHIELDS = 40
STARTSHEILDS = 20
LOWSHIELDS = 5

HIGHSCORE_FILE = "starcruiser/game/data/highscores.txt"

# SOUNDS - - - - - - -
SOUNDS_FOLDER = "starcruiser/game/sounds/"
# ship
SHIP_FIRE_SOUND = f"{SOUNDS_FOLDER}lasr.mp3"
SHIP_HIT_SOUND = f"{SOUNDS_FOLDER}ship-hit.mp3"
SHIP_EXPLOSION_SOUND = f"{SOUNDS_FOLDER}ship-exp.mp3"
# Asteroids
ASTEROIDS_HIT_SOUND = f"{SOUNDS_FOLDER}ast-hit.mp3"
ASTEROIDS_HIT_SML_SOUND = f"{SOUNDS_FOLDER}ast-hit-sml.mp3"
ASTEROIDS_HIT_LRG_SOUND = f"{SOUNDS_FOLDER}ast-hit-lrg.mp3"
ASTEROIDS_HIT_GIANT_SOUND = f"{SOUNDS_FOLDER}ast-hit-giant.mp3"
ASTEROIDS_HUGE_EXP_SOUND = f"{SOUNDS_FOLDER}ast-hit-huge-exp.mp3"
ASTEROIDS_GIANT_EXP_SOUND = f"{SOUNDS_FOLDER}ast-hit-giant-exp.mp3"
# menu
MENU_SELECT_SOUND = f"{SOUNDS_FOLDER}menu-selct.mp3"
MENU_START_SOUND = f"{SOUNDS_FOLDER}menu-start.mp3"
ENTER_INITIAL_SOUND = f"{SOUNDS_FOLDER}entr-initial.mp3"
NEW_HIGHSCORE_SOUND = f"{SOUNDS_FOLDER}new-hscore.mp3"
# game
GAMEOVER_SOUND = f"{SOUNDS_FOLDER}gm-over.mp3"
NEW_STAGE_SOUND = f"{SOUNDS_FOLDER}new-stge.mp3"
UPGRADE_SOUND = f"{SOUNDS_FOLDER}upgrd.mp3"
LOW_SHIELDS_WARNING_SOUND = f"{SOUNDS_FOLDER}shields-low.mp3"
# music
MUSIC_MENU_SOUND = f"{SOUNDS_FOLDER}music-menu.mp3"
MUSIC_GAMEPLAY_SOUND = f"{SOUNDS_FOLDER}music-play.mp3"


# UPGRADES  LIST [points required (int), upgrade type (string)]
UPGRADE_LIST = [[100,"shield"],[200,"gun-rapid"], [300,"shield"], [400,"gun-rapid"], [500,"shield"]]

GUN_UPGRADE_MAX_SHOTS = {
                            "rapid": 50
                        }


# SHIP LAYOUT [text character, x, y, color reference]
SHIP_LAYOUT = [["+", 0, 0, 0], ["A", 0, 1, 0], ["H", 0, 2, 1], [
    "=", -1, 2, 0], ["=", 1, 2, 0], ["_", -2, 2, 0], ["_", 2, 2, 0], ['*', 0, 3, 2]]
SHIP_COLORS = [BLUE, WHITE, RED]

# ASTEROID ATTRIBUTES - - - - - - - - - - - - - - - -

"""
   ASTEROID_TYPES_LIST (object values):
        name (string): "SML", "MED", "LRG", "SML-xmove", "GIANT", "HUGE", used to look up asteroid attributes in the ASTEROID_TYPES_LIST (constants)
        text (string): used to display the asteroid, ex: medium asteroid = "*" large asteroid = "@"
        damage (int): how much damage the asteroid does to the player
        health (int): how many shots it takes to destroy this asteroid
        points (int): how many points the asteroid is worth if it's destroyed
        movewait (int): waits this many frames between moving (used to make asteroids move slower)
        color (Color): color of the asteroid
        hit_sound ("string"): reference to sound to play when this asteroid gets shot by a laser
        exp_sound ("string"): reference to sound to play when this asteroid gets blown up
"""

ASTEROID_TYPES_LIST = [
    {
        "name": "SML",
        "text": "°",
        "damage": 1,
        "health": 1,
        "points": 1,
        "movewait": lambda: random.choice([2, 3, 4]),
        "color": YELLOW,
        "hit-sound": "",
        "destroy-snd": "ast-hit"
    },
    {
        "name": "MED",
        "text": "*",
        "damage": 2,
        "health": 1,
        "points": 1,
        'movewait': lambda: random.choice([3, 4]),
        "color": ORANGE,
        "hit-sound": "",
        "destroy-snd": "ast-hit-sml"
    },
    {
        "name": "LRG",
        "text": "@",
        "damage": 2,
        "health": 2,
        "points": 2,
        'movewait': lambda: random.choice([4, 5]),
        "color": BROWN,
        "hit-sound": "ast-hit",
        "destroy-snd": "ast-hit-lrg"
    },
    {
        "name": "SML-xmove",
        "text": "¤",
        "damage": 2,
        "health": 1,
        "points": 3,
        'movewait': lambda: random.choice([2, 3]),
        "color": PURPLE,
        "hit-sound": "",
        "destroy-snd": "ast-hit-lrg"
    },
    {
        "name": "HUGE",
        "text": "@",
        "damage": 4,
        "health": 3,
        "points": 4,
        'movewait': lambda: random.choice([4, 5, 6]),
        "color": RED,
        "hit-sound": "ast-hit-giant",
        "destroy-snd": "ast-exp-huge"
    },
    {
        "name": "GIANT",
        "text": "★",
        "damage": 6,
        "health": 5,
        "points": 6,
        'movewait': lambda: random.choice([5, 6]),
        "color": BROWN,
        "hit-sound": "ast-hit-giant",
        "destroy-snd": "ast-exp-giant"
    }]

# ASTEROID LAYOUTS [text character, x, y, color reference]
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




"""Notes:
GAME_STAGES controls the difficulty progression of the game. 
Each "stage" lasts a certain amount of time, and creates certain enemy types at a certain frequency.
Some stages are "display stages", meaning, they don't spawn enemies, they just display a message for a certain amount of time. Ex: "Stage One"

Enemy types available:
    asteroid-small
    asteroid-medium
    asteroid-large
    asteroid-small-xmove
    asteroid-huge
    asteroid-giant

GAME STAGES {
                delaystart (float): time in seconds to wait before stage begins
                duration (float): time in seconds this stage will run for
                enemytypes (list of strings): references to enemy types that will be created during this stage. One of each on the list is created when waitspawn timer is reached.
                waitspawn (float): time in seconds to wait between enemy spawns
                y_randomness (int): how many cells upwards (y direction) enemies might randomly spawn to give variety. If zero, enemies spawn in a straight row.
                stagedisplay (string): "none" or a display message  (Ex: "Stage One")
             }
""" 
GAME_STAGES = [
            {
                "delaystart": 1,
                "duration": 2,
                "stagedisplay": "Stage One"
            },
            {
                "delaystart": 0,
                "duration": 10,
                "enemytypes": ["asteroid-small"],
                "waitspawn": 0.8,
                "y_randomness": 5,
                "stagedisplay": "none"
            },
            {
                "delaystart": 0,
                "duration": 10,
                "enemytypes": ["asteroid-medium"],
                "waitspawn": 0.7,
                "y_randomness": 5,
                "stagedisplay": "none"
            },
            {
                "delaystart": 0,
                "duration": 10,
                "enemytypes": ["asteroid-large", "asteroid-large"],
                "waitspawn": 1,
                "y_randomness": 8,
                "stagedisplay": "none"
            },
            {
                "delaystart": 1,
                "duration": 2,
                "stagedisplay": "Stage Two"
            },
            {
                "delaystart": 0,
                "duration": 6,
                "enemytypes": ["asteroid-small-xmove", "asteroid-small"],
                "waitspawn": 1,
                "y_randomness": 2,
                "stagedisplay": "none"
            },
            {
                "delaystart": 5,
                "duration": 5,
                "enemytypes": ["asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large",
                               "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-small-xmove"],
                "waitspawn": 2,
                "y_randomness": 0,
                "stagedisplay": "none"
            },
            {
                "delaystart": 6,
                "duration": 6,
                "enemytypes": ["asteroid-small", "asteroid-small", "asteroid-small"],
                "waitspawn": 0.2,
                "y_randomness": 2,
                "stagedisplay": "none"
            },
            {
                "delaystart": 1,
                "duration": 2,
                "stagedisplay": "Stage Three"
            },
            {
                "delaystart": 0,
                "duration": 6,
                "enemytypes": ["asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-small-xmove"],
                "waitspawn": 1,
                "y_randomness": 10,
                "stagedisplay": "none"
            },
            {
                "delaystart": 4,
                "duration": 12,
                "enemytypes": ["asteroid-huge"],
                "waitspawn": 1,
                "y_randomness": 4,
                "stagedisplay": "none"
            },
            {
                "delaystart": 5,
                "duration": 10,
                "enemytypes": ["asteroid-giant"],
                "waitspawn": 2,
                "y_randomness": 5,
                "stagedisplay": "none"
            },
            {
                "delaystart": 1,
                "duration": 2,
                "stagedisplay": "Stage Four"
            },
            {
                "delaystart": 0,
                "duration": 10,
                "enemytypes": ["asteroid-large", "asteroid-large", "asteroid-small-xmove", "asteroid-huge", "asteroid-small-xmove"],
                "waitspawn": 1.3,
                "y_randomness": 10,
                "stagedisplay": "none"
            },
            {
                "delaystart": 1,
                "duration": 4,
                "enemytypes": ["asteroid-huge"],
                "waitspawn": 1,
                "y_randomness": 4,
                "stagedisplay": "none"
            },
            {
                "delaystart": 2,
                "duration": 4,
                "enemytypes": ["asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large",
                               "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large",
                               "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-small-xmove"],
                "waitspawn": 3.5,
                "y_randomness": 0,
                "stagedisplay": "none"
            },
            {
                "delaystart": 2,
                "duration": 10,
                "enemytypes": ["asteroid-small", "asteroid-small", "asteroid-small"],
                "waitspawn": 0.4,
                "y_randomness": 2,
                "stagedisplay": "none"
            },
            {
                "delaystart": 5,
                "duration": 10,
                "enemytypes": ["asteroid-giant", "asteroid-large", "asteroid-large", "asteroid-large"],
                "waitspawn": 2,
                "y_randomness": 5,
                "stagedisplay": "none"
            },
            {
                "delaystart": 1,
                "duration": 2,
                "stagedisplay": "Stage Five"
            },
            {
                "delaystart": 0,
                "duration": 25,
                "enemytypes": ["asteroid-giant", "asteroid-giant", "asteroid-large", "asteroid-small", "asteroid-medium",
                               "asteroid-small-xmove", "asteroid-small-xmove", "asteroid-small-xmove", "asteroid-small-xmove",
                               "asteroid-small-xmove", "asteroid-small-xmove", "asteroid-small-xmove", "asteroid-small-xmove"],
                "waitspawn": 5,
                "y_randomness": 5,
                "stagedisplay": "none"
            },
            {
                "delaystart": 2,
                "duration": 5,
                "enemytypes": ["asteroid-small", "asteroid-small", "asteroid-small", "asteroid-small", "asteroid-small", "asteroid-small"],
                "waitspawn": 0.1,
                "y_randomness": 2,
                "stagedisplay": "none"
            },
            {
                "delaystart": 1,
                "duration": 2,
                "stagedisplay": "Stage Six"
            },
            {
                "delaystart": 1,
                "duration": 1,
                "enemytypes": ["asteroid-small-xmove"],
                "waitspawn": 0.2,
                "y_randomness": 2,
                "stagedisplay": "none"
            },
            {
                "delaystart": 1,
                "duration": 1,
                "enemytypes": ["asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large"],
                "waitspawn": 0.2,
                "y_randomness": 0,
                "stagedisplay": "none"
            },
            {
                "delaystart": 1,
                "duration": 3,
                "enemytypes": ["asteroid-giant", "asteroid-giant", "asteroid-giant", "asteroid-giant"],
                "waitspawn": 2,
                "y_randomness": 0,
                "stagedisplay": "none"
            },
            {
                "delaystart": 1,
                "duration": 3,
                "enemytypes": ["asteroid-huge", "asteroid-huge", "asteroid-huge"],
                "waitspawn": 2,
                "y_randomness": 0,
                "stagedisplay": "none"
            },
            {
                "delaystart": 1,
                "duration": 3,
                "enemytypes": ["asteroid-medium"],
                "waitspawn": 0.7,
                "y_randomness": 5,
                "stagedisplay": "none"
            },
            {
                "delaystart": 1,
                "duration": 2,
                "stagedisplay": "Stage Seven"
            },
            {
                "delaystart": 0,
                "duration": 10,
                "enemytypes": ["asteroid-small"],
                "waitspawn": 0.4,
                "y_randomness": 5,
                "stagedisplay": "none"
            },
            {
                "delaystart": 0,
                "duration": 10,
                "enemytypes": ["asteroid-medium"],
                "waitspawn": 0.4,
                "y_randomness": 5,
                "stagedisplay": "none"
            },
            {
                "delaystart": 0,
                "duration": 10,
                "enemytypes": ["asteroid-large", "asteroid-large"],
                "waitspawn": 0.5,
                "y_randomness": 8,
                "stagedisplay": "none"
            },
            {
                "delaystart": 0,
                "duration": 1,
                "enemytypes": ["asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large"],
                "waitspawn": 0.3,
                "y_randomness": 0,
                "stagedisplay": "none"
            },
            {
                "delaystart": 0,
                "duration": 1,
                "enemytypes": ["asteroid-medium", "asteroid-medium", "asteroid-medium", "asteroid-medium", "asteroid-medium", "asteroid-medium"],
                "waitspawn": 0.2,
                "y_randomness": 0,
                "stagedisplay": "none"
            },
            {
                "delaystart": 0,
                "duration": 1,
                "enemytypes": ["asteroid-small", "asteroid-small", "asteroid-small", "asteroid-small", "asteroid-small", "asteroid-small"],
                "waitspawn": 0.2,
                "y_randomness": 0,
                "stagedisplay": "none"
            },
            {
                "delaystart": 0,
                "duration": 1,
                "enemytypes": ["asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large"],
                "waitspawn": 0.3,
                "y_randomness": 0,
                "stagedisplay": "none"
            },
            {
                "delaystart": 0,
                "duration": 1,
                "enemytypes": ["asteroid-huge", "asteroid-huge", "asteroid-huge", "asteroid-huge", "asteroid-huge", "asteroid-huge"],
                "waitspawn": 0.5,
                "y_randomness": 0,
                "stagedisplay": "none"
            },
            {
                "delaystart": 0,
                "duration": 3,
                "stagedisplay": "You beat the game! (So far)"
            },
            {
                "delaystart": 0,
                "duration": 100,
                "enemytypes": ["asteroid-small-xmove", "asteroid-giant"],
                "waitspawn": 0.8,
                "y_randomness": 5,
                "stagedisplay": "none"
            },
        ]