import constants
from game.scripting.action import Action
from game.shared.point import Point
from game.casting.actor import Actor
from game.casting.laser import Laser


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

    def execute(self, cast, script):
        """Executes the control actors action.

        Args:
            cast (Cast): The cast of Actors in the game.
            script (Script): The script of Actions in the game.
        """

        # default is not moving
        self._player_direction = Point(0, 0)

        # left
        if self._keyboard_service.is_key_down('left'):
            self._player_direction = Point(-constants.CELL_SIZE, 0)
            key_pressed = True

        # right
        if self._keyboard_service.is_key_down('right'):
            self._player_direction = Point(constants.CELL_SIZE, 0)
            key_pressed = True

        # apply direction to player
        ship = cast.get_first_actor("ships")
        ship.control_ship(self._player_direction)

        # handle shooting
        if self._keyboard_service.is_key_down('space') and self._key_fire == False:
            # set key fire down to avoid rapid fire
            self._key_fire = True
            self._key_fire_timer = 10

            # shoot
            ship_parts = ship.get_parts()
            ship_position = ship_parts[0].get_position()

            position = Point(ship_position.get_x(),
                             ship_position.get_y() + 1 * constants.CELL_SIZE)
            velocity = Point(0, -constants.CELL_SIZE)
            text = "^"
            color = constants.RED
            laser = Laser(cast)
            laser.set_position(position)
            laser.set_velocity(velocity)
            laser.set_text(text)
            laser.set_color(color)

            cast.add_actor("lasers", laser)

        if self._key_fire == True:
            if self._keyboard_service.is_key_up('space') and self._key_fire_timer <= 0:
                # reset key fire when key is released
                self._key_fire = False
            # increment timer
            if self._key_fire_timer > 0:
                self._key_fire_timer -= 1
            else:
                # ready to fire
                self._key_fire_timer = 0
