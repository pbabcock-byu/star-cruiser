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
        self._wait_spawn = 0
        self._game_stage = ""
        self._game_stage_number = 0
        self._stage_seconds = 0
        self._randomocity = 0
        self._current_stage = -1
        self._paused = False
        self._last_spawn_list = []
        self._game_stages = [
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
                "randomocity": 5,
                "stagedisplay": "none"
            },
            {
                "delaystart": 0,
                "duration": 10,
                "enemytypes": ["asteroid-medium"],
                "waitspawn": 0.7,
                "randomocity": 5,
                "stagedisplay": "none"
            },
            {
                "delaystart": 0,
                "duration": 10,
                "enemytypes": ["asteroid-large", "asteroid-large"],
                "waitspawn": 1,
                "randomocity": 8,
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
                "randomocity": 2,
                "stagedisplay": "none"
            },
            {
                "delaystart": 5,
                "duration": 5,
                "enemytypes": ["asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large",
                               "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-small-xmove"],
                "waitspawn": 2,
                "randomocity": 0,
                "stagedisplay": "none"
            },
            {
                "delaystart": 6,
                "duration": 6,
                "enemytypes": ["asteroid-small", "asteroid-small", "asteroid-small"],
                "waitspawn": 0.2,
                "randomocity": 2,
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
                "randomocity": 10,
                "stagedisplay": "none"
            },
            {
                "delaystart": 4,
                "duration": 12,
                "enemytypes": ["asteroid-huge"],
                "waitspawn": 1,
                "randomocity": 4,
                "stagedisplay": "none"
            },
            {
                "delaystart": 5,
                "duration": 10,
                "enemytypes": ["asteroid-giant"],
                "waitspawn": 2,
                "randomocity": 5,
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
                "randomocity": 10,
                "stagedisplay": "none"
            },
            {
                "delaystart": 1,
                "duration": 4,
                "enemytypes": ["asteroid-huge"],
                "waitspawn": 1,
                "randomocity": 4,
                "stagedisplay": "none"
            },
            {
                "delaystart": 2,
                "duration": 4,
                "enemytypes": ["asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large",
                               "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large",
                               "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large", "asteroid-small-xmove"],
                "waitspawn": 3.5,
                "randomocity": 0,
                "stagedisplay": "none"
            },
            {
                "delaystart": 2,
                "duration": 10,
                "enemytypes": ["asteroid-small", "asteroid-small", "asteroid-small"],
                "waitspawn": 0.4,
                "randomocity": 2,
                "stagedisplay": "none"
            },
            {
                "delaystart": 5,
                "duration": 10,
                "enemytypes": ["asteroid-giant", "asteroid-large", "asteroid-large", "asteroid-large"],
                "waitspawn": 2,
                "randomocity": 5,
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
                "randomocity": 5,
                "stagedisplay": "none"
            },
            {
                "delaystart": 2,
                "duration": 5,
                "enemytypes": ["asteroid-small", "asteroid-small", "asteroid-small", "asteroid-small", "asteroid-small", "asteroid-small"],
                "waitspawn": 0.1,
                "randomocity": 2,
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
                "randomocity": 2,
                "stagedisplay": "none"
            },
            {
                "delaystart": 1,
                "duration": 1,
                "enemytypes": ["asteroid-large", "asteroid-large", "asteroid-large", "asteroid-large"],
                "waitspawn": 0.2,
                "randomocity": 0,
                "stagedisplay": "none"
            },
            {
                "delaystart": 1,
                "duration": 3,
                "enemytypes": ["asteroid-giant", "asteroid-giant", "asteroid-giant", "asteroid-giant"],
                "waitspawn": 2,
                "randomocity": 0,
                "stagedisplay": "none"
            },
            {
                "delaystart": 1,
                "duration": 3,
                "enemytypes": ["asteroid-huge", "asteroid-huge", "asteroid-huge"],
                "waitspawn": 2,
                "randomocity": 0,
                "stagedisplay": "none"
            },
            {
                "delaystart": 1,
                "duration": 3,
                "enemytypes": ["asteroid-medium"],
                "waitspawn": 0.7,
                "randomocity": 5,
                "stagedisplay": "none"
            },
            {
                "delaystart": 0,
                "duration": 3,
                "stagedisplay": "You beat the game! (So far)"
            },
            {
                "delaystart": 0,
                "duration": 50,
                "enemytypes": ["asteroid-small-xmove", "asteroid-giant"],
                "waitspawn": 0.7,
                "randomocity": 5,
                "stagedisplay": "none"
            },
        ]

    def set_paused(self, paused):
        self._paused = paused

    def execute(self, cast, script):
        """Executes the handle enemy creation action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        if not self._is_game_over:
            if self._paused == False:
                # handle action
                self._handle_stage_progression(cast)
            else:
                cast.remove_actors("stage messages")

        else:
            pass

    def _create_enemy_of_type(self, cast, enemy_type):
        """ Blah
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        enemy = 0
        if enemy_type == "asteroid-small":
            asteroid = self._make_asteriod(cast, 0)
            cast.add_actor("asteroids", asteroid)
            enemy = asteroid

        if enemy_type == "asteroid-medium":
            asteroid = self._make_asteriod(cast, 1)
            cast.add_actor("asteroids", asteroid)
            enemy = asteroid

        if enemy_type == "asteroid-large":
            asteroid = self._make_asteriod(cast, 2)
            cast.add_actor("asteroids", asteroid)
            enemy = asteroid

        if enemy_type == "asteroid-small-xmove":
            asteroid = self._make_asteriod(cast, 3)
            cast.add_actor("asteroids", asteroid)
            enemy = asteroid

        if enemy_type == "asteroid-huge":
            asteroid = self._make_asteriod(cast, 4)
            cast.add_actor("asteroids", asteroid)
            enemy = asteroid

        if enemy_type == "asteroid-giant":
            asteroid = self._make_asteriod(cast, 5)
            cast.add_actor("asteroids", asteroid)
            enemy = asteroid

        return enemy

    def _handle_stage_progression(self, cast):
        """ Blah
        Args:
            cast (Cast): The cast of Actors in the game.
        """

        # update stage info if it's a new stage
        if self._current_stage != self._game_stages[self._game_stage_number]:
            self._current_stage = self._game_stages[self._game_stage_number]
            # reset stage timer
            self._stage_seconds = 0

        # if this is not a "stage display" stage
        if self._current_stage["stagedisplay"] == "none":

            # increment game timer
            self._stage_seconds += 1 / constants.FRAME_RATE
            # wait the delay time
            if self._stage_seconds > self._current_stage["delaystart"]:

                # create enemies every time the wait spawn is zero
                # if the wait spawn timer is over
                if self._wait_spawn <= 0:
                    # reset to wait again
                    self._wait_spawn = self._current_stage["waitspawn"]
                    # set up randomocity for spawn y positions
                    self._randomocity = self._current_stage["randomocity"]
                    # for every enemy in the enemytypes list for this stage
                    self._last_spawn_list = []
                    for enemytype in self._current_stage["enemytypes"]:
                        # create an enemy
                        enemy = self._create_enemy_of_type(cast, enemytype)
                        if enemy != 0:
                            self._last_spawn_list.append(enemy)
                else:
                    # count down timer in seconds
                    self._wait_spawn -= 1 / constants.FRAME_RATE

            # update _game_stage
            if self._game_stage != self._current_stage["stagedisplay"]:
                self._game_stage = self._current_stage["stagedisplay"]
                # delete the game stage display message
                cast.remove_actors("stage messages")
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

                # increment stage timer
                self._stage_seconds += 1 / constants.FRAME_RATE
                # after delaystart
                if self._stage_seconds > self._current_stage["delaystart"]:
                    # display stage message
                    if self._game_stage != self._current_stage["stagedisplay"]:
                        self._game_stage = self._current_stage["stagedisplay"]
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
                        cast.add_actor("stage messages", message)
        # if we are past the duration of this stage
        if self._stage_seconds > self._current_stage["delaystart"] + self._current_stage["duration"]:
            # reset stage timer
            self._stage_seconds = 0
            # move to next stage
            self._game_stage_number += 1

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
        tries = 10
        free = True

        x = random.randint(1, constants.COLUMNS - 1)
        y = random.randint(-5 - self._randomocity, -5)
        position = Point(x, y)

        while not free:
            # reset
            free = True
            if tries > 0:
                # try n times to find a free position
                tries -= 1
                # if position is not free continue the loop
                for enemy in self._last_spawn_list:
                    if position.equals(enemy.get_position()):
                        free = False
            if free == False:
                # pick a new spot to try
                x = random.randint(1, constants.COLUMNS - 1)
                y = random.randint(-5 - self._randomocity, -5)
                position = Point(x, y)

        position = position.scale(constants.CELL_SIZE)
        velocity = Point(0, constants.CELL_SIZE)
        asteroid = Asteroid(cast)
        asteroid.set_color(constants.BROWN)
        asteroid.set_position(position)
        asteroid.set_velocity(velocity)
        asteroid.set_up_type(asteroidtype)
        # returns it so we can add it to the cast "asteriods" group
        return asteroid
