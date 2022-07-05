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
        self._game_stage = ""
        self._randomocity = 0
        self._game_stages = [
            {
                "starttime": 1,
                "endtime": 2,
                "stagedisplay": "Stage One"
            },
            {
                "starttime": 3,
                "endtime": 18,
                "enemytypes": ["asteroid-giant"],
                "waitspawn": 3,
                "randomocity": 5,
                "stagedisplay": "none"
            },
            {
                "starttime": 20,
                "endtime": 35,
                "enemytypes": ["asteroid-medium"],
                "waitspawn": 2,
                "randomocity": 5,
                "stagedisplay": "none"
            },
            {
                "starttime": 37,
                "endtime": 55,
                "enemytypes": ["asteroid-large", "asteroid-large"],
                "waitspawn": 5,
                "randomocity": 8,
                "stagedisplay": "none"
            },
            {
                "starttime": 56,
                "endtime": 57,
                "stagedisplay": "Stage Two"
            },
            {
                "starttime": 58,
                "endtime": 64,
                "enemytypes": ["asteroid-small-xmove", "asteroid-small"],
                "waitspawn": 2,
                "randomocity": 2,
                "stagedisplay": "none"
            },
            {
                "starttime": 72,
                "endtime": 76,
                "enemytypes": ["asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large"],
                "waitspawn": 2,
                "randomocity": 0,
                "stagedisplay": "none"
            },
            {
                "starttime": 90,
                "endtime": 95,
                "enemytypes": ["asteroid-small", "asteroid-small", "asteroid-small"],
                "waitspawn": 0.2,
                "randomocity": 2,
                "stagedisplay": "none"
            },
            {
                "starttime": 96,
                "endtime": 97,
                "stagedisplay": "Stage Three"
            },
            {
                "starttime": 98,
                "endtime": 103,
                "enemytypes": ["asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large"],
                "waitspawn": 1,
                "randomocity": 10,
                "stagedisplay": "none"
            },
            {
                "starttime": 108,
                "endtime": 120,
                "enemytypes": ["asteroid-huge"],
                "waitspawn": 1,
                "randomocity": 4,
                "stagedisplay": "none"
            },
            {
                "starttime": 128,
                "endtime": 138,
                "enemytypes": ["asteroid-giant"],
                "waitspawn": 2,
                "randomocity": 5,
                "stagedisplay": "none"
            },
            {
                "starttime": 139,
                "endtime": 140,
                "stagedisplay": "YOU BEAT THE GAME! (so far)"
            },
        ]

    def execute(self, cast, script):
        """Executes the handle enemy creation action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if not self._is_game_over:
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

        if enemy_type == "asteroid-small-xmove":
            asteroid = self._make_asteriod(cast, 3)
            cast.add_actor("asteroids", asteroid)

        if enemy_type == "asteroid-huge":
            asteroid = self._make_asteriod(cast, 4)
            cast.add_actor("asteroids", asteroid)

        if enemy_type == "asteroid-giant":
            asteroid = self._make_asteriod(cast, 5)
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
            # if this is not a "stage display" stage
            if current_stage["stagedisplay"] == "none":

                # increment game timer
                self._game_seconds += 1 / constants.FRAME_RATE

                # if the wait spawn timer is over
                if self._wait_spawn <= 0:
                    # reset to wait again
                    self._wait_spawn = current_stage["waitspawn"]
                    # set up randomocity for spawn y positions
                    self._randomocity = current_stage["randomocity"]
                    # for every enemy in the enemytypes list for this stage
                    for enemytype in current_stage["enemytypes"]:
                        # create an enemy
                        self._create_enemy_of_type(cast, enemytype)
                        print(enemytype)
                else:
                    # count down timer in seconds
                    self._wait_spawn -= 1 / constants.FRAME_RATE

                # update _game_stage
                if self._game_stage != current_stage["stagedisplay"]:
                    self._game_stage = current_stage["stagedisplay"]
                    # delete the game stage display message
                    cast.remove_actor(
                        "messages", cast.get_first_actor("messages"))
                    # reset other display color to show
                    display_elements = cast.get_actors("scores")
                    for display in display_elements:
                        display.set_color(constants.WHITE)
                    display_elements = cast.get_actors("shields")
                    for display in display_elements:
                        display.set_color(constants.WHITE)

            else:
                # reset
                self._wait_spawn = 0

                # update _game_stage
                if self._no_enemies_exist(cast):
                    # increment game timer
                    self._game_seconds += 1 / constants.FRAME_RATE

                    if self._game_stage != current_stage["stagedisplay"]:
                        self._game_stage = current_stage["stagedisplay"]
                        # hide current display elements
                        display_elements = cast.get_actors("scores")
                        for display in display_elements:
                            display.set_color(constants.BLACK)
                        display_elements = cast.get_actors("shields")
                        for display in display_elements:
                            display.set_color(constants.BLACK)
                        # display game stage name as a message on the screen
                        x = int(constants.MAX_X / 2)
                        y = int(constants.MAX_Y / 2)
                        position = Point(x, y)
                        message = Actor()
                        message.set_text(self._game_stage)
                        message.set_position(position)
                        cast.add_actor("messages", message)
        else:
            # increment game timer
            self._game_seconds += 1 / constants.FRAME_RATE

    def _no_enemies_exist(self, cast):
        """Determines whether there are no enemies still on screen
        Returns:
            true of false
        """
        # set default
        result = True
        # check enemy types - - - - -
        # if any asteroids exist
        if len(cast.get_actors("asteroids")) > 0:
            result = False
        # return final result
        return result

    def _make_asteriod(self, cast, asteroidtype):
        """Creates a new asteroid at the top of the screen

        Returns:
            reference to the new meteoroid
        """

        x = random.randint(1, constants.COLUMNS - 1)
        y = random.randint(-5 - self._randomocity, -4)

        position = Point(x, y)
        position = position.scale(constants.CELL_SIZE)
        velocity = Point(0, constants.CELL_SIZE)
        if asteroidtype == 3:
            velocity = Point(random.choice(
                [-constants.CELL_SIZE, constants.CELL_SIZE]), constants.CELL_SIZE)

        type = constants.ASTEROID_TYPES[asteroidtype]
        asteroid = Asteroid(cast, type[0])
        asteroid.set_text(type[1])
        asteroid.set_color(constants.BROWN)
        asteroid.set_position(position)
        asteroid.set_velocity(velocity)
        asteroid.set_up_parts()
        # returns it so we can add it to the cast "asteriods" group
        return asteroid
