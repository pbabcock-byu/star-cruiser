import constants
import random

from game.casting.actor import Actor
from game.scripting.action import Action
from game.shared.point import Point
from game.casting.asteroid import Asteroid


class HandleEnemyCreation(Action):
    """
    An update action that handles the creations of enemies and game difficulty.

    The responsibility of HandleEnemyCreation is to handle the creation of enemies at the top of the screen
    and to increase the game difficulty over time by creating more enemies.

    Attributes:
        _is_game_over (boolean): Whether or not the game is over.
        _game_seconds (double): Keeps track of how many seconds the game has been running
    """

    def __init__(self):
        """Constructs a new HandleEnemyCreation."""
        self._is_game_over = False
        self._game_seconds = 0
        self._wait_spawn = 0
        self._game_stages = [
            {
                "starttime": 4,
                "endtime": 18,
                "enemytypes": ["asteroid-small"],
                "waitspawn": 3,
                "randomocity": 50,
                "stagename": "first"
            },
            {
                "starttime": 20,
                "endtime": 35,
                "enemytypes": ["asteroid-medium"],
                "waitspawn": 4,
                "randomocity": 50,
                "stagename": "second"
            },
            {
                "starttime": 40,
                "endtime": 55,
                "enemytypes": ["asteroid-large"],
                "waitspawn": 5,
                "randomocity": 50,
                "stagename": "second"
            }
        ]

    def execute(self, cast, script):
        """Executes the handle enemy creation action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if not self._is_game_over:
            # increment game timer
            self._game_seconds += 1 / constants.FRAME_RATE
            # handle action
            self._handle_stage_progression(cast)
        else:
            pass

    def _create_enemy_of_type(self, cast, enemy_type):
        """ Blah
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        if enemy_type == "asteroid-small":
            asteroid = self._make_asteriod(cast, 0)
            cast.add_actor("asteroids", asteroid)

        if enemy_type == "asteroid-medium":
            asteroid = self._make_asteriod(cast, 1)
            cast.add_actor("asteroids", asteroid)

        if enemy_type == "asteroid-large":
            asteroid = self._make_asteriod(cast, 2)
            cast.add_actor("asteroids", asteroid)

    def _handle_stage_progression(self, cast):
        """ Blah
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        # reset
        current_stage = "no stage"

        # determine stage
        for stage in self._game_stages:
            # check to see if the _game_seconds is within this stages start/end time
            if self._game_seconds >= stage["starttime"] and self._game_seconds <= stage["endtime"]:
                # if so, it is the current stage
                current_stage = stage

        if current_stage != "no stage":
            # if the wait spawn timer is over
            if self._wait_spawn <= 0:
                # reset to wait again
                self._wait_spawn = current_stage["waitspawn"]
                # for every enemy in the enemytypes list for this stage
                for enemytype in current_stage["enemytypes"]:
                    # create an enemy
                    self._create_enemy_of_type(cast, enemytype)
                    print(enemytype)
            else:
                # count down timer in seconds
                self._wait_spawn -= 1 / constants.FRAME_RATE

    def _make_asteriod(self, cast, asteroidtype):
        """Creates a new asteroid at the top of the screen

        Returns:
            reference to the new meteoroid
        """
        # define
        asteroid_types = [["SML", "`"], ["MED", "*"], ["LRG", "@"]]

        x = random.randint(1, constants.COLUMNS - 1)
        y = random.randint(-5, -3)

        position = Point(x, y)
        position = position.scale(constants.CELL_SIZE)

        asteroid = Asteroid(cast)
        type = asteroid_types[asteroidtype]
        asteroid.set_type(type[0])
        asteroid.set_text(type[1])
        asteroid.set_color(constants.BROWN)
        asteroid.set_position(position)
        asteroid.set_velocity(Point(0, constants.CELL_SIZE))
        # returns it so we can add it to the cast "asteriods" group
        return asteroid
