import constants
from game.scripting.action import Action
from game.shared.point import Point
from game.casting.actor import Actor
from game.casting.laser import Laser
# need this module to play sounds
from playsound import playsound
import pyray as pyray


class ControlActorsAction(Action):
    """
    An input action that controls the snake.

    The responsibility of ControlActorsAction is to get the direction and move the snake's head.

    Attributes:
        _keyboard_service (KeyboardService): An instance of KeyboardService.
    """

    def __init__(self, keyboard_service):
        """Constructs a new ControlActorsAction using the specified KeyboardService.

        Args:
            keyboard_service (KeyboardService): An instance of KeyboardService.
        """
        self._keyboard_service = keyboard_service
        self._key_fire = False
        self._key_fire_timer = 0

        self._player_direction = Point(0, 0)

        # this is to initialize the audion device
        pyray.init_audio_device()

    def _handle_player_movement(self, cast):
        """Executes the control actors action to control player movement
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        # reset movement
        self._player_direction = Point(0, 0)
        # left
        if self._keyboard_service.is_key_down('left'):
            self._player_direction = Point(-constants.CELL_SIZE, 0)
        # right
        if self._keyboard_service.is_key_down('right'):
            self._player_direction = Point(constants.CELL_SIZE, 0)
         # apply direction to player
        ship = cast.get_first_actor("ships")
        ship.control_ship(self._player_direction)

    def _handle_player_fire_weapon(self, cast):
        """Executes the control actors action to handle player firing weapon
        Args:
            cast (Cast): The cast of Actors in the game.
        """
        ship = cast.get_first_actor("ships")

        # make sure player is not in hurt mode
        if ship.get_is_dead() == False and ship.get_is_hurt() == False:
            # if player presses the space bar
            if self._keyboard_service.is_key_down('space') and self._key_fire == False:

                # this plays the sound bype
                #playsound(constants.SHIPFIRE_SOUND, block=False)
                lazer = pyray.load_sound(constants.SHIPFIRE_SOUND)
                pyray.play_sound(lazer)
                print(
                    f'playing sound using  playsound: {constants.SHIPFIRE_SOUND}')

                # set key fire so only one bullet is fired at a time
                self._key_fire = True
                # set timer to control how rapidly player can fire
                self._key_fire_timer = 6

                # get the position of the front of the ship
                ship_parts = ship.get_parts()
                ship_position = ship_parts[0].get_position()
                # create a point one cell above the front of the ship
                position = Point(ship_position.get_x(),
                                 ship_position.get_y() - 1 * constants.CELL_SIZE)
                # set a velocity to move upward
                velocity = Point(0, -constants.CELL_SIZE)
                text = "^"
                color = constants.GREEN
                # apply attributes to a new instance of laser
                laser = Laser(cast)
                laser.set_position(position)
                laser.set_velocity(velocity)
                laser.set_text(text)
                laser.set_color(color)
                # add laser to the "lasers" cast
                cast.add_actor("lasers", laser)

        # handle rapid fire timer and key hold
        if self._key_fire == True:
            # if the player lets up off the key and the timer is zero
            # self._keyboard_service.is_key_up('space') and  to make it so you have to press each time
            if self._key_fire_timer <= 0:
                # reset key fire so we can shoot again
                self._key_fire = False
            # increment timer if greater than zero
            if self._key_fire_timer > 0:
                self._key_fire_timer -= 1

    def execute(self, cast, script):
        """Executes the control actors action.
        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """

        # handle player movement
        self._handle_player_movement(cast)
        # handle player fire weapon
        self._handle_player_fire_weapon(cast)
