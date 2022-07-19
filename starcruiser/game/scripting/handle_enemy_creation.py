import constants
import random

from game.casting.actor import Actor
from game.scripting.action import Action
from game.shared.point import Point
from game.casting.asteroid import Asteroid
from game.casting.ufo import Ufo

class HandleEnemyCreation(Action):
    """
    An update action that handles the creations of enemies and game difficulty.

    The responsibility of HandleEnemyCreation is to handle the creation of enemies at the top of the screen
    and to increase the game difficulty over time by creating more enemies.

    Attributes:
        is_game_over (boolean): Whether or not the game is over.
        wait_spawn (int): Used to wait a number of frames between spawning enemies
        game_stage (string): Used to display and keep track of the current stage display value
        game_stage_number (int): Used when updating the current stage
        game_stage_number (int): Used to keep track of the current stage
        stage_seconds (float): increments in seconds how long each stage will run
        y_randomness (int): controls the randomness of the y position (vertical) that enemies will spawn, if zero enemies spawn in a straight row
        paused (bool): used to pause the stage succession by stopping the stage_seconds timer
        last_spawn_list (list): remembers recent enemy positions to avoid spawning a new one at the same x/y position

        game_stages (object): stores the information for each stage (length, enemy types, rapidness of spawn, stagename, etc.)
    """

    def __init__(self, audio_service):
        """Constructs a new HandleEnemyCreation."""
        self._audio_service = audio_service

        self._is_game_over = False
        self._wait_spawn = 0
        self._game_stage = ""
        self._game_stage_number = 0
        self._current_stage = -1
        self._stage_seconds = 0
        self._y_randomness = 0
        self._paused = False
        self._last_spawn_list = []
        # get game stages information
        self._game_stages = constants.GAME_STAGES

    def set_paused(self, paused):
        self._paused = paused

    def execute(self, cast, script):
        """Executes the handle enemy creation action.
        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """
        # if the game is still going
        if not self._is_game_over:
            # and it's not paused
            if self._paused == False:
                # run handle action
                self._handle_stage_progression(cast)
            else:
                # if player pauses, remove stage name display message (if any)
                cast.remove_actors("stage messages")


    def _handle_stage_progression(self, cast):
        """ Handles the stage progression by keeping track of how long each stage runs for, running spawn timer, and creating enemies of given types.
        Args:
            cast (Cast): The cast of Actors in the game.
        """

        # update stage info object if it's a new stage
        if self._current_stage != self._game_stages[self._game_stage_number]:
            self._current_stage = self._game_stages[self._game_stage_number]
            # reset stage timer
            self._stage_seconds = 0

        # make sure it's not a "stage display" only stage
        if self._current_stage["stagedisplay"] == "none":

            # increment game timer in seconds
            self._stage_seconds += 1 / constants.FRAME_RATE

            # wait until the delay start is over
            if self._stage_seconds > self._current_stage["delaystart"]:

                # now create enemies every time the wait spawn reaches zero
                if self._wait_spawn <= 0:

                    # reset to wait again
                    self._wait_spawn = self._current_stage["waitspawn"]

                    # set up y_randomness for spawn y positions
                    self.y_randomness = self._current_stage["y_randomness"]

                    # reset recent enemies spawned list
                    self._last_spawn_list = []

                    # for every enemy type in the enemytypes list for this stage
                    for enemytype in self._current_stage["enemytypes"]:
                        # create an enemy of that type
                        enemy = self._create_enemy_of_type(cast, enemytype)
                        # make sure it was created succesfully
                        if enemy != 0:
                            # if so, add it to the recent enemies spawned list
                            self._last_spawn_list.append(enemy)
                else:
                    # count down wait spawn timer in seconds
                    self._wait_spawn -= 1 / constants.FRAME_RATE

            # if we just finished with a display stage
            if self._game_stage != self._current_stage["stagedisplay"]:
                self._game_stage = self._current_stage["stagedisplay"]
                # delete the game stage display message
                cast.remove_actors("stage messages")
                # reset other display elements color to show (Score, Shields)
                display_elements = cast.get_actors("scores")
                for display in display_elements:
                    display.set_color(constants.WHITE)
                display_elements = cast.get_actors("shields")
                for display in display_elements:
                    display.set_color(constants.WHITE)

        else: # if this is a display stage

            # reset wait spawn timer
            self._wait_spawn = 0

            # make sure no enemies exist before moving on
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

                        # get position for stage name as a message on the screen
                        x = int(constants.MAX_X / 2)
                        y = int(constants.MAX_Y / 2)
                        position = Point(x, y)
                        message = Actor()
                        message.set_text(self._game_stage)
                        message.set_position(position)
                        cast.add_actor("stage messages", message)

                        # play stage start sound
                        self._audio_service.play_sound("new-stage")

        # if we are past the duration of this stage
        if self._stage_seconds > self._current_stage["delaystart"] + self._current_stage["duration"]:
            # reset stage timer
            self._stage_seconds = 0
            # move to next stage
            self._game_stage_number += 1


    def _create_enemy_of_type(self, cast, enemy_type):
        """ Creates an enemy of a given type.
        Args:
            cast (Cast): The cast of Actors in the game.
            enemy_type (string): The type of enemy to make
        """

        # default is zero
        enemy = 0

        # call the correct method and add the actor to the correct cast group
        if enemy_type == "asteroid-small":
            enemy = self._make_asteriod(cast, 0)
            cast.add_actor("asteroids", enemy)

        if enemy_type == "asteroid-medium":
            enemy = self._make_asteriod(cast, 1)
            cast.add_actor("asteroids", enemy)

        if enemy_type == "asteroid-large":
            enemy = self._make_asteriod(cast, 2)
            cast.add_actor("asteroids", enemy)

        if enemy_type == "asteroid-small-xmove":
            enemy = self._make_asteriod(cast, 3)
            cast.add_actor("asteroids", enemy)

        if enemy_type == "asteroid-huge":
            enemy = self._make_asteriod(cast, 4)
            cast.add_actor("asteroids", enemy)

        if enemy_type == "asteroid-giant":
            enemy = self._make_asteriod(cast, 5)
            cast.add_actor("asteroids", enemy)

        if enemy_type == "ufo":
            enemy = self._make_ufo(cast)
            cast.add_actor("ufos", enemy)

        # return enemy reference (zero if unsuccesful)
        return enemy



    def _no_enemies_exist(self, cast):
        """Determines whether there are zero enemies still on screen
        Returns:
            True of false
        """
        # default is True
        result = True
        # check enemy types - - - - -

        # if any asteroids exist
        if len(cast.get_actors("asteroids")) > 0:
            result = False

        # return final result
        return result

    def _make_asteriod(self, cast, asteroidtype):
        """Creates a new asteroid at the top of the screen of a given type
        Args:
        asteroidtype (int): reference to index of constants.ASTEROID_TYPES_LIST
        Returns:
            reference to the new meteoroid
        """
        # how many times to try finding an empty position to create another anemy
        tries = 10
        # used to track if the position is free or not
        free = True
        # start by selecting a random position to try
        x = random.randint(1, constants.COLUMNS - 1)
        y = random.randint(-5 - self.y_randomness, -5)
        position = Point(x, y)
        position = position.scale(constants.CELL_SIZE)

        # keep trying (tries) n times for an empty spot
        while not free:
            # reset
            free = True

            if tries > 0:
                # try n times to find a free position
                tries -= 1
                # check recently made enemies list
                for enemy in self._last_spawn_list:
                    # if position is not free
                    if position.equals(enemy.get_position()):
                        #continue the loop
                        free = False

            if free == False:
                # pick a new spot to try
                x = random.randint(1, constants.COLUMNS - 1)
                y = random.randint(-5 - self.y_randomness, -5)
                position = Point(x, y)
                position = position.scale(constants.CELL_SIZE)
                # then the loop will run again

        # once the loop breaks we will use the position
        velocity = Point(0, constants.CELL_SIZE)
        asteroid = Asteroid(cast)
        asteroid.set_position(position)
        asteroid.set_velocity(velocity)
        # run set up type to update the asteroids attributes using the constants.ASTEROID_TYPES_LIST
        asteroid.set_up_type(asteroidtype)
        # returns it so the calling method can add it to the cast "asteriods" group
        return asteroid

    def _make_ufo(self, cast):
        """Creates a new ufo at the top of the screen
        Args:
        Returns:
            reference to the actor
        """
        # start by selecting a random position to try
        x = random.randint(5, constants.COLUMNS - 5)
        y = random.randint(0, 0)
        position = Point(x, y)
        position = position.scale(constants.CELL_SIZE)

        # once the loop breaks we will use the position
        velocity = Point(random.choice([-constants.CELL_SIZE,constants.CELL_SIZE]), 0)
        ufo = Ufo(cast, self._audio_service)
        ufo.set_position(position)
        ufo.set_velocity(velocity)
        # call set up to create body
        ufo.set_up_ufo()
        # returns it so the calling method can add it to the cast "asteriods" group
        return ufo
